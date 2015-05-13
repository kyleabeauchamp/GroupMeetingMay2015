% title: Making sense of large-scale simulations
% author: Kyle A. Beauchamp


---
title: Big (MD) Data

<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>frames</th>
      <th>n_traj</th>
      <th>n_trimmed</th>
      <th>name</th>
      <th>trimmed_frames</th>
      <th>trimmed_ns</th>
    </tr>
    <tr>
      <th>project</th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>10466</th>
      <td>2827085</td>
      <td>889</td>
      <td>310</td>
      <td>T4</td>
      <td>2338536</td>
      <td>584634.0</td>
    </tr>
    <tr>
      <th>10467</th>
      <td>2374175</td>
      <td>499</td>
      <td>305</td>
      <td>src</td>
      <td>1811264</td>
      <td>452816.0</td>
    </tr>
    <tr>
      <th>10468</th>
      <td>2351895</td>
      <td>499</td>
      <td>298</td>
      <td>abl</td>
      <td>1765658</td>
      <td>441414.5</td>
    </tr>
    <tr>
      <th>10478</th>
      <td>1340625</td>
      <td>928</td>
      <td>345</td>
      <td>setd8</td>
      <td>1034670</td>
      <td>258667.5</td>
    </tr>
  </tbody>
</table>


---
title: Lagtime matters: T4 Lysozyme


<center>
<img width=600 src=figures/t4_implied_timescales.png />
</center>


---
title: Lagtime matters: T4 Lysozyme tICA

<center>
<img width=600 src=figures/T4_tica_lag1.png />
</center>


---
title: Lagtime matters: T4 Lysozyme tICA


<center>
<img width=600 src=figures/T4_tica_lag400.png />
</center>

---
title: Lagtime matters: T4 Lysozyme tICA

- Easy to be misled!
- Slow eigenfunctions have poor overlap with dihedrals
- Better features are desirable--but finding them is a research project


---
title: setd8: Disconnected


<center>
<img width=600 src=figures/setd8_tica_lag400.png />
</center>

---
title: Is tICA overfit? (src)

- Probably not for dihedrals (low model complexity)
- Easy to overfit distances (high model complexity)
- Better safe than sorry--use best practices

---
title: Hyperparameter optimization: Osprey

- Create input dataset (e.g. `msmb DihedralFeaturizer`)
- Describe model space: `code/osprey_configs/tica.yaml`
- Submit cluster jobs via array submission: `qsub submit.sh -t 0-40%20`


<footer class="source">
https://github.com/pandegroup/osprey
</footer>


---
title: Describing the model space in YAML

<pre class="prettyprint" data-lang="yaml">
estimator:
    pickle: my-model.pkl
    entry_point: msmbuilder.decomposition.tICA
    eval: |
        Pipeline([
            ('tica', tICA(n_components=20, lag_time=400))
        ])
    eval_scope: msmbuilder

strategy:
    name: hyperopt_tpe  # or moe, hyperopt_tpe

[...]
</pre>

---
title: Describing the model space in YAML

<pre class="prettyprint" data-lang="yaml">
[...]

search_space:
  tica__gamma:
    min: 5e-4
    max: 2e-1
    type: float
    warp: log       # optimize using the log of the parameter

cv: 5  # the order of K-fold cross validation to use

dataset_loader:
  name: msmbuilder
  params:
    path: ./dihedrals
trials:
  uri: sqlite:///tica.db
</pre>


---
title: Optimizing Clustering models

- What kind of clustering should we use? (GMM, kmeans)
- How many tICA components should we use?
- How many clusters?

---
title: Optimizing Clustering models

<pre class="prettyprint" data-lang="yaml">
estimator:
    pickle: my-model.pkl
    entry_point: msmbuilder.decomposition.tICA
    eval: |
        Pipeline([
                ("slicer", FirstSlicer()),
                ("clusterer", GMM()),
                ("msm", MarkovStateModel(n_timescales=8, lag_time=400))
        ])
    eval_scope: msmbuilder

cv: 5  # the order of K-fold cross validation to use

strategy:
    name: hyperopt_tpe  # or moe, hyperopt_tpe

[...]

</pre>



---
title: Optimizing Clustering models

<pre class="prettyprint" data-lang="yaml">
search_space:
  slicer__first:
    min: 2
    max: 20
    type: int

  clusterer__n_components:
    min: 9
    max: 30
    type: int

dataset_loader:
  name: msmbuilder
  params:
    path: ./tica.h5
    
trials:
  uri: sqlite:///gmm.db
</pre>


---
title: tICA Cross Validation: src

<center>
<img width=600 src=figures/src_tica_cross_validation.png />
</center>


<footer class="source">
Note the gap!
</footer>


---
title: tICA Cross Validation: src

<center>
<img width=600 src=figures/src_tica_lag400_012.png />
</center>


---
title: Conclusions

- We can almost do automated analysis of large-scale MSMs
- Lagtime matters
- Trimming is still unsolved
- Still want better features
- Still more engineering to make the process painless

---
title: Acknowledgements

Sonya, Rafal, Robert McGibbon
