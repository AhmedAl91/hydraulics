K_VALUES = {
    
    # Entry losses
    "pipe_entry_sharp_edged": {
        "lower": 0.50,
        "upper": 0.50,
    },
    "pipe_entry_re_entrant": {
        "lower": 0.80,
        "upper": 0.80,
    },
    "pipe_entry_slightly_rounded": {
        "lower": 0.25,
        "upper": 0.25,
    },
    "pipe_entry_bellmouth": {
        "lower": 0.05,
        "upper": 0.05,
    },
    "pipe_entry_foot_valve_and_strainer": {
        "lower": 2.5,
        "upper": 2.5,
    },
    # Elbows
    "pipe_elbow_22_5_degrees": {
        "lower": 0.20,
        "upper": 0.20,
    },
    "pipe_elbow_45_degrees": {
        "lower": 0.40,
        "upper": 0.40,
    },
    "pipe_elbow_90_degrees": {
        "lower": 1.00,
        "upper": 1.00,
    },
    # Bends - short : 1D, long: 2 to 7D, sweep: 8 to 50D
    "pipe_bend_22_5_degrees_short": {
        "lower": 0.15,
        "upper": 0.15,
    },
    "pipe_bend_45_degrees_short": {
        "lower": 0.30,
        "upper": 0.30,
    },
    "pipe_bend_90_degrees_short": {
        "lower": 0.75,
        "upper": 0.75,
    },
    "pipe_bend_22_5_degrees_long": {
        "lower": 0.10,
        "upper": 0.10,
    },
    "pipe_bend_45_degrees_long": {
        "lower": 0.20,
        "upper": 0.20,
    },
    "pipe_bend_90_degrees_long": {
        "lower": 0.40,
        "upper": 0.40,
    },
    "pipe_bend_22_5_degrees_sweep": {
        "lower": 0.05,
        "upper": 0.05,
    },
    "pipe_bend_45_degrees_sweep": {
        "lower": 0.10,
        "upper": 0.10,
    },
    "pipe_bend_90_degrees_sweep": {
        "lower": 0.20,
        "upper": 0.20,
    },
    # Tees
    "pipe_tee_in_line": {
        "lower": 0.35,
        "upper": 0.35,
    },
    "pipe_tee_branch_radiused": {
        "lower": 0.8,
        "upper": 0.8,
    },
    "pipe_tee_branch_sharp": {
        "lower": 1.20,
        "upper": 1.20,
    },
    # Angled branches
    "pipe_angle_in_line": {
        "lower": 0.35,
        "upper": 0.35,
    },
    "pipe_angle_branch_30_degrees": {
        "lower": 0.40,
        "upper": 0.40,
    },
    "pipe_angle_branch_45_degrees": {
        "lower": 0.60,
        "upper": 0.60,
    },
    "pipe_tee_branch_90_degrees": {
        "lower": 0.80,
        "upper": 0.80,
    },
    # Sudden enlargements
    "enlargement_4_5": {
        "lower": 0.15,
        "upper": 0.15,
    },
    "enlargement_3_4": {
        "lower": 0.20,
        "upper": 0.20,
    },
    "enlargement_2_3": {
        "lower": 0.35,
        "upper": 0.35,
    },
    "enlargement_1_2": {
        "lower": 0.60,
        "upper": 0.60,
    },
    "enlargement_1_3": {
        "lower": 0.80,
        "upper": 0.80,
    },
    "enlargement_1_5": {
        "lower": 1.00,
        "upper": 1.00,
    },
    # Sudden contractions
    "contraction_5_4": {
        "lower": 0.15,
        "upper": 0.15,
    },
    "contraction_4_3": {
        "lower": 0.20,
        "upper": 0.20,
    },
    "contraction_3_2": {
        "lower": 0.30,
        "upper": 0.30,
    },
    "contraction_2_1": {
        "lower": 0.35,
        "upper": 0.35,
    },
    "contraction_3_1": {
        "lower": 0.45,
        "upper": 0.45,
    },
    "contraction_5_1": {
        "lower": 0.50,
        "upper": 0.50,
    },
    # B.S. tapers
    "taper_down": {
        "lower": 0.00,
        "upper": 0.00,
    },
    "taper_up_4_5": {
        "lower": 0.03,
        "upper": 0.03,
    },
    "taper_up_3_4": {
        "lower": 0.04,
        "upper": 0.04,
    },
    "taper_up_1_2": {
        "lower": 0.12,
        "upper": 0.12,
    },
    # Valves
    "gate_valve_full_open": {
        "lower": 0.12,
        "upper": 0.12,
    },
    "gate_valve_quarter_closed": {
        "lower": 1.00,
        "upper": 1.00,
    },
    "gate_valve_half_closed": {
        "lower": 6.00,
        "upper": 6.00,
    },
    "gate_valve_three_quarters_closed": {
        "lower": 24.00,
        "upper": 24.00,
    },
    "globe_valve_full_open": {
        "lower": 10.00,
        "upper": 10.00,
    },
    "right_angled_valve_full_open": {
        "lower": 5.00,
        "upper": 5.00,
    },
    "butterfly_valve_full_open": {
        "lower": 0.30,
        "upper": 0.30,
    },
    # Other valves
    "non_return_valve": {
        "lower": 2.00,
        "upper": 2.00,
    },
    "pressure_reducing_valve": {
        "lower": 10.00,
        "upper": 10.00,
    },
    # Exit losses
    "pipe_exit_sudden_enlargement": {
        "lower": 1.00,
        "upper": 1.00,
    },
    "pipe_exit_bellmouth_outlet": {
        "lower": 0.20,
        "upper": 0.20,
    },
    "flap_valve": {
        "lower": 2.00,
        "upper": 2.00,
    },
    # Manhole losses
    "pipe_entry_into_manhole": {    # Taken from Crane for 0 R/D
        "lower": 0.50,
        "upper": 0.50,
    },
    "pipe_exit_into_manhole": { # Taken from Crane
        "lower": 1.00,
        "upper": 1.00,
    },

}
