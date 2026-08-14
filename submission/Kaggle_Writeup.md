# 🌌 Zero-Block Deconstruction: Comprehensive Scientific Writeup

*An exhaustive analysis of the on-chain behavioral reconstruction of a dominant Solana sniper bot.*

---

## 1. Executive Summary & The Core Mystery

In the hyper-competitive landscape of Solana decentralized finance (DeFi), specifically within token deployment platforms like pump.fun, the "zero-block" represents the absolute frontier of arbitrage and execution speed. During the exact slot a token is deployed and initialized, highly sophisticated sniper bots evaluate the token's parameters, the deployer's history, and the surrounding market context to decide whether to execute a buy transaction in the very same block.

The fundamental research question driving this project is: **Can we reconstruct the dominant observable decision policy of a Solana sniper using only point-in-time on-chain evidence—without fabricating execution or economic outcomes?**

We specifically targeted the bot address `5brv79eFZ2rGprXNvqgVJBkBptkkw8GJX1XydJyZLyAr`. Rather than attempting to simulate its economic P&L—which is impossible without access to its proprietary exit strategies, slippage tolerances, and latency constraints—we focused entirely on the *behavioral decision boundary*. By formulating this as a binary classification problem at the exact microsecond of decision ($t_{decision}$), we engineered a strictly chronological, zero-leakage feature space to reverse-engineer what the bot cares about.

The results proved profound. The target bot does not rely heavily on token economics or deployment metadata; rather, it is highly sensitive to the *historical on-chain behavior of the token deployer*. Using a LightGBM ensemble, we captured a PR-AUC of 0.396 on unseen deployers (an 8.4x improvement over random baseline) and successfully replicated 47.8% of the bot's decisions on a completely frozen chronological test set.

This document outlines the complete architectural, methodological, and scientific framework of the Zero-Block Deconstruction project.

---

## 2. Observability and the Evidence Boundary

A critical pillar of this research is maintaining a strict epistemological boundary regarding what is "known" versus what is "assumed." In on-chain data science, it is dangerously easy to leak future information (look-ahead bias) or to fabricate assumptions about trading execution.

### 2.1 The Known Universe
We possess complete visibility into:
- The universe of 411,137 eligible token deployments on the pump.fun platform.
- 4.9 million historical wallet activity events mapped to these deployments.
- The timestamps, block slots, and transaction signatures for every deployment.
- 15,927 confirmed "Buy" events executed by the target bot.

### 2.2 The Unknown Universe
We explicitly acknowledge that we cannot observe:
- **Bot Buy Latency:** We know the bot bought in the zero-block, but we do not know its exact mempool propagation latency.
- **Entry Size and Slippage:** The exact amount of SOL deployed per trade and the slippage incurred during execution.
- **Exit Timing and P&L:** The bot's sell transactions, hold duration, and realized/unrealized profit and loss.
- **Off-Chain Signals:** Any social media scraping (e.g., Twitter, Telegram) or private node RPC metadata the bot might use.

### 2.3 The Label Accounting Protocol
To ensure our model evaluated reality, we mapped the 15,927 bot selections against our deployment universe.
- **Positive Labels (1):** 13,818 confirmed target bot buys successfully joined to our deployment data.
- **Negative Labels (0):** 395,210 token deployments where the bot did *not* execute a buy.
- **Excluded Data:** 2,109 bot selections could not be cleanly mapped to a known deployment. *Crucially, these were excluded entirely.* We never assumed an "unknown" was a "negative."

The resulting baseline prevalence (the random chance of picking a token the bot bought) in our test set was established at **4.74%**.

---

## 3. Strict Temporal Isolation (The Time Model)

Because the bot operates at $t_{decision}$ (the zero-block), the feature engineering pipeline must respect a flawless temporal isolation boundary. Any data point generated at $t > t_{decision}$, or even exactly at $t_{decision}$ but physically after the deployment transaction, is strictly forbidden.

### 3.1 Defining the Temporal Vectors
- **`t_deployment`**: The Unix timestamp or Solana slot when the token deployment transaction is finalized on-chain.
- **`t_decision`**: Because the bot is a zero-block sniper, it enters in the exact same slot as the deployment. Thus, `t_decision = t_deployment` (specifically at the `blockSlot` level).
- **`t_activity`**: The timestamp of any historical event performed by a wallet prior to the deployment.

