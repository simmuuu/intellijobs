import os
import torch
from dotenv import load_dotenv

# import datetime
from pinecone import Pinecone
from sentence_transformers import SentenceTransformer
from groq import Groq
load_dotenv()


device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

embedding_model = SentenceTransformer("thenlper/gte-base").to(device)

pc = Pinecone(api_key=os.getenv('pinecone_api'))
index = pc.Index("intellijobs")



def get_embedding(text):
    if not text.strip():
        print("Attempted to get embedding for empty text.")
        return []

    embedding = embedding_model.encode(text)

    return embedding.tolist()   



def get_similar_jobs(user_query, top_k=5):
    user_vector = get_embedding(user_query)
    results = index.query(vector=user_vector, top_k=top_k, include_metadata=True, include_values=False)

    # Process and display results
    # for match in results['matches']:
    #     print(f"ID: {match['id']}, Score: {match['score']}")
    
    
    return results
    
    

    # print('\n')
    # for document in results:
    #     print(f"{document['title']} {document['locations']} {document['keywords']} {document['experience']}")
    #     print("-------------------------------------")
    # print('\n')



    

def read_markdown_file(file_path):
    with open(file_path, 'r') as file:
        content = file.read()
    return content



def generate_response(prompt,similar_jobs):
    
    descriptions = '\n\n'.join([match['metadata']['description'] for match in similar_jobs['matches']])    
    
    context_template = read_markdown_file('context_template.md')
    context = context_template.replace('{{descriptions}}', descriptions).replace('{{prompt}}', prompt)

    
    
    
    
    client = Groq(api_key=os.getenv('groq_api'))
    completion = client.chat.completions.create(
        model="llama3-70b-8192",
        messages=[
             {
            "role": "system",
            "content": "You are a conversational assistant who helps users with their job search. Your tasks include providing job listings relevant to the user's query and answering any questions related to these listings."
            },
            {
                "role": "user",
                "content": context
            }
        ],
        temperature=0,
        max_tokens=2500,
        top_p=1,
        stream=True,
        stop=None,
    )
    
    
    response_content = ""
    for chunk in completion:
        response_content += chunk.choices[0].delta.content or ""

    return response_content






    
    # timestamp=datetime.datetime.now().strftime("%Y-%m-%d %H-%M-%S")
    # output_file_name=f"naukri_response {timestamp}.md"
    # with open(output_file_name,'w') as output_file:
    #     for chunk in completion:
    #         print(chunk.choices[0].delta.content or "",end="")
    #         output_file.write(chunk.choices[0].delta.content or "")
    
    
    
    
    

def search_jobs(user_query):
    similar_jobs = get_similar_jobs(user_query)
    return generate_response(user_query,similar_jobs)




