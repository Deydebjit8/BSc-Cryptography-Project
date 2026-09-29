# Survey: neural networks and information security

Background, literature survey, applications and bibliography from the project report *A Survey on Information Security Using Artificial Neural Network* (April 2024). The implementation is described in [algorithm.md](algorithm.md).

## 1. Why information security needs adaptive methods

Sensitive data such as health records and financial transactions lives on interconnected systems. That exposes it to data breaches, unauthorised access, infiltration and manipulation, and the threats keep changing. Security solutions therefore have to be robust and adaptable.

Artificial neural networks (ANNs) are inspired by the structure and learning ability of the brain. They can find patterns in large data sets, learn from new data and adapt to a changing environment, which makes them a candidate technique for security tasks.

## 2. Cryptography in brief

Cryptography scrambles data with mathematical algorithms so that unauthorised parties cannot read it. The report highlights three properties:

| Property | Meaning |
|---|---|
| Confidentiality | Only authorised users can read the information; encrypted data looks like gibberish without the key. |
| Integrity | Data stays unaltered in transit or storage; unauthorised changes are detected. |
| Authenticity | The source of the data is verified and impersonation is prevented. |

There are two families of cryptographic systems:

- **Symmetric cryptography** uses one secret key for encryption and decryption. It is efficient, but the key must be shared securely, and a leaked key exposes everything it protects. The project implements a symmetric scheme.
- **Asymmetric cryptography** uses a public/private key pair: the public key is distributed and encrypts, the private key stays secret and decrypts. Key distribution is easier, but the computations are more expensive.

## 3. Artificial neural networks

An ANN is a network of simple processing units (neurons) arranged in layers:

- **Input layer** receives the raw data, for example network traffic or system logs.
- **Hidden layers** extract features and learn relationships. Their number and size depend on the task.
- **Output layer** produces the result, such as a classification (normal or malicious) or a prediction.

Neurons are connected by *synapses*; each connection carries a *weight* that scales the signal, like a volume knob. During training the weights are adjusted whenever the output is wrong, which is how the network learns. In the biological analogy used by the report, *dendrites* collect incoming signals and a single *axon* passes the result on.

Common architectures:

- **Perceptron** — the simplest network: the inputs feed one output neuron directly, with no hidden layer.
- **Multilayer perceptron (MLP)** — one or more hidden layers; widely used for pattern recognition and classification.
- **Convolutional neural network (CNN)** — suited to grid-like data such as images and time series; used for image recognition and traffic-anomaly detection.
- **Feed-forward neural network (FNN)** — connections never form cycles, so information moves one way from the input through the hidden layers to the output. It is the model the project uses for the layout of its encryption heuristic.

Key capabilities: pattern recognition, learning and adaptation.

## 4. Where ANNs help in security

- **Malware detection** — learn from large sets of malicious and benign samples and recognise malicious code by its patterns.
- **Spam filtering** — separate legitimate e-mail from spam using content and sender features.
- **Anomaly detection** — flag deviations from normal behaviour, such as unauthorised access attempts or unusual resource use.
- **Data security** — spot unusual data-access patterns and help prevent exfiltration.

## 5. Literature survey

| Ref. | Work | Focus |
|---|---|---|
| [1] | Pawlicki, Kozik, Choraś (2022) | Survey of neural networks for cyber-security and of the security of neural networks; challenges of ANN-based intrusion detection, combining a literature review with the authors' experience. |
| [2] | Karmakar, Kundu, Paul (2018) | Data transmission with symmetric-key cryptography on a multilayer feed-forward network; a random key is generated and coded through the hidden layers. |
| [3] | Paul et al. (2013) | Network security with a genetic algorithm: public-key cryptography aiming at confidentiality, authentication, integrity and non-repudiation. |
| [4] | Tragha, Omary, Mouloudi (2006) | Improved cryptography inspired by genetic algorithms. |
| [5] | Mondal, Mollah, Samanta, Paul (2016) | Survey of network security with a genetic algorithm, using symmetric-key cryptography for confidentiality, authentication, integrity and non-repudiation. |
| [6] | Lee, Kim, Kim, Han (2019) | Cyber-threat detection with artificial neural networks using event profiles. |
| [7] | Cantemir, Kandemir (2024) | CNNs for architectural-style classification, an example of ANN use outside security. |

## 6. Applications

The report lists these areas for ANN-based security:

1. **Network security** — intrusion detection that analyses traffic in real time to identify malware, DDoS attacks and unauthorised access.
2. **Financial institutions** — fraud detection by finding anomalous patterns in transaction data.
3. **Healthcare** — protecting sensitive patient information and supporting regulatory compliance such as HIPAA.
4. **E-commerce** — analysing user behaviour, transaction history and payment data to detect card fraud and identity theft.
5. **Endpoint security** — monitoring system behaviour to detect malware, ransomware and other threats.
6. **Critical infrastructure** — power plants, transport and water treatment: detecting cyber threats and vulnerabilities from operational data.
7. **Cloud security** — monitoring traffic, detecting unauthorised access and anomalies in cloud applications and services.
8. **Mobile security** — analysing app behaviour, network communication and device activity to counter malware and phishing.

## 7. Bibliography

1. Marek Pawlicki, Rafał Kozik, Michał Choraś, "A survey on neural networks for (cyber-) security and (cyber-) security of neural networks", Elsevier, Volume 500, 21 August 2022, pp. 1075–87.
2. Kushal Karmakar, Soumik Kundu, Soumya Paul, "Design and Implementation of Information Security using Neural Network Architecture", International Journal of Applied Engineering Research, ISSN 0973-4562, Volume 13, Number 11 (2018), pp. 9916–9923.
3. Soumya Paul et al., "Implementation of Network Security Using Genetic Algorithm", Vol. 3, Issue 2, February 2013, ISSN 2277-128X.
4. A. Tragha, F. Omary, A. Mouloudi, "Improved Cryptography Inspired by Genetic Algorithms", ICIGA, 2006 International Conference on Hybrid Information Technology (ICHIT'06).
5. Subhrajit Mondal, Tania Khatun Mollah, Arindam Samanta, Soumya Paul, "A Survey on Network Security Using Genetic Algorithm", International Journal of Innovative Research in Science, Engineering and Technology, Vol. 5, Issue 1, January 2016.
6. Jonghoon Lee, Jonghyun Kim, Ikkyun Kim, Kijun Han, "Cyber Threat Detection Based on Artificial Neural Networks Using Event Profiles", IEEE Access, Volume 7, 2019.
7. Ece Cantemir, Ozlem Kandemir, "Use of artificial neural networks in architecture: determining the architectural style of a building with a convolutional neural networks", Springer, Volume 36, 2024, pp. 6195–6207.
8. William Stallings, *Cryptography and Network Security*, 2nd edition.
9. Puneet Goswami, *Neural Network: An Approach for Cryptography*.
10. Atul Kahate, *Cryptography and Network Security*.
11. Rajib Mall, *Fundamentals of Software Engineering*.
12. Roger S. Pressman, *Software Engineering: A Practitioner's Approach*.
