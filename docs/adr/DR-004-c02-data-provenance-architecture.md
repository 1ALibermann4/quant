# DR-004 — C02 : architecture « Data Provenance & Dataset Snapshot »

> **Identifier :** DR-004
> **Status :** ACCEPTED
> **Authority class :** DECISION RECORD
> **Protocol :** QDP v0.1
> **Date :** 2026-09-23
> **Implémenté par :** `specs/contracts/C02/C02_v1.1.yaml`, profil `C02-I01` v1.0

## Context

`research/I01/DATA-REQ-I01.md` v0.1 §7.3 a relevé deux écarts sur C02 v1.0 :

- **DATA-GAP-01** : C02 v1.0 ne peut pas représenter les métadonnées REQUIRED du §7.1
  (provenance structurée, empreinte brute *et* empreinte canonique, lignée des transformations,
  calendrier versionné, fuseaux, comptages, licence).
- **DATA-GAP-02** : le texte YAML de la précondition `availability_cutoff` est inversé par
  rapport au code et aux tests.

DR-003 (INCONCLUSIVE) a montré en outre que :

- certains fournisseurs ne publient pas de version d'interface (PA-14 UNKNOWN) : le contrat doit
  pouvoir l'enregistrer comme inconnue sans inventer de valeur ;
- aucun fournisseur ne livre de calendrier de marché versionné (DR-003 F-05) ;
- la conservation de la copie brute dépend de la licence et de sa durée (DR-003 F-06).

C02 v1.0 n'a qu'un `fingerprint` « sur une représentation canonique » non définie. Il ne distingue
pas ce qui a été **reçu** de ce qui a été **consommé**, et parsing, sélection de colonnes,
normalisation des dates ou filtrage peuvent modifier les données sans modifier le fichier source.

## Decision

### D-1 — Périmètre de C02

C02 conserve son identifiant et devient **Data Provenance & Dataset Snapshot**. Il porte
l'ensemble de la chaîne de provenance des données scientifiques.

### D-2 — Chaîne de provenance et séparation brut / scientifique

```text
ProviderArtifact ──► TransformationRecord* ──► DatasetSnapshot ◄── MarketCalendarSnapshot
```

| Objet | Question à laquelle il répond | Identité |
|-------|-------------------------------|----------|
| `ProviderArtifact` | Qu'avons-nous exactement reçu du fournisseur ? | `content_sha256` des octets reçus |
| `TransformationRecord` | Quelle étape déterministe a produit quelle sortie ? | `application_key` (type, id, version, paramètres, entrées) |
| `DatasetSnapshot` | Sur quelles données exactes l'expérience a-t-elle été exécutée ? | `fingerprint` = SHA-256 de la table canonique QCT-1 |

Le brut et le scientifique ont chacun leur empreinte ; la lignée les relie et se vérifie de bout
en bout (la sortie de la dernière transformation est le `fingerprint` du snapshot). Aucun des
deux objets n'est appelé « snapshot » à la place de l'autre.

### D-3 — Le calendrier est une dépendance scientifique matérialisée

`MarketCalendarSnapshot` porte la **liste matérialisée** des séances (QCC-1), l'heure de clôture
régulière et les clôtures anticipées. Son identité (`content_fingerprint`) ne dépend que du
contenu. `source`, `source_version` et `generated_at` sont enregistrés (CAL-01) mais n'entrent pas
dans l'identité : deux versions de bibliothèque produisant exactement la même liste ont le même
contenu scientifique. Le snapshot référence le calendrier par empreinte, et la lignée peut le
déclarer comme entrée d'une transformation (alignement).

Une chaîne telle que `NYSE` n'est pas une identité scientifique. Ce DR ne choisit **aucune source
réelle de calendrier** et n'en fabrique aucune (DR-003 DEF-04 reste ouvert).

### D-4 — Pas de contrat C06

Artefact, transformation, calendrier et snapshot restent dans C02. Le calendrier n'est pas une
capacité métier autonome : c'est une dépendance de reproductibilité du dataset. Extraction vers un
contrat dédié seulement si plusieurs marchés, sessions intraday, calendriers 24/7 ou futures
rendent sa gestion autonome.

### D-5 — Un type unique pour la connaissance partielle

`Knowable[T]` = `{status: KNOWN | UNKNOWN | NOT_APPLICABLE, value, note}` avec l'invariant
`value présent ⇔ status = KNOWN`. Toute métadonnée externe potentiellement inconnue l'utilise ;
aucune convention n'est inventée champ par champ.

### D-6 — Représentations canoniques normatives

Le **contrat**, et non l'implémentation, définit les représentations dont dérivent les empreintes :

