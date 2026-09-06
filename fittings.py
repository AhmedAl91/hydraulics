K_VALUES = {

    # Entry losses
    "pipe_entry_sharp_edged": 0.50,
    "pipe_entry_re_entrant": 0.80,
    "pipe_entry_slightly_rounded": 0.25,
    "pipe_entry_bellmouth": 0.05,
    "pipe_entry_foot_valve_and_strainer": 2.50,

    # Elbows
    "pipe_elbow_22_5_degrees": 0.20,
    "pipe_elbow_45_degrees": 0.40,
    "pipe_elbow_90_degrees": 1.00,

    # Bends - short: 1D, long: 2 to 7D, sweep: 8 to 50D
    "pipe_bend_22_5_degrees_short": 0.15,
    "pipe_bend_45_degrees_short": 0.30,
    "pipe_bend_90_degrees_short": 0.75,

    "pipe_bend_22_5_degrees_long": 0.10,
    "pipe_bend_45_degrees_long": 0.20,
    "pipe_bend_90_degrees_long": 0.40,

    "pipe_bend_22_5_degrees_sweep": 0.05,
    "pipe_bend_45_degrees_sweep": 0.10,
    "pipe_bend_90_degrees_sweep": 0.20,

    # Tees
    "pipe_tee_in_line": 0.35,
    "pipe_tee_branch_radiused": 0.80,
    "pipe_tee_branch_sharp": 1.20,

    # Angled branches
    "pipe_angle_in_line": 0.35,
    "pipe_angle_branch_30_degrees": 0.40,
    "pipe_angle_branch_45_degrees": 0.60,
    "pipe_tee_branch_90_degrees": 0.80,

    # Sudden enlargements
    "enlargement_4_5": 0.15,
    "enlargement_3_4": 0.20,
    "enlargement_2_3": 0.35,
    "enlargement_1_2": 0.60,
    "enlargement_1_3": 0.80,
    "enlargement_1_5": 1.00,

    # Sudden contractions
    "contraction_5_4": 0.15,
    "contraction_4_3": 0.20,
    "contraction_3_2": 0.30,
    "contraction_2_1": 0.35,
    "contraction_3_1": 0.45,
    "contraction_5_1": 0.50,

    # B.S. tapers
    "taper_down": 0.00,
    "taper_up_4_5": 0.03,
    "taper_up_3_4": 0.04,
    "taper_up_1_2": 0.12,

    # Valves
    "gate_valve_full_open": 0.12,
    "gate_valve_quarter_closed": 1.00,
    "gate_valve_half_closed": 6.00,
    "gate_valve_three_quarters_closed": 24.00,
    "globe_valve_full_open": 10.00,
    "right_angled_valve_full_open": 5.00,
    "butterfly_valve_full_open": 0.30,

    # Other valves
    "non_return_valve": 2.00,
    "pressure_reducing_valve": 10.00,

    # Exit losses
    "pipe_exit_sudden_enlargement": 1.00,
    "pipe_exit_bellmouth_outlet": 0.20,
    "flap_valve": 2.00,

    # Manhole losses
    "pipe_entry_into_manhole": 0.50,  # Taken from Crane for 0 R/D
    "pipe_exit_into_manhole": 1.00,   # Taken from Crane
}