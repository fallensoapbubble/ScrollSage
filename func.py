import requests
import json
import google.generativeai as genai
from langchain.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from typing import List, Dict, Any
import os
from datetime import datetime


import os
from dotenv import load_dotenv

load_dotenv()  # Loads variables from .env into environment
qloo_key = os.getenv("QLOO_API_KEY")


class EntityInsightsGenerator:
    def __init__(self, gemini_api_key: str, qloo_api_key: str =qloo_key):
        """
        Initialize the insights generator with API keys
        """
        self.qloo_api_key = qloo_api_key
        self.qloo_base_url = "https://hackathon.api.qloo.com"
        
        # Initialize Gemini
        genai.configure(api_key=gemini_api_key)
        self.gemini_llm = ChatGoogleGenerativeAI(
            model="gemini-1.5-flash",
            google_api_key=gemini_api_key,
            temperature=0.7
        )
        
        # Setup LangChain prompt template
        self.insights_prompt = PromptTemplate(
            input_variables=["entities", "qloo_data", "context"],
            template="""
            Based on the following user entities and external data, generate comprehensive insights:
            
            User Entities: {entities}
            External Data: {qloo_data}
            Context: {context}
            
            Analyze these entities and provide insights in the following JSON format:
            {{
                "clusters": [3-4 distinct user personality/behavior clusters],
                "biases": [3-4 potential cognitive or cultural biases],
                "narratives": [3-4 emerging themes or storylines],
                "recommendations": [3-4 actionable recommendations]
            }}
            
            Make sure the insights are:
            - Specific to the entities provided
            - Culturally aware and diverse
            - Actionable and practical
            - Based on current trends and behaviors
            
            Return only valid JSON without any additional text.
            """
        )



        
        # Use RunnableSequence as per LangChain 0.1.17+ (fixed deprecation)
        self.insights_chain = self.insights_prompt | self.gemini_llm




   
    def fetch_qloo_insights(self, entities: List[Dict]) -> Dict:
        headers = {
            "accept": "application/json",
            "X-Api-Key": self.qloo_api_key
        }
        
        results = {}
        for entity in entities:
            name = entity["name"]
            entity_type = entity["type"]
            # Mapping to urn (customize if needed)
            urn_type = f"urn:entity:{entity_type}"

            params = {
                "filter.name": name,
                "filter.type": urn_type
            }

            response = requests.get(self.qloo_base_url, headers=headers, params=params)
            if response.status_code == 200:
                results[name] = response.json()
            else:
                results[name] = {"error": response.status_code, "message": response.text}

        return results
    






    def generate_insights(self, entities: List[Dict]) -> Dict:
        """
        Main function to generate insights from entities
        """
        print(f"Processing {len(entities)} entities...")
        
        # Fetch Qloo data
        print("Fetching Qloo insights...")
        qloo_data = self.fetch_qloo_insights(entities)
        print("Qloo data:", qloo_data, '\n\n===\n')
        
        # Prepare context
        context = f"Similar past insights: Generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        
        # Generate insights using LangChain + Gemini
        print("Generating insights with Gemini...")
        try:
            # Use invoke for RunnableSequence (fixed deprecation)
            raw_insights = self.insights_chain.invoke({
                "entities": json.dumps(entities),
                "qloo_data": json.dumps(qloo_data),
                "context": context
            })
            
            # Extract content from AIMessage properly (fixed JSON parsing error)
            if hasattr(raw_insights, "content"):
                raw_insights_str = raw_insights.content
            elif isinstance(raw_insights, dict) and "content" in raw_insights:
                raw_insights_str = raw_insights["content"]
            else:
                raw_insights_str = str(raw_insights)
            
            print("Raw AI response:", raw_insights_str)
            
            # Clean the response to extract only JSON
            raw_insights_str = raw_insights_str.strip()
            if raw_insights_str.startswith('```json'):
                raw_insights_str = raw_insights_str.replace('```json', '').replace('```', '').strip()
            elif raw_insights_str.startswith('```'):
                raw_insights_str = raw_insights_str.replace('```', '').strip()
            
            insights_data = json.loads(raw_insights_str)
            print("Parsed insights:", insights_data, '\n\n===\n')
            
        except json.JSONDecodeError as e:
            print(f"JSON parsing error: {str(e)}")
            print(f"Raw response was: {raw_insights_str}")
            
            # Generate entity-specific fallback insights
            entity_names = [entity.get('name', '') for entity in entities]
            entity_types = [entity.get('type', '') for entity in entities]
            
            # Fallback insights if JSON parsing fails
            insights_data = {
                "clusters": [
                    f"Fans of {entity_names[0] if entity_names else 'premium content'}",
                    f"Consumers interested in {', '.join(entity_types[:2])}",
                    "Digital content explorers",
                    "Quality-focused entertainment seekers"
                ],
                "biases": [
                    "Preference for mainstream content",
                    "Algorithm-influenced discovery patterns",
                    "Brand loyalty over product evaluation",
                    "Visual content preference"
                ],
                "narratives": [
                    "Quality entertainment vs. quantity consumption",
                    "Brand authenticity in digital age",
                    "Personalized content curation trends",
                    f"Growing interest in {entity_types[0] if entity_types else 'entertainment'} content"
                ],
                "recommendations": [
                    "Explore niche content creators in your areas of interest",
                    "Balance algorithmic suggestions with manual discovery",
                    "Research brand values beyond marketing messages",
                    f"Discover similar {entity_types[0] if entity_types else 'content'} from different cultures"
                ]
            }



            
        
        except Exception as e:
            print(f"Unexpected error: {str(e)}")
            # Even more basic fallback
            insights_data = {
                "clusters": [
                    "Entertainment enthusiasts",
                    "Brand-conscious consumers", 
                    "Digital content explorers",
                    "Mainstream media followers"
                ],
                "biases": [
                    "Western-centric media consumption",
                    "Algorithm-influenced discovery patterns",
                    "Brand loyalty over product evaluation",
                    "Visual over textual content preference"
                ],
                "narratives": [
                    "Quality entertainment vs. quantity consumption",
                    "Brand authenticity in digital age",
                    "Personalized content curation trends",
                    "Cross-platform content discovery"
                ],
                "recommendations": [
                    "Explore niche content creators in your areas of interest",
                    "Balance algorithmic suggestions with manual discovery",
                    "Research brand values beyond marketing messages",
                    "Diversify content sources across different platforms"
                ]
            }
        
        # Prepare final output
        result = {
            'user_entities': entities,
            'insights': insights_data,
            'qloo_data_available': len(qloo_data) > 0,
            'timestamp': datetime.now().isoformat()
        }
        
        return result

