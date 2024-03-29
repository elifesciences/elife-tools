from collections import OrderedDict

# output from elife05502.xml
expected = [
    OrderedDict(
        [
            ("doi", "10.7554/eLife.05502.001"),
            ("doi_url", "https://doi.org/10.7554/eLife.05502.001"),
            (
                "content",
                "Toll-dependent patterning of the dorsoventral axis in Drosophila represents one of the best understood gene regulatory networks. However, its evolutionary origin has remained elusive. Outside the insects Toll is not known for a patterning function, but rather for a role in pathogen defense. Here, we show that in the milkweed bug Oncopeltus fasciatus, whose lineage split from Drosophila's more than 350 million years ago, Toll is only required to polarize a dynamic BMP signaling network. A theoretical model reveals that this network has self-regulatory properties and that shallow Toll signaling gradients are sufficient to initiate axis formation. Such gradients can account for the experimentally observed twinning of insect embryos upon egg fragmentation and might have evolved from a state of uniform Toll activity associated with protecting insect eggs against pathogens. DOI: http://dx.doi.org/10.7554/eLife.05502.001",
            ),
            ("article_doi", "10.7554/eLife.05502"),
            ("type", "abstract"),
            ("position", 1),
            ("ordinal", 1),
            ("sibling_ordinal", 1),
            ("asset", None),
        ]
    ),
    OrderedDict(
        [
            ("doi", "10.7554/eLife.05502.002"),
            ("doi_url", "https://doi.org/10.7554/eLife.05502.002"),
            ("title", "eLife digest"),
            ("full_title", "eLife digest"),
            (
                "content",
                "How an animal develops from a fertilized egg has fascinated scientists for decades. As such, much effort has gone into answering the related question: what makes the belly (or underside) of an animal develop differently from its back? Like almost all other biological processes, the development of an embryo is controlled by interactions between different molecules within cells and tissues. Some of these molecules promote the activity of others; some have the opposite effect; and together these molecules and their interactions form ‘signaling networks’. One such network, which involves a protein called BMP, is needed to establish the belly-to-back axis of nearly all animals. However, insects are a unique exception. Most insects (including flies, beetles and wasps) use a different signaling network to control their development from their belly to their back, one that involves a protein called Toll instead. This is unexpected because, in other animals, Toll proteins are best known for their role in the immune system; and it remains unclear how Toll signaling came to be involved in insect development. Now, Sachs, Chen et al. have studied an insect—called the milkweed bug—that is unlike most insects in that it does not have a larval stage (i.e., a maggot or a caterpillar) in its life-cycle. This characteristic makes the milkweed bug more similar to the ancestor of all insects, and thus makes it an excellent model to study how the Toll protein took over from BMP in insect development. First, Sachs, Chen et al. experimentally reduced BMP signaling in milkweed bug embryos. This caused the embryos to develop features all around their bodies that are normally only associated with the animal's underside. In other insects, the development of these so-called ‘ventral’ features is typically controlled by Toll signaling; but in the milkweed bug this activity instead depends on a protein called Sog. Indeed, when Sachs, Chen et al. experimentally reduced both BMP and Toll signaling, the effect was the same as having reduced only BMP signaling, implying that Toll is not needed. Instead, Toll increased the level of the Sog protein up to a particular threshold. Above this threshold, Sog and BMP control each other to set out the animal's body plan. As insects evolved, it seems likely that Toll transitioned from being a trigger of BMP signaling to an important controller of insect development in its own right. But why was Toll put in the egg in the first place? It is possible that Toll was required to protect the eggs of early insects from attack by bacteria and fungi. Future work will now test this assumption and aim to explain how and why the Toll protein changed its role—from immunity to development—during evolution. DOI: http://dx.doi.org/10.7554/eLife.05502.002",
            ),
            ("article_doi", "10.7554/eLife.05502"),
            ("type", "abstract"),
            ("position", 2),
            ("ordinal", 2),
            ("sibling_ordinal", 2),
            ("asset", None),
        ]
    ),
    OrderedDict(
        [
            ("doi", "10.7554/eLife.05502.003"),
            ("doi_url", "https://doi.org/10.7554/eLife.05502.003"),
            ("id", "fig1"),
            (
                "title",
                "The evolution of Toll's role in dorsoventral (DV) patterning in insects.",
            ),
            (
                "full_title",
                "The evolution of Toll's role in dorsoventral (DV) patterning in insects.",
            ),
            ("label", "Figure 1."),
            ("full_label", "Figure 1."),
            (
                "caption",
                "In holometabolous insects Toll signaling is activated by ventral eggshell cues and forms an activity gradient (red) that is essential at the very least for specifying the ventral-most cells on the DV axis, giving rise to the mesoderm (brown), by activating the gene twist (twi) (black arrow). In the fly Drosophila Toll signaling not only determines the mesoderm, but also the neuroectoderm (yellow) and restricts BMP signaling to the dorsal side through several parallel mechanisms, including the activation of the BMP inhibitor short gastrulation (sog) (black arrow) and repression of the major BMP ligand decapentaplegic (dpp) (black T-bar) (Hong et al., 2008; Reeves and Stathopoulos, 2009). On the dorsal side a BMP gradient (blue) is established (gray arrow and T-bar indicate BMP ligand production and inhibition, respectively) that specifies non-neurogenic ectoderm (blue) and extraembryonic tissue (green) (O'Connor et al., 2006). Toll signaling is dynamic in Tribolium and polarizes BMP signaling only by activating sog (Nunes da Fonseca et al., 2008). BMP signaling in turn has an increased role in ectodermal patterning compared to flies (van der Zee et al., 2006). In contrast to both Drosophila and Tribolium Toll signaling in the wasp Nasonia appears to be restricted to a narrow ventral region where it is only transiently active. Here, Toll signaling is required to induce mesodermal and mesectodermal fates. But the size of the mesodermal region as well as the fate and position of all other regions along the DV axis are determined by a BMP signaling gradient emanating from the dorsal side by an unknown (Toll-independent) mechanism (black T-bar indicates repression of twi) (Özüak et al., 2014a, 2014b). Thus, in the holometabolous insects BMP signaling gets increasingly more important towards basally branching groups, while Toll's role is diminished, but remains essential for ventral-most cell fates. Here we provide evidence that the bug Oncopeltus, representing the Hemiptera within the sister group of Holometabola (Paraneoptera), uses Toll signaling only as spatial cue (dashed black arrow) to polarize a dynamic BMP signaling network that establishes a gradient responsible for patterning the cell fates along the DV axis. The key regulatory element of this network is the transcriptional repression of sog by BMP signaling. A reaction-diffusion model which incorporates this regulatory element shows that the formation of stable BMP gradients requires only weakly polarized Toll signaling (Box 1).",
            ),
            (
                "full_caption",
                'In holometabolous insects Toll signaling is activated by ventral eggshell cues and forms an activity gradient (red) that is essential at the very least for specifying the ventral-most cells on the DV axis, giving rise to the mesoderm (brown), by activating the gene <italic>twist</italic> (<italic>twi</italic>) (black arrow). In the fly <italic>Drosophila</italic> Toll signaling not only determines the mesoderm, but also the neuroectoderm (yellow) and restricts BMP signaling to the dorsal side through several parallel mechanisms, including the activation of the BMP inhibitor <italic>short gastrulation</italic> (<italic>sog</italic>) (black arrow) and repression of the major BMP ligand <italic>decapentaplegic</italic> (<italic>dpp</italic>) (black T-bar) (<xref ref-type="bibr" rid="bib22">Hong et al., 2008</xref>; <xref ref-type="bibr" rid="bib48">Reeves and Stathopoulos, 2009</xref>). On the dorsal side a BMP gradient (blue) is established (gray arrow and T-bar indicate BMP ligand production and inhibition, respectively) that specifies non-neurogenic ectoderm (blue) and extraembryonic tissue (green) (<xref ref-type="bibr" rid="bib40">O\'Connor et al., 2006</xref>). Toll signaling is dynamic in <italic>Tribolium</italic> and polarizes BMP signaling only by activating sog (<xref ref-type="bibr" rid="bib39">Nunes da Fonseca et al., 2008</xref>). BMP signaling in turn has an increased role in ectodermal patterning compared to flies (<xref ref-type="bibr" rid="bib65">van der Zee et al., 2006</xref>). In contrast to both <italic>Drosophila</italic> and <italic>Tribolium</italic> Toll signaling in the wasp <italic>Nasonia</italic> appears to be restricted to a narrow ventral region where it is only transiently active. Here, Toll signaling is required to induce mesodermal and mesectodermal fates. But the size of the mesodermal region as well as the fate and position of all other regions along the DV axis are determined by a BMP signaling gradient emanating from the dorsal side by an unknown (Toll-independent) mechanism (black T-bar indicates repression of <italic>twi</italic>) (<xref ref-type="bibr" rid="bib43">Özüak et al., 2014a</xref>, <xref ref-type="bibr" rid="bib44">2014b</xref>). Thus, in the holometabolous insects BMP signaling gets increasingly more important towards basally branching groups, while Toll\'s role is diminished, but remains essential for ventral-most cell fates. Here we provide evidence that the bug <italic>Oncopeltus</italic>, representing the Hemiptera within the sister group of Holometabola (Paraneoptera), uses Toll signaling only as spatial cue (dashed black arrow) to polarize a dynamic BMP signaling network that establishes a gradient responsible for patterning the cell fates along the DV axis. The key regulatory element of this network is the transcriptional repression of <italic>sog</italic> by BMP signaling. A reaction-diffusion model which incorporates this regulatory element shows that the formation of stable BMP gradients requires only weakly polarized Toll signaling (<xref ref-type="boxed-text" rid="box1">Box 1</xref>).',
            ),
            (
                "content",
                "In holometabolous insects Toll signaling is activated by ventral eggshell cues and forms an activity gradient (red) that is essential at the very least for specifying the ventral-most cells on the DV axis, giving rise to the mesoderm (brown), by activating the gene twist (twi) (black arrow). In the fly Drosophila Toll signaling not only determines the mesoderm, but also the neuroectoderm (yellow) and restricts BMP signaling to the dorsal side through several parallel mechanisms, including the activation of the BMP inhibitor short gastrulation (sog) (black arrow) and repression of the major BMP ligand decapentaplegic (dpp) (black T-bar) (Hong et al., 2008; Reeves and Stathopoulos, 2009). On the dorsal side a BMP gradient (blue) is established (gray arrow and T-bar indicate BMP ligand production and inhibition, respectively) that specifies non-neurogenic ectoderm (blue) and extraembryonic tissue (green) (O'Connor et al., 2006). Toll signaling is dynamic in Tribolium and polarizes BMP signaling only by activating sog (Nunes da Fonseca et al., 2008). BMP signaling in turn has an increased role in ectodermal patterning compared to flies (van der Zee et al., 2006). In contrast to both Drosophila and Tribolium Toll signaling in the wasp Nasonia appears to be restricted to a narrow ventral region where it is only transiently active. Here, Toll signaling is required to induce mesodermal and mesectodermal fates. But the size of the mesodermal region as well as the fate and position of all other regions along the DV axis are determined by a BMP signaling gradient emanating from the dorsal side by an unknown (Toll-independent) mechanism (black T-bar indicates repression of twi) (Özüak et al., 2014a, 2014b). Thus, in the holometabolous insects BMP signaling gets increasingly more important towards basally branching groups, while Toll's role is diminished, but remains essential for ventral-most cell fates. Here we provide evidence that the bug Oncopeltus, representing the Hemiptera within the sister group of Holometabola (Paraneoptera), uses Toll signaling only as spatial cue (dashed black arrow) to polarize a dynamic BMP signaling network that establishes a gradient responsible for patterning the cell fates along the DV axis. The key regulatory element of this network is the transcriptional repression of sog by BMP signaling. A reaction-diffusion model which incorporates this regulatory element shows that the formation of stable BMP gradients requires only weakly polarized Toll signaling (Box 1). DOI: http://dx.doi.org/10.7554/eLife.05502.003",
            ),
            ("article_doi", "10.7554/eLife.05502"),
            ("type", "fig"),
            ("position", 3),
            ("ordinal", 1),
            ("sibling_ordinal", 1),
            ("asset", None),
        ]
    ),
    OrderedDict(
        [
            ("doi", "10.7554/eLife.05502.004"),
            ("doi_url", "https://doi.org/10.7554/eLife.05502.004"),
            ("id", "fig2"),
            (
                "title",
                "Knockdown (KD) of BMP signaling components results in completely ventralized (dpp-, tld-RNAi) or completely dorsalized (sog-, tsg-RNAi) embryos.",
            ),
            (
                "full_title",
                "Knockdown (KD) of BMP signaling components results in completely ventralized (<italic>dpp-, tld-</italic>RNAi) or completely dorsalized (<italic>sog-</italic>, <italic>tsg-</italic>RNAi) embryos.",
            ),
            ("label", "Figure 2."),
            ("full_label", "Figure 2."),
            (
                "caption",
                "Expression of twi (A, E, I, M, Q), sim (B, F, J, N, R) and sog (C, G, K, O, S) in wild type (wt) embryos (A–C), dpp-RNAi embryos (E–G), sog-RNAi embryos (I–K), tsg-RNAi embryos (M–O) and tld-RNAi embryos (Q–S) monitored by whole mount in situ hybridization (ISH). The view is lateral with the dorsal side pointing up (A–C), ventral (K), or not determined as the expression is DV-symmetric (E–G, I, J, M–O, Q–S). Embryos are at the blastoderm stage (∼26–32 hpf: A, C, E–G, I–K, M, O, Q, S), or at the beginning of anatrepsis (posterior invagination of the embryo, ∼33–37 hpf) (B). Scale bar (A) corresponds to 200 µm. For phenotype frequencies and confirmation of KD see Figure 2—figure supplement 2 and Figure 5—figure supplement 1. (D, H, L, P, T) Simulations of the reaction diffusion system described in Box 1 on a two-dimensional cylinder (Figure 10). Depicted is one half of the cylinder surface stretching from the dorsal (D) to the ventral (V) midline. Blue: sog expression (η). Gray: BMP concentration (b). (D) In wt sog expression is confined to a ventral stripe. (H) Loss of BMP (b = 0) leads to uniform derepression of sog. (L) Loss of sog (s = 0) leads to uniformly high levels of BMP. (P) Loss of Tsg was modeled by assuming that no Sog-BMP complexes are formed (k+ = 0). This results in high BMP signaling throughout the embryo. (T) Loss of Tld was modeled by reducing the degradation constant of Sog (αs) by 90%. As Sog-BMP complexes are not degraded, BMP is not released, causing uniform derepression of sog.",
            ),
            (
                "full_caption",
                'Expression of <italic>twi</italic> (<bold>A</bold>, <bold>E</bold>, <bold>I</bold>, <bold>M</bold>, <bold>Q</bold>), <italic>sim</italic> (<bold>B</bold>, <bold>F</bold>, <bold>J</bold>, <bold>N</bold>, <bold>R</bold>) and <italic>sog</italic> (<bold>C</bold>, <bold>G</bold>, <bold>K</bold>, <bold>O</bold>, <bold>S</bold>) in wild type (wt) embryos (<bold>A</bold>–<bold>C</bold>), <italic>dpp</italic>-RNAi embryos (<bold>E</bold>–<bold>G</bold>), <italic>sog</italic>-RNAi embryos (<bold>I</bold>–<bold>K</bold>), <italic>tsg</italic>-RNAi embryos (<bold>M</bold>–<bold>O</bold>) and <italic>tld</italic>-RNAi embryos (<bold>Q</bold>–<bold>S</bold>) monitored by whole mount in situ hybridization (ISH). The view is lateral with the dorsal side pointing up (<bold>A</bold>–<bold>C</bold>), ventral (<bold>K</bold>), or not determined as the expression is DV-symmetric (<bold>E</bold>–<bold>G</bold>, <bold>I</bold>, <bold>J</bold>, <bold>M</bold>–<bold>O</bold>, <bold>Q</bold>–<bold>S</bold>). Embryos are at the blastoderm stage (∼26–32 hpf: <bold>A</bold>, <bold>C</bold>, <bold>E</bold>–<bold>G</bold>, <bold>I</bold>–<bold>K</bold>, <bold>M</bold>, <bold>O</bold>, <bold>Q</bold>, <bold>S</bold>), or at the beginning of anatrepsis (posterior invagination of the embryo, ∼33–37 hpf) (<bold>B</bold>). Scale bar (<bold>A</bold>) corresponds to 200 µm. For phenotype frequencies and confirmation of KD see <xref ref-type="fig" rid="fig2s2">Figure 2—figure supplement 2</xref> and <xref ref-type="fig" rid="fig5s1">Figure 5—figure supplement 1</xref>. (<bold>D</bold>, <bold>H</bold>, <bold>L</bold>, <bold>P</bold>, <bold>T</bold>) Simulations of the reaction diffusion system described in <xref ref-type="boxed-text" rid="box1">Box 1</xref> on a two-dimensional cylinder (<xref ref-type="fig" rid="fig10">Figure 10</xref>). Depicted is one half of the cylinder surface stretching from the dorsal (D) to the ventral (V) midline. Blue: <italic>sog</italic> expression (<italic>η</italic>). Gray: BMP concentration (<bold><italic><bold>b</bold></italic></bold>). (<bold>D</bold>) In wt <italic>sog</italic> expression is confined to a ventral stripe. (<bold>H</bold>) Loss of BMP (<italic>b</italic> = 0) leads to uniform derepression of <italic>sog</italic>. (<bold>L</bold>) Loss of <italic>sog</italic> (<italic>s</italic> = 0) leads to uniformly high levels of BMP. (<bold>P</bold>) Loss of Tsg was modeled by assuming that no Sog-BMP complexes are formed (<italic>k</italic><sub><italic>+</italic></sub> = 0). This results in high BMP signaling throughout the embryo. (<bold>T</bold>) Loss of Tld was modeled by reducing the degradation constant of Sog (<italic>α</italic><sub><italic>s</italic></sub>) by 90%. As Sog-BMP complexes are not degraded, BMP is not released, causing uniform derepression of <italic>sog</italic>.',
            ),
            (
                "content",
                "Expression of twi (A, E, I, M, Q), sim (B, F, J, N, R) and sog (C, G, K, O, S) in wild type (wt) embryos (A–C), dpp-RNAi embryos (E–G), sog-RNAi embryos (I–K), tsg-RNAi embryos (M–O) and tld-RNAi embryos (Q–S) monitored by whole mount in situ hybridization (ISH). The view is lateral with the dorsal side pointing up (A–C), ventral (K), or not determined as the expression is DV-symmetric (E–G, I, J, M–O, Q–S). Embryos are at the blastoderm stage (∼26–32 hpf: A, C, E–G, I–K, M, O, Q, S), or at the beginning of anatrepsis (posterior invagination of the embryo, ∼33–37 hpf) (B). Scale bar (A) corresponds to 200 µm. For phenotype frequencies and confirmation of KD see Figure 2—figure supplement 2 and Figure 5—figure supplement 1. (D, H, L, P, T) Simulations of the reaction diffusion system described in Box 1 on a two-dimensional cylinder (Figure 10). Depicted is one half of the cylinder surface stretching from the dorsal (D) to the ventral (V) midline. Blue: sog expression (η). Gray: BMP concentration (b). (D) In wt sog expression is confined to a ventral stripe. (H) Loss of BMP (b = 0) leads to uniform derepression of sog. (L) Loss of sog (s = 0) leads to uniformly high levels of BMP. (P) Loss of Tsg was modeled by assuming that no Sog-BMP complexes are formed (k+ = 0). This results in high BMP signaling throughout the embryo. (T) Loss of Tld was modeled by reducing the degradation constant of Sog (αs) by 90%. As Sog-BMP complexes are not degraded, BMP is not released, causing uniform derepression of sog. DOI: http://dx.doi.org/10.7554/eLife.05502.004",
            ),
            ("article_doi", "10.7554/eLife.05502"),
            ("type", "fig"),
            ("position", 4),
            ("ordinal", 2),
            ("sibling_ordinal", 2),
            ("asset", None),
        ]
    ),
    OrderedDict(
        [
            ("doi", "10.7554/eLife.05502.005"),
            ("doi_url", "https://doi.org/10.7554/eLife.05502.005"),
            ("id", "fig2s1"),
            ("title", "Expression of BMP signaling components during blastoderm."),
            ("full_title", "Expression of BMP signaling components during blastoderm."),
            ("label", "Figure 2—figure supplement 1."),
            ("full_label", "Figure 2—figure supplement 1."),
            (
                "caption",
                "Anterior is to the left. DV orientation cannot be determined at this stage. The expression of dpp and tsg cannot be detected by ISH during blastoderm stages between 26 to 28 hpf. gbb and tld show uniform expression along the embryonic circumference.",
            ),
            (
                "full_caption",
                "Anterior is to the left. DV orientation cannot be determined at this stage. The expression of <italic>dpp</italic> and <italic>tsg</italic> cannot be detected by ISH during blastoderm stages between 26 to 28 hpf<italic>. gbb</italic> and <italic>tld</italic> show uniform expression along the embryonic circumference.",
            ),
            ("parent_type", "fig"),
            ("parent_ordinal", 2),
            ("parent_sibling_ordinal", 2),
            ("parent_asset", None),
            (
                "content",
                "Anterior is to the left. DV orientation cannot be determined at this stage. The expression of dpp and tsg cannot be detected by ISH during blastoderm stages between 26 to 28 hpf. gbb and tld show uniform expression along the embryonic circumference. DOI: http://dx.doi.org/10.7554/eLife.05502.005",
            ),
            ("article_doi", "10.7554/eLife.05502"),
            ("type", "fig"),
            ("position", 5),
            ("ordinal", 3),
            ("sibling_ordinal", 2),
            ("asset", "figsupp"),
        ]
    ),
    OrderedDict(
        [
            ("doi", "10.7554/eLife.05502.006"),
            ("doi_url", "https://doi.org/10.7554/eLife.05502.006"),
            ("id", "fig2s2"),
            ("title", "Phenotype frequencies after parental RNAi."),
            ("full_title", "Phenotype frequencies after parental RNAi."),
            ("label", "Figure 2—figure supplement 2."),
            ("full_label", "Figure 2—figure supplement 2."),
            (
                "caption",
                "The KD of dpp and tld by parental RNAi caused partial or complete ventralization. No wt embryos were observed. Completely ventralized embryos show a uniform expansion of twi, sog, or the ventral-anterior sim domain (analyzed by ISH) and lack detectable pMAD staining (analyzed by immunostaining). In partially ventralized embryos marker gene expansion was not complete and residual pMAD staining could be detected. Each marker was analyzed separately. The KD of sog and tsg caused partial or complete dorsalization. Completely dorsalized embryos lack twi, sog or sim (except for the terminal domain) and exhibit uniform levels of nuclear localized pMAD levels. Partially dorsalized embryos show residual twi, sog or sim expression and their nuclear pMAD levels are not completely uniform. No wt-like patterns were observed. The table shows % of complete ventralization or complete dorsalization.",
            ),
            (
                "full_caption",
                "The KD of <italic>dpp</italic> and <italic>tld</italic> by parental RNAi caused partial or complete ventralization. No wt embryos were observed. Completely ventralized embryos show a uniform expansion of <italic>twi</italic>, <italic>sog,</italic> or the ventral-anterior <italic>sim</italic> domain (analyzed by ISH) and lack detectable pMAD staining (analyzed by immunostaining). In partially ventralized embryos marker gene expansion was not complete and residual pMAD staining could be detected. Each marker was analyzed separately. The KD of <italic>sog</italic> and <italic>tsg</italic> caused partial or complete dorsalization. Completely dorsalized embryos lack <italic>twi</italic>, <italic>sog</italic> or <italic>sim</italic> (except for the terminal domain) and exhibit uniform levels of nuclear localized pMAD levels. Partially dorsalized embryos show residual <italic>twi</italic>, <italic>sog</italic> or <italic>sim</italic> expression and their nuclear pMAD levels are not completely uniform. No wt-like patterns were observed. The table shows % of complete ventralization or complete dorsalization.",
            ),
            ("parent_type", "fig"),
            ("parent_ordinal", 2),
            ("parent_sibling_ordinal", 2),
            ("parent_asset", None),
            (
                "content",
                "The KD of dpp and tld by parental RNAi caused partial or complete ventralization. No wt embryos were observed. Completely ventralized embryos show a uniform expansion of twi, sog, or the ventral-anterior sim domain (analyzed by ISH) and lack detectable pMAD staining (analyzed by immunostaining). In partially ventralized embryos marker gene expansion was not complete and residual pMAD staining could be detected. Each marker was analyzed separately. The KD of sog and tsg caused partial or complete dorsalization. Completely dorsalized embryos lack twi, sog or sim (except for the terminal domain) and exhibit uniform levels of nuclear localized pMAD levels. Partially dorsalized embryos show residual twi, sog or sim expression and their nuclear pMAD levels are not completely uniform. No wt-like patterns were observed. The table shows % of complete ventralization or complete dorsalization. DOI: http://dx.doi.org/10.7554/eLife.05502.006",
            ),
            ("article_doi", "10.7554/eLife.05502"),
            ("type", "fig"),
            ("position", 6),
            ("ordinal", 4),
            ("sibling_ordinal", 3),
            ("asset", "figsupp"),
        ]
    ),
    OrderedDict(
        [
            ("doi", "10.7554/eLife.05502.007"),
            ("doi_url", "https://doi.org/10.7554/eLife.05502.007"),
            ("id", "fig3"),
            (
                "title",
                "BMP signaling activity is uniformly abolished or expanded in ventralized or dorsalized phenotypes, respectively.",
            ),
            (
                "full_title",
                "BMP signaling activity is uniformly abolished or expanded in ventralized or dorsalized phenotypes, respectively.",
            ),
            ("label", "Figure 3."),
            ("full_label", "Figure 3."),
            (
                "caption",
                "pMAD distribution in blastoderm stage (26–32 hr post fertilization, hpf) wt (A, A′, F, F′), dpp-RNAi (B, B′, G, G′), sog-RNAi (C, C′, H, H′), tsg-RNAi (D, D′, I, I′) and Toll1-RNAi (E, E′, J, J′) embryos. For each embryo a ventral and a dorsal view, or views from opposite sides if DV polarity is lacking (B–G, D-J) are shown. Magnified surface views to the right of each embryo (x') reveal the presence or absence of pMAD in individual nuclei. The scale bar (A, A′) corresponds to 50 µm. For identifying the polarity of the DV axis and for BMP signaling activity during later development see Figure 3—figure supplement 1.",
            ),
            (
                "full_caption",
                'pMAD distribution in blastoderm stage (26–32 hr post fertilization, hpf) wt (<bold>A</bold>, <bold>A′</bold>, <bold>F</bold>, <bold>F′</bold>), <italic>dpp</italic>-RNAi (<bold>B</bold>, <bold>B′</bold>, <bold>G</bold>, <bold>G′</bold>), <italic>sog</italic>-RNAi (<bold>C</bold>, <bold>C′</bold>, <bold>H</bold>, <bold>H′</bold>), <italic>tsg</italic>-RNAi (<bold>D</bold>, <bold>D′</bold>, <bold>I</bold>, <bold>I′</bold>) and <italic>Toll1</italic>-RNAi (<bold>E</bold>, <bold>E′</bold>, <bold>J</bold>, <bold>J′</bold>) embryos. For each embryo a ventral and a dorsal view, or views from opposite sides if DV polarity is lacking (<bold>B</bold>–<bold>G</bold>, <bold>D</bold>-<bold>J</bold>) are shown. Magnified surface views to the right of each embryo (x\') reveal the presence or absence of pMAD in individual nuclei. The scale bar (<bold>A</bold>, <bold>A′</bold>) corresponds to 50 µm. For identifying the polarity of the DV axis and for BMP signaling activity during later development see <xref ref-type="fig" rid="fig3s1">Figure 3—figure supplement 1</xref>.',
            ),
            (
                "content",
                "pMAD distribution in blastoderm stage (26–32 hr post fertilization, hpf) wt (A, A′, F, F′), dpp-RNAi (B, B′, G, G′), sog-RNAi (C, C′, H, H′), tsg-RNAi (D, D′, I, I′) and Toll1-RNAi (E, E′, J, J′) embryos. For each embryo a ventral and a dorsal view, or views from opposite sides if DV polarity is lacking (B–G, D-J) are shown. Magnified surface views to the right of each embryo (x') reveal the presence or absence of pMAD in individual nuclei. The scale bar (A, A′) corresponds to 50 µm. For identifying the polarity of the DV axis and for BMP signaling activity during later development see Figure 3—figure supplement 1. DOI: http://dx.doi.org/10.7554/eLife.05502.007",
            ),
            ("article_doi", "10.7554/eLife.05502"),
            ("type", "fig"),
            ("position", 7),
            ("ordinal", 5),
            ("sibling_ordinal", 3),
            ("asset", None),
        ]
    ),
    OrderedDict(
        [
            ("doi", "10.7554/eLife.05502.008"),
            ("doi_url", "https://doi.org/10.7554/eLife.05502.008"),
            ("id", "fig3s1"),
            (
                "title",
                "Nuclear density and late pMAD distribution identify the dorsal side of Oncopeltus blastoderm embryos.",
            ),
            (
                "full_title",
                "Nuclear density and late pMAD distribution identify the dorsal side of <italic>Oncopeltus</italic> blastoderm embryos.",
            ),
            ("label", "Figure 3—figure supplement 1."),
            ("full_label", "Figure 3—figure supplement 1."),
            (
                "caption",
                "Top: the embryo was stained for pMAD and nucleic acids (SYTOX) to visualize the distribution of nuclei. Differences in nuclear density can be used to detect the polarity of the DV axis. At the dorsal side nuclear density is higher than at the ventral side. pMAD nuclear accumulation is found in regions of higher nuclear density, indicating that pMAD can be used as a marker for the dorsal region. Bottom: pMAD distribution at mid-blastoderm (∼26–28 hpf), late blastoderm (∼29–32 hpf) and at the beginning of the posterior invagination (anatrepsis) (∼33–37 hpf). For each embryo a dorsal, lateral and ventral view is shown. The pMAD distribution is progressively confined to the dorsal side. At the beginning of anatrepsis pMAD is restricted to a dorsal domain comprising approximately 30% of the embryonic circumference. The scale bar corresponds to 200 µm.",
            ),
            (
                "full_caption",
                "Top: the embryo was stained for pMAD and nucleic acids (SYTOX) to visualize the distribution of nuclei. Differences in nuclear density can be used to detect the polarity of the DV axis. At the dorsal side nuclear density is higher than at the ventral side. pMAD nuclear accumulation is found in regions of higher nuclear density, indicating that pMAD can be used as a marker for the dorsal region. Bottom: pMAD distribution at mid-blastoderm (∼26–28 hpf), late blastoderm (∼29–32 hpf) and at the beginning of the posterior invagination (anatrepsis) (∼33–37 hpf). For each embryo a dorsal, lateral and ventral view is shown. The pMAD distribution is progressively confined to the dorsal side. At the beginning of anatrepsis pMAD is restricted to a dorsal domain comprising approximately 30% of the embryonic circumference. The scale bar corresponds to 200 µm.",
            ),
            ("parent_type", "fig"),
            ("parent_ordinal", 5),
            ("parent_sibling_ordinal", 3),
            ("parent_asset", None),
            (
                "content",
                "Top: the embryo was stained for pMAD and nucleic acids (SYTOX) to visualize the distribution of nuclei. Differences in nuclear density can be used to detect the polarity of the DV axis. At the dorsal side nuclear density is higher than at the ventral side. pMAD nuclear accumulation is found in regions of higher nuclear density, indicating that pMAD can be used as a marker for the dorsal region. Bottom: pMAD distribution at mid-blastoderm (∼26–28 hpf), late blastoderm (∼29–32 hpf) and at the beginning of the posterior invagination (anatrepsis) (∼33–37 hpf). For each embryo a dorsal, lateral and ventral view is shown. The pMAD distribution is progressively confined to the dorsal side. At the beginning of anatrepsis pMAD is restricted to a dorsal domain comprising approximately 30% of the embryonic circumference. The scale bar corresponds to 200 µm. DOI: http://dx.doi.org/10.7554/eLife.05502.008",
            ),
            ("article_doi", "10.7554/eLife.05502"),
            ("type", "fig"),
            ("position", 8),
            ("ordinal", 6),
            ("sibling_ordinal", 2),
            ("asset", "figsupp"),
        ]
    ),
    OrderedDict(
        [
            ("doi", "10.7554/eLife.05502.009"),
            ("doi_url", "https://doi.org/10.7554/eLife.05502.009"),
            ("id", "fig4"),
            ("title", "Late phenotypes of dpp, sog and Toll1 KD embryos."),
            (
                "full_title",
                "Late phenotypes of dpp, <italic>sog</italic> and <italic>Toll1</italic> KD embryos.",
            ),
            ("label", "Figure 4."),
            ("full_label", "Figure 4."),
            (
                "caption",
                "Expression of msh (top row), sim (center row), and twi (bottom row) in wt (A–C), dpp-RNAi (D–F), sog-RNAi (G–I) and Toll1-RNAi (J–L) embryos monitored by ISH. The anterior of the embryo is on the left. Embryos are at the germ band stage (∼40–48 hpf). msh: in wt germ band stage embryos msh is expressed in the dorsal-most part of the CNS and in the mesoderm of the limb buds (dorsal-lateral view). dpp-RNAi germ band embryos lack msh expression except for an anterior domain. sog- or Toll1-pRNAi embryos have a tube-like appearance lacking mesoderm and limb buds. Along these tubes msh is either not expressed or it is expressed at uniform levels around the entire circumference. This indicates that the ectoderm of sog- and Toll1 KD embryos is dorsalized either at the level of the dorsal non-neurogenic or the dorsal-most neurogenic ectoderm. sim: in wt germ band stage embryos sim is expressed along the ventral midline (ventral-lateral view). Upon dpp-, sog- or Toll1-pRNAi, sim expression is lacking except for a ring of expression at the posterior tip of the growth zone in sog-RNAi and Toll1-RNAi embryos. This indicates that the ventral neuroectoderm is lost in these KD embryos. twi: in germ band stage embryos twi is expressed in the invaginated mesoderm, which forms initially a cord within the embryo (lateral view). In dpp-RNAi embryos twi is expressed in the entire germ band indicating complete mesodermalization. In sog-and Toll1-RNAi embryos twi is not expressed. This, in addition to the loss of sim expression, indicates that sog and Toll1 KD embryos consistently lack ventral cell fates along their entire AP axis. Scale bar corresponds to 200 µm.",
            ),
            (
                "full_caption",
                "Expression of <italic>msh</italic> (top row), <italic>sim</italic> (center row), and <italic>twi</italic> (bottom row) in wt (<bold>A</bold>–<bold>C</bold>), <italic>dpp</italic>-RNAi (<bold>D</bold>–<bold>F</bold>), <italic>sog</italic>-RNAi (<bold>G</bold>–<bold>I</bold>) and <italic>Toll1</italic>-RNAi (<bold>J</bold>–<bold>L</bold>) embryos monitored by ISH. The anterior of the embryo is on the left. Embryos are at the germ band stage (∼40–48 hpf). <bold><italic>msh</italic></bold>: in wt germ band stage embryos <italic>msh</italic> is expressed in the dorsal-most part of the CNS and in the mesoderm of the limb buds (dorsal-lateral view). <italic>dpp</italic>-RNAi germ band embryos lack <italic>msh</italic> expression except for an anterior domain. <italic>sog-</italic> or <italic>Toll1</italic>-pRNAi embryos have a tube-like appearance lacking mesoderm and limb buds. Along these tubes <italic>msh</italic> is either not expressed or it is expressed at uniform levels around the entire circumference. This indicates that the ectoderm of <italic>sog-</italic> and <italic>Toll1</italic> KD embryos is dorsalized either at the level of the dorsal non-neurogenic or the dorsal-most neurogenic ectoderm. <bold><italic>sim</italic></bold>: in wt germ band stage embryos <italic>sim</italic> is expressed along the ventral midline (ventral-lateral view). Upon <italic>dpp</italic>-, <italic>sog-</italic> or <italic>Toll1-</italic>pRNAi, <italic>sim</italic> expression is lacking except for a ring of expression at the posterior tip of the growth zone in <italic>sog</italic>-RNAi and <italic>Toll1</italic>-RNAi embryos. This indicates that the ventral neuroectoderm is lost in these KD embryos. <bold><italic>twi</italic></bold>: in germ band stage embryos <italic>twi</italic> is expressed in the invaginated mesoderm, which forms initially a cord within the embryo (lateral view). In <italic>dpp</italic>-RNAi embryos <italic>twi</italic> is expressed in the entire germ band indicating complete mesodermalization. In <italic>sog</italic>-and <italic>Toll1</italic>-RNAi embryos <italic>twi</italic> is not expressed. This, in addition to the loss of <italic>sim</italic> expression, indicates that <italic>sog</italic> and <italic>Toll1</italic> KD embryos consistently lack ventral cell fates along their entire AP axis. Scale bar corresponds to 200 µm.",
            ),
            (
                "content",
                "Expression of msh (top row), sim (center row), and twi (bottom row) in wt (A–C), dpp-RNAi (D–F), sog-RNAi (G–I) and Toll1-RNAi (J–L) embryos monitored by ISH. The anterior of the embryo is on the left. Embryos are at the germ band stage (∼40–48 hpf). msh: in wt germ band stage embryos msh is expressed in the dorsal-most part of the CNS and in the mesoderm of the limb buds (dorsal-lateral view). dpp-RNAi germ band embryos lack msh expression except for an anterior domain. sog- or Toll1-pRNAi embryos have a tube-like appearance lacking mesoderm and limb buds. Along these tubes msh is either not expressed or it is expressed at uniform levels around the entire circumference. This indicates that the ectoderm of sog- and Toll1 KD embryos is dorsalized either at the level of the dorsal non-neurogenic or the dorsal-most neurogenic ectoderm. sim: in wt germ band stage embryos sim is expressed along the ventral midline (ventral-lateral view). Upon dpp-, sog- or Toll1-pRNAi, sim expression is lacking except for a ring of expression at the posterior tip of the growth zone in sog-RNAi and Toll1-RNAi embryos. This indicates that the ventral neuroectoderm is lost in these KD embryos. twi: in germ band stage embryos twi is expressed in the invaginated mesoderm, which forms initially a cord within the embryo (lateral view). In dpp-RNAi embryos twi is expressed in the entire germ band indicating complete mesodermalization. In sog-and Toll1-RNAi embryos twi is not expressed. This, in addition to the loss of sim expression, indicates that sog and Toll1 KD embryos consistently lack ventral cell fates along their entire AP axis. Scale bar corresponds to 200 µm. DOI: http://dx.doi.org/10.7554/eLife.05502.009",
            ),
            ("article_doi", "10.7554/eLife.05502"),
            ("type", "fig"),
            ("position", 9),
            ("ordinal", 7),
            ("sibling_ordinal", 4),
            ("asset", None),
        ]
    ),
    OrderedDict(
        [
            ("doi", "10.7554/eLife.05502.010"),
            ("doi_url", "https://doi.org/10.7554/eLife.05502.010"),
            ("id", "fig5"),
            ("title", "BMP signaling is epistatic to Toll signaling in Oncopeltus."),
            (
                "full_title",
                "BMP signaling is epistatic to Toll signaling in <italic>Oncopeltus</italic>.",
            ),
            ("label", "Figure 5."),
            ("full_label", "Figure 5."),
            (
                "caption",
                "Expression of twi (A, E, H, L), sim (B, F, I, M), sog (C, G, J, N, P, R, T, V) in wt embryos (A–C, R, T, V), Toll1-RNAi embryos (E–G, P), dl1-RNAi embryos (H–J) and Toll1-dpp-RNAi embryos (L–N) monitored by ISH. The view is ventral (A–C, J, T, V), or not determined as the expression is DV symmetric (E–G, H, I, L–N, P, R). Embryos are at the blastoderm stage (A–C, E–G, H–J, L–N: 26–32 hpf; P–V see figure labels). Green arrowheads mark the anterior border of sim expression. The scale bar (A) corresponds to 200 µm. For phenotype frequencies and confirmation of KD see Figure 5—figure supplement 1. (D, K, O, Q, S, U, W) Simulations of the reaction diffusion system described in Box 1 on a two-dimensional cylinder (Figure 10). Depicted is the ventral part of the cylinder. Blue: sog expression level (η). Gray: BMP concentration (b). (D) wt: sog expression is confined to a ventral stripe. (K) Upon loss of active NF-κB/Dorsal (d = 0) due to either KD of Toll1 or KD of dl1, early activation of sog (P) is insufficient to initiate patterning resulting in uniformly high BMP signaling. (O) Upon simultaneous loss of Dorsal (d = 0) and BMP (b = 0) sog activation is possible despite lack of NF-κB/Dorsal; however, activation is uniform. (Q) sog activation at early stages in the absence of Toll signaling (d = 0). This reflects ηo, NF-κB/Dorsal-independent sog activation (Box 1). (S, U, W) Developmental progression of sog activation (η) during blastoderm stages.",
            ),
            (
                "full_caption",
                'Expression of <italic>twi</italic> (<bold>A</bold>, <bold>E</bold>, <bold>H</bold>, <bold>L</bold>), <italic>sim</italic> (<bold>B</bold>, <bold>F</bold>, <bold>I</bold>, <bold>M</bold>), <italic>sog</italic> (<bold>C</bold>, <bold>G</bold>, <bold>J</bold>, <bold>N</bold>, <bold>P</bold>, <bold>R</bold>, <bold>T</bold>, <bold>V</bold>) in wt embryos (<bold>A</bold>–<bold>C</bold>, <bold>R</bold>, <bold>T</bold>, <bold>V</bold>), <italic>Toll1</italic>-RNAi embryos (<bold>E</bold>–<bold>G</bold>, <bold>P</bold>), <italic>dl1</italic>-RNAi embryos (<bold>H</bold>–<bold>J</bold>) and <italic>Toll1-dpp</italic>-RNAi embryos (<bold>L</bold>–<bold>N</bold>) monitored by ISH. The view is ventral (<bold>A</bold>–<bold>C</bold>, <bold>J</bold>, <bold>T</bold>, <bold>V</bold>), or not determined as the expression is DV symmetric (<bold>E</bold>–<bold>G</bold>, <bold>H</bold>, <bold>I</bold>, <bold>L</bold>–<bold>N</bold>, <bold>P</bold>, <bold>R</bold>). Embryos are at the blastoderm stage (<bold>A</bold>–<bold>C</bold>, <bold>E</bold>–<bold>G</bold>, <bold>H</bold>–<bold>J</bold>, <bold>L</bold>–<bold>N</bold>: 26–32 hpf; <bold>P</bold>–<bold>V</bold> see figure labels). Green arrowheads mark the anterior border of <italic>sim</italic> expression. The scale bar (<bold>A</bold>) corresponds to 200 µm. For phenotype frequencies and confirmation of KD see <xref ref-type="fig" rid="fig5s1">Figure 5—figure supplement 1</xref>. (<bold>D</bold>, <bold>K</bold>, <bold>O</bold>, <bold>Q</bold>, <bold>S</bold>, <bold>U</bold>, <bold>W</bold>) Simulations of the reaction diffusion system described in <xref ref-type="boxed-text" rid="box1">Box 1</xref> on a two-dimensional cylinder (<xref ref-type="fig" rid="fig10">Figure 10</xref>). Depicted is the ventral part of the cylinder. Blue: <italic>sog</italic> expression level (<italic>η</italic>). Gray: BMP concentration (<bold><italic>b</italic></bold>). (<bold>D</bold>) wt: <italic>sog</italic> expression is confined to a ventral stripe. (<bold>K</bold>) Upon loss of active NF-κB/Dorsal (<italic>d</italic> = 0) due to either KD of <italic>Toll1</italic> or KD of <italic>dl1</italic>, early activation of <italic>sog</italic> (<bold>P</bold>) is insufficient to initiate patterning resulting in uniformly high BMP signaling. (<bold>O</bold>) Upon simultaneous loss of Dorsal (<italic>d</italic> = 0) and BMP (<italic>b</italic> = 0) <italic>sog</italic> activation is possible despite lack of NF-κB/Dorsal; however, activation is uniform. (<bold>Q</bold>) <italic>sog</italic> activation at early stages in the absence of Toll signaling (<italic>d</italic> = 0). This reflects <italic>η</italic><sub><italic>o</italic></sub>, NF-κB/Dorsal-independent <italic>sog</italic> activation (<xref ref-type="boxed-text" rid="box1">Box 1</xref>). (<bold>S</bold>, <bold>U</bold>, <bold>W</bold>) Developmental progression of <italic>sog</italic> activation (<italic>η</italic>) during blastoderm stages.',
            ),
            (
                "content",
                "Expression of twi (A, E, H, L), sim (B, F, I, M), sog (C, G, J, N, P, R, T, V) in wt embryos (A–C, R, T, V), Toll1-RNAi embryos (E–G, P), dl1-RNAi embryos (H–J) and Toll1-dpp-RNAi embryos (L–N) monitored by ISH. The view is ventral (A–C, J, T, V), or not determined as the expression is DV symmetric (E–G, H, I, L–N, P, R). Embryos are at the blastoderm stage (A–C, E–G, H–J, L–N: 26–32 hpf; P–V see figure labels). Green arrowheads mark the anterior border of sim expression. The scale bar (A) corresponds to 200 µm. For phenotype frequencies and confirmation of KD see Figure 5—figure supplement 1. (D, K, O, Q, S, U, W) Simulations of the reaction diffusion system described in Box 1 on a two-dimensional cylinder (Figure 10). Depicted is the ventral part of the cylinder. Blue: sog expression level (η). Gray: BMP concentration (b). (D) wt: sog expression is confined to a ventral stripe. (K) Upon loss of active NF-κB/Dorsal (d = 0) due to either KD of Toll1 or KD of dl1, early activation of sog (P) is insufficient to initiate patterning resulting in uniformly high BMP signaling. (O) Upon simultaneous loss of Dorsal (d = 0) and BMP (b = 0) sog activation is possible despite lack of NF-κB/Dorsal; however, activation is uniform. (Q) sog activation at early stages in the absence of Toll signaling (d = 0). This reflects ηo, NF-κB/Dorsal-independent sog activation (Box 1). (S, U, W) Developmental progression of sog activation (η) during blastoderm stages. DOI: http://dx.doi.org/10.7554/eLife.05502.010",
            ),
            ("article_doi", "10.7554/eLife.05502"),
            ("type", "fig"),
            ("position", 10),
            ("ordinal", 8),
            ("sibling_ordinal", 5),
            ("asset", None),
        ]
    ),
    OrderedDict(
        [
            ("doi", "10.7554/eLife.05502.011"),
            ("doi_url", "https://doi.org/10.7554/eLife.05502.011"),
            ("id", "fig5s1"),
            ("title", "Phenotype frequencies and transcript levels after RNAi."),
            ("full_title", "Phenotype frequencies and transcript levels after RNAi."),
            ("label", "Figure 5—figure supplement 1."),
            ("full_label", "Figure 5—figure supplement 1."),
            (
                "caption",
                "Top: the KD of Toll and dl1 caused partial or complete dorsalization. Completely dorsalized embryos lack twi, sog or sim (except for the terminal domain) expression and exhibit uniform levels of nuclear localized pMAD levels. Partially dorsalized embryos show residual twi, sog or sim expression and their nuclear pMAD levels are not completely uniform. No wt-like patterns were observed. The table shows % of complete ventralization or complete dorsalization. The double KD of dpp plus Toll by parental RNAi caused complete ventralization. Completely ventralized embryos show a uniform expansion of twi, sog, or the ventral-anterior sim domain (analyzed by ISH). Each marker was analyzed separately. Bottom: expression of actin 5C, dpp and/or Toll1 in Toll1-RNAi, dpp-RNAi, Toll1-dpp-RNAi compared to wt (left column) detected by gel electrophoresis after semi-qPCR.",
            ),
            (
                "full_caption",
                "Top: the KD of <italic>Toll</italic> and <italic>dl1</italic> caused partial or complete dorsalization. Completely dorsalized embryos lack <italic>twi</italic>, <italic>sog</italic> or <italic>sim</italic> (except for the terminal domain) expression and exhibit uniform levels of nuclear localized pMAD levels. Partially dorsalized embryos show residual <italic>twi</italic>, <italic>sog</italic> or <italic>sim</italic> expression and their nuclear pMAD levels are not completely uniform. No wt-like patterns were observed. The table shows % of complete ventralization or complete dorsalization. The double KD of <italic>dpp</italic> plus <italic>Toll</italic> by parental RNAi caused complete ventralization. Completely ventralized embryos show a uniform expansion of <italic>twi</italic>, <italic>sog,</italic> or the ventral-anterior <italic>sim</italic> domain (analyzed by ISH). Each marker was analyzed separately. Bottom: expression of <italic>actin 5C</italic>, <italic>dpp</italic> and/or <italic>Toll1</italic> in <italic>Toll1</italic>-RNAi, <italic>dpp</italic>-RNAi, <italic>Toll1-dpp-</italic>RNAi compared to wt (left column) detected by gel electrophoresis after semi-qPCR.",
            ),
            ("parent_type", "fig"),
            ("parent_ordinal", 8),
            ("parent_sibling_ordinal", 5),
            ("parent_asset", None),
            (
                "content",
                "Top: the KD of Toll and dl1 caused partial or complete dorsalization. Completely dorsalized embryos lack twi, sog or sim (except for the terminal domain) expression and exhibit uniform levels of nuclear localized pMAD levels. Partially dorsalized embryos show residual twi, sog or sim expression and their nuclear pMAD levels are not completely uniform. No wt-like patterns were observed. The table shows % of complete ventralization or complete dorsalization. The double KD of dpp plus Toll by parental RNAi caused complete ventralization. Completely ventralized embryos show a uniform expansion of twi, sog, or the ventral-anterior sim domain (analyzed by ISH). Each marker was analyzed separately. Bottom: expression of actin 5C, dpp and/or Toll1 in Toll1-RNAi, dpp-RNAi, Toll1-dpp-RNAi compared to wt (left column) detected by gel electrophoresis after semi-qPCR. DOI: http://dx.doi.org/10.7554/eLife.05502.011",
            ),
            ("article_doi", "10.7554/eLife.05502"),
            ("type", "fig"),
            ("position", 11),
            ("ordinal", 9),
            ("sibling_ordinal", 2),
            ("asset", "figsupp"),
        ]
    ),
    OrderedDict(
        [
            ("doi", "10.7554/eLife.05502.012"),
            ("doi_url", "https://doi.org/10.7554/eLife.05502.012"),
            ("id", "fig6"),
            ("title", "Toll signaling affects AP patterning."),
            ("full_title", "Toll signaling affects AP patterning."),
            ("label", "Figure 6."),
            ("full_label", "Figure 6."),
            (
                "caption",
                "Expression of msh is monitored by ISH in blastoderm embryos. The view is lateral (A), or not determined as the expression is DV symmetric (B–D). The red arrowheads mark the posterior border of msh expression which is positioned at approximately 60% egg length (0% posterior pole) in wt (A) and tsg KD (D) embryos. In Toll1 and dl1 KD embryos, the msh domain expands to the anterior tip of the embryo and its posterior border is shifted anteriorly (to approximately 80% egg length).",
            ),
            (
                "full_caption",
                "Expression of <italic>msh</italic> is monitored by ISH in blastoderm embryos. The view is lateral (<bold>A</bold>), or not determined as the expression is DV symmetric (<bold>B</bold>–<bold>D</bold>). The red arrowheads mark the posterior border of <italic>msh</italic> expression which is positioned at approximately 60% egg length (0% posterior pole) in wt (<bold>A</bold>) and <italic>tsg</italic> KD (<bold>D</bold>) embryos. In <italic>Toll1</italic> and <italic>dl1</italic> KD embryos, the <italic>msh</italic> domain expands to the anterior tip of the embryo and its posterior border is shifted anteriorly (to approximately 80% egg length).",
            ),
            (
                "content",
                "Expression of msh is monitored by ISH in blastoderm embryos. The view is lateral (A), or not determined as the expression is DV symmetric (B–D). The red arrowheads mark the posterior border of msh expression which is positioned at approximately 60% egg length (0% posterior pole) in wt (A) and tsg KD (D) embryos. In Toll1 and dl1 KD embryos, the msh domain expands to the anterior tip of the embryo and its posterior border is shifted anteriorly (to approximately 80% egg length). DOI: http://dx.doi.org/10.7554/eLife.05502.012",
            ),
            ("article_doi", "10.7554/eLife.05502"),
            ("type", "fig"),
            ("position", 12),
            ("ordinal", 10),
            ("sibling_ordinal", 6),
            ("asset", None),
        ]
    ),
    OrderedDict(
        [
            ("doi", "10.7554/eLife.05502.013"),
            ("doi_url", "https://doi.org/10.7554/eLife.05502.013"),
            ("id", "fig7"),
            ("title", "Expression of cact1 and cact3."),
            (
                "full_title",
                "Expression of <italic>cact1</italic> and <italic>cact3</italic>.",
            ),
            ("label", "Figure 7."),
            ("full_label", "Figure 7."),
            (
                "caption",
                "Expression of cact1 (A–D) and cact3 (E–H) are monitored by ISH with embryos at early to late blastoderm stages (20–32 hpf). (A′–D′, E′, H′) SYTOX Green staining shows nuclear density to determine developmental stage. (A, B) cact1 expression is initiated evenly. (C) With proceeding development cact1 expression vanishes from the dorsal side. (D) 20% of Toll1 KD embryos lack cact1 expression. The remainder show reduced expression compared to wt. (E) cact3 expression is initiated uniformly along the DV axis between 20% and 60% egg length. (F, G) In older blastoderm stages cact3 is expressed in a broad domain encompassing 60–80% of the egg circumference. (H) 47% of Toll1 KD embryos lack cact3 expression. The remainder show reduced expression compared to wt. (I, J) Double ISH for cact3 (blue) and sog (red) confirms that cact3 is expressed ventrally and that its domain expands more dorsally than the sog domain.",
            ),
            (
                "full_caption",
                "Expression of <italic>cact1</italic> (<bold>A</bold>–<bold>D</bold>) and <italic>cact3</italic> (<bold>E</bold>–<bold>H</bold>) are monitored by ISH with embryos at early to late blastoderm stages (20–32 hpf). (<bold>A′</bold>–<bold>D′</bold>, <bold>E′</bold>, <bold>H′</bold>) SYTOX Green staining shows nuclear density to determine developmental stage. (<bold>A</bold>, <bold>B</bold>) <italic>cact1</italic> expression is initiated evenly. (<bold>C</bold>) With proceeding development <italic>cact1</italic> expression vanishes from the dorsal side. (<bold>D</bold>) 20% of <italic>Toll1</italic> KD embryos lack <italic>cact1</italic> expression. The remainder show reduced expression compared to wt. (<bold>E</bold>) <italic>cact3</italic> expression is initiated uniformly along the DV axis between 20% and 60% egg length. (<bold>F</bold>, <bold>G</bold>) In older blastoderm stages <italic>cact3</italic> is expressed in a broad domain encompassing 60–80% of the egg circumference. (<bold>H</bold>) 47% of <italic>Toll1</italic> KD embryos lack <italic>cact3</italic> expression. The remainder show reduced expression compared to wt. (<bold>I</bold>, <bold>J</bold>) Double ISH for <italic>cact3</italic> (blue) and <italic>sog</italic> (red) confirms that <italic>cact3</italic> is expressed ventrally and that its domain expands more dorsally than the <italic>sog</italic> domain.",
            ),
            (
                "content",
                "Expression of cact1 (A–D) and cact3 (E–H) are monitored by ISH with embryos at early to late blastoderm stages (20–32 hpf). (A′–D′, E′, H′) SYTOX Green staining shows nuclear density to determine developmental stage. (A, B) cact1 expression is initiated evenly. (C) With proceeding development cact1 expression vanishes from the dorsal side. (D) 20% of Toll1 KD embryos lack cact1 expression. The remainder show reduced expression compared to wt. (E) cact3 expression is initiated uniformly along the DV axis between 20% and 60% egg length. (F, G) In older blastoderm stages cact3 is expressed in a broad domain encompassing 60–80% of the egg circumference. (H) 47% of Toll1 KD embryos lack cact3 expression. The remainder show reduced expression compared to wt. (I, J) Double ISH for cact3 (blue) and sog (red) confirms that cact3 is expressed ventrally and that its domain expands more dorsally than the sog domain. DOI: http://dx.doi.org/10.7554/eLife.05502.013",
            ),
            ("article_doi", "10.7554/eLife.05502"),
            ("type", "fig"),
            ("position", 13),
            ("ordinal", 11),
            ("sibling_ordinal", 7),
            ("asset", None),
        ]
    ),
    OrderedDict(
        [
            ("doi", "10.7554/eLife.05502.014"),
            ("doi_url", "https://doi.org/10.7554/eLife.05502.014"),
            ("id", "box1"),
            ("label", "Box 1."),
            ("full_label", "Box 1."),
            (
                "caption",
                "We built a reaction-diffusion model of the BMP/Sog system based on (i) inhibition of sog expression by BMP, (ii) sog transcriptional activation by NF-κB/Dorsal, (iii) the binding of Sog to BMP and (iv) the rapid diffusion of the Sog-BMP complex.",
            ),
            (
                "full_caption",
                "We built a reaction-diffusion model of the BMP/Sog system based on (i) inhibition of <italic>sog</italic> expression by BMP, (ii) <italic>sog</italic> transcriptional activation by NF-κB/Dorsal, (iii) the binding of Sog to BMP and (iv) the rapid diffusion of the Sog-BMP complex.",
            ),
            (
                "content",
                "We built a reaction-diffusion model of the BMP/Sog system based on (i) inhibition of sog expression by BMP, (ii) sog transcriptional activation by NF-κB/Dorsal, (iii) the binding of Sog to BMP and (iv) the rapid diffusion of the Sog-BMP complex. A simple Michaelis–Menten model of sog regulation gives the rate of sog expressionηs(b,d)=\u2009η0\u2009+\u2009η1\u2009d/d0(1+b/b0)(1+d/d0),in terms of the local concentrations b (BMP) and d (NF-κB/Dorsal). η0 is the rate of sog expression in the absence of NF-κB/Dorsal and BMP, η1 > η0 is the asymptotic rate of sog expression at high concentrations of NF-κB/Dorsal and in the absence of BMP. This model can exhibit an instability of the homogeneous state (Box figure 1). Consider a small ‘seed’ of elevated Sog concentration arising from the polarity cue provided by NF-κB/Dorsal. Sog molecules bind BMP and the complexes diffuse away quickly, leading to a depletion of BMP. Since BMP represses sog, this leads to a local increase of sog expression, causing the seed to grow. In the steady state, there is a region of high Sog levels (where BMP diffuses away quickly due to complex formation) around the original seed, and a region of high BMP levels away from the seed, where sog is repressed by BMP.10.7554/eLife.05502.015Box figure 1.Temporal progression of pattern formation.Simulated concentration profiles of NF-κB/Dorsal, Sog and BMP are plotted at successive time points, starting from a broad peak of NF-κB/Dorsal (left to right: t = 0 hr, 4 hr, 6 hr and steady state; see Table 1 for parameter values). The x-axis shows the circumference of the embryo, with the dorsal and ventral sides marked as D and V, respectively.DOI: http://dx.doi.org/10.7554/eLife.05502.015 Simulated concentration profiles of NF-κB/Dorsal, Sog and BMP are plotted at successive time points, starting from a broad peak of NF-κB/Dorsal (left to right: t = 0 hr, 4 hr, 6 hr and steady state; see Table 1 for parameter values). The x-axis shows the circumference of the embryo, with the dorsal and ventral sides marked as D and V, respectively. DOI: http://dx.doi.org/10.7554/eLife.05502.015 The instability turns out to be controlled by the level of NF-κB/Dorsal. A threshold amount of NF-κB/Dorsal is required initially to build a stripe of high Sog concentration near the initial NF-κB/Dorsal maximum (Figures 8, 9). This effect also leads to the phenomenon of twinning: if the amount of NF-κB/Dorsal is above the threshold in both halves of the embryo, a cut along the DV axis can lead to the formation of a stripe in each half (Box figure 2).10.7554/eLife.05502.016Box figure 2.Embryonic twinning in Euscelis.Simulation of wt (left) showing Sog (red) and BMP (green) protein concentration profiles along the DV axis at steady state given initial NF-κB/Dorsal protein levels (blue: dashed line). A schematic drawing on the left shows a wt Euscelis embryo at the germ band stage. Simulations after the DV axis is split in two halves (right) result in the formation of one BMP gradient in each half. Thus, the proposed model can account for the embryonic twinning observed in Euscelis after production of dorsal and ventral egg fragments shown schematically on the left (Sander, 1971).DOI: http://dx.doi.org/10.7554/eLife.05502.016 Simulation of wt (left) showing Sog (red) and BMP (green) protein concentration profiles along the DV axis at steady state given initial NF-κB/Dorsal protein levels (blue: dashed line). A schematic drawing on the left shows a wt Euscelis embryo at the germ band stage. Simulations after the DV axis is split in two halves (right) result in the formation of one BMP gradient in each half. Thus, the proposed model can account for the embryonic twinning observed in Euscelis after production of dorsal and ventral egg fragments shown schematically on the left (Sander, 1971). DOI: http://dx.doi.org/10.7554/eLife.05502.016 The dynamics of our model are similar to those of activator-inhibitor models of pattern formation (Turing, 1952; Gierer and Meinhardt, 1972). However, in our model there is no explicit activator. Instead, the patterning mechanism emerges from the transport of the Sog-BMP complex away from areas with elevated Sog concentration, leading to a derepression of sog by removal of BMP. DOI: http://dx.doi.org/10.7554/eLife.05502.014",
            ),
            ("article_doi", "10.7554/eLife.05502"),
            ("type", "boxed-text"),
            ("position", 14),
            ("ordinal", 1),
            ("sibling_ordinal", 1),
            ("asset", None),
        ]
    ),
    OrderedDict(
        [
            ("doi", "10.7554/eLife.05502.015"),
            ("doi_url", "https://doi.org/10.7554/eLife.05502.015"),
            ("id", "fig13"),
            ("title", "Temporal progression of pattern formation."),
            ("full_title", "Temporal progression of pattern formation."),
            ("label", "Box figure 1."),
            ("full_label", "Box figure 1."),
            (
                "caption",
                "Simulated concentration profiles of NF-κB/Dorsal, Sog and BMP are plotted at successive time points, starting from a broad peak of NF-κB/Dorsal (left to right: t = 0 hr, 4 hr, 6 hr and steady state; see Table 1 for parameter values). The x-axis shows the circumference of the embryo, with the dorsal and ventral sides marked as D and V, respectively.",
            ),
            (
                "full_caption",
                'Simulated concentration profiles of NF-κB/Dorsal, Sog and BMP are plotted at successive time points, starting from a broad peak of NF-κB/Dorsal (left to right: t = 0 hr, 4 hr, 6 hr and steady state; see <xref ref-type="table" rid="tbl1">Table 1</xref> for parameter values). The x-axis shows the circumference of the embryo, with the dorsal and ventral sides marked as D and V, respectively.',
            ),
            ("parent_type", "boxed-text"),
            ("parent_ordinal", 1),
            ("parent_sibling_ordinal", 1),
            ("parent_asset", None),
            (
                "content",
                "Simulated concentration profiles of NF-κB/Dorsal, Sog and BMP are plotted at successive time points, starting from a broad peak of NF-κB/Dorsal (left to right: t = 0 hr, 4 hr, 6 hr and steady state; see Table 1 for parameter values). The x-axis shows the circumference of the embryo, with the dorsal and ventral sides marked as D and V, respectively. DOI: http://dx.doi.org/10.7554/eLife.05502.015",
            ),
            ("article_doi", "10.7554/eLife.05502"),
            ("type", "fig"),
            ("position", 15),
            ("ordinal", 12),
            ("sibling_ordinal", 8),
            ("asset", None),
        ]
    ),
    OrderedDict(
        [
            ("doi", "10.7554/eLife.05502.016"),
            ("doi_url", "https://doi.org/10.7554/eLife.05502.016"),
            ("id", "fig14"),
            ("title", "Embryonic twinning in Euscelis."),
            ("full_title", "Embryonic twinning in <italic>Euscelis</italic>."),
            ("label", "Box figure 2."),
            ("full_label", "Box figure 2."),
            (
                "caption",
                "Simulation of wt (left) showing Sog (red) and BMP (green) protein concentration profiles along the DV axis at steady state given initial NF-κB/Dorsal protein levels (blue: dashed line). A schematic drawing on the left shows a wt Euscelis embryo at the germ band stage. Simulations after the DV axis is split in two halves (right) result in the formation of one BMP gradient in each half. Thus, the proposed model can account for the embryonic twinning observed in Euscelis after production of dorsal and ventral egg fragments shown schematically on the left (Sander, 1971).",
            ),
            (
                "full_caption",
                'Simulation of wt (left) showing Sog (red) and BMP (green) protein concentration profiles along the DV axis at steady state given initial NF-κB/Dorsal protein levels (blue: dashed line). A schematic drawing on the left shows a wt <italic>Euscelis</italic> embryo at the germ band stage. Simulations after the DV axis is split in two halves (right) result in the formation of one BMP gradient in each half. Thus, the proposed model can account for the embryonic twinning observed in <italic>Euscelis</italic> after production of dorsal and ventral egg fragments shown schematically on the left (<xref ref-type="bibr" rid="bib53">Sander, 1971</xref>).',
            ),
            ("parent_type", "boxed-text"),
            ("parent_ordinal", 1),
            ("parent_sibling_ordinal", 1),
            ("parent_asset", None),
            (
                "content",
                "Simulation of wt (left) showing Sog (red) and BMP (green) protein concentration profiles along the DV axis at steady state given initial NF-κB/Dorsal protein levels (blue: dashed line). A schematic drawing on the left shows a wt Euscelis embryo at the germ band stage. Simulations after the DV axis is split in two halves (right) result in the formation of one BMP gradient in each half. Thus, the proposed model can account for the embryonic twinning observed in Euscelis after production of dorsal and ventral egg fragments shown schematically on the left (Sander, 1971). DOI: http://dx.doi.org/10.7554/eLife.05502.016",
            ),
            ("article_doi", "10.7554/eLife.05502"),
            ("type", "fig"),
            ("position", 16),
            ("ordinal", 13),
            ("sibling_ordinal", 9),
            ("asset", None),
        ]
    ),
    OrderedDict(
        [
            ("doi", "10.7554/eLife.05502.017"),
            ("doi_url", "https://doi.org/10.7554/eLife.05502.017"),
            ("id", "fig8"),
            ("title", "Dynamics of pattern formation."),
            ("full_title", "Dynamics of pattern formation."),
            ("label", "Figure 8."),
            ("full_label", "Figure 8."),
            (
                "caption",
                "Each plot shows the concentration of a particular protein species in space (x running from 0 to lx along the front of the plot parameterizing the circumference of the cylinder) and time (running towards the back). Left: the concentration of NF-κB/Dorsal shows a broad Gaussian profile that decays to zero with time. Center: starting from a uniform distribution a region of high Sog concentrations forms where the initial distribution of NF-κB/Dorsal had its maximum. Right: BMP is depleted where Sog levels are high. Initial conditions are b(x, t = 0) = 0.32, s(x, t = 0) = 0.01, c(x, t = 0) = 0.14, d(x, t = 0) = Do\u2061exp{−12(2/lx)2(x−2/lx)2}. Throughout the text Do=0.3, except in the twinning figure (Box 1), where Do=1 was used to ensure a sufficient amount of NF-κB/Dorsal in both halves of the embryo.",
            ),
            (
                "full_caption",
                'Each plot shows the concentration of a particular protein species in space (<italic>x</italic> running from 0 to <italic>l</italic><sub><italic>x</italic></sub> along the front of the plot parameterizing the circumference of the cylinder) and time (running towards the back). Left: the concentration of NF-κB/Dorsal shows a broad Gaussian profile that decays to zero with time. Center: starting from a uniform distribution a region of high Sog concentrations forms where the initial distribution of NF-κB/Dorsal had its maximum. Right: BMP is depleted where Sog levels are high. Initial conditions are <italic>b</italic>(<italic>x, t</italic> = 0) = 0.32, <italic>s</italic>(<italic>x, t</italic> = 0) = 0.01, <italic>c</italic>(<italic>x, t</italic> = 0) = 0.14, <italic>d</italic>(<italic>x, t</italic> = 0) = <inline-formula><mml:math id="inf1"><mml:mrow><mml:msub><mml:mi>D</mml:mi><mml:mi>o</mml:mi></mml:msub><mml:mo>\u2061</mml:mo><mml:mi>exp</mml:mi><mml:mrow><mml:mo>{</mml:mo><mml:mrow><mml:mo>−</mml:mo><mml:mfrac><mml:mn>1</mml:mn><mml:mn>2</mml:mn></mml:mfrac><mml:msup><mml:mrow><mml:mrow><mml:mo>(</mml:mo><mml:mrow><mml:mn>2</mml:mn><mml:mo>/</mml:mo><mml:msub><mml:mi>l</mml:mi><mml:mi>x</mml:mi></mml:msub></mml:mrow><mml:mo>)</mml:mo></mml:mrow></mml:mrow><mml:mn>2</mml:mn></mml:msup><mml:msup><mml:mrow><mml:mrow><mml:mo>(</mml:mo><mml:mrow><mml:mi>x</mml:mi><mml:mo>−</mml:mo><mml:mn>2</mml:mn><mml:mo>/</mml:mo><mml:msub><mml:mi>l</mml:mi><mml:mi>x</mml:mi></mml:msub></mml:mrow><mml:mo>)</mml:mo></mml:mrow></mml:mrow><mml:mn>2</mml:mn></mml:msup></mml:mrow><mml:mo>}</mml:mo></mml:mrow></mml:mrow></mml:math></inline-formula>. Throughout the text <inline-formula><mml:math id="inf2"><mml:mrow><mml:msub><mml:mi>D</mml:mi><mml:mi>o</mml:mi></mml:msub><mml:mo>=</mml:mo><mml:mn>0.3</mml:mn></mml:mrow></mml:math></inline-formula>, except in the twinning figure (<xref ref-type="boxed-text" rid="box1">Box 1</xref>), where <inline-formula><mml:math id="inf3"><mml:mrow><mml:msub><mml:mi>D</mml:mi><mml:mi>o</mml:mi></mml:msub><mml:mo>=</mml:mo><mml:mn>1</mml:mn></mml:mrow></mml:math></inline-formula> was used to ensure a sufficient amount of NF-κB/Dorsal in both halves of the embryo.',
            ),
            (
                "content",
                "Each plot shows the concentration of a particular protein species in space (x running from 0 to lx along the front of the plot parameterizing the circumference of the cylinder) and time (running towards the back). Left: the concentration of NF-κB/Dorsal shows a broad Gaussian profile that decays to zero with time. Center: starting from a uniform distribution a region of high Sog concentrations forms where the initial distribution of NF-κB/Dorsal had its maximum. Right: BMP is depleted where Sog levels are high. Initial conditions are b(x, t = 0) = 0.32, s(x, t = 0) = 0.01, c(x, t = 0) = 0.14, d(x, t = 0) = Do\u2061exp{−12(2/lx)2(x−2/lx)2}. Throughout the text Do=0.3, except in the twinning figure (Box 1), where Do=1 was used to ensure a sufficient amount of NF-κB/Dorsal in both halves of the embryo. DOI: http://dx.doi.org/10.7554/eLife.05502.017",
            ),
            ("article_doi", "10.7554/eLife.05502"),
            ("type", "fig"),
            ("position", 17),
            ("ordinal", 14),
            ("sibling_ordinal", 10),
            ("asset", None),
        ]
    ),
    OrderedDict(
        [
            ("doi", "10.7554/eLife.05502.018"),
            ("doi_url", "https://doi.org/10.7554/eLife.05502.018"),
            ("id", "fig9"),
            (
                "title",
                "Pattern formation from different initial levels of NF-κB/Dorsal.",
            ),
            (
                "full_title",
                "Pattern formation from different initial levels of NF-κB/Dorsal.",
            ),
            ("label", "Figure 9."),
            ("full_label", "Figure 9."),
            (
                "caption",
                "The initial concentration gradient of NF-κB/Dorsal is shown on top (gray). Initial amplitudes of NF-κB/Dorsal are Do=0.15,\u20090.3,\u20091 from left to right, the dashed line indicates the threshold NF-κB/Dorsal concentration required for patterning. Below, steady-state levels of free BMP (red) and free Sog are shown (blue, rescaled to facilitate plotting on the same plot as BMP).",
            ),
            (
                "full_caption",
                'The initial concentration gradient of NF-κB/Dorsal is shown on top (gray). Initial amplitudes of NF-κB/Dorsal are <inline-formula><mml:math id="inf4"><mml:mrow><mml:msub><mml:mi>D</mml:mi><mml:mi>o</mml:mi></mml:msub><mml:mo>=</mml:mo><mml:mn>0.15</mml:mn><mml:mo>,</mml:mo><mml:mo>\u2009</mml:mo><mml:mn>0.3</mml:mn><mml:mo>,</mml:mo><mml:mo>\u2009</mml:mo><mml:mn>1</mml:mn></mml:mrow></mml:math></inline-formula> from left to right, the dashed line indicates the threshold NF-κB/Dorsal concentration required for patterning. Below, steady-state levels of free BMP (red) and free Sog are shown (blue, rescaled to facilitate plotting on the same plot as BMP).',
            ),
            (
                "content",
                "The initial concentration gradient of NF-κB/Dorsal is shown on top (gray). Initial amplitudes of NF-κB/Dorsal are Do=0.15,\u20090.3,\u20091 from left to right, the dashed line indicates the threshold NF-κB/Dorsal concentration required for patterning. Below, steady-state levels of free BMP (red) and free Sog are shown (blue, rescaled to facilitate plotting on the same plot as BMP). DOI: http://dx.doi.org/10.7554/eLife.05502.018",
            ),
            ("article_doi", "10.7554/eLife.05502"),
            ("type", "fig"),
            ("position", 18),
            ("ordinal", 15),
            ("sibling_ordinal", 11),
            ("asset", None),
        ]
    ),
    OrderedDict(
        [
            ("doi", "10.7554/eLife.05502.019"),
            ("doi_url", "https://doi.org/10.7554/eLife.05502.019"),
            ("id", "tbl1"),
            ("label", "Table 1."),
            ("full_label", "Table 1."),
            ("caption", "Model parameters."),
            ("full_caption", "Model parameters."),
            (
                "content",
                "Model parameters. DOI: http://dx.doi.org/10.7554/eLife.05502.019 Units are arbitrary but are suggested to be seconds for time and meters for length.",
            ),
            ("article_doi", "10.7554/eLife.05502"),
            ("type", "table-wrap"),
            ("position", 19),
            ("ordinal", 1),
            ("sibling_ordinal", 1),
            ("asset", None),
        ]
    ),
    OrderedDict(
        [
            ("doi", "10.7554/eLife.05502.020"),
            ("doi_url", "https://doi.org/10.7554/eLife.05502.020"),
            ("id", "fig10"),
            ("title", "Pattern formation in two dimensions."),
            ("full_title", "Pattern formation in two dimensions."),
            ("label", "Figure 10."),
            ("full_label", "Figure 10."),
            (
                "caption",
                "Starting from a distribution of NF-κB/Dorsal with a broad maximum running in parallel to the cylinder's axis (bottom, shown in green), a stripe of high Sog concentration develops (top, Sog shown in blue, BMP shown in red). The figures show concentrations at times 0, 1000, 2000, 3000, 4000 from left to right.",
            ),
            (
                "full_caption",
                "Starting from a distribution of NF-κB/Dorsal with a broad maximum running in parallel to the cylinder's axis (bottom, shown in green), a stripe of high Sog concentration develops (top, Sog shown in blue, BMP shown in red). The figures show concentrations at times 0, 1000, 2000, 3000, 4000 from left to right.",
            ),
            (
                "content",
                "Starting from a distribution of NF-κB/Dorsal with a broad maximum running in parallel to the cylinder's axis (bottom, shown in green), a stripe of high Sog concentration develops (top, Sog shown in blue, BMP shown in red). The figures show concentrations at times 0, 1000, 2000, 3000, 4000 from left to right. DOI: http://dx.doi.org/10.7554/eLife.05502.020",
            ),
            ("article_doi", "10.7554/eLife.05502"),
            ("type", "fig"),
            ("position", 20),
            ("ordinal", 16),
            ("sibling_ordinal", 12),
            ("asset", None),
        ]
    ),
    OrderedDict(
        [
            ("doi", "10.7554/eLife.05502.021"),
            ("doi_url", "https://doi.org/10.7554/eLife.05502.021"),
            ("id", "fig11"),
            (
                "title",
                "Independence from the stripe of initial conditions (same data as Figure 10).",
            ),
            (
                "full_title",
                'Independence from the stripe of initial conditions (same data as <xref ref-type="fig" rid="fig10">Figure 10</xref>).',
            ),
            ("label", "Figure 11."),
            ("full_label", "Figure 11."),
            (
                "caption",
                "(top) The initial distribution of NF-κB/Dorsal from Figure 10 varies along the cylinder's axis (y-direction of this contour plot, with the x-direction describing the circumference) in both standard deviation and amplitude by about 10%; d(x,t=0)\u2009=\u2009\u2061exp{−522(1+0.1\u2061sin(πy/ly))2(x−2/lx)2}\u2009(1+0.1\u2061sin(πy/ly)), and decays over time (time points 0, 1000, 2000, 3000, 4000 shown from left to right). (bottom) The resulting distribution of Sog (and correspondingly of BMP) becomes uniform along the cylinder axis.",
            ),
            (
                "full_caption",
                '(top) The initial distribution of NF-κB/Dorsal from <xref ref-type="fig" rid="fig10">Figure 10</xref> varies along the cylinder\'s axis (y-direction of this contour plot, with the x-direction describing the circumference) in both standard deviation and amplitude by about 10%; <inline-formula><mml:math id="inf5"><mml:mrow><mml:mi>d</mml:mi><mml:mrow><mml:mo>(</mml:mo><mml:mrow><mml:mi>x</mml:mi><mml:mo>,</mml:mo><mml:mi>t</mml:mi><mml:mo>=</mml:mo><mml:mn>0</mml:mn></mml:mrow><mml:mo>)</mml:mo></mml:mrow><mml:mo>\u2009</mml:mo><mml:msub><mml:mo>=</mml:mo><mml:mo>\u2009</mml:mo></mml:msub><mml:mo>\u2061</mml:mo><mml:mi>exp</mml:mi><mml:mrow><mml:mo>{</mml:mo><mml:mrow><mml:mo>−</mml:mo><mml:mfrac><mml:mrow><mml:msup><mml:mn>5</mml:mn><mml:mn>2</mml:mn></mml:msup></mml:mrow><mml:mrow><mml:mn>2</mml:mn><mml:msup><mml:mrow><mml:mrow><mml:mo>(</mml:mo><mml:mrow><mml:mn>1</mml:mn><mml:mo>+</mml:mo><mml:mn>0.1</mml:mn><mml:mo>\u2061</mml:mo><mml:mi>sin</mml:mi><mml:mrow><mml:mo>(</mml:mo><mml:mrow><mml:mi>π</mml:mi><mml:mi>y</mml:mi><mml:mo>/</mml:mo><mml:msub><mml:mi>l</mml:mi><mml:mi>y</mml:mi></mml:msub></mml:mrow><mml:mo>)</mml:mo></mml:mrow></mml:mrow><mml:mo>)</mml:mo></mml:mrow></mml:mrow><mml:mn>2</mml:mn></mml:msup></mml:mrow></mml:mfrac><mml:msup><mml:mrow><mml:mrow><mml:mo>(</mml:mo><mml:mrow><mml:mi>x</mml:mi><mml:mo>−</mml:mo><mml:mn>2</mml:mn><mml:mo>/</mml:mo><mml:msub><mml:mi>l</mml:mi><mml:mi>x</mml:mi></mml:msub></mml:mrow><mml:mo>)</mml:mo></mml:mrow></mml:mrow><mml:mn>2</mml:mn></mml:msup></mml:mrow><mml:mo>}</mml:mo></mml:mrow><mml:mo>\u2009</mml:mo><mml:mrow><mml:mo>(</mml:mo><mml:mrow><mml:mn>1</mml:mn><mml:mo>+</mml:mo><mml:mn>0.1</mml:mn><mml:mo>\u2061</mml:mo><mml:mi>sin</mml:mi><mml:mrow><mml:mo>(</mml:mo><mml:mrow><mml:mi>π</mml:mi><mml:mi>y</mml:mi><mml:mo>/</mml:mo><mml:msub><mml:mi>l</mml:mi><mml:mi>y</mml:mi></mml:msub></mml:mrow><mml:mo>)</mml:mo></mml:mrow></mml:mrow><mml:mo>)</mml:mo></mml:mrow></mml:mrow></mml:math></inline-formula>, and decays over time (time points 0, 1000, 2000, 3000, 4000 shown from left to right). (bottom) The resulting distribution of Sog (and correspondingly of BMP) becomes uniform along the cylinder axis.',
            ),
            (
                "content",
                "(top) The initial distribution of NF-κB/Dorsal from Figure 10 varies along the cylinder's axis (y-direction of this contour plot, with the x-direction describing the circumference) in both standard deviation and amplitude by about 10%; d(x,t=0)\u2009=\u2009\u2061exp{−522(1+0.1\u2061sin(πy/ly))2(x−2/lx)2}\u2009(1+0.1\u2061sin(πy/ly)), and decays over time (time points 0, 1000, 2000, 3000, 4000 shown from left to right). (bottom) The resulting distribution of Sog (and correspondingly of BMP) becomes uniform along the cylinder axis. DOI: http://dx.doi.org/10.7554/eLife.05502.021",
            ),
            ("article_doi", "10.7554/eLife.05502"),
            ("type", "fig"),
            ("position", 21),
            ("ordinal", 17),
            ("sibling_ordinal", 13),
            ("asset", None),
        ]
    ),
    OrderedDict(
        [
            ("doi", "10.7554/eLife.05502.022"),
            ("doi_url", "https://doi.org/10.7554/eLife.05502.022"),
            ("id", "tbl2"),
            ("label", "Table 2."),
            ("full_label", "Table 2."),
            (
                "caption",
                "Range of model parameter values where a single stripe is formed",
            ),
            (
                "full_caption",
                "Range of model parameter values where a single stripe is formed",
            ),
            (
                "content",
                "Range of model parameter values where a single stripe is formed DOI: http://dx.doi.org/10.7554/eLife.05502.022 Each parameter is varied keeping the other parameters fixed at the values specified in Table 1. One exception is the parameters η0\u2009and\u2009η1, which affect pattern formation jointly through the parameter ηs¯(d)≡\u2009η0+\u2009η1d/d01+d/d0 which is set to 1.2 × 10−3 (except in the first line, where this parameter itself is varied).",
            ),
            ("article_doi", "10.7554/eLife.05502"),
            ("type", "table-wrap"),
            ("position", 22),
            ("ordinal", 2),
            ("sibling_ordinal", 1),
            ("asset", None),
        ]
    ),
    OrderedDict(
        [
            ("doi", "10.7554/eLife.05502.023"),
            ("doi_url", "https://doi.org/10.7554/eLife.05502.023"),
            ("id", "fig12"),
            ("title", "Stability of the homogeneous fixed point."),
            ("full_title", "Stability of the homogeneous fixed point."),
            ("label", "Figure 12."),
            ("full_label", "Figure 12."),
            (
                "caption",
                "This contour plot shows the largest eigenvalue w of A − Dk2 for k = 2π/lx. The thick line separates the parameters leading to a stable homogeneous fixed point (w < 0) from an instable homogeneous fixed point (w > 0). (left) w is plotted as a function of the diffusion constant of the Sog-BMP complex and the rate of sog expression at zero BMP, ηs¯. (right) The same data are plotted against log(d) using ηs¯(d)≡η0+\u2009η1d/d01+d/d0. The homogeneous fixed point becomes unstable for sufficiently large values of the diffusion constant of the complex Dc and the concentration of NF-κB/Dorsal d. The remaining parameters are as given in Table 1.",
            ),
            (
                "full_caption",
                'This contour plot shows the largest eigenvalue <italic>w</italic> of <bold>A</bold> − <bold>D</bold><italic>k</italic><sup><italic>2</italic></sup> for <italic>k</italic> = 2<italic>π</italic>/<italic>l</italic><sub><italic>x</italic></sub>. The thick line separates the parameters leading to a stable homogeneous fixed point (<italic>w</italic> < 0) from an instable homogeneous fixed point (<italic>w</italic> > 0). (left) <italic>w</italic> is plotted as a function of the diffusion constant of the Sog-BMP complex and the rate of <italic>sog</italic> expression at zero BMP, <inline-formula><mml:math id="inf17"><mml:mrow><mml:mover><mml:mrow><mml:msub><mml:mi>η</mml:mi><mml:mi>s</mml:mi></mml:msub></mml:mrow><mml:mo stretchy="true">¯</mml:mo></mml:mover></mml:mrow></mml:math></inline-formula>. (right) The same data are plotted against log(<italic>d</italic>) using <inline-formula><mml:math id="inf18"><mml:mrow><mml:mrow><mml:mover><mml:mrow><mml:msub><mml:mi>η</mml:mi><mml:mi>s</mml:mi></mml:msub></mml:mrow><mml:mo stretchy="true">¯</mml:mo></mml:mover></mml:mrow><mml:mrow><mml:mo>(</mml:mo><mml:mi>d</mml:mi><mml:mo>)</mml:mo></mml:mrow><mml:mo>≡</mml:mo><mml:mfrac><mml:mrow><mml:msub><mml:mi>η</mml:mi><mml:mn>0</mml:mn></mml:msub><mml:mo>+</mml:mo><mml:mo>\u2009</mml:mo><mml:msub><mml:mi>η</mml:mi><mml:mn>1</mml:mn></mml:msub><mml:mrow><mml:mi>d</mml:mi><mml:mo>/</mml:mo><mml:mrow><mml:msub><mml:mi>d</mml:mi><mml:mn>0</mml:mn></mml:msub></mml:mrow></mml:mrow></mml:mrow><mml:mrow><mml:mn>1</mml:mn><mml:mo>+</mml:mo><mml:mrow><mml:mi>d</mml:mi><mml:mo>/</mml:mo><mml:mrow><mml:msub><mml:mi>d</mml:mi><mml:mn>0</mml:mn></mml:msub></mml:mrow></mml:mrow></mml:mrow></mml:mfrac></mml:mrow></mml:math></inline-formula>. The homogeneous fixed point becomes unstable for sufficiently large values of the diffusion constant of the complex <italic>D</italic><sub><italic>c</italic></sub> and the concentration of NF-κB/Dorsal <italic>d</italic>. The remaining parameters are as given in <xref ref-type="table" rid="tbl1">Table 1</xref>.',
            ),
            (
                "content",
                "This contour plot shows the largest eigenvalue w of A − Dk2 for k = 2π/lx. The thick line separates the parameters leading to a stable homogeneous fixed point (w < 0) from an instable homogeneous fixed point (w > 0). (left) w is plotted as a function of the diffusion constant of the Sog-BMP complex and the rate of sog expression at zero BMP, ηs¯. (right) The same data are plotted against log(d) using ηs¯(d)≡η0+\u2009η1d/d01+d/d0. The homogeneous fixed point becomes unstable for sufficiently large values of the diffusion constant of the complex Dc and the concentration of NF-κB/Dorsal d. The remaining parameters are as given in Table 1. DOI: http://dx.doi.org/10.7554/eLife.05502.023",
            ),
            ("article_doi", "10.7554/eLife.05502"),
            ("type", "fig"),
            ("position", 23),
            ("ordinal", 18),
            ("sibling_ordinal", 14),
            ("asset", None),
        ]
    ),
    OrderedDict(
        [
            ("doi", "10.7554/eLife.05502.024"),
            ("doi_url", "https://doi.org/10.7554/eLife.05502.024"),
            ("id", "SD1-data"),
            ("label", "Supplementary file 1."),
            ("full_label", "Supplementary file 1."),
            ("caption", "PCR primers for production of ISH probes and dsRNA."),
            ("full_caption", "PCR primers for production of ISH probes and dsRNA."),
            (
                "content",
                "PCR primers for production of ISH probes and dsRNA. DOI: http://dx.doi.org/10.7554/eLife.05502.024",
            ),
            ("mimetype", "application"),
            ("mime-subtype", "docx"),
            ("article_doi", "10.7554/eLife.05502"),
            ("type", "supplementary-material"),
            ("position", 24),
            ("ordinal", 1),
            ("sibling_ordinal", 1),
            ("asset", "supp"),
        ]
    ),
    OrderedDict(
        [
            ("doi", "10.7554/eLife.05502.025"),
            ("doi_url", "https://doi.org/10.7554/eLife.05502.025"),
            ("id", "SA1"),
            ("title", "Decision letter"),
            ("full_title", "Decision letter"),
            (
                "contributors",
                [
                    {
                        "type": "editor",
                        "role": "Reviewing editor",
                        "surname": "Barkai",
                        "given-names": "Naama",
                        "affiliations": [
                            {
                                "institution": "Weizmann Institute of Science",
                                "country": "Israel",
                            }
                        ],
                    }
                ],
            ),
            (
                "content",
                "eLife posts the editorial decision letter and author response on a selection of the published articles (subject to the approval of the authors). An edited version of the letter sent to the authors after peer review is shown, indicating the substantive concerns or comments; minor concerns are not usually shown. Reviewers have the opportunity to discuss the decision before the letter is sent (see review process). Similarly, the author response typically shows only responses to the major concerns raised by the reviewers. Thank you for sending your work entitled “Toll's patterning role emerged as a polarity cue for self-regulatory BMP signaling” for consideration at eLife. Your article has been favorably evaluated by Diethard Tautz (Senior editor), a Reviewing editor, and three reviewers. Sachs et al., study DV patterning in the milkweed bug Oncopeltus fasciatus. They use RNAi methods and mathematical modeling to study interactions between the Toll and BMP signaling pathways. From their RNAi data, the authors conclude that (1) BMP signaling is active throughout the DV axis and must be repressed ventrally through expression of sog to allow ventral patterning; and (2) Toll is not required to support any cell types but is required for symmetry breaking. All reviewers agreed that this is an interesting study addressing an important question in developmental biology, namely how do DV patterning mechanisms in different animals relate and what was the ancestral system like. The authors make a convincing argument for looking at the milkweed bug. However, it was also agreed by all that more information is needed, especially in view of the recent CB paper from the PI lab on Nasonia, which already makes the point regarding the decreasing role of the Toll pathway. Several additional data are therefore essential: 1) More information on the expression patterns of the different players in the BMP pathway is essential: Where is dpp expressed? It is implied that dpp is no longer under Toll-dependent regulation in the milkweed bug (e.g. Figure 1 diagram), however no in situ data is included. The authors also suggest that multiple BMP ligands may be supporting activation of this signaling pathway. Their expression should be shown and discussed. Could they be repressed by Dorsal? 2) What is the expression pattern of Tolloid? Similar arguments to point 1. 3) The ability to trace the expression of the Zen homologue as an indicator of maximal BMP signaling in different backgrounds could be very informative. 4) More information on the pattern of the Toll gradient shape would be important. 5) Additional support for the Toll1-dpp-RNAi results should be provided. (one may worry that the Toll1 RNAi support weak activation that becomes apparent in the absence of BMP signaling; What does Toll1-dl1-dpp RNAi look like? How about Toll1-tld RNAi?). In addition, it would be interesting to directly define the shape of the Dorsal gradient (e.g. by indirect immunofluorescence if antibodies are available or could be produced in a reasonable length of time) as this shape is an important output of the modeling. In Box 1, the first diagram suggests that the height and width of the Dorsal gradient increases in time. What is the evidence to support this in the milkweed bug? In Box 1, the second diagram shows that in the middle of the “twinned” embryo, a peak of BMP signaling abuts a domain of high sog expression. How is this possible? The authors should also discuss how sog can be expressed in a small ventral domain in dl1-RNAi mutants. There must be some “polarity cue” and yet development does not proceed normally. So the levels of Dorsal are important to some degree? Previous studies in Drosophila have provided evidence that genes expressed in lateral regions (e.g. brinker) are ubiquitously expressed in dl dpp double mutants. Is sog expressed ubiquitously within dl dpp double Drosophila mutants? Reviewer 2: In the manuscript by Sachs et al., the authors present an analysis of DV patterning in the milkweed bug Oncopeltus fasciatus. They use RNAi methods and mathematical modeling to study interactions between the Toll and BMP signaling pathways. From their RNAi data, the authors conclude that (1) BMP signaling is active throughout the DV axis and must be repressed ventrally through expression of sog to allow ventral patterning; and (2) Toll is not required to support any cell types but is required for symmetry breaking. This is an interesting study addressing an important question in developmental biology, namely how do DV patterning mechanisms in different animals relate and what was the ancestral system like. The authors make a convincing argument for looking at the milkweed bug. The data are suggestive of the hypothesis, that Toll signaling is symmetry breaking, but do not demonstrate it. Alternately, rather, the data show that BMP signaling acts broadly and then is refined. Furthermore, the addition of some data and controls is necessary. Methods available in this new model system are limited, understandably. Perhaps this is why the mathematical modeling was included, because it was accessible; and yet I found the addition of modeling to explain “twinning” more confusing than helpful. In any case, the individual and joint contributions of dorsal genes, BMP ligand expression and roles, and the possibility of off-target effects for RNAi constructs should (and can) be addressed. In summary, this is a very interesting study and the results are significant. However, either additional experimental evidence must be included or the title should be revised. If the study is revised to refocus on the broad role of BMP signaling, then the novelty of the study is perhaps compromised by the authors' recent study in Nasonia (Ozuak et al., 2014). Specific comments: 1) Where is dpp expressed? It is implied that dpp is no longer under Toll-dependent regulation in the milkweed bug (e.g. Figure 1 diagram), however no in situ data is included. The authors also suggest that multiple BMP ligands may be supporting activation of this signaling pathway. Their expression should be shown and discussed. Could they be repressed by Dorsal? 2) Previous studies in Drosophila have provided evidence that genes expressed in lateral regions (e.g. brinker) are ubiquitously expressed in dl dpp double mutants. Is sog expressed ubiquitously within dl dpp double Drosophila mutants? 3) In Box 1, the first diagram suggests that the height and width of the Dorsal gradient increases in time. What is the evidence to support this in the milkweed bug? 4) In Box 1, the second diagram shows that in the middle of the “twinned” embryo, a peak of BMP signaling abuts a domain of high sog expression. How is this possible? Reviewer 3: The paper by Sachs et al. examines the roles of the Toll and BMP pathways in DV patterning of the Hemimetabolous insect Oncopelus. With the universal role of BMP DV patterning in multicellular organisms, and the restricted role of the Toll pathway in DV patterning of Holometabolous insects like Drosophila, the question was what is the relation of the Toll and BMP pathways in DV patterning of Oncopelus. They show that BMP signaling is required to repress expression of early ventral and lateral genes (twi and sog) in the dorsal region. At early embryogenesis Sog displays a low and uniform expression. The role of Toll signaling is only to break this symmetry and lead to an increase (even a moderate one) in Sog levels at the ventral side. In a double RNAi mutant for Toll and dpp, ventral fates take over the entire embryo, indicating that in this species this is the default, and the role of Toll is only to repress BMP signaling in the ventral region by elevating the level of Sog. Because of the cross regulatory interactions between dpp and Sog, this leads to a stable BMP activation pattern and expression of the cardinal genes in restricted domains. Computational analysis indicates that this regulatory circuitry is robust to fluctuations, and requires only a minimal bias by the Toll pathway. In general, the detailed dissection of developmental pathways in organisms that are removed from Drosophila, which is successfully used by the Roth lab, and especially the deviations from what we know in Drosophila, provide a fresh view not only on the evolution of these pathways, but also on their regulatory logic. This work is a case in point. Several experiments were missing and would provide a broader view of the topic: 1) What is the expression profile of dpp in Oncopelus embryos at different stages? This is important because it would provide the context to interpret the results in Sog RNAi embryos. Is the global activation of the BMP pathway a result of BMP diffusion from the dorsal region, or a reflection of a uniform expression of dpp? If dpp expression is restricted to the dorsal region, is the repression of expression in the ventral region dependent on Toll signaling, similar to the induction of Sog? 2) What is the expression pattern of Tolloid? Similar arguments to point 1. 3) What is the nuclear distribution pattern of Dorsal1 and Dorsal2 in wt embryos, and in embryos in which dpp signaling has been eliminated? I know that this analysis would require a significant work of raising antibodies, but perhaps it could be circumvented by injection of a plasmid expressing tagged or GFP-linked Dorsal1. It would be important to see the pattern of the Toll activation gradient, and to assess if it extends sufficiently into the dorsal side, to account for the proposed bias in that region in the that is relevant to the Sander experiment (Box 1). It would also be important to demonstrate that the Toll gradient is the primary symmetry-breaking event, and is not affected by the loss of the downstream BMP pathway. Several points should be clarified further in the text, without a requirement for additional experiments: Sog levels were not erased but only reduced in the Sog RNAi embryos (Figure 2K). While the residual Sog is now uniformly expressed, there still appears to be some difference between the level of pMad in the dorsal vs. ventral parts of the embryo (Figure 3C,H). This would not agree with the model, but perhaps the embryos shown are not representative, or maybe there is still some bias in the expression of Sog which resolves only to a very shallow pMad pattern because of the limited levels of Sog? The central point of the paper is the switch from a uniform distribution of Sog, to the restricted expression of Sog in the ventral and ventro-lateral domains, and the complementary pattern of BMP activation, triggered by the ventral bias of Toll signaling. The ability to convert even a small bias (as in the middle panel of Figure 8) to a bistable robust BMP pattern, clearly relies on transport of the Sog-BMP complex and its cleavage in the dorsal region by Tolloid. In this respect the logic of modulating BMP signaling is similar to what was described in Drosophila. It is not clear however whether this process is also responsible (as it is in Drosophila) for generating a graded pattern WITHIN the domain of BMP signaling. As far as I could tell, the pMad levels in embryos that are depleted for Sog were comparable to wt, suggesting that in the absence of inhibition by Sog, the levels of dpp are sufficient to elicit maximal signaling and no further concentration of the ligand is required. Also, the late patterns of pMad show sharp borders and fairly uniform expression within the dorsal region (Figure 3F). I would like to see some more discussion of this issue, regarding the question whether a graded BMP activation pattern is or is not generated within the dorsal region.",
            ),
            ("article_doi", "10.7554/eLife.05502"),
            ("type", "sub-article"),
            ("position", 25),
            ("ordinal", 1),
            ("sibling_ordinal", 1),
            ("asset", "dec"),
        ]
    ),
    OrderedDict(
        [
            ("doi", "10.7554/eLife.05502.026"),
            ("doi_url", "https://doi.org/10.7554/eLife.05502.026"),
            ("id", "SA2"),
            ("title", "Author response"),
            ("full_title", "Author response"),
            (
                "content",
                "Sachs et al., study DV patterning in the milkweed bug Oncopeltus fasciatus. They use RNAi methods and mathematical modeling to study interactions between the Toll and BMP signaling pathways. From their RNAi data, the authors conclude that (1) BMP signaling is active throughout the DV axis and must be repressed ventrally through expression of sog to allow ventral patterning; and (2) Toll is not required to support any cell types but is required for symmetry breaking. All reviewers agreed that this is an interesting study addressing an important question in developmental biology, namely how do DV patterning mechanisms in different animals relate and what was the ancestral system like. The authors make a convincing argument for looking at the milkweed bug. However, it was also agreed by all that more information is needed, especially in view of the recent CB paper from the PI lab on Nasonia, which already makes the point regarding the decreasing role of the Toll pathway. Several additional data are therefore essential: The reviewers have noted that a decreasing role of Toll signaling accompanied by an expanded function of BMP was already described in our recent CB paper on Nasonia. Indeed, we had found evidence for a diminished role of Toll signaling even in earlier work on the beetle Tribolium (van der Zee et al., 2006). To show that our new findings for Oncopeltus provide an important step in an evolutionary progression we have expanded Figure 1 and included Tribolium as well as Nasonia. We also added more material to the Introduction and Discussion to explain the difference between Nasonia and Oncopeltus. In brief: Nasonia represents a highly derived system as it is the only insect known so far which establishes the DV pattern in a bipolar manner. The BMP gradient appears to emerge from a maternal source along the dorsal midline independently from Toll and without transport through a ventrally expressed inhibitor. Sog is missing from the genome. In this respect Nasonia’s DV patterning system is more derived than that of Drosophila. Nasonia Toll on the other hand remains responsible for ventral fates providing highly refined patterning information along the ventral midline. The Toll dpp double knockdown in Nasonia lacks mesoderm, in contrast to the double knockdown in Oncopeltus. Taken together while BMP is the dominant morphogen in Nasonia both the formation of the BMP gradient and the continued requirement of Toll signaling for the mesoderm/mesectoderm formation are in strong contrast to the DV patterning system of Oncopeltus that clearly represents an ancestral state with similarities to spiders and vertebrates. 1) More information on the expression patterns of the different players in the BMP pathway is essential: Where is dpp expressed? It is implied that dpp is no longer under Toll-dependent regulation in the milkweed bug (e.g. Figure 1 diagram), however no in situ data is included. The authors also suggest that multiple BMP ligands may be supporting activation of this signaling pathway. Their expression should be shown and discussed. Could they be repressed by Dorsal? The expression of the components of the BMP system including dpp, a second BMP ligand (gbb), tolloid and twisted gastrulation (tsg) are now shown in Figure 2—figure supplement 1. All of these components are either uniformly expressed or have extremely low expression levels, so that they cannot be detected at early blastoderm stages when their activity is required for BMP gradient formation. We know that the probes work since they detect the conserved local expression in late stages. Very low levels are apparently sufficient to support patterning. A similar situation was observed in Tribolium and Nasonia where early dpp and tsg are weakly and evenly expressed at the stages when the BMP gradient forms (van der Zee et al., 2006; Fonseca et al., 2010; Özüak et al., 2014). Thus, regulatory inputs of Toll signaling on these components are alreadylacking in Tribolium and Nasonia and might have evolved only in the lineage leading to Drosophila. 2) What is the expression pattern of Tolloid? Similar arguments to point 1. See response to point 1. 3) The ability to trace the expression of the Zen homologue as an indicator of maximal BMP signaling in different backgrounds could be very informative. Low levels of Oncopeltus zen expression are found along the entire circumference of early blastoderm embryos and resolves into a complex pattern that spans the egg circumference at the differentiated blastoderm stage (Panfilio et al., 2006). This is one example of many genes dorsally expressed in Drosophila and other holometabolous insects, which we tried to use as marker genes and found that they are absent, evenly expressed, or have altered expression domains during blastoderm stages. The failure of the candidate gene approach highlights one of the difficulties connected to working with a hemimetabolous insect. Many aspects of DV patterning are apparently not conserved. In the future we plan unbiased genomic approaches (RNA-seq) combined with RNAi KD to identify new marker genes. 4) More information on the pattern of the Toll gradient shape would be important. The closest approximation of the Toll activation gradient is the nuclear Dorsal gradient since it has not been possible in insects to directly detect activated Toll receptors or the distribution of the Toll ligand Spätzle. We agree that it would be crucial to show the nuclear Dorsal gradient and have raised antibodies against Oncopeltus Dorsal1 already at the beginning of our study. However, the antibodies are only useful for western blots and have not worked for whole mount stainings. The fixation methods for early Oncopeltus blastoderm embryos are excellent for ISH, but do not reliably preserve protein epitopes. The pMAD stainings provided a lucky exception. We have also tried transient expression essays with GFP constructs. But this was not successful so far. In the future we plan to establish transgenesis and, using the genome which is close to completion, we want to perform genome editing with the CRISPR/Cas9 system. Given the lack of Dorsal staining we have added cactus in situs. This had been our proxy for Toll activity in Nasonia where we also lack anti-Dorsal antibodies. In all insects studied so far including Drosophila (Sandmann et al 2007) cactus is an early target gene of Toll signaling and this seems to be an ancestral regulatory circuitry since it has also been observed as an essential element in the innate immune system. Oncopeltus possesses several cactus paralogs. Strong knockdown of early expressed paralogs lead to a failure of normal blastoderm formation. However, weak knockdown shows mild ventralization, indicating that at least two of the paralogs are involved in DV patterning. One of them shows early ventral expression which encompasses approximately 60-70% of the egg circumference (the domain is wider than that of sog). This indicates that early Toll signaling extends into the dorsal half of the embryo, a prerequisite for explaining the Sander experiment. These considerations are now addressed in the manuscript with the additional cact data (new Figure 7). 5) Additional support for the Toll1-dpp-RNAi results should be provided. (one may worry that the Toll1 RNAi support weak activation that becomes apparent in the absence of BMP signaling; What does Toll1-dl1-dpp RNAi look like? How about Toll1-tld RNAi?). For the epistasis analysis we have chosen the two genes which give the most complete and most penetrant knockdowns: Toll1 and dpp. All other Toll signalling or BMP signalling components give more variable knockdown results (Figure 2—figure supplement 2). This applies in particular to dorsal1 as there are two dorsal genes (dl1 and dl2) which as single KD lead only to partial dorsalization. Most importantly we are sure that we are dealing with double KD embryos as we observed a phenotypic feature of the Toll KD in the background of the Toll-dpp KD: the anterior shift of twi, sim and sog domains. We have now more explicitly described the function of Toll signalling in AP patterning (Figure 6). We are confident that other double KD combinations like Toll-tld or dl1-pp could not provide clearer results. In this context it is important to note that elevated BMP levels also provide strong evidence for a fundamental difference in ventral gene regulation between Oncopeltus and the known Holometabolous insects. In Drosophila and Tribolium, twi and sog cannot be repressed by elevating BMP levels. Toll/Dorsal rigidly determines their expression domains. However, in Oncopeltus they are readily repressed by elevated BMP, indicating that their expression state is primarily dependent on the BMP levels and not on Toll/Dorsal. In addition, it would be interesting to directly define the shape of the Dorsal gradient (e.g. by indirect immunofluorescence if antibodies are available or could be produced in a reasonable length of time) as this shape is an important output of the modeling. In Box 1, the first diagram suggests that the height and width of the Dorsal gradient increases in time. What is the evidence to support this in the milkweed bug? In Box 1, the second diagram shows that in the middle of the “twinned” embryo, a peak of BMP signaling abuts a domain of high sog expression. How is this possible? See response to point 4. The authors should also discuss how sog can be expressed in a small ventral domain in dl1-RNAi mutants. There must be some “polarity cue” and yet development does not proceed normally. So the levels of Dorsal are important to some degree? Previous studies in Drosophila have provided evidence that genes expressed in lateral regions (e.g. brinker) are ubiquitously expressed in dl dpp double mutants. Is sog expressed ubiquitously within dl dpp double Drosophila mutants? In contrast to the Toll knockdown, the dl1 knockdown does not cause a complete disruption of Toll signalling (possibly due to redundancy with dl2). Despite the fact that all dl1 knockdown embryos have residual sog the majority lack twi and sim. Thus, we have to assume a threshold for sog which has to be exceeded to initiated stable patterning. Sog is not expressed in dl-dpp double mutants since its activation is strictly dependent on Dorsal like in all other insects studied so far except in Oncopeltus. The same applies for early brinker expression in Drosophila. It is only the late brinker (shortly before gastrulation) that is expressed in dl-dpp mutant embryos since at this stage dpp is required to repress brk. Reviewer 2: […] In summary, this is a very interesting study and the results are significant. However, either additional experimental evidence must be included or the title should be revised. If the study is revised to refocus on the broad role of BMP signaling, then the novelty of the study is perhaps compromised by the authors' recent study in Nasonia (Ozuak et al., 2014). Specific comments: 1) Where is dpp expressed? It is implied that dpp is no longer under Toll-dependent regulation in the milkweed bug (e.g. Figure 1 diagram), however no in situ data is included. The authors also suggest that multiple BMP ligands may be supporting activation of this signaling pathway. Their expression should be shown and discussed. Could they be repressed by Dorsal? 2) Previous studies in Drosophila have provided evidence that genes expressed in lateral regions (e.g. brinker) are ubiquitously expressed in dl dpp double mutants. Is sog expressed ubiquitously within dl dpp double Drosophila mutants? 3) In Box 1, the first diagram suggests that the height and width of the Dorsal gradient increases in time. What is the evidence to support this in the milkweed bug? In Box 1 we assumed that Dorsal (blue) decreases in time. In Tribolium the upregulation of cactus leads to decreasing nuclear Dorsal concentrations and a disappearance of the gradient. The same is likely to be the case in Nasonia. If cactus has a similar function in Oncopeltus it also would attenuate Toll signalling (see point 4). For the purpose of modelling we want to show in Box 1 that the BMP system is self-organizing and after initiation through Dorsal (by activating sog) becomes independent from Dorsal. 4) In Box 1, the second diagram shows that in the middle of the “twinned” embryo, a peak of BMP signaling abuts a domain of high sog expression. How is this possible? We are now explaining the Sander experiment in more detail. Sander used a guillotine to fragment the embryos in two separate halves along the lateral midline. Thus, there is no flow of signalling proteins between the dorsal and ventral fragments. Therefore, high BMP can be exposed to high Sog along the lateral plane bisection. Reviewer 3: […] In general, the detailed dissection of developmental pathways in organisms that are removed from Drosophila, which is successfully used by the Roth lab, and especially the deviations from what we know in Drosophila, provide a fresh view not only on the evolution of these pathways, but also on their regulatory logic. This work is a case in point. Several experiments were missing and would provide a broader view of the topic: 1) What is the expression profile of dpp in Oncopelus embryos at different stages? This is important because it would provide the context to interpret the results in Sog RNAi embryos. Is the global activation of the BMP pathway a result of BMP diffusion from the dorsal region, or a reflection of a uniform expression of dpp? If dpp expression is restricted to the dorsal region, is the repression of expression in the ventral region dependent on Toll signaling, similar to the induction of Sog? 2) What is the expression pattern of Tolloid? Similar arguments to point 1. 3) What is the nuclear distribution pattern of Dorsal1 and Dorsal2 in wt embryos, and in embryos in which dpp signaling has been eliminated? I know that this analysis would require a significant work of raising antibodies, but perhaps it could be circumvented by injection of a plasmid expressing tagged or GFP-linked Dorsal1. It would be important to see the pattern of the Toll activation gradient, and to assess if it extends sufficiently into the dorsal side, to account for the proposed bias in that region in the that is relevant to the Sander experiment (Box 1). It would also be important to demonstrate that the Toll gradient is the primary symmetry-breaking event, and is not affected by the loss of the downstream BMP pathway. Several points should be clarified further in the text, without a requirement for additional experiments: Sog levels were not erased but only reduced in the Sog RNAi embryos (Figure 2K). While the residual Sog is now uniformly expressed, there still appears to be some difference between the level of pMad in the dorsal vs. ventral parts of the embryo (Figure 3C,H). Figure 2K shows the embryo from the ventral side. Residual sog expression is present only ventrally and correlates with a weak pMAD gradient in sog RNAi embryos. Like the residual sog expression in dl1 RNAi embryos this is not sufficient to initiate stable patterning since 100% of the sog RNAi embryos lack twi expression. Apparently the system shifts only into a stable patterning regime if a certain threshold for pMAD asymmetry is exceeded. This would not agree with the model, but perhaps the embryos shown are not representative, or maybe there is still some bias in the expression of Sog which resolves only to a very shallow pMad pattern because of the limited levels of Sog? The central point of the paper is the switch from a uniform distribution of Sog, to the restricted expression of Sog in the ventral and ventro-lateral domains, and the complementary pattern of BMP activation, triggered by the ventral bias of Toll signaling. The ability to convert even a small bias (as in the middle panel of Figure 8) to a bistable robust BMP pattern, clearly relies on transport of the Sog-BMP complex and its cleavage in the dorsal region by Tolloid. In this respect the logic of modulating BMP signaling is similar to what was described in Drosophila. It is not clear however whether this process is also responsible (as it is in Drosophila) for generating a graded pattern WITHIN the domain of BMP signaling. As far as I could tell, the pMad levels in embryos that are depleted for Sog were comparable to wt, suggesting that in the absence of inhibition by Sog, the levels of dpp are sufficient to elicit maximal signaling and no further concentration of the ligand is required. Also, the late patterns of pMad show sharp borders and fairly uniform expression within the dorsal region (Figure 3F). I would like to see some more discussion of this issue, regarding the question whether a graded BMP activation pattern is or is not generated within the dorsal region. We agree that there is no detectable BMP gradient within the early BMP domain and that the sog as well as the tsg knockdowns produce uniform high levels of BMP signalling similar to those found in wt within the dorsal 30%. We are now commenting on these observations in the Discussion section. In Oncopeltus, a more fine grained pattern of BMP signalling with a sharp dorsal peak is established later during gastrulation and requires the function of the second BMP ligand Gbb as well as the local up-regulation of dpp transcription. We believe that during blastoderm stages the DV fate map of Oncopeltus does not reach (most notably at the dorsal side) the high spatial precision known from (the long-germ insects) Drosophila and Nasonia. This precision is only established at later stages. The situation is similar to (the short germ insect) Tribolium (Fonseca et al., 2010). We are currently in the process of preparing a manuscript, which addresses these later events.",
            ),
            ("article_doi", "10.7554/eLife.05502"),
            ("type", "sub-article"),
            ("position", 26),
            ("ordinal", 2),
            ("sibling_ordinal", 2),
            ("asset", "resp"),
        ]
    ),
]
