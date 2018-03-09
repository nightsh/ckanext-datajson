# Cherry picking from another forks

How to cherry pick from another forks?

```
git remote add <other-fork-alias> <other-fork-URL>
git checkout <branch>
git fetch <other-fork-alias>
git cherry-pick <commit-hash>
git push <your-fork-alias>
```

# Merge all actives versions
To upgrade this extension we analyzed other many. We started forking [the OKF datajson ext](https://github.com/avdata99/ckanext-datajson).  
Adding external forks

```
git remote add opengov https://github.com/OpenGov-OpenData/ckanext-datajson
git remote add viderum https://github.com/ViderumGlobal/ckanext-datajson
git remote add akariv https://github.com/akariv/ckanext-datajson
git remote add gsa https://github.com/GSA/ckanext-datajson
```

Fetching
```
git fetch opengov
git fetch viderum
git fetch akariv
git fetch gsa
```



List of commit to cherry-pick or analyze to include:  

20180309 https://github.com/OpenGov-OpenData/ckanext-datajson/commit/ae2748f6029b08223b42b6d03ad475957876fed5
20180309 paginate data.json https://github.com/OpenGov-OpenData/ckanext-datajson/commit/b668dcfd23e770b21b838872ee05e6f33287eb8d
20180801 [NO] removes bureau and progman codes https://github.com/OpenGov-OpenData/ckanext-datajson/commit/f5ab8afd54343e0207cb418467dbc7b9ec325c82
20180831 [YES] Fix validation https://github.com/ViderumGlobal/ckanext-datajson/commit/8cb92134e6e21a25c795557ddecbe14b887e1ef9
20180904 [YES] Fix getting extras https://github.com/ViderumGlobal/ckanext-datajson/commit/daedda3ba769150927136a5502db23db4362b2cf
check all ED branch at OKF
20181119 [?] AT ED BRANCH FROM Bureau and progman as extras https://github.com/okfn/ckanext-datajson/commit/a12768fd165f78112fd7f36f3d442555e7886c30
20181120 [?] Spatial as no-extra https://github.com/okfn/ckanext-datajson/commit/81b752de7c5bc91cdbc5d70736e169f1caa21a2a
20181120 [?] Temportal as no-extra https://github.com/okfn/ckanext-datajson/commit/2be2fe429f95e5b685ca715d2301f254de5588e4
20181207 Add missing pod schema https://github.com/OpenGov-OpenData/ckanext-datajson/commit/784489ca0ef05659314317d3c836d0e7e4ad5aad
20181210 Add mediaType https://github.com/OpenGov-OpenData/ckanext-datajson/commit/e58fa780b18999738b0518017ca768053109fd53+
20181212 Simplify validation languaje https://github.com/OpenGov-OpenData/ckanext-datajson/commit/685c8c38b4c4fc7fd1b3b33dec9abb4d48ee78fc
--> and back ... https://github.com/OpenGov-OpenData/ckanext-datajson/commit/3f50f43ac77def7708c3e409449c72851890c3a0
20181212 Only datasets for data.json https://github.com/OpenGov-OpenData/ckanext-datajson/commit/88eb76cae2aa262cf88c4d8a9e25a841e1ade771
20190528 Analyze accrual_periodicity https://github.com/ViderumGlobal/ckanext-datajson/commit/205e748b13cd8159d60d29696a6171c70ace62fb
20190425 Hotfix dict https://github.com/akariv/ckanext-datajson/commit/407294c12dbdd290c0a829748f4a4413a25d96e1
20190425 More on accrual_periodicity https://github.com/akariv/ckanext-datajson/commit/d0386071216ec69c5981ae32cacc5c15fecf390c
20190425 Check https://github.com/akariv/ckanext-datajson/commit/1620a73af9330108a8e9ac3a2fa40164d617b32c
--> and https://github.com/akariv/ckanext-datajson/commit/15ddbd88cb52ec63e637768d17451281c9251bc0
20190530 fix export map path https://github.com/OpenGov-OpenData/ckanext-datajson/commit/10691e4c2d1069782caf37dc686afee2d62832e6
20190530 fix package to pod https://github.com/OpenGov-OpenData/ckanext-datajson/commit/5915c95c5e71b2c440bce255eb187fb5ca002060
20190604 logs for GSA https://github.com/GSA/ckanext-datajson/commit/91254e49fba5079835943d5818cbfdb7f4aad6d7
20190614 fix SSL https://github.com/ViderumGlobal/ckanext-datajson/commit/33660c62bd537f664f3cd0cbd42b30277bf20141
20190628 check mailto at mantainer_email https://github.com/ViderumGlobal/ckanext-datajson/commit/873e7c83018ae23eb29c56164561d3f637625f7a
20190819 If pagination reaches the last page we don't want to display the full dataset results https://github.com/OpenGov-OpenData/ckanext-datajson/commit/61f216e487dd3a530c61cf8672bd71e425e76160
20190827 Don't add resources to data.json if it's missing a url https://github.com/OpenGov-OpenData/ckanext-datajson/commit/0d900484a70c2030dccae7511a80e298e081841d
20190910 fix import https://github.com/akariv/ckanext-datajson/commit/0fa0cd1c6cc86afc900bab49fe4ac686ab1f6bfa