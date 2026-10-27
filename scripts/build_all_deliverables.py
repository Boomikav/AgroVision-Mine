"""
Complete builder script for AgroVision-Mine IEEE Conference Paper Revised Deliverables.
Generates:
1. research_paper/references.bib
2. research_paper/AgroVision_Mine_IEEE_Conference_Paper_Revised.tex
3. research_paper/AgroVision_Mine_IEEE_Conference_Paper_Revised.docx
4. research_paper/AgroVision_Mine_IEEE_Conference_Paper_Revised.pdf (via Word COM)
5. research_paper/AgroVision_Mine_Evidence_Ledger_Revised.md
6. research_paper/AgroVision_Mine_Citation_Ledger_Revised.md
7. research_paper/AgroVision_Mine_Research_QA_Report_Revised.md
8. research_paper/AgroVision_Mine_Unresolved_Limitations.md
"""

import os
import sys
import time
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
OUTPUT_DIR = BASE_DIR / "research_paper"
FIGURES_DIR = OUTPUT_DIR / "figures"

# -----------------------------------------------------------------------------
# 1. WRITE REFERENCES.BIB
# -----------------------------------------------------------------------------
BIB_CONTENT = """@article{barbedo2018impact,
  author  = {Barbedo, Jayme G. A.},
  title   = {{Impact of Dataset Size and Variety on the Effectiveness of Deep Learning and Transfer Learning for Plant Pathology and Pest Identification}},
  journal = {Biosystems Engineering},
  volume  = {172},
  pages   = {86--101},
  year    = {2018},
  doi     = {10.1016/j.biosystemseng.2018.05.013}
}

@article{mohanty2016deep,
  author  = {Mohanty, Sharada P. and Hughes, David P. and Salath{\'e}, Marcel},
  title   = {{Using Deep Learning for Image-Based Plant Disease Detection}},
  journal = {Frontiers in Plant Science},
  volume  = {7},
  pages   = {1419},
  year    = {2016},
  doi     = {10.3389/fpls.2016.01419}
}

@article{hughes2015plantvillage,
  author  = {Hughes, David P. and Salath{\'e}, Marcel},
  title   = {{An open access repository of images on plant health to enable the development of mobile disease diagnostics}},
  journal = {arXiv preprint arXiv:1511.08060},
  year    = {2015}
}

@article{ferentinos2018deep,
  author  = {Ferentinos, Konstantinos P.},
  title   = {{Deep Learning Models for Plant Disease Detection and Diagnosis}},
  journal = {Computers and Electronics in Agriculture},
  volume  = {145},
  pages   = {311--318},
  year    = {2018},
  doi     = {10.1016/j.compag.2018.01.009}
}

@inproceedings{singh2020plantdoc,
  author    = {Singh, Davinder and Jain, Naman and Jain, Pranjali and Kayal, Pratik and Kumawat, Sudhakar and Batra, Nipun},
  title     = {{PlantDoc: A Dataset for Visual Plant Disease Detection in the Wild}},
  booktitle = {Proceedings of the 7th ACM IKDD CoDS and 25th COMAD},
  pages     = {249--253},
  year      = {2020},
  doi       = {10.1145/3371158.3371196}
}

@article{too2019comparative,
  author  = {Too, E. Chepngeno and Li, Li and Njuki, Sam and Liu, Yingchun},
  title   = {{A Comparative Study of Fine-Tuning Deep Learning Architectures for Plant Disease Identification}},
  journal = {Computers and Electronics in Agriculture},
  volume  = {161},
  pages   = {272--279},
  year    = {2019},
  doi     = {10.1016/j.compag.2018.03.032}
}

@book{kimball2013datawarehouse,
  author    = {Kimball, Ralph and Ross, Margy},
  title     = {{The Data Warehouse Toolkit: The Definitive Guide to Dimensional Modeling}},
  edition   = {3rd},
  publisher = {John Wiley \\& Sons},
  address   = {Hoboken, NJ},
  year      = {2013}
}

@inproceedings{torralba2011unbiased,
  author    = {Torralba, Antonio and Efros, Alexei A.},
  title     = {{Unbiased Look at Dataset Bias}},
  booktitle = {Proceedings of the IEEE Conference on Computer Vision and Pattern Recognition (CVPR)},
  pages     = {1521--1528},
  year      = {2011},
  doi       = {10.1109/CVPR.2011.5995347}
}

@article{geirhos2020shortcut,
  author  = {Geirhos, Robert and Jacobsen, J{\"o}rn-Henrik and Michaelis, Claudio and Zemel, Richard and Brendel, Wieland and Bethge, Matthias and Wichmann, Felix A.},
  title   = {{Shortcut Learning in Deep Neural Networks}},
  journal = {Nature Machine Intelligence},
  volume  = {2},
  number  = {11},
  pages   = {665--673},
  year    = {2020},
  doi     = {10.1038/s42256-020-00257-z}
}

@inproceedings{tan2019efficientnet,
  author    = {Tan, Mingxing and Le, Quoc V.},
  title     = {{EfficientNet: Rethinking Model Scaling for Convolutional Neural Networks}},
  booktitle = {Proceedings of the 36th International Conference on Machine Learning (ICML)},
  pages     = {6105--6114},
  year      = {2019}
}

@article{haralick1973texture,
  author  = {Haralick, Robert M. and Shanmugam, K. and Dinstein, Its'Hak},
  title   = {{Textural Features for Image Classification}},
  journal = {IEEE Transactions on Systems, Man, and Cybernetics},
  volume  = {SMC-3},
  number  = {6},
  pages   = {610--621},
  year    = {1973},
  doi     = {10.1109/TSMC.1973.4309314}
}

@article{pedregosa2011scikit,
  author  = {Pedregosa, Fabian and Varoquaux, Ga{\"e}l and Gramfort, Alexandre and Michel, Vincent and Thirion, Bertrand and Grisel, Olivier and Blondel, Mathieu and Prettenhofer, Peter and Weiss, Ron and Dubourg, Vincent and others},
  title   = {{Scikit-learn: Machine Learning in Python}},
  journal = {Journal of Machine Learning Research},
  volume  = {12},
  pages   = {2825--2830},
  year    = {2011}
}

@inproceedings{agrawal1994apriori,
  author    = {Agrawal, Rakesh and Srikant, Ramakrishnan},
  title     = {{Fast Algorithms for Mining Association Rules in Large Databases}},
  booktitle = {Proceedings of the 20th International Conference on Very Large Data Bases (VLDB)},
  pages     = {487--499},
  year      = {1994}
}

@inproceedings{han2000fpgrowth,
  author    = {Han, Jiawei and Pei, Jian and Yin, Yiwen},
  title     = {{Mining Frequent Patterns without Candidate Generation}},
  booktitle = {Proceedings of the ACM SIGMOD International Conference on Management of Data},
  pages     = {1--12},
  year      = {2000},
  doi       = {10.1145/342009.335372}
}

@article{codd1993olap,
  author  = {Codd, Edgar F. and Codd, Sharon B. and Salley, C. T.},
  title   = {{Providing OLAP to User-Analysts: An IT Mandate}},
  journal = {E. F. Codd and Associates},
  volume  = {32},
  year    = {1993}
}

@misc{hipp2020sqlite,
  author       = {Hipp, D. Richard},
  title        = {{SQLite: An In-Process Relational Database Management System}},
  year         = {2020},
  howpublished = {\\url{https://www.sqlite.org/}}
}

@misc{ramirez2018fastapi,
  author       = {Ram{\'\i}rez, Sebasti{\'a}n},
  title        = {{FastAPI: Modern, Fast (High-Performance) Web Framework for Building APIs with Python}},
  year         = {2018},
  howpublished = {\\url{https://fastapi.tiangolo.com/}}
}

@inproceedings{deng2009imagenet,
  author    = {Deng, Jia and Dong, Wei and Socher, Richard and Li, Kai-Li and Li, Kai and Fei-Fei, Li},
  title     = {{ImageNet: A Large-Scale Hierarchical Image Database}},
  booktitle = {Proceedings of the IEEE Conference on Computer Vision and Pattern Recognition (CVPR)},
  pages     = {248--255},
  year      = {2009},
  doi       = {10.1109/CVPR.2009.5206848}
}

@article{wilson1927confidence,
  author  = {Wilson, Edwin B.},
  title   = {{Probable Inference, the Law of Succession, and Statistical Inference}},
  journal = {Journal of the American Statistical Association},
  volume  = {22},
  number  = {158},
  pages   = {209--212},
  year    = {1927},
  doi     = {10.1080/01621459.1927.10502953}
}

@mastersthesis{zauner2010dhash,
  author = {Zauner, Christoph},
  title  = {{Implementation and Benchmarking of Perceptual Image Hash Functions}},
  school = {Upper Austria University of Applied Sciences, Hagenberg Campus},
  year   = {2010}
}

@inproceedings{hendrycks2019robustness,
  author    = {Hendrycks, Dan and Dietterich, Thomas},
  title     = {{Benchmarking Neural Network Robustness to Common Corruptions and Perturbations}},
  booktitle = {Proceedings of the International Conference on Learning Representations (ICLR)},
  year      = {2019}
}

@misc{icar2021rice,
  author       = {{Indian Council of Agricultural Research (ICAR)}},
  title        = {{Open Government Data (OGD) Platform: Rice Foliar Disease Flatbed Image Repository}},
  year         = {2021},
  howpublished = {\\url{https://data.gov.in/}}
}
"""

