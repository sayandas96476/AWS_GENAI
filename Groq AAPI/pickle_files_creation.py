import google.generativeai as genai
import pickle

genai.configure(api_key="Gemini API Key")



#Reading Raw text file
file_path = r"D:\batman.txt"
with open(file_path, 'r', encoding='utf-8') as file:
    text = file.read()

texts = text.split("\n\n")


#creation of vector db
def vectorstore():
    vector=[]
    for i in texts:
        response = genai.embed_content(
            model="models/embedding-001",  # or "models/embedding-gecko-001" etc.
            content=i,
            task_type="retrieval_document"
        )

        vector.append(response["embedding"])
    return vector

vectors = vectorstore()



# Storing the vector db to a pickle file
with open('D:/batman.pkl', 'wb') as file:
    pickle.dump(vectors, file)

# Storing the text list to pickle file
with open('D:/batman_text.pkl', 'wb') as file:
    pickle.dump(texts, file)