### 3.2 The Causal-in-Time Constraint
We implemented three layers of leakage prevention:
1. **Event Filtering (Layer A):** When aggregating a deployer's historical trades or launches, the database join requires `timestamp < t_deployment`. Strict inequality ensures the current token launch is never accidentally included in the deployer's history.
2. **Exclusion of Price Action (Layer B):** Because the bot buys in the zero-block, there is no bonding curve or price action available at $t_{decision}$. All price features (`price_usd`, `cost_usd`) from subsequent trades were explicitly banned from the feature engine.
3. **Mempool Payload Data (Layer C):** Data extracted directly from the deployment payload (e.g., priority fees paid by the deployer, initial SOL bonded) is permissible, as the bot can observe this in the mempool or Jito bundle prior to execution.

---

## 4. Feature Engineering and the Feature Dictionary

With strict temporal boundaries established, we engineered a set of purely behavioral features that summarize a deployer's on-chain identity up to the exact millisecond before they launch a new token.

### 4.1 Historical Activity Aggregates
- **`past_launches` (int):** The total number of token deployments this specific wallet address executed strictly prior to the current $t_{decision}$. This serves as a proxy for "serial deployers" versus "fresh developers."
- **`past_buys` (int):** The total number of buy transactions executed by the deployer across all tokens prior to $t_{decision}$. Indicates general ecosystem participation.
- **`past_sells` (int):** The total number of sell transactions executed by the deployer.
- **`past_burns` (int):** The total number of token burn events executed by the deployer.

### 4.2 Temporal Context
- **`deployer_age_seconds` (float):** The duration (in seconds) between the deployer's very first recorded on-chain action and the current $t_{decision}$. This distinguishes between a wallet spun up 5 minutes ago and a seasoned wallet that has existed for months.

### 4.3 Deployment Mechanics (Payload Level)
- **`priority_fee` (float):** The additional compute budget priority fee attached to the deployment transaction.
- **`jito_tip` (float):** The bribe paid to Jito validators to ensure atomic bundle inclusion.
- **`initial_sol` (float):** The amount of SOL used to seed the initial bonding curve liquidity.

*Note: While deployment mechanics were included in the initial exploratory models, the feature importance algorithms revealed that the target bot largely ignores them in favor of the historical behavioral aggregates.*

---

## 5. Machine Learning Architecture: LightGBM

To model the bot's decision boundary, we required an algorithm capable of handling non-linear relationships, robust to outliers (e.g., a deployer with 10,000 past buys), and highly interpretable. We selected **LightGBM** (Light Gradient Boosting Machine).

### 5.1 Training Protocol and Data Splitting
The data was not split randomly; it was split *chronologically* to simulate the flow of time and test for forward-looking generalization.
- **Training Set:** The earliest 70% of chronological deployments.
- **Validation Set:** The next 15% of deployments, used for hyperparameter tuning and establishing the pre-registered decision thresholds.
- **Frozen Test Set:** The final 15% of deployments. This set was entirely locked during training and model selection. It represents a strict out-of-sample forward-time evaluation.

### 5.2 Handling Extreme Class Imbalance
With a positive class prevalence of only ~4.7%, accuracy is a meaningless metric. A model that predicts "0" for every token achieves 95.3% accuracy but fails completely at the task.

We optimized the model using **Log Loss (Binary Cross-Entropy)** and evaluated success exclusively using **Precision-Recall Area Under Curve (PR-AUC)** and **Recall (Capture Rate)** at fixed precision thresholds.

### 5.3 Model Convergence
The LightGBM ensemble grew iteratively, splitting nodes based on the optimal information gain derived from the causal-in-time features. Regularization parameters (L1/L2 penalties, min_data_in_leaf) were strictly enforced to prevent the model from memorizing specific deployer addresses. We wanted the model to learn the *behavior*, not the *identity*.

---

## 6. Interpreting the Dominant Behavioral Fingerprint

Once the model was trained, we applied SHAP (SHapley Additive exPlanations) to crack open the "black box" and read the exact policy the bot was utilizing.

The bot relies on a specific, dual-layered behavioral fingerprint:

