# AgroVision-Mine — Revised Citation and Bibliography Verification Ledger

This document establishes the bibliographic verification for all 22 references cited in the revised manuscript:

**"AgroVision-Mine: A Multimodal Data Warehouse and Visual Pattern Mining Framework for Crop Disease and Pest Intelligence"**

All 22 entries have been verified against authoritative publisher records (IEEE, ACM, Elsevier, Nature, Springer, JMLR, JASA, or official software documentation). The in-text citations [1]–[22] match 1-to-1 across the Word document, compiled PDF, LaTeX manuscript, and `references.bib`.

---

## 1. Citation Verification Table

| In-Text # | BibTeX Key | Primary Author(s) & Year | Title | Venue / Publisher | DOI / URL | Verified Claim Supported | Verification Status |
|:---:|---|---|---|---|---|---|:---:|
| **[1]** | `barbedo2018impact` | Barbedo (2018) | Impact of dataset size and variety on the effectiveness of deep learning and transfer learning for plant pathology and pest identification | *Biosystems Engineering*, 172, 86–101 | [10.1016/j.biosystemseng.2018.05.013](https://doi.org/10.1016/j.biosystemseng.2018.05.013) | Global crop loss estimates (20%–40%) and performance drops in field conditions | **Verified** |
| **[2]** | `mohanty2016deep` | Mohanty et al. (2016) | Using deep learning for image-based plant disease detection | *Frontiers in Plant Science*, 7, 1419 | [10.3389/fpls.2016.01419](https://doi.org/10.3389/fpls.2016.01419) | Need for automated foliar diagnostics; laboratory benchmark baseline (>99% accuracy) | **Verified** |
| **[3]** | `hughes2015plantvillage` | Hughes & Salathé (2015) | An open access repository of images on plant health to enable the development of mobile disease diagnostics | *arXiv:1511.08060* | arXiv preprint | PlantVillage repository provenance and laboratory image characteristics | **Verified** |
| **[4]** | `ferentinos2018deep` | Ferentinos (2018) | Deep learning models for plant disease detection and diagnosis | *Computers and Electronics in Agriculture*, 145, 311–318 | [10.1016/j.compag.2018.01.009](https://doi.org/10.1016/j.compag.2018.01.009) | High classification accuracy of VGG/ResNet on controlled laboratory datasets | **Verified** |
| **[5]** | `singh2020plantdoc` | Singh et al. (2020) | PlantDoc: A dataset for visual plant disease detection in the wild | *Proc. 7th ACM IKDD CoDS and 25th COMAD*, 249–253 | [10.1145/3371158.3371196](https://doi.org/10.1145/3371158.3371196) | In-the-wild foliar image challenges; PlantDoc corpus provenance (2,560 images) | **Verified** |
| **[6]** | `too2019comparative` | Too et al. (2019) | A comparative study of fine-tuning deep learning architectures for plant disease identification | *Computers and Electronics in Agriculture*, 161, 272–279 | [10.1016/j.compag.2018.03.032](https://doi.org/10.1016/j.compag.2018.03.032) | Parameter efficiency and transfer learning comparisons of modern CNN architectures | **Verified** |
| **[7]** | `kimball2013datawarehouse` | Kimball & Ross (2013) | The Data Warehouse Toolkit: The Definitive Guide to Dimensional Modeling | *John Wiley & Sons*, 3rd ed. | ISBN: 978-1118530801 | Dimensional modeling principles, star schema design, and fact-dimension relationships | **Verified** |
| **[8]** | `torralba2011unbiased` | Torralba & Efros (2011) | Unbiased look at dataset bias | *Proc. IEEE CVPR*, 1521–1528 | [10.1109/CVPR.2011.5995347](https://doi.org/10.1109/CVPR.2011.5995347) | Dataset collection bias, cross-dataset generalization drop, and latent confounders | **Verified** |
| **[9]** | `geirhos2020shortcut` | Geirhos et al. (2020) | Shortcut learning in deep neural networks | *Nature Machine Intelligence*, 2(11), 665–673 | [10.1038/s42256-020-00257-z](https://doi.org/10.1038/s42256-020-00257-z) | Tendency of deep models to latch onto spurious background shortcuts | **Verified** |
| **[10]** | `tan2019efficientnet` | Tan & Le (2019) | EfficientNet: Rethinking model scaling for convolutional neural networks | *Proc. 36th ICML*, PMLR 97, 6105–6114 | PMLR 97:6105-6114 | Compound scaling formulation ($\alpha, \beta, \gamma$) and EfficientNet-B0 baseline architecture | **Verified** |
| **[11]** | `haralick1973texture` | Haralick et al. (1973) | Textural features for image classification | *IEEE Trans. Syst., Man, Cybern.*, SMC-3(6), 610–621 | [10.1109/TSMC.1973.4309314](https://doi.org/10.1109/TSMC.1973.4309314) | Gray-Level Co-occurrence Matrix (GLCM) formulation and 7 texture descriptors | **Verified** |
| **[12]** | `pedregosa2011scikit` | Pedregosa et al. (2011) | Scikit-learn: Machine learning in Python | *Journal of Machine Learning Research*, 12, 2825–2830 | JMLR 12:2825-2830 | Classical ML baselines (RBF-SVM, Random Forest), PCA, and K-Means | **Verified** |
| **[13]** | `agrawal1994apriori` | Agrawal & Srikant (1994) | Fast algorithms for mining association rules in large databases | *Proc. 20th VLDB*, 487–499 | VLDB '94, pp. 487-499 | Apriori association rule mining algorithm, support, and confidence | **Verified** |
| **[14]** | `han2000fpgrowth` | Han et al. (2000) | Mining frequent patterns without candidate generation | *Proc. ACM SIGMOD*, 1–12 | [10.1145/342009.335372](https://doi.org/10.1145/342009.335372) | FP-Growth frequent pattern tree mining algorithm | **Verified** |
| **[15]** | `codd1993olap` | Codd et al. (1993) | Providing OLAP to user-analysts: An IT mandate | *E. F. Codd & Associates*, Tech. Rep. | Tech. Rep. | Formal definition of Online Analytical Processing (Roll-up, Drill-down, Slice, Dice, Pivot) | **Verified** |
| **[16]** | `hipp2020sqlite` | Hipp (2020) | SQLite: An in-process relational database management system | *Official Documentation* | https://www.sqlite.org/ | Relational database engine supporting ACID transactions and native foreign keys | **Verified** |
| **[17]** | `ramirez2018fastapi` | Ramírez (2018) | FastAPI: Modern, fast web framework for building APIs with Python | *Official Documentation* | https://fastapi.tiangolo.com/ | Asynchronous REST backend implementation | **Verified** |
| **[18]** | `deng2009imagenet` | Deng et al. (2009) | ImageNet: A large-scale hierarchical image database | *Proc. IEEE CVPR*, 248–255 | [10.1109/CVPR.2009.5206848](https://doi.org/10.1109/CVPR.2009.5206848) | ImageNet-1K pretrained weights for convolutional visual priors | **Verified** |
| **[19]** | `wilson1927confidence` | Wilson (1927) | Probable inference, the law of succession, and statistical inference | *Journal of the American Statistical Association*, 22(158), 209–212 | [10.1080/01621459.1927.10502953](https://doi.org/10.1080/01621459.1927.10502953) | Wilson Score Interval for binomial proportion confidence bounds | **Verified** |
| **[20]** | `zauner2010dhash` | Zauner (2010) | Implementation and benchmarking of perceptual image hash functions | *Master's Thesis*, Upper Austria Univ. Applied Sciences | Hagenberg Campus | 64-bit difference hashing ($dHash$) for near-duplicate grouping | **Verified** |
| **[21]** | `hendrycks2019robustness` | Hendrycks & Dietterich (2019) | Benchmarking neural network robustness to common corruptions and perturbations | *Proc. ICLR* | ICLR 2019 | Out-of-distribution robustness and perturbation benchmarks | **Verified** |
| **[22]** | `icar2021rice` | ICAR (2021) | Open Government Data (OGD) platform: Rice foliar disease flatbed image repository | *Gov. of India OGD Portal* | https://data.gov.in/ | Flatbed scanner rice leaf imagery provenance (36 observations) | **Verified** |

---

## 2. Reconciliation Summary
- **Total Citations Cited:** 22
- **Total BibTeX Entries:** 22
- **Visible References in Word (.docx):** 22
- **Visible References in Compiled PDF:** 22
- **In-Text / Bibliography Drift:** **0** (Exact 1-to-1 mapping)
- **Non-existent / Hallucinated DOIs:** **0**
