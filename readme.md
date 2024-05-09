## Inspiration ✨
The quest for quick and accurate information in an academic setting can be a daunting task. We noticed that students and staff at the University of Waterloo often spent excessive time navigating through various documents, wikis, technical support issues, how-tos, FAQs, tutorials, and setup guides. Our aim was to create a solution that saves time and reduces the frustration of manually searching through extensive documentation.

The existing IST UWaterloo bot falls short in answering these diverse and complex queries - in fact, it replied saying that it could not answer our question! And the service desk's limited working hours further complicate access to information.

GooseQuery is our answer to these challenges, providing immediate, accurate, and easy access to the information you need, anywhere, anytime.

## What it does 📖
GooseQuery revolutionizes the way information is accessed at UWaterloo. Instead of the laborious process of scouring through documents spread across numerous pages and sources, users can simply interact with our Discord bot, ensuring ease of use and accessibility for all students and staff. By asking questions in a conversational manner, users receive precise and contextually relevant answers, streamlining their search for information and making the learning process more efficient and enjoyable.

## How we built it 🛠️
We leveraged the user-friendly interface of Discord by integrating our bot using the Discord API. To gather data, we used Scrapy to scrape relevant documents from IST, CSCF, and Quest, ensuring a comprehensive knowledge base. We then created a set of embeddings for these documents using Cohere Embed, allowing for nuanced understanding and retrieval of information. To match user queries with the most relevant documents, we implemented a fast KNN algorithm, which passed through Cohere Rerank API to further refine the search results. The final responses are generated using the Cohere Chat API, drawing on context from the top results to provide accurate and helpful answers.

## Challenges we ran into 🚒
One of the most significant challenges was scraping the web and curating documentation from various sources. We had to ensure that the information was not only accurate but also up-to-date and relevant. Additionally, integrating different technologies and APIs posed its own set of technical complexities that we had to navigate through.

## Accomplishments that we're proud of 😎
Successfully developing GooseQuery in a tight timeframe of just 4 hours!
Seamlessly integrating and utilizing Cohere's powerful APIs.
Automating the data sourcing process, to effectively create the knowledge base.

## What we learned 🧠
Implementing Retrieval-Augmented Generation (RAG) for effective information retrieval.
Gaining practical experience with Cohere's APIs, exploring their potential in real-world applications.

## What's next for GooseQuery 🤖
Expanding the bot's capabilities to more internal UWaterloo subdomains, enabling it to serve a wider audience
An easy deployment process for integration into various UWaterloo Discord servers to make GooseQuery a ubiquitous resource for the university community.