1. **The "Goldilocks" Deployer History (`past_launches`):** 
   The bot aggressively targets deployers with a very low number of prior launches. If a deployer has launched 50 tokens in the past, the bot rejects them immediately. However, it does not exclusively target "first-time" deployers either. It seeks out a specific low-history threshold.
   
2. **The Maturation Requirement (`deployer_age_seconds`):**
   While the bot wants deployers with low launch histories, it actively *avoids* brand-new wallets. If a wallet has an age of 0 (it was created and immediately deployed a token), the bot penalizes it. The bot prefers wallets that have existed on-chain for some time, perhaps exhibiting normal user behavior (some buys, some sells) before finally deploying a token.

In summary: **The target bot hunts for aged wallets executing their first or second token deployment.** It systematically avoids serial rug-pullers (high `past_launches`) and sybil-attack fresh wallets (zero `deployer_age`).

---

## 7. Results: The Scientific Scoreboard

The true test of the hypothesis occurred when the model was evaluated against the **Frozen Chronological Test Set** (61,673 deployments).

### 7.1 Generalization to Unseen Deployers
The most rigorous test of a behavioral model is evaluating it on entities it has never seen before. We filtered the test set to include *only* deployers who never appeared in the training set (0% overlap). 

- **Random Baseline PR-AUC:** 0.047
- **Frozen Model PR-AUC:** 0.286
- **Unseen Deployers PR-AUC:** **0.396**

The fact that the model performs *better* (0.396) on unseen deployers proves that the bot's strategy is fundamentally behavioral. The model successfully learned the underlying rules of the game, rather than just memorizing which deployers the bot liked in the past.

### 7.2 Executable Replication (The Top-5% Policy)
We did not just want a descriptive model; we wanted an executable replica. On the validation set, we established a strict "Top-5% selection budget" policy. We took this pre-registered operating point and applied it blindly to the frozen test set.

- **Target Bot Capture (Recall):** The replica successfully captured **47.8%** of the exact tokens the target bot bought in the future timeframe.
- **Precision:** Of all the tokens the replica flagged as a "Buy", 31.7% were actually bought by the target bot.
- **Selection Ratio:** The replica achieved this massive capture rate while only selecting 1.50× the number of tokens the bot selected. It did not blindly buy everything; it was highly surgical.

---

## 8. Failure Analysis and Residual Intelligence (The Two Regimes)

Scientific rigor requires analyzing where the model fails just as heavily as where it succeeds. The model captured 47.8% of the bot's actions. What about the other 52.2%?

By analyzing the false negatives (tokens the bot bought, but the replica rejected), we discovered **Two Regimes** in the bot's behavior.

### 8.1 The Dominant Regime (The Shared Selections)
This is the regime our model successfully reverse-engineered. It consists of the "Aged Wallet / Low Launch" behavioral fingerprint. The observable on-chain data perfectly explains this strategy.

### 8.2 The Residual Regime (The Bot-Only Selections)
The tokens the bot bought that our model vehemently rejected share a fascinating characteristic: **Extreme Serial Deployers.**
In this secondary regime, the target bot is buying tokens from deployers who have launched hundreds of tokens in the past. 

Why would the bot buy from serial deployers when its primary rule is to avoid them? 
Because our model is restricted purely to *observable on-chain data*, we can hypothesize that the bot has access to *off-chain intelligence* or *hidden metadata* for these specific tokens. 

**Hypotheses for the Residual Regime:**
1. **Missing Wallet Relationships:** The bot may be analyzing funding graphs (e.g., tracing Binance withdrawal wallets) to group serial deployers into clusters, identifying a profitable underlying entity.
2. **Off-Chain Metadata Scraping:** The bot may be scraping Twitter or Telegram for specific keywords, contract addresses, or influencer mentions. If an influencer launches a token, the bot buys it regardless of the deployer's on-chain history.
3. **Capital Availability Constraints:** The bot may adjust its risk tolerance dynamically based on its available SOL inventory, occasionally taking high-risk bets on serial deployers when its primary criteria are starved for options.

*Conclusion on Failure:* The inability to capture the residual regime is not a failure of the machine learning model; it is a successful mapping of the **evidence boundary**. We have mathematically proven exactly where on-chain data ceases to be useful and where off-chain or hidden graph intelligence begins.

---

## 9. Engineering: Transpiling ML to a Zero-Dependency Edge Architecture