| Représentation | Usage |
|----------------|-------|
| QCJ-1 | JSON canonique des objets d'identité : clés triées, UTF-8, séparateurs minimaux, **pas de nombre non entier**, instants UTC à 6 décimales |
| QCT-1 | Table canonique : colonnes dans l'ordre du schéma, lignes triées par clé primaire, `,` et `\n`, décimaux à échelle fixe arrondis au pair sur la valeur exacte, champ vide pour valeur manquante |
| QCC-1 | Liste de séances : une date ISO par ligne, strictement croissante, `\n` final |

Des vecteurs de test (octets + empreintes) figurent dans le contrat ; deux implémentations
conformes doivent les reproduire.

### D-7 — Identité du contenu ≠ métadonnées d'exécution

`acquired_at`, `executed_at`, `generated_at`, `evaluated_at` décrivent une exécution et ne
modifient aucune identité. Participent à l'identité d'une transformation : type, identifiant,
version d'implémentation, paramètres canoniques, empreintes d'entrée. Le contrat documente pour
chaque empreinte ce qui y entre et ce qui en est exclu.

### D-8 — Empreinte brute agrégée : sémantique d'ensemble

`raw_fingerprint` = QCJ-1 de `{"kind":"C02.raw_artifact_set","members":[content_sha256 triés]}`.
L'ordre de consommation appartient à la lignée, pas à l'agrégat. L'enveloppe s'applique même à un
artefact unique, pour une règle sans cas particulier.

### D-9 — Verdict DATA hors du snapshot

Le §7.1 exige les résultats Q-01…Q-14 et le verdict DATA, mais le gate DATA est évalué sur un
snapshot **déjà figé**. Les inscrire dans le snapshot le modifierait après publication (REV-D-02).
Ils vont dans un objet distinct, `DataGateAssessment`, qui référence le snapshot par
`(snapshot_id, fingerprint)`. Le snapshot ne porte que `intended_use`, déclaré avant l'évaluation
(§4.3).

### D-10 — Compatibilité et profils

- C02 v1.1 est **additif** : aucun champ v1.0 renommé ni supprimé ; tout objet v1.0 valide le reste.
- Un objet déclaré `1.0` ne peut pas porter de champ v1.1.
- Les exigences propres à une investigation sont des **profils de validation** (`C02-I01` v1.0),
  pas des champs obligatoires du contrat générique.
- Tout renommage ou resserrement rétroactif relève de C02 v2.0.
- `ContractRef.c02` (C01) garde sa valeur par défaut `1.0` ; un run sur un snapshot v1.1 déclare
  `c02 = "1.1"` explicitement. Changer ce défaut serait une modification de C01.

### D-11 — Transport de la licence et revue obligatoire avant usage commercial

- Chaque `ProviderArtifact` porte un `LicenseRef` : conditions, palier, droit de conservation de la
  copie brute (REP-05), condition de conservation, et `usage_basis_ref`.
- `usage_basis_ref` **référence** la décision qui fonde l'usage. Pour I01, l'hypothèse d'usage
  individuel non commercial est l'**ASSUMPTION A-1 de DR-003** ; DR-004 et C02 la transportent,
  ils n'en sont pas une seconde source normative.
- **Déclencheur obligatoire :** tout passage à un usage commercial, ou tout autre écart entre
  l'usage réel et l'usage fondé par `usage_basis_ref`, exige une **revue de licence avant toute
  utilisation correspondante des données**. Les artefacts et snapshots existants ne peuvent pas
  servir cet usage tant que la revue n'a pas conclu et qu'un nouveau fondement n'est pas enregistré.

### D-12 — Conservation de la provenance

Une empreinte n'est jamais recalculée pour « réparer » un objet : un contenu différent produit un
nouvel objet (nouveau `snapshot_id`, nouvel `artifact_id`). La copie brute est conservée à côté de
la table canonique pour rejouer la lignée, dans les limites de sa licence (DR-003 F-06).

## Constraints

- Aucune API, aucune donnée de marché, aucun loader, aucune source de calendrier réelle.
- DR-003 n'est pas modifié ; ses UNKNOWN ne sont pas résolus ici.
- Aucune hypothèse scientifique, gate SCI ou paramètre d'I01 n'est modifié.
- Tests exclusivement synthétiques.

## Authorities consulted

