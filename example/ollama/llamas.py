# Example based on https://ollama.com/blog/embedding-models
# using objectbox as a vector store

import ollama
import objectbox

documents = [
  "Llamas are members of the camelid family meaning they're pretty closely related to vicuñas and camels",
  "Llamas were first domesticated and used as pack animals 4,000 to 5,000 years ago in the Peruvian highlands",
  "Llamas can grow as much as 6 feet tall though the average llama between 5 feet 6 inches and 5 feet 9 inches tall",
  "Llamas weigh between 280 and 450 pounds and can carry 25 to 30 percent of their body weight",
  "Llamas are vegetarians and have very efficient digestive systems",
  "Llamas live to be about 20 years old, though some only live for 15 years and others live to be 30 years old",
]


from objectbox.model import *
from objectbox.model.properties import *
import numpy as np

# Have fresh data for each start
objectbox.Store.remove_db_files("objectbox")

@Entity(id=1, uid=1)
class DocumentEmbedding:
    id = Id(id=1, uid=1001)
    document = Property(str, id=2, uid=1002)
    embedding = Property(np.ndarray, type=PropertyType.floatVector, id=3, uid=1003, index=HnswIndex(
        id=3, uid=10001,
        dimensions=1024,
        distance_type=VectorDistanceType.COSINE
    ))

model = Model()
model.entity(DocumentEmbedding, last_property_id=IdUid(3, 1003))
model.last_entity_id = IdUid(1, 1)
model.last_index_id = IdUid(3,10001)

store = objectbox.Store(model=model)
box = store.box(DocumentEmbedding)

print("Documents to embed: ", len(documents))

# store each document in a vector embedding database
for i, d in enumerate(documents):
  response = ollama.embeddings(model="mxbai-embed-large", prompt=d)
  embedding = response["embedding"]

  box.put(DocumentEmbedding(document=d,embedding=embedding))
  print(f"Document {i + 1} embedded")
 
# an example prompt
prompt = "What animals are llamas related to?"

# generate an embedding for the prompt and retrieve the most relevant doc
response = ollama.embeddings(
  prompt=prompt,
  model="mxbai-embed-large"
)


embedding_prop: Property = DocumentEmbedding.get_property("embedding")
query = box.query(
    embedding_prop.nearest_neighbor(response["embedding"], 1)
).build()

results = query.find_with_scores()
data = results[0][0].document 

print(f"Data most relevant to \"{prompt}\" : {data}")

print("Generating the response now...")

# generate a response combining the prompt and data we retrieved in step 2
output = ollama.generate(
  model="llama3",
  prompt=f"Using this data: {data}. Respond to this prompt: {prompt}"
)

print(output['response'])