While the data science pipeline was executed in heavy Python environments (Jupyter, Pandas, NumPy, Scikit-Learn), deploying a gradient boosting machine to a low-latency web application traditionally requires heavy containerization (Docker) or expensive API hosting.

To solve this, we engineered a **dependency-free serverless inference pipeline**.

### 9.1 The `m2cgen` Transpilation
Using the `m2cgen` (Model to Code Generator) library, we transpiled the trained LightGBM ensemble tree structures directly into a raw Abstract Syntax Tree (AST), which was then compiled into pure, native Python code.

The resulting artifact is a single `.py` file containing nothing but nested `if/else` statements representing the exact decision splits of the LightGBM trees.

### 9.2 Vercel Edge Deployment
Because the inference file requires exactly **zero external dependencies** (no `pandas`, no `numpy`, no `lightgbm` runtime), it can be deployed directly to Vercel Serverless Functions.

When a user interacts with the Next.js frontend (the Policy Explorer), the sliders pass the hypothetical deployer features (e.g., `past_launches = 2`, `deployer_age = 86400`) to the Vercel serverless API. The API routes the data through the raw Python `if/else` statements and returns the probability score in under 50 milliseconds.

### 9.3 CI/CD Equivalence Testing
To ensure the transpiled AST model did not lose precision during conversion, we implemented strict Continuous Integration (CI) testing. We generated a "Golden Inference Vector"—a dataset of 10,000 predictions made by the original LightGBM model. 

During the GitHub Actions build step, the raw Python AST model must score all 10,000 vectors with **100.00% floating-point equivalence** to the LightGBM baseline before the build is allowed to pass.

---

## 10. The Next.js Interactive Dashboard

The culmination of this research is not a static PDF, but a highly interactive React application built on Next.js 16 and Tailwind CSS v4.

### 10.1 The Policy Explorer
The flagship feature of the dashboard is the interactive Policy Explorer. Users are presented with a real-time UI where they can manually manipulate the causal-in-time features of a hypothetical token deployer. 

As the user slides the "Wallet Age" or "Previous Launches" toggles, the UI pings the serverless AST endpoint, returning the exact probability that the target bot would snipe the token. This allows anyone to visually feel the decision boundary of the bot without writing a line of code.

### 10.2 Transparent Scientific Communication
The dashboard translates the complex PR-AUC metrics, temporal isolation boundaries, and SHAP analyses into beautiful, animated UI components. By leveraging Framer Motion and Lucide icons, the heavy data science concepts are made accessible to DeFi researchers, developers, and investors alike.

---

## 11. Conclusion and Future Horizons

The Zero-Block Deconstruction project successfully proves that highly complex, latency-sensitive MEV and sniper bot strategies leave indelible behavioral fingerprints on the blockchain. By adhering to rigorous scientific standards—refusing to fabricate P&L, enforcing strict chronological data splits, and acknowledging the boundaries of our evidence—we were able to reverse-engineer a dominant on-chain trading policy.

The bot is not performing magic. It is executing a highly disciplined, risk-averse strategy that filters out noise (brand new wallets) and filters out serial scammers (high launch histories) to find the "Goldilocks" deployers.

### 11.1 Future Research Directions
1. **Graph Convolutional Networks (GCNs):** Expanding the feature space to include the funding graph. If we can trace where the deployer's initial SOL originated (e.g., a centralized exchange hot wallet), we may be able to capture the "Residual Regime" of serial deployers.
2. **NLP on Token Metadata:** Analyzing the token name, ticker, and description using lightweight LLMs or TF-IDF to see if the bot has semantic preferences (e.g., preferring meme-coins over utility tokens).
3. **Multi-Bot Clustering:** Applying unsupervised learning (e.g., DBSCAN or K-Means) to the entire population of pump.fun buyers to cluster different "species" of sniper bots based on their behavioral fingerprints.

### 11.2 The Open Science Commitment
This entire pipeline—from the raw SQL extraction queries, to the temporal feature engine, to the LightGBM training notebook, to the Next.js serverless dashboard—is fully open-sourced. 

We invite the community to clone the repository, run the `pytest` scientific integrity suites, and explore the boundaries of on-chain behavioral analysis.

*(End of Comprehensive Writeup)*
