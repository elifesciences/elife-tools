from collections import OrderedDict

expected = OrderedDict(
    [
        ("type", "code"),
        (
            "code",
            u'<MotifGraft name="motif_grafting"\n      context_structure="%%context%%"\n      motif_structure="truncatedBH3.pdb"\n      RMSD_tolerance="3.0"\n      NC_points_RMSD_tolerance="2.0"\n      clash_score_cutoff="0"\n      clash_test_residue="ALA"\n      hotspots="9:12:13:14:16:17"\n      combinatory_fragment_size_delta="0:0"\n      max_fragment_replacement_size_delta="0:0"\n      full_motif_bb_alignment="1"\n      allow_independent_alignment_per_fragment="0"\n      graft_only_hotspots_by_replacement="0"\n      only_allow_if_N_point_match_aa_identity="0"\n      only_allow_if_C_point_match_aa_identity="0"\n      revert_graft_to_native_sequence="1"\n      allow_repeat_same_graft_output="1"/>',
        ),
    ]
)