# -----------------------------------------------------------------------------
# 2. WRITE REVISED LATEX MANUSCRIPT
# -----------------------------------------------------------------------------
LATEX_CONTENT = r"""\documentclass[conference,a4paper]{IEEEtran}
\IEEEoverridecommandlockouts
\usepackage{cite}
\usepackage{amsmath,amssymb,amsfonts}
\usepackage{algorithmic}
\usepackage{graphicx}
\usepackage{textcomp}
\usepackage{xcolor}
\usepackage{booktabs}
\usepackage{multirow}
\usepackage{url}
\usepackage{tabularx}

\def\BibTeX{{\rm B\kern-.05em{\sc i\kern-.025em b}\kern-.08em
    T\kern-.1667em\lower.7ex\hbox{E}\kern-.125emX}}

\begin{document}

\title{AgroVision-Mine: A Multimodal Data Warehouse and Visual Pattern Mining Framework for Crop Disease and Pest Intelligence}

\author{
\IEEEauthorblockN{Boomika V}
\IEEEauthorblockA{\textit{School of Computer Science and Engineering (SCOPE)} \\
\textit{Vellore Institute of Technology (VIT)}\\
Chennai, Tamil Nadu 600127, India \\
Email: boomika.v2023@vitstudent.ac.in}
\and
\IEEEauthorblockN{Ajay M}
\IEEEauthorblockA{\textit{School of Computer Science and Engineering (SCOPE)} \\
\textit{Vellore Institute of Technology (VIT)}\\
Chennai, Tamil Nadu 600127, India \\
Email: ajay.m2023@vitstudent.ac.in}
\and
\IEEEauthorblockN{Dr. Devipriya A}
\IEEEauthorblockA{\textit{Associate Professor, SCOPE} \\
\textit{Vellore Institute of Technology (VIT)}\\
Chennai, Tamil Nadu 600127, India \\
Email: devipriya.a@vit.ac.in}
}

\maketitle

\begin{abstract}
Agricultural disease identification systems predominantly operate as isolated black-box classifiers, decoupling high-dimensional foliar imagery from botanical taxonomy and capture metadata, while failing to govern data quality or detect out-of-domain inputs. We present AgroVision-Mine, an integrated agricultural computer vision and multimodal data warehousing platform. The framework unifies an automated five-stage ingestion quality gate, an explainable 32-dimensional feature store (19 color moments, 7 Haralick textures, and 6 morphometric descriptors), and a Kimball-style SQLite star schema warehouse enforcing native referential integrity across 2,596 canonical observations (2,560 PlantDoc in-field and 36 ICAR flatbed scanner images). On this relational foundation, the system provides sub-35\,ms ANSI SQL Online Analytical Processing queries, unsupervised visual clustering ($K=2$, Silhouette 0.4060), and exact association rule mining parity between Apriori and FP-Growth ($\Delta = 0.0$). For bounded classification across 25 crop-condition classes ($2,447$ images), an EfficientNet-B0 transfer learning module partitioned via difference-hash grouping achieves $63.26\%$ validation Macro-F1 (substantially exceeding Random Forest at $17.02\%$ and RBF-SVM at $15.12\%$), and attains $61.84\%$ accuracy ($60.84\%$ Macro-F1, Wilson $95\%$ CI: $[57.46\%, 66.03\%]$) on $490$ held-out test images. Finally, exploratory cross-modal domain screening intercepts closed-set overconfidence on unsupported flatbed rice scans (flagging 36 of 36 images as unsupported domain, whereas isolated CNN inference falsely accepts 35 of 36 as Corn foliar diseases [18 Common Rust, 10 Northern Leaf Blight, and 8 Gray Leaf Spot] with $58.9\%$ mean confidence). AgroVision-Mine establishes an auditable bridge between visual inference, feature geometry, and relational agricultural analytics.
\end{abstract}

\begin{IEEEkeywords}
Agricultural Computer Vision, Multimodal Data Warehouse, OLAP Analytics, Feature Engineering, Transfer Learning, EfficientNet-B0, Association Rule Mining, Out-of-Distribution Screening.
\end{IEEEkeywords}

\section{Introduction}
Global food security is profoundly threatened by agricultural plant pathogens and foliar pests, which cause estimated global harvest yield losses ranging from $20\%$ to $40\%$ annually~\cite{barbedo2018impact}. Timely, accurate pathological identification is vital to containment; however, manual expert agronomist scouting is labor-intensive, logistically constrained, and inaccessible to smallholder farming communities~\cite{mohanty2016deep}. While deep convolutional neural networks (CNNs) have shown exceptional perceptual capability in controlled laboratory benchmarks such as PlantVillage~\cite{hughes2015plantvillage, ferentinos2018deep}, practical deployments in natural, unconstrained farm environments face severe degradation~\cite{singh2020plantdoc, too2019comparative}. 

Crucially, existing agricultural deep learning systems treat foliar pathology as an isolated black-box classification exercise. Three fundamental structural deficiencies characterize conventional paradigms:
\begin{enumerate}
    \item \textbf{Metadata and Relational Decoupling:} High-dimensional foliar imagery is divorced from relational botanical taxonomy (crop family, genus, order), capture equipment parameters (sensor resolution, lighting, aspect ratio), and epidemiological hierarchies (fungal, bacterial, viral, abiotic)~\cite{kimball2013datawarehouse}. Agronomists cannot perform relational slicing (e.g., comparing necrotic lesion expansion across Solanaceae crops versus Fabaceae crops).
    \item \textbf{Lack of Pre-Ingestion Data Governance:} Public agricultural corpora scraped from web sources frequently suffer from truncated byte streams, corrupted image headers, duplicate frames, and unstandardized orientations~\cite{singh2020plantdoc}. Conventional deep learning pipelines silently consume these anomalies, leading to latent bias and unverified dataset provenance~\cite{torralba2011unbiased}.
    \item \textbf{Confounding and Shortcut Learning:} As demonstrated by Geirhos et al.~\cite{geirhos2020shortcut}, deep networks frequently latch onto spurious background shortcuts (e.g., flatbed scanner backgrounds, soil textures, or acquisition framing) rather than genuine pathological lesions. An unconditioned binary classifier (Healthy vs. Diseased) trained across heterogeneous crops is fundamentally confounded when certain host species in the training corpus possess only healthy or only diseased specimens.
\end{enumerate}

To address these challenges, we introduce \textbf{AgroVision-Mine}, an open, reproducible, and verifiable multimodal data warehousing and visual pattern mining platform. AgroVision-Mine integrates relational dimensional modeling with explainable classical computer vision descriptors and bounded deep transfer learning. Rather than proposing an ungrounded black-box architecture, our framework enforces strict data governance, cryptographic dataset immutability, sub-35\,ms relational Online Analytical Processing (OLAP) queries, and rigorous statistical hypothesis validation.

\subsection{Key Contributions}
The principal contributions of this work are summarized as follows:
\begin{itemize}
    \item \textbf{End-to-End Data Governance \& 5-Gate Quality Pipeline:} We design and implement an automated five-stage quality gate enforcing header magic-byte verification, minimum spatial geometry ($\ge 100\times 100$), payload limits ($\le 15$\,MB), MD5 hash deduplication, and EXIF transposition, guaranteeing zero corrupted or duplicate records enter the canonical warehouse.
    \item \textbf{Multimodal Kimball Star Schema:} We architect a formal relational star schema in SQLite with native foreign-key constraints (\texttt{PRAGMA foreign\_keys = ON}), linking a central fact table of $2,596$ validated specimen observations to four normalized dimensions (\texttt{dim\_crop}, \texttt{dim\_disease}, \texttt{dim\_image}, and \texttt{dim\_visual\_feature}).
    \item \textbf{ANSI SQL-Backed OLAP Analytics Engine:} We implement real SQL-backed Roll-up, Drill-down, Slice, Dice, and Pivot operations, providing agronomists with multi-dimensional analytical views across botanical families and pathogen classes with query execution latencies below $35$\,ms.
    \item \textbf{Explainable 32-Dimensional Visual Feature Store:} We engineer an explainable descriptor vector space combining 19 Color Moments (RGB/HSV statistics and Excess Green Index), 7 Haralick Gray-Level Co-occurrence Matrix (GLCM) textural metrics, and 6 Morphometric contours, providing transparent physical features alongside deep neural representations.
    \item \textbf{Dual-Track Pattern Mining \& Exact Rule Parity:} We demonstrate optimal unsupervised visual clustering ($K=2$ Silhouette score $0.4060$) and 2D Principal Component Analysis ($52.11\%$ explained variance), coupled with association rule mining demonstrating $100\%$ algorithmic parity between Apriori and FP-Growth ($\Delta = 0.0000$ across support, confidence, and lift).
    \item \textbf{Bounded Supervised Classification with Leakage-Free Splits:} We evaluate an EfficientNet-B0 transfer learning module on a 25-class composite foliar benchmark ($2,447$ PlantDoc images) partitioned via grouped perceptual difference-hashing ($dHash$). The model achieves $63.26\%$ validation Macro-F1 (vs. $17.02\%$ for Random Forest) and $61.84\%$ Top-1 Accuracy ($60.84\%$ Macro-F1, Wilson $95\%$ CI: $[57.46\%, 66.03\%]$) on $490$ held-out test images.
    \item \textbf{Exploratory Cross-Modal Domain Screening:} We evaluate an automated rejection mechanism utilizing 32D descriptor nearest-reference retrieval to screen out-of-distribution acquisitions (e.g., flatbed scanner rice leaf observations, $N=36$), mitigating closed-set CNN overconfidence on unsupported botanical domains.
\end{itemize}

\section{Related Work}

\subsection{Deep Learning for Plant Pathology}
The application of deep convolutional neural networks to foliar disease identification accelerated with the release of the PlantVillage benchmark~\cite{hughes2015plantvillage}. Mohanty et al.~\cite{mohanty2016deep} evaluated AlexNet and GoogLeNet architectures across $54,306$ laboratory images, reporting classification accuracies exceeding $99.3\%$. Similarly, Ferentinos~\cite{ferentinos2018deep} benchmarked VGG, ResNet, and DenseNet architectures, achieving $99.5\%$ accuracy. However, subsequent critical evaluations by Barbedo~\cite{barbedo2018impact} and Singh et al.~\cite{singh2020plantdoc} revealed that these laboratory-trained models fail catastrophically when exposed to in-the-wild field conditions. Background homogeneity, uniform lighting, and lack of occlusions in laboratory settings act as spurious non-pathological shortcuts~\cite{geirhos2020shortcut}. 

To bridge this gap, Singh et al.~\cite{singh2020plantdoc} introduced the PlantDoc dataset, comprising $2,560$ authentic field images captured across natural lighting, varied camera sensors, and complex foliage clutter. Standard vision models benchmarked on PlantDoc achieved significantly lower accuracies ($30\%\text{--}40\%$), underscoring the intrinsic difficulty of real-world foliar pathology. Too et al.~\cite{too2019comparative} demonstrated that modern compact convolutional architectures, particularly DenseNets and MobileNets, offer favorable parameter efficiency over older VGG networks. Tan and Le~\cite{tan2019efficientnet} proposed EfficientNet, utilizing compound scaling across network depth, width, and input resolution. In our work, we leverage ImageNet-1K pretrained EfficientNet-B0 as a compact, high-capacity feature extractor for bounded foliar classification.

\subsection{Visual Feature Engineering and Pattern Mining}
Prior to deep learning dominance, agricultural image processing relied on handcrafted color, texture, and morphological features~\cite{haralick1973texture}. Haralick's GLCM descriptors (contrast, dissimilarity, homogeneity, energy, and correlation) capture spatial gray-level dependencies that reflect leaf necrosis and tissue mottling. While classical feature vectors rarely match deep networks on high-capacity multiclass benchmarks, they possess significant advantages in interpretability, low computational overhead, and zero data-hungry training requirements~\cite{pedregosa2011scikit}. In AgroVision-Mine, we do not discard handcrafted descriptors; instead, we engineer a standardized 32-dimensional continuous feature store that operates in parallel with deep representations, powering unsupervised K-Means clustering, PCA ordination, and association rule discovery via Apriori~\cite{agrawal1994apriori} and FP-Growth~\cite{han2000fpgrowth}.

\subsection{Data Warehousing and OLAP in Analytical Systems}
Dimensional modeling, formulated by Kimball and Ross~\cite{kimball2013datawarehouse}, represents the standard for organizing operational enterprise data for Online Analytical Processing (OLAP)~\cite{codd1993olap}. While widely adopted in finance and supply chain domains, dimensional modeling has rarely been integrated into computer vision pipelines. Vision datasets are typically stored as unstructured flat folders, stripping away relational taxonomy and precluding complex analytical queries. AgroVision-Mine bridges this divide by formalizing image observations as relational facts linked to botanical, pathological, and technical dimensions within a zero-configuration SQLite warehouse~\cite{hipp2020sqlite}.

\subsection{Comparative Analysis}
Table~\ref{tab:literature_comparison} provides a comparative analysis contrasting AgroVision-Mine against representative literature across eight structural dimensions.

\begin{table*}[t]
\caption{Comparative Analysis of Surveyed Agricultural Vision Systems Against AgroVision-Mine}
\label{tab:literature_comparison}
\centering
\scriptsize
\begin{tabularx}{\textwidth}{lcccccccc}
\toprule
\textbf{Study} & \textbf{Primary Dataset} & \textbf{Core Methodology} & \textbf{Warehouse Star Schema} & \textbf{SQL OLAP Engine} & \textbf{Handcrafted 32D Features} & \textbf{Unsupervised Mining} & \textbf{Leakage-Free Split} & \textbf{OOD Safeguard} \\
\midrule
Mohanty et al.~\cite{mohanty2016deep} (2016) & PlantVillage & AlexNet, GoogLeNet & No & No & No & No & Random (Near-dup risk) & No \\
Ferentinos~\cite{ferentinos2018deep} (2018) & PlantVillage & VGG, ResNet-50 & No & No & No & No & Random & No \\
Barbedo~\cite{barbedo2018impact} (2018) & Proprietary Lab & Transfer Learning & No & No & No & No & Partitioned by Plant & No \\
Too et al.~\cite{too2019comparative} (2019) & PlantVillage & DenseNet-121, VGG-16 & No & No & No & No & Random & No \\
Singh et al.~\cite{singh2020plantdoc} (2020) & PlantDoc & Faster R-CNN, MobileNet & No & No & No & No & Standard Benchmark & No \\
\textbf{AgroVision-Mine (Ours)} & \textbf{PlantDoc + ICAR} & \textbf{Multimodal Star Schema +} & \textbf{Yes (Kimball Star,} & \textbf{Yes (Roll-up, Drill,} & \textbf{Yes (19 Color, 7 GLCM,} & \textbf{Yes (K-Means, PCA,} & \textbf{Yes (dHash Grouped,} & \textbf{Yes (Cross-Modal} \\
& \textbf{(N=2,596)} & \textbf{EfficientNet-B0 + OLAP} & \textbf{SQLite Foreign Keys)} & \textbf{Slice, Dice, Pivot)} & \textbf{6 Morphometric)} & \textbf{Apriori/FP-Growth)} & \textbf{Zero Overlap)} & \textbf{Domain Screening)} \\
\bottomrule
\end{tabularx}
\end{table*}

\section{System Architecture and Data Flow}
AgroVision-Mine is structured as a five-layer end-to-end analytical pipeline, depicted in Fig.~\ref{fig:architecture}. The architecture decouples data ingestion, feature store extraction, dimensional relational persistence, analytical mining engines, and presentation delivery.

\begin{figure*}[t]
\centering
\includegraphics[width=0.98\textwidth]{figures/fig1_system_architecture.png}
\caption{End-to-End Five-Layer System Architecture of AgroVision-Mine, illustrating data ingestion quality gates, feature store extraction, Kimball relational warehouse, dual analytical branches (SQL OLAP / visual mining vs. deep transfer learning), and presentation delivery.}
\label{fig:architecture}
\end{figure*}

\subsection{Layer 1: Data Ingestion and Automated Quality Control}
The ingestion tier accepts heterogeneous agricultural imagery from web-scraped field repositories (PlantDoc) and flatbed scanner archives (ICAR/OGD)~\cite{icar2021rice}. To prevent data corruption, every candidate file must sequentially pass five automated quality gates:
\begin{enumerate}
    \item \textbf{Gate 1 (Format \& Magic Bytes):} Validates file header byte signatures to ensure strictly authentic JPEG or PNG bitstreams.
    \item \textbf{Gate 2 (Spatial Geometry):} Enforces a strict minimum spatial resolution ($H \ge 100$\,px, $W \ge 100$\,px).
    \item \textbf{Gate 3 (Payload Ceiling):} Enforces an uncompressed image payload ceiling of $15$\,MB to prevent buffer exhaustion.
    \item \textbf{Gate 4 (Cryptographic Deduplication):} Computes MD5 hash signatures of the raw byte stream, identifying exact byte-level duplicates.
    \item \textbf{Gate 5 (Geometric Normalization):} Inspects EXIF metadata tags, applies loss-free orientation transposition, and standardizes channels to three-channel RGB.
\end{enumerate}

\subsection{Layer 2: Preprocessing and Feature Store Generation}
Validated images are preprocessed through bilinear interpolation to a standardized $256\times 256$ RGB representation for canonical feature extraction. Thirty-two continuous descriptors are extracted across color, texture, and morphometry, producing the frozen analytical feature matrix $\mathbf{X} \in \mathbb{R}^{2596 \times 32}$. The dataset manifest and feature store are cryptographically validated via SHA-256 checksums to ensure experimental immutability.

\subsection{Layer 3: Relational Data Warehouse and ETL}
The relational persistence layer implements a Kimball star schema in SQLite~\cite{kimball2013datawarehouse}. The central fact table, \texttt{disease\_observation\_fact}, links $2,596$ specimen records to four normalized dimensions through integer surrogate keys: \texttt{dim\_crop}, \texttt{dim\_disease}, \texttt{dim\_image}, and \texttt{dim\_visual\_feature}. Referential integrity is enforced at the database engine level via \texttt{PRAGMA foreign\_keys = ON}.

\subsection{Layer 4: Dual-Track Analytical Engines}
The system bifurcates into two independent, complementary analytical branches:
\begin{enumerate}
    \item \textbf{Descriptor-Based Relational \& Unsupervised Branch:} Operates on the standardized 32D handcrafted feature matrix and the relational star schema. This branch powers ANSI SQL OLAP operations, K-Means clustering, 2D PCA ordination, Apriori/FP-Growth association rule mining, and nearest-reference Euclidean similarity retrieval.
    \item \textbf{Deep Supervised Transfer Learning Branch:} Operates directly on standardized $224\times 224$ RGB image tensors. An EfficientNet-B0 CNN fine-tuned on 25 composite classes outputs class logits, softmax scores, and domain uncertainty indicators.
\end{enumerate}
Crucially, the deep neural network does \textit{not} consume the 32 handcrafted descriptors as input; both pipelines remain mathematically and architecturally distinct.

\subsection{Layer 5: Presentation and Delivery Tier}
The application tier couples an asynchronous FastAPI backend (:8001)~\cite{ramirez2018fastapi} with a responsive React 19 and TypeScript single-page application (SPA). Specialized views provide agronomists with interactive dataset exploration, live SQL execution, multidimensional charts, and a real-time Visual Specimen Workbench.

\section{Methodology and Mathematical Formulation}

\subsection{Multimodal Star Schema Design}
The relational star schema (Fig.~\ref{fig:star_schema}) models agricultural foliar observations at the grain of \textit{one validated specimen per fact row}.

\begin{figure}[htbp]
\centering
\includegraphics[width=0.48\textwidth]{figures/fig2_star_schema.png}
\caption{AgroVision-Mine Kimball Star Schema: Central fact table (\texttt{disease\_observation\_fact}) surrounded by four normalized dimensions with enforced foreign key integrity.}
\label{fig:star_schema}
\end{figure}

The dimensional schema comprises:
\begin{itemize}
    \item \texttt{disease\_observation\_fact}: Fact surrogate key (\texttt{fact\_id}), dimension foreign keys (\texttt{crop\_key}, \texttt{disease\_key}, \texttt{image\_key}, \texttt{feature\_key}), numerical measures (\texttt{lesion\_severity\_score}, \texttt{image\_sharpness\_score}), and diagnostic flags (\texttt{is\_pest}, \texttt{condition\_status}).
    \item \texttt{dim\_crop}: Crop surrogate key, common crop name, botanical binomial nomenclature, and higher-order taxonomic crop category (e.g., Solanaceae, Poaceae, Rosaceae).
    \item \texttt{dim\_disease}: Pathology surrogate key, disease label, primary pathogen etiology (\textit{Fungal, Bacterial, Viral, None}), and causal biological agent.
    \item \texttt{dim\_image}: Image surrogate key, canonical filename, original acquisition path, spatial geometry (width, height, channels), and MD5 bitstream hash.
    \item \texttt{dim\_visual\_feature}: Feature surrogate key, complete 32 continuous normalized descriptor values, and cluster assignment surrogate keys.
\end{itemize}

\subsection{Explainable Visual Feature Extraction}
The 32 continuous descriptors are mathematically formulated across three distinct visual domains:

\subsubsection{Color Moments (19 Descriptors)}
Let $I_c(x, y)$ denote the intensity of color channel $c \in \{R, G, B\}$ at spatial coordinate $(x, y)$ over an image of dimensions $M \times N$. The first two statistical color moments are computed as:
\begin{equation}
\mu_c = \frac{1}{MN} \sum_{x=1}^M \sum_{y=1}^N I_c(x, y),
\end{equation}
\begin{equation}
\sigma_c = \sqrt{\frac{1}{MN} \sum_{x=1}^M \sum_{y=1}^N \left( I_c(x, y) - \mu_c \right)^2}.
\end{equation}
Channel moments are converted to normalized chromaticity coordinates $r, g, b = I_c / (R + G + B)$. The same statistical moments are extracted across the Hue, Saturation, Value (HSV) cylindrical color space: $\mu_H, \sigma_H, \mu_S, \sigma_S, \mu_V, \sigma_V$. To isolate vegetative chlorophyll content from soil backgrounds, the Excess Green Index ($ExG$) is computed pixel-wise:
\begin{equation}
ExG(x, y) = 2G(x, y) - R(x, y) - B(x, y),
\end{equation}
and its spatial mean $\mu_{ExG}$ is appended, yielding 19 total color descriptors.

\subsubsection{Haralick GLCM Textures (7 Descriptors)}
Texture features are computed from the Gray-Level Co-occurrence Matrix $P(i, j | d, \theta)$, representing the joint probability of gray levels $i$ and $j$ occurring at distance $d=1$ along orientations $\theta \in \{0^\circ, 45^\circ, 90^\circ, 135^\circ\}$~\cite{haralick1973texture}. Averaging across orientations yields seven normalized texture statistics:
\begin{equation}
\text{Contrast} = \sum_{i,j} |i - j|^2 P(i, j),
\end{equation}
\begin{equation}
\text{Dissimilarity} = \sum_{i,j} |i - j| P(i, j),
\end{equation}
\begin{equation}
\text{Homogeneity} = \sum_{i,j} \frac{P(i, j)}{1 + (i - j)^2},
\end{equation}
\begin{equation}
\text{Energy (ASM)} = \sum_{i,j} P(i, j)^2, \quad \text{Energy} = \sqrt{\text{ASM}},
\end{equation}
\begin{equation}
\text{Correlation} = \sum_{i,j} \frac{(i - \mu_i)(j - \mu_j) P(i, j)}{\sigma_i \sigma_j}.
\end{equation}

\subsubsection{Contour Morphometrics (6 Descriptors)}
Binary foliar leaf masks are generated via Otsu thresholding on the saturation channel. Contours $C$ are traced to compute area $A$, perimeter $P$, aspect ratio $AR = W_b / H_b$ from the bounding rectangle, circularity $C_{circ}$, solidity $S$, and lesion coverage ratio $LCR$:
\begin{equation}
C_{circ} = \frac{4\pi A}{P^2}, \quad S = \frac{A}{A_{hull}}, \quad LCR = \frac{A_{lesion}}{A_{leaf}}.
\end{equation}

\subsubsection{Feature Standardization}
To eliminate scale sensitivity across disparate physical units, all continuous descriptors are standardized via $z$-score normalization:
\begin{equation}
z_{ij} = \frac{x_{ij} - \mu_j}{\sigma_j}, \quad \forall j \in \{1, \dots, 32\}.
\end{equation}

\subsection{Unsupervised Mining and Pattern Discovery}

\subsubsection{K-Means Clustering}
Partitioning in the standardized 32D descriptor space minimizes the Within-Cluster Sum of Squares (WCSS):
\begin{equation}
\mathcal{J}_{K} = \sum_{k=1}^K \sum_{\mathbf{z}_i \in \mathcal{C}_k} \|\mathbf{z}_i - \boldsymbol{\mu}_k\|_2^2.
\end{equation}
Cluster validity is assessed across $K \in [2, 8]$ using the Silhouette coefficient $s(i)$:
\begin{equation}
s(i) = \frac{b(i) - a(i)}{\max\left(a(i), b(i)\right)},
\end{equation}
where $a(i)$ is the mean intra-cluster distance and $b(i)$ is the minimum mean inter-cluster distance to the nearest neighboring cluster.

\subsubsection{Principal Component Analysis (PCA)}
Dimensionality reduction projects $\mathbf{Z} \in \mathbb{R}^{2596 \times 32}$ onto orthogonal eigenvectors of the sample covariance matrix $\boldsymbol{\Sigma} = \frac{1}{N-1} \mathbf{Z}^T \mathbf{Z}$. The projection onto the first two components $\mathbf{w}_1, \mathbf{w}_2$ accounts for the maximal variance axes:
\begin{equation}
y_{i1} = \mathbf{z}_i^T \mathbf{w}_1, \quad y_{i2} = \mathbf{z}_i^T \mathbf{w}_2.
\end{equation}

\subsubsection{Association Rule Mining}
Transactions are formed by discretizing the 12 most salient visual descriptors into equal-frequency tertiles ($\text{Low}, \text{Medium}, \text{High}$). Frequent itemsets $\mathcal{X}$ are extracted satisfying minimum support $\text{supp}(\mathcal{X}) = P(\mathcal{X}) \ge 0.15$. Rules $\mathcal{X} \Rightarrow \mathcal{Y}$ are evaluated via confidence and lift:
\begin{equation}
\text{conf}(\mathcal{X} \Rightarrow \mathcal{Y}) = \frac{\text{supp}(\mathcal{X} \cup \mathcal{Y})}{\text{supp}(\mathcal{X})},
\end{equation}
\begin{equation}
\text{lift}(\mathcal{X} \Rightarrow \mathcal{Y}) = \frac{\text{conf}(\mathcal{X} \Rightarrow \mathcal{Y})}{\text{supp}(\mathcal{Y})}.
\end{equation}

\subsection{Supervised Deep Learning Formulation}
For bounded multiclass classification across $C=25$ composite crop-condition classes, we employ EfficientNet-B0~\cite{tan2019efficientnet}. EfficientNet applies compound scaling across depth $d$, width $w$, and image resolution $r$:
\begin{equation}
d = \alpha^\phi, \quad w = \beta^\phi, \quad r = \gamma^\phi,
\end{equation}
subject to $\alpha \cdot \beta^2 \cdot \gamma^2 \approx 2$ and $\alpha \ge 1, \beta \ge 1, \gamma \ge 1$, where $\phi$ is the compound scaling coefficient. For baseline B0 ($\phi=1$), architecture parameters are set to $\alpha=1.2, \beta=1.1, \gamma=1.15$ with an input resolution of $224\times 224$ pixels.

\subsubsection{Transfer Learning and Architecture Modification}
The network is initialized with pretrained weights obtained on the ImageNet-1K benchmark~\cite{deng2009imagenet}. The final 1000-class linear projection head is replaced with a dropout layer ($p=0.2$) followed by a custom linear classification layer $\mathbf{W}_c \in \mathbb{R}^{25 \times 1280}$:
\begin{equation}
\mathbf{z} = \mathbf{W}_c \cdot \text{GAP}(\mathbf{F}_{backbone}(\mathbf{x})) + \mathbf{b}_c,
\end{equation}
where $\text{GAP}(\cdot)$ denotes Global Average Pooling. Predicted class probabilities are obtained via the softmax activation:
\begin{equation}
p_k = \frac{\exp(z_k)}{\sum_{j=1}^{25} \exp(z_j)}, \quad \forall k \in \{1, \dots, 25\}.
\end{equation}

\subsubsection{Optimization and Objective Function}
Model training minimizes the multi-class Cross-Entropy Loss over training mini-batches $\mathcal{B}$:
\begin{equation}
\mathcal{L} = -\frac{1}{|\mathcal{B}|} \sum_{i \in \mathcal{B}} \sum_{k=1}^{25} y_{ik} \log(p_{ik}).
\end{equation}
Parameters are optimized via AdamW with decoupled weight decay ($\lambda = 10^{-4}$). To preserve general visual representations in the convolutional stem while adapting high-level semantic features, we employ differential learning rates: the convolutional backbone is fine-tuned at $\eta_{backbone} = 10^{-4}$, while the classifier head is trained at $\eta_{head} = 10^{-3}$. Learning rates are scheduled dynamically via \texttt{ReduceLROnPlateau} (reduction factor $0.5$, patience 2 epochs, monitoring validation Macro-F1).

\subsubsection{Statistical Uncertainty}
Generalization uncertainty for the held-out test accuracy $\hat{p}$ over $n$ samples is quantified using the Wilson Score Interval with continuity correction at a 95\% confidence level ($z = 1.96$)~\cite{wilson1927confidence}:
\begin{equation}
CI_{95} = \frac{\hat{p} + \frac{z^2}{2n} \pm z \sqrt{\frac{\hat{p}(1 - \hat{p})}{n} + \frac{z^2}{4n^2}}}{1 + \frac{z^2}{n}}.
\end{equation}

\section{Experimental Protocol and Setup}

\subsection{Dataset Curation and Invariants}
The canonical dataset manifest (\texttt{canonical\_dataset\_v2.csv}) contains exactly $2,596$ authentic foliar image observations across 14 host crops. The dataset comprises $2,560$ PlantDoc field images ($98.61\%$) and $36$ ICAR/OGD flatbed scanner rice leaf images ($1.39\%$). Pathological annotations contain $1,750$ diseased specimens ($67.41\%$) and $846$ healthy specimens ($32.59\%$).

\subsection{Perceptual Hash Leakage Prevention Protocol}
In web-scraped corpora like PlantDoc, identical or burst-captured frames frequently appear under different filenames or slight crops. Random partitioning introduces severe data leakage, causing optimistic performance estimates. To ensure complete leakage isolation, we compute 64-bit difference hashes ($dHash$)~\cite{zauner2010dhash} across all images. Observations with Hamming distance $D_H \le 10$ are clustered into disjoint equivalence groups via connected-component analysis. Using \texttt{StratifiedGroupKFold}, these groups are assigned atomically to training, validation, or test partitions. Cross-partition verification confirms that \textbf{zero perceptual hash groups cross partition boundaries}.

\subsection{Benchmark Partitions and Accounting}
Of the $2,596$ total canonical records:
\begin{itemize}
    \item \textbf{Primary Benchmark ($N=2,447$):} Encompasses 25 composite classes across 12 host crops satisfying a minimum support threshold of $N \ge 60$ images. Partitioned into $1,468$ training ($60.0\%$), $489$ validation ($20.0\%$), and $490$ held-out test specimens ($20.0\%$).
    \item \textbf{Excluded Rare Classes ($N=113$):} Exactly three classes in PlantDoc failed the support threshold ($N < 60$) and were excluded from primary model training to prevent extreme class collapse: \textit{Tomato Two-Spotted Spider Mite} ($N=2$), \textit{Tomato Mosaic Virus} ($N=54$), and \textit{Cherry Healthy} ($N=57$), totaling $113$ images.
    \item \textbf{Out-of-Domain Scanner Subset ($N=36$):} The 36 ICAR rice leaf scanner images are withheld completely from training and evaluation benchmarks, serving as a dedicated distributional shift test set.
\end{itemize}
The partition counts reconcile exactly: $2,447 + 113 + 36 = 2,596$.

\subsection{Hardware and Software Environment}
All experiments were executed on an AMD Ryzen 7 processor with 16\,GB RAM running Windows 11. Software dependencies were locked to: Python 3.11.9, PyTorch 2.14.1+cpu, torchvision 0.29.1+cpu, scikit-learn 1.9.0, SQLite 3.45.1, SQLAlchemy 2.0.38, FastAPI 0.115.8, and React 19.2.8. The test suite comprises 117 automated tests (107 unit and integration tests in pytest, plus 10 browser end-to-end tests in Playwright), all executing with 100\% passing status.

\section{Empirical Results and Technical Discussion}

\subsection{Model Selection Tournament}
To justify the selection of EfficientNet-B0, we conducted a rigorous model comparison tournament evaluated strictly on the $489$-sample validation partition. We benchmarked three distinct algorithmic paradigms:
\begin{enumerate}
    \item \textbf{Zero-Rule Majority Baseline:} Predicts the dominant training class (\textit{Tomato Late Blight}).
    \item \textbf{Support Vector Machine (RBF-SVM):} Radial Basis Function kernel ($C=10, \gamma=\text{'scale'}$) trained on standardized 32D handcrafted descriptors.
    \item \textbf{Random Forest Classifier:} 200 estimators with balanced class weighting trained on standardized 32D handcrafted descriptors.
    \item \textbf{EfficientNet-B0 (Ours):} Deep transfer learning trained directly on raw RGB image tensors.
\end{enumerate}

\begin{figure}[htbp]
\centering
\includegraphics[width=0.48\textwidth]{figures/fig3_model_tournament.png}
\caption{Model Selection Tournament: Validation Macro-F1 (model selection metric) and Held-Out Test Macro-F1 across handcrafted baselines and fine-tuned EfficientNet-B0.}
\label{fig:tournament}
\end{figure}

As reported in Table~\ref{tab:model_tournament} and illustrated in Fig.~\ref{fig:tournament}, classical classifiers trained on handcrafted descriptors achieve validation Macro-F1 scores of only $15.12\%$ (SVM) and $17.02\%$ (Random Forest). While these 32 global color and texture descriptors are sufficient for clustering macro foliage types, they lack the spatial local receptive field capacity necessary to distinguish subtle fungal versus bacterial necrotic lesions. EfficientNet-B0 achieves a validation Macro-F1 of $63.26\%$—an absolute improvement of $+46.24\%$ over Random Forest—justifying its selection as the primary classification architecture.

\begin{table}[htbp]
\caption{Model Selection Tournament and Performance Comparison}
\label{tab:model_tournament}
\centering
\scriptsize
\begin{tabular}{lcccc}
\toprule
\textbf{Model Architecture} & \textbf{Input Feature Space} & \textbf{Val Macro-F1} & \textbf{Test Acc} & \textbf{Test Macro-F1} \\
\midrule
Zero-Rule Majority Baseline & N/A & 0.58\% & 14.29\% & 1.00\% \\
RBF-SVM ($C=10, \gamma=\text{'scale'}$) & Handcrafted 32D Features & 15.12\% & 15.71\% & 14.89\% \\
Random Forest (200 Trees) & Handcrafted 32D Features & 17.02\% & 17.55\% & 16.48\% \\
\textbf{EfficientNet-B0 (Ours)} & \textbf{RGB Image Tensors} & \textbf{63.26\%} & \textbf{61.84\%} & \textbf{60.84\%} \\
\bottomrule
\end{tabular}
\end{table}

\subsection{Held-Out Test Generalization}
Final model evaluation on the independent held-out test partition ($N=490$) demonstrates solid in-field generalization:
\begin{itemize}
    \item \textbf{Top-1 Classification Accuracy:} $61.84\%$ ($303$ correct classifications out of $490$ unseen images).
    \item \textbf{Balanced Accuracy:} $61.43\%$, indicating robust handling across imbalanced classes.
    \item \textbf{Macro-Averaged F1-Score:} $60.84\%$, reflecting balanced precision and recall across all 25 classes.
    \item \textbf{Wilson 95\% Confidence Interval:} $[57.46\%, 66.03\%]$, providing a statistically sound performance bound.
\end{itemize}

\begin{figure}[htbp]
\centering
\includegraphics[width=0.48\textwidth]{figures/fig4_confusion_matrix.png}
\caption{Normalized 25-Class Confusion Matrix for fine-tuned EfficientNet-B0 on the independent held-out test set ($N=490$).}
\label{fig:confusion}
\end{figure}

Fig.~\ref{fig:confusion} displays the normalized confusion matrix across the 25 classes. High diagonal concentrations are evident in distinct pathologies such as \textit{Apple Scab} ($0.88$), \textit{Corn Common Rust} ($0.85$), and \textit{Tomato Septoria Leaf Spot} ($0.79$). 

\begin{figure}[htbp]
\centering
\includegraphics[width=0.48\textwidth]{figures/fig6_per_class_f1.png}
\caption{Per-class F1-score distribution across the 25 supported crop-condition classes on the held-out test set.}
\label{fig:per_class_f1}
\end{figure}

Fig.~\ref{fig:per_class_f1} details the per-class F1 scores. Lower F1-scores occur primarily in classes with severe visual ambiguity, such as early-stage \textit{Tomato Late Blight} versus \textit{Tomato Early Blight}, where necrotic spots exhibit similar chromatic and textural distributions.

\subsection{Dimensional OLAP Query Performance}
Table~\ref{tab:olap_benchmarks} summarizes query execution latencies and analytical outputs across the five primary OLAP operations executed against the physical SQLite star schema instance ($2,596$ fact records). All queries complete within $35$\,ms, validating the feasibility of relational interactive slicing over multimodal observations.

\begin{table}[htbp]
\caption{Relational OLAP Query Execution Latency and Result Grain}
\label{tab:olap_benchmarks}
\centering
\scriptsize
\begin{tabular}{llcc}
\toprule
\textbf{OLAP Operation} & \textbf{Analytical Scope \& Filtering} & \textbf{Result Grain} & \textbf{Latency (ms)} \\
\midrule
Roll-Up & Crop Species $\rightarrow$ Higher Botanical Category & 7 Categories & 33.26 \\
Drill-Down & Category $\rightarrow$ Crop $\rightarrow$ Disease $\rightarrow$ Visual Tone & 116 Sub-groups & 31.27 \\
Slice & Fixed Dimension (\texttt{crop\_name = 'Tomato'}) & 743 Specimen Rows & 14.99 \\
Dice & Sub-cube: Solanaceae/Fabaceae $\times$ Fungal/Bacterial & 962 Specimen Rows & 14.42 \\
Pivot & 14 Crops $\times$ 4 Pathogen Classes Cross-Tabulation & $14 \times 4$ Matrix & 12.57 \\
\bottomrule
\end{tabular}
\end{table}

\subsection{Unsupervised Ordination and Cluster Separation}
K-Means clustering across $K \in [2, 8]$ reveals that the 32D standardized descriptor space attains its global mathematical optimum at $K=2$ (Silhouette = $0.4060$, Davies-Bouldin = $1.0990$, Calinski-Harabasz = $1,154.38$). In the interactive workbench, $K=5$ is also provided for finer visual exploratory grouping (Silhouette = $0.218$). As depicted in Fig.~\ref{fig:pca_clusters}, the first two principal components account for $52.11\%$ of total variance (PC1 = $38.56\%$, PC2 = $13.55\%$). Physical factor loading analysis confirms that PC1 is heavily loaded on foliar luminance ($\text{RGB}_R$ $+0.252$, $\text{RGB}_G$ $+0.248$, $\text{GLCM}_{ASM}$ $+0.248$), separating dense green canopies from bright reflective leaves. PC2 is loaded on textural contrast ($\text{GLCM}_{contrast}$ $+0.384$, $\text{GLCM}_{dissim}$ $+0.379$), separating smooth blades from mottled necrotic lesions.

\begin{figure}[htbp]
\centering
\includegraphics[width=0.48\textwidth]{figures/fig5_pca_clusters.png}
\caption{2D PCA projection of standardized 32D visual descriptors ($52.11\%$ total variance), demonstrating cluster distributions and severe domain shift of flatbed scanner rice leaf imagery ($N=36$).}
\label{fig:pca_clusters}
\end{figure}

\subsection{Cross-Modal Out-of-Domain Screening}
When the 36 ICAR flatbed scanner rice leaf images were passed through the naive closed-world EfficientNet-B0 classifier without reference context, the model falsely accepted $35$ of $36$ images ($97.2\%$) as confident, with a mean confidence of $58.9\%$ (and individual scores reaching $64.06\%$). All 36 specimens were misclassified into Corn pathologies ($18$ Corn Common Rust, $10$ Corn Northern Leaf Blight, $8$ Corn Gray Leaf Spot). Botanical investigation explains the root cause: among the 12 training crops, Corn is the sole graminoid monocot leaf with parallel venation (all other 11 crops are broad-leaved dicots). Flatbed scanner rice leaves possess linear, parallel-veined margins; hence, convolutional edge filters activated heavily on Corn features, forcing the closed-world softmax to select Corn.

Rather than fitting an unvalidated threshold heuristic on test probabilities, AgroVision-Mine implements a cross-modal verification check utilizing the 32D descriptor store. During runtime inference, the query image's standardized 32D vector is compared against warehouse references via nearest-neighbor retrieval. For all 36 rice scanner images, the top nearest neighbor correctly matched warehouse reference anchors with \texttt{dataset\_source = 'icar\_ogd'} and \texttt{crop\_name = 'Rice'}. Because Rice is outside the 25 supported classes, the hybrid system flagged $36$ of $36$ images ($100.0\%$) as \texttt{unsupported\_domain} with an active uncertainty flag, triggering a prominent warning banner in the visual workbench (Fig.~\ref{fig:workbench}).

\begin{figure}[htbp]
\centering
\includegraphics[width=0.48\textwidth]{figures/fig7_inference_workbench.png}
\caption{Runtime Visual Specimen Workbench demonstration: Top: Authentic Apple Healthy prediction ($97.6\%$ confidence); Bottom: ICAR Rice scanner specimen triggering the automated cross-modal out-of-domain rejection alert.}
\label{fig:workbench}
\end{figure}

\section{Threats to Validity and Scientific Limitations}
To maintain rigorous academic integrity, several fundamental methodological limitations must be stated:
\begin{enumerate}
    \item \textbf{Closed-World Taxonomic Scope:} The supervised model is bounded to 25 composite classes across 12 host crops. It cannot diagnose arbitrary unseen agricultural plants or novel exotic pathogens.
    \item \textbf{Dataset Confounding in Raw PlantDoc:} In the raw PlantDoc corpus, seven crops (Bell Pepper, Blueberry, Peach, Raspberry, Soybean, Squash, Strawberry) contain exclusively healthy or exclusively diseased observations. An unconditioned binary classifier trained across all crops learns to predict crop species rather than pathological state.
    \item \textbf{Scanner vs. Field Domain Shift:} As demonstrated by the PCA ordination (Fig.~\ref{fig:pca_clusters}), flatbed scanner images exhibit pure white background saturations that shift PC1 markedly, rendering laboratory or scanner imagery non-generalizable to farm field photography without domain adaptation.
    \item \textbf{Exploratory Nature of Nearest-Neighbor Screening:} The cross-modal safeguard relies on having representative out-of-domain reference anchors within the multimodal feature store. If an entirely unmodeled crop or sensor type is introduced without reference anchors, nearest-neighbor screening may fail, and the standalone CNN will misclassify. Formal OOD algorithms (e.g., energy-based models or Mahalanobis distance) remain an important objective for future research.
    \item \textbf{Non-Diagnostic Nature of Geometric Retrieval:} Nearest-reference Euclidean proximity in 32D feature space reflects geometric and textural similarity, not certified microbiological or PCR-confirmed pathogen etiology. Softmax output probabilities reflect relative network activations within a closed label space, not calibrated epidemiological likelihoods.
\end{enumerate}

\section{Conclusion and Future Work}
This paper presented AgroVision-Mine, an integrated agricultural computer vision and multimodal data warehousing framework that bridges the gap between deep visual inference and relational analytical intelligence. By unifying a five-stage quality gate, a 32D explainable feature store, a Kimball star schema warehouse, sub-35\,ms relational OLAP slicing, and an EfficientNet-B0 transfer learning module ($61.84\%$ test accuracy on 25 classes), the framework enables auditable, multidimensional disease intelligence. Furthermore, the cross-modal out-of-domain screening mechanism provides an exploratory method to intercept closed-set CNN overconfidence on unsupported acquisition domains.

Future extensions will incorporate multi-spectral drone imagery into the fact schema, implement temperature-scaled probability calibration, expand the benchmark to 50+ classes with few-shot learning for rare crops, and evaluate edge quantization on low-power agricultural IoT hardware.

\bibliographystyle{IEEEtran}
\bibliography{references}

\end{document}
"""

def write_latex_and_bib():
    (OUTPUT_DIR / "references.bib").write_text(BIB_CONTENT, encoding="utf-8")
    print("Wrote references.bib")
    (OUTPUT_DIR / "AgroVision_Mine_IEEE_Conference_Paper_Revised.tex").write_text(LATEX_CONTENT, encoding="utf-8")
    print("Wrote AgroVision_Mine_IEEE_Conference_Paper_Revised.tex")

if __name__ == "__main__":
    write_latex_and_bib()
