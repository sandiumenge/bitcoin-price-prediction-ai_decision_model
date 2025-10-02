# Decision-Based Deep Learning for Bitcoin ROI Maximization  

This project explores how **deep learning and Natural Language Processing (NLP)** can be applied to financial decision-making. Instead of predicting Bitcoin prices directly, it introduces a **decision-based model** that aims to **maximize Return on Investment (ROI)** by leveraging **Twitter emotion classification**.  

Traditional approaches often rely on simplified sentiment analysis or regression-style predictions. In contrast, this work:  
- Uses **emotion classification** (fear, greed, optimism, anger, etc.) for richer investor psychology signals.  
- Combines these insights with **Bitcoin price and volatility data**.  
- Trains an **LSTM-based model** to recommend **Buy, Sell, or Hold** actions, optimizing directly for ROI.  

## Key Contributions  
- Built a custom pipeline for **data scraping, preprocessing, and labeling** of millions of crypto-related tweets.  
- Developed and fine-tuned **spam/human and emotion classifiers** using **BERTweet**.  
- Designed a **decision-focused deep learning model** trained to outperform standard investment strategies.  
- Demonstrated that emotion-based features lead to **higher ROI and reduced losses** compared to Buy & Hold or sentiment-only models.  

## Results (Highlights)  
- The model consistently **outperformed Buy & Hold** in volatile or bearish markets.  
- Emotion classification proved more informative than binary sentiment, improving decision robustness.  
- ROI-focused training delivered better **investment-oriented outcomes** than traditional price-prediction models.  

*(Insert key visual comparisons here — e.g. model vs Buy & Hold performance, emotion distribution)*  



## Future Directions  
- Scale with **larger, multi-year datasets**.  
- Incorporate **tweet reach/impact metrics** (likes, retweets, followers).  
- Explore **transformer-based decision architectures** for longer-term forecasting.  

---  

This project highlights how **AI-driven decision models** can leverage social media data to tackle real-world financial challenges, with direct applications in **algorithmic trading, risk management, and behavioral finance**.  