| Document | Rôle |
|----------|------|
| `research/I01/DATA-REQ-I01.md` v0.1 | §7.1 (métadonnées), §7.3 (DATA-GAP-01/02), §8 (REP-04, REP-05), §2.2 (CAL-*), §4.3, §12 |
| `docs/adr/DR-003-i01-market-data-source-selection.md` | ASSUMPTION A-1, F-05, F-06, DEF-04, éléments pour C02 v1.1 |
| `specs/contracts/C02/C02_v1.0.yaml` | Contrat révisé |
| `specs/contracts/C01`, `C03` | `DatasetSnapshotRef`, contrainte `as_of <= availability_cutoff` |
| `docs/governance/versioning_axes.md` | Règle : changement de garantie ⇒ nouvelle version de contrat |

## Evidence

- Contrat : `specs/contracts/C02/C02_v1.1.yaml` ; profil : `specs/contracts/C02/profiles/C02-I01_v1.0.yaml`.
- Implémentation : `src/quant/contracts/{knowledge,canonical,lineage,market_calendar,dataset_snapshot,data_assessment}.py`,
  `src/quant/contracts/profiles/i01.py`.
- Tests : `tests/contracts/test_{knowable,canonical,provider_artifact,lineage,market_calendar,dataset_snapshot,profile_i01}.py`,
  `tests/trace/test_decision_trace_c02_v11.py`.
- Rapport : `docs/validation/C02-v1.1-validation-report.md`.

## Alternatives considered

| Alternative | Évaluation |
|-------------|------------|
| Contrat C06 pour `ProviderArtifact` et/ou le calendrier | Rejeté : prolifération prématurée ; même protocole de provenance (D-4) |
| Un seul `fingerprint` couvrant brut et canonique | Rejeté : ne distingue pas reçu et consommé |
| Calendrier référencé par nom (`NYSE`) ou par version de bibliothèque | Rejeté : ne garantit pas le contenu (D-3) |
| Liste des séances embarquée dans chaque snapshot | Rejeté : duplication ; la référence par empreinte suffit et permet le partage entre snapshots |
| Empreinte définie par l'implémentation (sérialisation Python) | Rejeté : non reproductible par une autre implémentation (REP-04) |
| Flottants autorisés dans QCJ-1 | Rejeté : représentation textuelle des flottants non déterministe entre langages |
| Verdict DATA dans le snapshot | Rejeté : contredit l'immuabilité (D-9) |
| Champs I01 obligatoires dans C02 générique | Rejeté : invaliderait rétroactivement les objets v1.0 ; profil (D-10) |
| Renommer `snapshot_id` → `dataset_snapshot_id`, `fingerprint` → `dataset_fingerprint` | Rejeté pour v1.1 : casse C01, C03 et `DecisionTrace` ; candidat v2.0 seulement |
| `raw_fingerprint` sur liste ordonnée | Rejeté : l'ordre est porté par la lignée ; l'ensemble évite deux empreintes pour le même contenu |

## Rejected alternatives

- Réécrire `C02_v1.0.yaml` pour corriger DATA-GAP-02 : un contrat publié n'est pas réécrit ; la
  correction passe par l'erratum E-01 de v1.1.
- Choisir une bibliothèque de calendrier pour « tester en vrai » : anticiperait DEF-04.

## Consequences

- Un snapshot I01 est représentable sans champ ad hoc (DATA-GAP-01 résolu) ; la précondition
  `availability_cutoff` est corrigée par erratum (DATA-GAP-02 résolu).
- Tout futur chargeur devra produire `ProviderArtifact` + `TransformationRecord` + table QCT-1 et
  réussir `validate_i01_snapshot` ; DATA-PASS reste impossible tant qu'un UNKNOWN REQUIRED subsiste.
- Aucune acquisition n'est débloquée : DR-003 reste une gate indépendante (INCONCLUSIVE).
- Les runs I01 déclareront `contract_refs.c02 = "1.1"`.

## Deferred items

| ID | Objet | Déclencheur |
|----|-------|-------------|
| DEF-01 | Source réelle du calendrier de marché (DR-003 DEF-04) | Avant le premier chargeur |
| DEF-02 | Format de stockage physique (CSV, Parquet, …) — la représentation canonique ne le fixe pas | Avec le chargeur |
| DEF-03 | Registre d'expériences appliquant C02-INV-03 (unicité des fingerprints) | Avec le premier run |
| DEF-04 | Valeur par défaut de `ContractRef.c02` (C01) | Prochaine révision de C01 |
| DEF-05 | Mise à jour textuelle de DATA-REQ-I01 §7.3 / §13 (écarts marqués résolus) | Prochaine révision de DATA-REQ |
| DEF-06 | Coquille `dataset_snapshot_id` dans P0-specification §6 (le champ est `snapshot_id`) | Prochaine révision documentaire P0 |

## Status

**ACCEPTED.**
