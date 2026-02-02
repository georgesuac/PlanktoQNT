# PlanktoQNT

**Currently under development**

PlanktoQNT is a modular Python pipeline for quantitative analysis of plankton images from the Imaging FlowCytobot (IFCB) data. It transforms classified regions of interest (ROIs) into ecological metrics, including cell abundance, size structure, biovolume, and carbon biomass. PlanktoQNT provides reproducible outputs for statistical analysis, ecosystem modeling, and carbon cycling studies of aquatic systems.

The classified images should be stored in different folders, according to species/group.

The latest PlanktoNET model (ver1_6) can classify 86 categories from the following groups:

Diatoms
	•	Centric Diatoms
	•	Bacillaria
	•	Biddulphia
	•	Cerataulina
	•	Chaetoceros
	•	Leptocylindrus
	•	Rhizosolenia
	•	Skeletonema
	•	Diatom_centrales
	•	Pennate Diatoms
	•	Cylindrotheca
	•	Cylindrotheca_big
	•	Diploneis
	•	Grammatophora
	•	Licmophora
	•	Navicula
	•	Pleurosigma
	•	Pseudonitzschia
	•	Tabellaria
	•	Diatom_pennate

⸻

Dinoflagellates
	•	Thecate (Armored) Dinoflagellates
	•	Alexandrium_sp
	•	Alexandrium_sp_big
	•	Alexandrium_sp_empty
	•	Alexandrium_tamarense
	•	Blixaea_quinquecornis
	•	Blixaea_quinquecornis_empty
	•	Ceratium_furca
	•	Ceratium_fusus
	•	Ceratium_sp1
	•	Ceratium_sp2
	•	Gambierdiscus
	•	Gambierdiscus_empty
	•	Gonyaulax
	•	Gonyaulax_empty
	•	Heterocapsa_lanceolata
	•	Heterocapsa_rotundata
	•	Heterocapsa_sp
	•	Heterocapsa_triquetra
	•	Ostreopsidaceae
	•	Prorocentrum_concavum
	•	Prorocentrum_lima
	•	Prorocentrum_lima_empty
	•	Prorocentrum_minimum
	•	Prorocentrum_sp1
	•	Protoperidinium_bipes
	•	Protoperidinium_bipes_empty
	•	Protoperidinium_brevipes
	•	Protoperidinium_ovatum
	•	Protoperidinium_pallidum
	•	Protoperidinium_steinii
	•	Scrippsiella_trochoidea
	•	Scrippsiella_trochoidea_empty
	•	Athecate (Unarmored) Dinoflagellates
	•	Akashiwo_sanguinea
	•	Cochlodinium
	•	Gymnodinium_big
	•	Gymnodinium_sp
	•	Karlodinium_sp
	•	Symbiodiniaceae
	•	Dinoflagellate_cluster

⸻

Ciliates
	•	Euplotes_sp
	•	Mesodinium_sp
	•	Strobilidium
	•	Strombidium_capitatum
	•	Tintinids
	•	Tintinnid_house

⸻

Cyanobacteria
	•	Cyanobacteria_filam
	•	Trichodesmium
	•	Moorena

⸻

Other Phytoplankton & Flagellates
	•	Coccolith-like
	•	Cryptomonas
	•	Dinobryon
	•	Euglenophyceae
	•	Heterosigma_akashiwo
	•	Nanoflagellate_cluster
	•	Nanoflagellates_other

⸻

Zooplankton & Protists
	•	Foraminifera
	•	Nauplii
	•	Radiolaria
	•	Astramoeba

⸻

Detritus & Artifacts
	•	Detritus
	•	Detritus_clear
	•	Detritus_small
	•	Fecal_pellet
	•	Exoskeleton_parts
	•	Bubble
	•	White_stick
	•	Elongated_empty
	•	Bad
