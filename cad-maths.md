
---

# 1.  Formal Core 1 Mathematical Definition (Risk Function)

We now turn Core 1 into a **well-defined forensic scoring function over a pretrained model**.

---

##  1.1 Notation

Let:

* ( M ) = pretrained HF model
* ( x \sim \mathcal{P} ) = synthetic probe distribution (no task labels required)
* ( f_M(\cdot) ) = model representation extractor (e.g., hidden states / embeddings)
* ( \delta(x) ) = perturbation operator
* ( h(\cdot) ) = clustering function (e.g., KMeans in latent space)
* ( g(\cdot) ) = geometry estimator (e.g., covariance / manifold drift metric)

---

##  1.2 Core signals

### (A) Embedding instability

[
S_{emb} = \mathbb{E}_{x \sim \mathcal{P}} \left[ | f_M(x) - f_M(\delta(x)) |_2 \right]
]

---

### (B) Cluster shift instability

Let:

* ( C_{clean} = h(f_M(x)) )
* ( C_{pert} = h(f_M(\delta(x))) )

[
S_{cluster} = d_H(C_{clean}, C_{pert})
]

(where ( d_H ) = clustering divergence metric, e.g., adjusted Rand distance or centroid displacement)

---

### (C) Geometry drift

[
S_{geo} = D\big(\Sigma_{clean}, \Sigma_{pert}\big)
]

where:

* ( \Sigma ) = covariance of embeddings
* ( D ) = matrix divergence (Frobenius, log-det divergence, etc.)

---

### (D) Perturbation sensitivity

[
S_{pert} = \mathbb{E}*{x \sim \mathcal{P}} \left[ | M(x) - M(\delta(x)) |*{pred} \right]
]

(logit divergence or KL divergence)

---

##  1.3 Unified Core 1 Risk Function

### Final risk score:

[
R(M) =
\alpha S_{emb}

* \beta S_{cluster}
* \gamma S_{geo}
* \lambda S_{pert}
  ]

---

##  1.4 Decision rule

[
\text{Decision}(M) =
\begin{cases}
\text{BACKDOOR} & \text{if } R(M) > \tau \
\text{CLEAN} & \text{otherwise}
\end{cases}
]

---

##  1.5 Key property (important for paper)

> Core 1 is a **model-only functional**:
> [
> R: M \rightarrow \mathbb{R}
> ]

No dataset labels required → only synthetic probe distribution.

---

# 2.  What is truly novel (peer-review survival test)

Now we isolate what is **actually defensible as novelty vs Pub 1–4**.

---

##  NOT novel (reviewers will reject if claimed alone)

These already exist in literature:

* activation clustering → Pub 2
* perturbation testing → Pub 3 & 4
* robustness sensitivity scoring → Pub 4
* backdoor taxonomy → Pub 1

---

##  Weak novelty (only incremental)

* combining clustering + perturbation
* adding geometry drift
* ensemble anomaly scoring

 Reviewers will say:

> “straightforward combination of known signals”

---

##  Strong novelty (what you MUST claim)

Core 1 is only novel if framed as:

---

##  1. Model-only forensic functional (strongest claim)

> Prior work operates on datasets or samples.
> Core 1 defines a **functional over the model itself**.

✔ This is key shift:

* sample-space → model-space

---

##  2. Dataset-free post-hoc auditing

> No reliance on labeled or poisoned data distributions

This is **not standard in Pub 1–4 combined**

---

##  3. Multi-signal consistency collapse model

Instead of independent metrics:

> Core 1 assumes backdoors induce **joint structural inconsistency across representation geometry, clustering stability, and perturbation response**

This is:

 a unified hypothesis model
 not present in prior work

---

##  4. Representation-space forensic abstraction

 You are not detecting triggers—you are detecting **geometry inconsistency of learned function**

This is the strongest theoretical framing.

---

##  Final novelty statement (review-safe)

> Core 1 introduces a dataset-free forensic auditing framework that models pretrained neural networks as geometric objects in representation space and detects backdoor-induced inconsistencies via a unified multi-signal risk functional over embedding stability, clustering divergence, and perturbation sensitivity.

---

# 3.  Experimental Section Design (dataset-free claim validation)

This is where most papers fail—so we design it carefully.

---

##  3.1 Experimental goal

You must prove:

> Core 1 detects backdoors WITHOUT relying on labeled datasets

NOT:

* “it works better than SOTA”
  (bad framing initially)

---

##  3.2 Experimental groups

### Group A — Clean HF models

* BERT
* RoBERTa
* DistilBERT
* domain fine-tuned variants

### Group B — Backdoored models

Constructed via:

* trigger-based poisoning
* fine-tune injection
* weight-level Trojan insertion

---

##  3.3 Protocol (critical)

### Step 1: No dataset usage constraint

Only allow:

* synthetic probes ( x \sim \mathcal{P} )
* random token sequences or embedding-space sampling

---

### Step 2: Core 1 audit

Compute:

[
R(M)
]

for all models.

---

### Step 3: Separation test

Measure:

* ROC-AUC
* distribution separation
* calibration gap

---

### Step 4: Ablation study

Remove each signal:

* only clustering
* only perturbation
* only geometry

Show:

> performance drops → proves multi-signal necessity

---

##  3.4 Key claim validation

You must show:

* no training data access
* no labeled evaluation required for detection
* still separable risk distributions

---

# 4.  Attack/Defense Benchmark Protocol (Core 1 validation system)

This is your **publication-grade benchmark design**.

---

##  4.1 Attack suite

You include:

### (A) Classic backdoors

* BadNets-style triggers

### (B) Clean-label attacks

* subtle poisoning

### (C) Feature-space attacks

* embedding-target poisoning

### (D) Fine-tune trojans

* HF model fine-tuning backdoors

---

##  4.2 Defense baselines

Compare Core 1 against:

* activation clustering (Pub 2 baseline)
* perturbation methods (Pub 3/4 baselines)
* simple confidence anomaly detection
* pruning-based heuristics

---

##  4.3 Metrics

### Primary:

* AUROC (backdoor vs clean separation)
* AUPRC

### Secondary:

* calibration error of risk score
* false positive rate on clean HF models
* robustness across architectures

---

##  4.4 Stress tests (important novelty support)

* architecture shift test (BERT → RoBERTa)
* domain shift test (NLP → domain-specific HF models)
* random initialization sanity check

---

##  4.5 Key validation claim

You must show:

> Core 1 generalizes across architectures without retraining or dataset adaptation

---

#  Final synthesis (what you now have)

You now have a full publishable structure:

###  Mathematical foundation (Core 1 defined)

###  Novelty boundaries (what is truly new)

###  Experimental protocol (dataset-free validation)

###  Benchmark framework (attack/defense evaluation)

---

# If you want next step (high value options)

next upgrades geplannt:

### 1. Write full **ICLR/NeurIPS-style Method section**

### 2. Create **Figure 1 (system diagram + math mapping)**

### 3. Write **“Threat model + assumptions” section (review-critical)**

### 4. Build **pseudo-code for Core 1 algorithm (Algorithm 1 in paper)**