def calltoAPI(obj):
    """
    Enhanced version of your original function
    """
    print("needed", obj)
    print("="*50)
    
    GEM_KEY = os.getenv('GEMINI_API_KEY')
    
    try:
        generator = EntityInsightsGenerator(GEM_KEY)
        insights = generator.generate_insights(obj)
        
        print("Generated Insights:")
        print(json.dumps(insights, indent=2))
        
        return insights
        
    except Exception as e:
        print(f"Error generating insights: {str(e)}")
        import traceback
        traceback.print_exc()
        
        # Return fallback structure with entity-specific content
        entity_names = [entity.get('name', '') for entity in obj] if obj else []
        entity_types = [entity.get('type', '') for entity in obj] if obj else []
        
        return {
            'user_entities': obj,
            'insights': {
                'clusters': [
                    f'Fans of {entity_names[0]}' if entity_names else 'Tech-forward early adopters',
                    f'Consumers of {entity_types[0]} content' if entity_types else 'Entertainment followers', 
                    'Digital content explorers',
                    'Mainstream media consumers'
                ],
                'biases': [
                    'Western-centric media consumption',
                    'Preference for visual over textual content',
                    'Algorithm-driven discovery patterns',
                    'Brand recognition over quality assessment'
                ],
                'narratives': [
                    'Digital minimalism vs. consumption culture',
                    'Authenticity in influencer marketing',
                    'Platform-specific content optimization',
                    f'Growing popularity of {entity_types[0]} content' if entity_types else 'Cross-platform content discovery'
                ],
                'recommendations': [
                    'Diversify content sources beyond English-speaking creators',
                    'Engage with long-form content to balance quick consumption',
                    'Follow creators from different cultural backgrounds',
                    f'Explore independent {entity_types[0]} creators' if entity_types else 'Support smaller content creators'
                ]
            },
            'error': str(e),
            'fallback_used': True,
            'timestamp': datetime.now().isoformat()
        }
    


   