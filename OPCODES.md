# Op-Code Legend

**Generated file — do not hand-edit.** Regenerate with `python tools/gen_opcode_legend.py` (verify freshness with `--check`).

The scratchpad vocabulary belongs to the model and evolves organically: generators may introduce new op-codes freely, and this legend is *descriptive*, not prescriptive. Steps are pipe-delimited strings (`CODE|field|field|...`, at most 4 payload fields) built with `helpers.step()`; the final step of every problem is `Z|<final_answer>`.

1782 distinct op-codes observed.

| Code | Payload fields | Example | Used by |
|---|---|---|---|
| `A` | 2, 3 | `A\|46\|46\|92` | ac_circuit_generator.py, activation_generator.py, adam_step_generator.py, algorithm_trace_generator.py, angle_defect_generator.py, angle_measure_generator.py, annuity_generator.py, arithmetic_coding_generator.py, arithmetic_sequence_generator.py, attention_generator.py, backprop_generator.py, base_conversion_generator.py, bayesian_update_generator.py, binomial_probability_generator.py, bisection_generator.py, bond_pricing_generator.py, branching_ratio_generator.py, calendar_arithmetic_generator.py, calorimetry_generator.py, cantor_pairing_generator.py, cardinal_arithmetic_generator.py, casimir_generator.py, cayley_table_generator.py, channel_capacity_generator.py, chi_square_generator.py, circle_equation_generator.py, classifier_metrics_generator.py, collision_generator.py, commutator_generator.py, complement_probability_generator.py, complex_division_generator.py, complex_locus_generator.py, complex_number_ops_generator.py, composite_arithmetic_generator.py, conditional_probability_generator.py, confidence_interval_generator.py, conic_standard_form_generator.py, continued_fraction_generator.py, contour_integral_generator.py, convolution_generator.py, coset_generator.py, countability_bijection_generator.py, counterexample_search_generator.py, counting_classics_generator.py, crt_generator.py, curve_analysis_generator.py, cyclic_group_generator.py, de_moivre_generator.py, dedekind_cut_generator.py, definite_integral_generator.py, density_matrix_generator.py, derangement_generator.py, derivative_limit_def_generator.py, determinant_generator.py, dft_generator.py, dijkstra_generator.py, distance_formula_generator.py, doppler_generator.py, dot_product_generator.py, dp_table_generator.py, einstein_summation_generator.py, electrostatics_generator.py, ellipse_features_generator.py, embedding_similarity_generator.py, energy_conservation_generator.py, entropy_change_generator.py, entropy_generator.py, entropy_rate_markov_generator.py, equivalence_relation_generator.py, euler_characteristic_generator.py, euler_formula_generator.py, euler_method_generator.py, evaluate_expression_generator.py, expected_value_generator.py, exponential_model_generator.py, extended_euclid_generator.py, feature_map_generator.py, fill_in_step_generator.py, finance_generator.py, finite_field_generator.py, five_number_summary_generator.py, fixed_point_generator.py, flops_memory_generator.py, four_vector_generator.py, fractal_iteration_generator.py, fraction_op_generator.py, frequency_table_generator.py, function_composition_generator.py, function_evaluation_generator.py, function_inner_product_generator.py, function_operations_generator.py, function_table_generator.py, game_theory_generator.py, gaussian_curvature_generator.py, generating_function_generator.py, geometric_mean_generator.py, geometry_area_perimeter_generator.py, gradient_descent_generator.py, gradient_step_generator.py, graph_counting_generator.py, graph_interpret_generator.py, grassmann_generator.py, great_circle_generator.py, hamiltonian_generator.py, heat_engine_generator.py, hermitian_check_generator.py, horner_evaluation_generator.py, huffman_coding_generator.py, hyperbola_features_generator.py, hyperbolic_distance_generator.py, hyperbolic_function_generator.py, hypercube_counting_generator.py, inclusion_exclusion_generator.py, index_gymnastics_generator.py, information_gain_generator.py, integers_as_pairs_generator.py, integrating_factor_generator.py, interpolation_generator.py, invariant_mass_generator.py, joint_distribution_generator.py, kernel_evaluation_generator.py, kernel_perceptron_generator.py, kernel_ridge_generator.py, kl_divergence_generator.py, kmeans_step_generator.py, knn_generator.py, kraft_inequality_generator.py, ladder_operator_generator.py, lagrangian_generator.py, laplace_ivp_generator.py, layer_norm_generator.py, legendre_construction_generator.py, lhopital_generator.py, limit_evaluation_generator.py, linear_approx_generator.py, low_rank_approx_generator.py, lp_corner_generator.py, lr_schedule_generator.py, manual_square_root_generator.py, markov_chain_generator.py, matrix_calculus_generator.py, matrix_group_check_generator.py, matrix_norm_generator.py, matrix_ops_generator.py, mean_value_theorem_generator.py, mgf_generator.py, midpoint_generator.py, minkowski_interval_generator.py, mixed_number_operation_generator.py, mobius_transform_generator.py, modular_arithmetic_generator.py, mst_generator.py, mutual_information_generator.py, naive_bayes_generator.py, named_distribution_generator.py, nets_surface_area_generator.py, newtons_laws_generator.py, npv_irr_generator.py, operation_properties_generator.py, or_formula_generator.py, order_of_operations_generator.py, order_statistics_generator.py, ordinal_arithmetic_generator.py, parabola_features_generator.py, param_count_generator.py, partition_function_generator.py, pascal_triangle_generator.py, pca_generator.py, percent_word_problem_generator.py, perceptron_generator.py, permutation_group_generator.py, piecewise_evaluation_generator.py, polar_parametric_generator.py, polygon_perimeter_generator.py, polynomial_zeros_generator.py, portfolio_generator.py, probability_addition_rule_generator.py, pythag_hyp_generator.py, quantization_generator.py, quark_composition_generator.py, quaternion_generator.py, radical_add_sub_generator.py, radical_multiply_generator.py, rational_expr_add_sub_generator.py, rationals_as_pairs_generator.py, recurrence_generator.py, recursive_definition_unfold_generator.py, recursive_explicit_generator.py, reed_solomon_generator.py, regression_generator.py, relativistic_energy_generator.py, remainder_factor_theorem_generator.py, riemann_sum_generator.py, riemann_tensor_generator.py, rotational_dynamics_generator.py, round_solids_generator.py, runge_kutta_generator.py, running_coupling_generator.py, rv_transform_generator.py, segment_partition_generator.py, separable_pde_generator.py, set_counting_generator.py, shm_generator.py, sigma_notation_generator.py, simple_stats_generator.py, simplex_generator.py, softmax_gradient_generator.py, solution_chem_generator.py, spherical_excess_generator.py, spherical_triangle_generator.py, spin_half_generator.py, standard_deviation_generator.py, stars_and_bars_generator.py, statics_generator.py, stereographic_generator.py, svm_margin_generator.py, synthetic_division_generator.py, tangent_line_generator.py, taxicab_geometry_generator.py, taylor_series_generator.py, temperature_conversion_generator.py, tip_bill_split_generator.py, transfer_function_generator.py, transformation_generator.py, transportation_generator.py, triangle_solve_generator.py, trig_identity_eval_generator.py, trig_six_functions_generator.py, two_sample_test_generator.py, undetermined_coeff_generator.py, variation_parameters_generator.py, vector_ops_generator.py, venn_region_count_generator.py, von_neumann_entropy_generator.py, wavefunction_generator.py, young_tableaux_generator.py, z_score_generator.py |
| `ABS` | 2 | `ABS\|5/12\|5/12` | fixed_point_generator.py, matrix_norm_generator.py, rv_transform_generator.py |
| `ABSORB_EQ` | 2 | `ABSORB_EQ\|u0=p0A+p00*u0+p01*u1\|u1=p1A+p10*u0+p11*u1` | markov_chain_generator.py |
| `ABS_CASE` | 2 | `ABS_CASE\|Case 1\|x - 8 = 4` | absolute_value_equation_generator.py |
| `ABS_CHECK` | 2 | `ABS_CHECK\|-6 < 0\|Absolute value cannot be negative` | absolute_value_equation_generator.py |
| `ABS_ERROR` | 2 | `ABS_ERROR\|1\|1/50` | quantization_generator.py |
| `ABS_INEQ_CHECK` | 2 | `ABS_INEQ_CHECK\|-5 < 0\|Absolute value cannot be negative` | absolute_value_inequality_generator.py |
| `ABS_INEQ_PART` | 2 | `ABS_INEQ_PART\|Part 1\|4x + 6 > 6 -> x > 0` | absolute_value_inequality_generator.py |
| `ABS_INEQ_SETUP` | 1 | `ABS_INEQ_SETUP\|abs(4x + 6) > 6` | absolute_value_inequality_generator.py |
| `ABS_INEQ_SPECIAL` | 2 | `ABS_INEQ_SPECIAL\|c = 0\|Check logic for >` | absolute_value_inequality_generator.py |
| `ABS_INEQ_SPLIT` | 2 | `ABS_INEQ_SPLIT\|OR case\|4x + 6 > 6 or 4x + 6 < -6` | absolute_value_inequality_generator.py |
| `ABS_SETUP` | 1 | `ABS_SETUP\|abs(x + 8) = -6` | absolute_value_equation_generator.py |
| `ABS_SPLIT` | 2, 3 | `ABS_SPLIT\|Two cases\|x - 8 = 4\|x - 8 = -4` | absolute_value_equation_generator.py |
| `ABS_VAL` | 2 | `ABS_VAL\|10\|10` | taxicab_geometry_generator.py |
| `AB_ADD` | 3 | `AB_ADD\|+4000\|5230\|9230` | abacus_addition_generator.py |
| `AB_SET` | 1 | `AB_SET\|5230` | abacus_addition_generator.py |
| `ACCEPT` | 1, 2 | `ACCEPT\|x = 2` | conditional_forms_generator.py, counterexample_search_generator.py, factor_trinomial_generator.py, knights_knaves_generator.py, log_conversion_generator.py, log_equation_generator.py, optimization_generator.py, polynomial_inequality_generator.py, radical_equation_generator.py, rational_equation_generator.py, rational_root_generator.py, set_builder_roster_generator.py, structure_isomorphism_generator.py |
| `ACT_DERIV` | 3 | `ACT_DERIV\|gelu\|0\|1/2` | activation_generator.py |
| `ACT_SETUP` | 3 | `ACT_SETUP\|activation=gelu\|x=4\|w1=-3,b1=12,w2=1,b2=3` | activation_generator.py |
| `ACT_VALUE` | 3 | `ACT_VALUE\|gelu\|0\|0` | activation_generator.py |
| `AC_COMPLEX` | 3 | `AC_COMPLEX\|Z\|24\|0j` | ac_circuit_generator.py |
| `AC_FORMULA` | 1 | `AC_FORMULA\|omega0^2=1/(L*C)` | ac_circuit_generator.py |
| `AC_PRODUCT` | 2 | `AC_PRODUCT\|4 × 9\|36` | factor_trinomial_generator.py |
| `AC_SETUP` | 3 | `AC_SETUP\|resonance\|R=24, L=12\|C=1/1452` | ac_circuit_generator.py |
| `ADAM_SETUP` | 3 | `ADAM_SETUP\|theta=2,g=-9\|beta1=9/10,beta2=99/100\|lr=1/20,epsilon=0` | adam_step_generator.py |
| `ADAM_UPDATE` | 2 | `ADAM_UPDATE\|theta_new\|41/20` | adam_step_generator.py |
| `ADD_COL` | 3 | `ADD_COL\|col_1\|0+0+0\|->0 (carry 0)` | multi_digit_addition_generator.py |
| `ADD_FORMULA` | 1 | `ADD_FORMULA\|P(A ∩ B) = P(A) + P(B) - P(A ∪ B)` | probability_addition_rule_generator.py |
| `ADD_PARTIALS` | 2 | `ADD_PARTIALS\|410370 + 3419750 + 61555500 + 68395000\|133780620` | decimal_mult_generator.py, multi_digit_multiplication_generator.py |
| `ADD_SETUP` | 2 | `ADD_SETUP\|P(A) = 7/12, P(B) = 7/12, P(A ∪ B) = 7/12\|P(A ∩ B)` | probability_addition_rule_generator.py |
| `ADJOINT` | 1 | `ADJOINT\|A^dagger=[[-19,6],[6,-19]]` | hermitian_check_generator.py |
| `ADJ_LIST` | 2 | `ADJ_LIST\|A\|B, C, D` | euler_circuit_generator.py, graph_traversal_generator.py |
| `ALG_SETUP` | 3 | `ALG_SETUP\|merge sort\|merges 4\|values 23, 33, 12, 21, 6` | algorithm_trace_generator.py |
| `ALIGN_NUM` | 2 | `ALIGN_NUM\|046.36\|177.07` | number_comparison_generator.py |
| `ALPHA` | 2 | `ALPHA\|line 1\|2: (n ∧ o) ∨ ¬n; 3: ¬n` | kernel_ridge_generator.py, semantic_tableau_generator.py |
| `ALPHA_RENAME` | 2 | `ALPHA_RENAME\|lambda f. e\|lambda z. e` | lambda_reduction_generator.py |
| `AMORT_ROW` | 3 | `AMORT_ROW\|1\|interest=$15060.00\|principal=$5165.00,balance=$70135.00` | annuity_generator.py |
| `AMPLITUDE` | 2 | `AMPLITUDE\|abs(3)\|3` | sinusoid_features_generator.py |
| `ANALOGY_SETUP` | 3 | `ANALOGY_SETUP\|man=(-4,1)\|woman=(-6,1)\|king=(-4,-2)` | embedding_similarity_generator.py |
| `ANALOGY_VECTOR` | 2 | `ANALOGY_VECTOR\|king-man+woman\|(-6,-2)` | embedding_similarity_generator.py |
| `ANGLE` | 2 | `ANGLE\|theta\|2pi/3` | positional_encoding_generator.py |
| `ANGLE_DEFECT_SETUP` | 2 | `ANGLE_DEFECT_SETUP\|R=17\|angles=60,30,30` | angle_defect_generator.py |
| `ANGLE_EVAL` | 2 | `ANGLE_EVAL\|theta=0..2*pi\|2*pi` | triple_integral_generator.py |
| `ANGLE_FORMULA` | 1 | `ANGLE_FORMULA\|add or subtract 360° until 0° ≤ θ < 360°` | angle_measure_generator.py |
| `ANGLE_RELATION` | 1 | `ANGLE_RELATION\|8x - 14 = 90` | angle_relationships_generator.py |
| `ANGLE_SETUP` | 2 | `ANGLE_SETUP\|complementary\|(4x + 11)° + (4x - 25)° = 90°` | angle_relationships_generator.py |
| `ANGLE_SOLVE` | 2 | `ANGLE_SOLVE\|8x = 104\|x = 13` | angle_relationships_generator.py |
| `ANGLE_WRAP` | 2 | `ANGLE_WRAP\|259 deg\|-101 deg` | complex_log_generator.py |
| `ANNUITY_FORMULA` | 1 | `ANNUITY_FORMULA\|PV = PMT/r` | annuity_generator.py |
| `ANNUITY_SETUP` | 2, 3 | `ANNUITY_SETUP\|perpetuity present value\|PMT=3609,r=18%` | annuity_generator.py |
| `ANTICHAIN` | 2 | `ANTICHAIN\|{13, 29, 36}\|size 3` | partial_order_generator.py |
| `ANTICOMM_ENTRY` | 3 | `ANTICOMM_ENTRY\|(1,1)\|0 + 0\|0` | pauli_algebra_generator.py |
| `ANTIDERIV` | 2 | `ANTIDERIV\|-15e^(3x)\|-5e^(3x)` | antiderivative_generator.py, arc_length_generator.py, area_between_curves_generator.py, definite_integral_generator.py, improper_integral_generator.py, integrating_factor_generator.py, integration_by_parts_generator.py, ode_substitution_generator.py, parametric_calculus_generator.py, partial_fractions_generator.py, separable_ode_generator.py, solid_revolution_generator.py, u_substitution_generator.py, variation_parameters_generator.py |
| `ANTIDERIVATIVE` | 1 | `ANTIDERIVATIVE\|-A*cos(nx)/n` | fourier_series_generator.py |
| `ANTISYM_CHECK` | 3 | `ANTISYM_CHECK\|(1, 2)\|reverse (2, 1)\|violation` | relation_check_generator.py |
| `APPLY` | 3 | `APPLY\|∧I\|1,2\|m ∧ a` | natural_deduction_generator.py |
| `APPLY_GATE` | 3 | `APPLY_GATE\|Z\|e^(i103π/114)·ket1\|-·e^(i103π/114)·ket1` | quantum_gate_generator.py |
| `APPLY_OPERATOR` | 2 | `APPLY_OPERATOR\|L[A]\|12A = -24` | commutator_generator.py, undetermined_coeff_generator.py |
| `APPLY_PAULI` | 2 | `APPLY_PAULI\|sigma_z psi\|[56/65,33/65]` | spin_half_generator.py |
| `APPLY_SUBST` | 1 | *(not observed in sampling)* | unification_generator.py |
| `APPROX` | 2 | `APPROX\|lora/full\|1053/27376` | param_count_generator.py |
| `APPROX_ENTRY` | 2 | `APPROX_ENTRY\|(1,1)\|15` | low_rank_approx_generator.py |
| `APPROX_SETUP` | 2 | `APPROX_SETUP\|estimate (3.05)^3\|linearize f(x) = x^3 at a = 3` | linear_approx_generator.py |
| `ARCCOS` | 2 | `ARCCOS\|cos(c)=1/2\|c=pi/3` | great_circle_generator.py |
| `ARCLEN_FORMULA` | 1 | `ARCLEN_FORMULA\|L = ∫ √((dx/dt)^2 + (dy/dt)^2) dt` | arc_length_generator.py, parametric_calculus_generator.py |
| `ARC_FORMULA` | 1 | `ARC_FORMULA\|L = rθ` | arc_sector_generator.py |
| `ARC_LENGTH` | 3 | `ARC_LENGTH\|int_0^T speed dt\|25*12\|300` | curve_geometry_generator.py |
| `ARC_SETUP` | 2 | `ARC_SETUP\|circle r = 4, central angle 40°\|sector area` | arc_sector_generator.py |
| `AREA` | 1 | `AREA\|66` | geometry_area_perimeter_generator.py |
| `AREA_INT` | 3 | `AREA_INT\|A = int y dx\|5*4^2/2\|40` | centroid_generator.py |
| `AREA_INTEGRAL` | 2 | `AREA_INTEGRAL\|sqrt(EG-F^2)=R\|area = R*theta*h` | fundamental_form_generator.py |
| `AREA_SCALE` | 3 | `AREA_SCALE\|uv rectangle area\|9*9\|81` | jacobian_generator.py |
| `AREA_SETUP` | 2 | `AREA_SETUP\|y = x^2 - 20x + 10 and y = -x^2 - 2x - 6\|area between the curves` | area_between_curves_generator.py |
| `ARGUMENT` | 2 | `ARGUMENT\|(10,-10)\|315 deg` | complex_log_generator.py, euler_formula_generator.py |
| `ARG_SETUP` | 2 | `ARG_SETUP\|((r ∧ q) ∨ (s ∧ q)) → ((p ∧ q) ∨ q); ¬((r ∧ q) ∨ (s ∧ q))\|¬((p ∧ q) ∨ q)` | argument_form_generator.py |
| `ARITH_INTERVAL` | 1 | `ARITH_INTERVAL\|[1/2,3/4)` | arithmetic_coding_generator.py |
| `ARITH_SETUP` | 2 | `ARITH_SETUP\|A=1/4, B=1/4, C=1/4, D=1/4\|message=CBAB` | arithmetic_coding_generator.py |
| `ARITH_SYMBOL` | 2 | `ARITH_SYMBOL\|C\|cum=[1/2,3/4)` | arithmetic_coding_generator.py |
| `ARRAY_STATE` | 2 | `ARRAY_STATE\|pass 1\|4, 17, 31, 13, 25` | algorithm_trace_generator.py |
| `ASSIGN` | 2 | `ASSIGN\|P1\|C1` | kmeans_step_generator.py |
| `ASSUME` | 1 | `ASSUME\|assume √5 = g/v in lowest terms` | direct_proof_algebra_generator.py, induction_verify_generator.py |
| `ASYMPTOTE` | 1 | `ASYMPTOTE\|y = -3 ± (3/4)(x - 6)` | hyperbola_features_generator.py |
| `ATA` | 2 | `ATA\|A^T A\|[[11024, 6400], [6400, 11024]]` | svd_generator.py |
| `ATOM_CHECK` | 3 | `ATOM_CHECK\|C\|left=1\|right=1` | stoichiometry_generator.py |
| `ATTN_OUTPUT` | 2 | `ATTN_OUTPUT\|1\|[[5/2,-5/2]]` | attention_generator.py |
| `ATTN_SCORE` | 2 | `ATTN_SCORE\|1,1\|0` | attention_generator.py |
| `ATTN_SETUP` | 1, 3 | `ATTN_SETUP\|tokens=2,d=2\|Q=[[0,0], [0,0]]\|K=[[0,0], [0,0]]` | attention_generator.py |
| `ATTR_CHECK` | 3 | `ATTR_CHECK\|4\|A: odd\|no` | attribute_sorting_generator.py |
| `AV_VECTOR` | 2 | `AV_VECTOR\|A*v1\|[132/√2, 132/√2]` | svd_generator.py |
| `AXIOM_MATCH` | 2 | `AXIOM_MATCH\|PM *1.5 Assoc\|p := (a ∨ ¬d), q := (j → b), r := ((k ∨ h) → (n ∨ h))` | hilbert_axiom_derivation_generator.py |
| `B` | 1, 3 | `B\|38\|1\|381` | decimal_div_generator.py, long_division_generator.py, percent_problem_generator.py, polynomial_long_division_generator.py |
| `BABY_STEP` | 2 | `BABY_STEP\|j=0\|1` | baby_step_giant_step_generator.py |
| `BACKPROP_DELTA` | 2 | `BACKPROP_DELTA\|h1\|delta=8` | backprop_generator.py |
| `BACKPROP_GRAD` | 2 | `BACKPROP_GRAD\|dL/dy_hat\|-4` | backprop_generator.py |
| `BACKPROP_SETUP` | 3 | `BACKPROP_SETUP\|x=(-1,-1)\|y=0\|eta=1/3` | backprop_generator.py |
| `BACK_SUB` | 2 | `BACK_SUB\|v = y/x\|y/x = -4 ln(x) + C` | ode_substitution_generator.py |
| `BACK_SUB_ROW` | 3 | `BACK_SUB_ROW\|r=174\|x=1\|y=0` | extended_euclid_generator.py, modular_inverse_generator.py, rsa_generator.py |
| `BALANCED_EQ` | 1 | `BALANCED_EQ\|CH4 + 2 O2 -> CO2 + 2 H2O` | stoichiometry_generator.py |
| `BALANCE_COEFFS` | 2 | `BALANCE_COEFFS\|reactants=1,2\|products=1,2` | stoichiometry_generator.py |
| `BASE` | 2 | `BASE\|rev(ε)\|ε` | recursive_definition_unfold_generator.py |
| `BASE_ADD_COL` | 3 | `BASE_ADD_COL\|col 0\|A + 5 + carry 0\|15 -> digit F, carry 0` | base_arithmetic_generator.py |
| `BASE_ARITH_SETUP` | 2 | `BASE_ARITH_SETUP\|base 8\|525 * 7` | base_arithmetic_generator.py |
| `BASE_CARRY` | 2 | `BASE_CARRY\|carry 4\|digit 4, carry 0` | base_arithmetic_generator.py |
| `BASE_MUL_COL` | 3 | `BASE_MUL_COL\|col 0\|5 * 7 + carry 0\|35 -> digit 3, carry 4` | base_arithmetic_generator.py |
| `BASE_SETUP` | 2 | `BASE_SETUP\|8_10\|binary` | base_conversion_generator.py |
| `BAYES_CELL` | 3 | `BAYES_CELL\|true positive\|44 * 3/4\|33` | conditional_probability_generator.py |
| `BAYES_FORMULA` | 1 | `BAYES_FORMULA\|P(disease=yes given positive) = TP/(TP + FP)` | conditional_probability_generator.py |
| `BAYES_SETUP` | 3 | `BAYES_SETUP\|disease=yes 44, disease=no 105\|sensitivity 3/4, specificity 4/5\|P(disease=yes given test positive)` | conditional_probability_generator.py |
| `BAYES_UPDATE_SETUP` | 2, 3 | `BAYES_UPDATE_SETUP\|normal_normal\|prior=Normal(-5,10)\|sigma^2=5` | bayesian_update_generator.py |
| `BCH_FORM` | 2 | `BCH_FORM\|A+B+1/2[A,B]\|[[0, 1, 0], [0, 0, 0], [4, -2, 0]]` | bch_generator.py |
| `BCH_SETUP` | 3 | `BCH_SETUP\|A=E12\|B=4E31\|order=2` | bch_generator.py |
| `BEC_FORMULA` | 1 | `BEC_FORMULA\|P(no erasures)=(1-epsilon)^n` | bec_channel_generator.py |
| `BEC_SETUP` | 1 | `BEC_SETUP\|epsilon=1/4` | bec_channel_generator.py |
| `BELL_ROW` | 3 | `BELL_ROW\|n=1\|1\|1` | set_counting_generator.py |
| `BEREZIN_RULE` | 2 | `BEREZIN_RULE\|int dtheta 1\|0` | grassmann_generator.py |
| `BETA` | 1, 3 | `BETA\|line 2\|1L: 4: n ∧ o\|1R: 5: ¬n` | lambda_reduction_generator.py, semantic_tableau_generator.py |
| `BETA_COUNT` | 1 | `BETA_COUNT\|1` | lambda_reduction_generator.py |
| `BEZOUT_CHECK` | 2 | `BEZOUT_CHECK\|174*21 + 166*-22\|2` | extended_euclid_generator.py |
| `BIAS_CORRECT` | 2 | `BIAS_CORRECT\|m_hat\|-9` | adam_step_generator.py |
| `BIJECTION_RULE` | 2 | `BIJECTION_RULE\|e(n)\|2n` | countability_bijection_generator.py |
| `BINARY` | 2 | `BINARY\|53897\|1101001010001001` | countability_bijection_generator.py |
| `BINARY_EXPONENT` | 2 | `BINARY_EXPONENT\|57\|111001` | mod_exp_generator.py, quadratic_residue_generator.py |
| `BINOM_FORMULA` | 1 | `BINOM_FORMULA\|Var(X) = n·p·(1-p)` | binomial_probability_generator.py |
| `BINOM_SETUP` | 2 | `BINOM_SETUP\|n = 8, p = 1/3\|Var(X)` | binomial_probability_generator.py |
| `BISECTION_SETUP` | 3 | `BISECTION_SETUP\|f(x)=x^2-80\|interval=[8, 9]\|iterations=5` | bisection_generator.py |
| `BISECT_UPDATE` | 3 | `BISECT_UPDATE\|1\|product > 0\|[17/2, 9]` | bisection_generator.py |
| `BIT` | 1, 2 | `BIT\|b\|A=1\|B=0` | characteristic_vector_generator.py |
| `BITWISE` | 1 | `BITWISE\|∨\|10011001\|01011000\|11011001` | characteristic_vector_generator.py |
| `BIT_ROW` | 2, 3 | `BIT_ROW\|bit 0\|1 OR 1\|1` | bitwise_ops_generator.py |
| `BIT_RULE` | 2 | `BIT_RULE\|OR\|1 when at least one bit is 1` | bitwise_ops_generator.py |
| `BIT_SETUP` | 2 | `BIT_SETUP\|0101 OR 0001\|4-bit mask` | bitwise_ops_generator.py |
| `BLACKBODY_FORMULA` | 1 | `BLACKBODY_FORMULA\|lambda_max=b/T` | blackbody_generator.py |
| `BLACKBODY_SETUP` | 3 | `BLACKBODY_SETUP\|wien_peak\|b=13504\|T=844` | blackbody_generator.py |
| `BOND_FORMULA` | 1 | `BOND_FORMULA\|price=sum coupon/(1+y)^t + face/(1+y)^n` | bond_pricing_generator.py |
| `BOND_PRICE` | 1 | `BOND_PRICE\|$5300.00` | bond_pricing_generator.py |
| `BOND_SETUP` | 2 | `BOND_SETUP\|face=5300\|coupon=4%,ytm=4%,years=2` | bond_pricing_generator.py |
| `BOOL_SETUP` | 2 | `BOOL_SETUP\|variables Q, R, S, T\|DNF from g=1 rows` | boolean_algebra_generator.py |
| `BORROW` | 3 | `BORROW\|col_1\|from_left\|1` | multi_digit_subtraction_generator.py |
| `BOX_FORMULA` | 1 | `BOX_FORMULA\|lambda=8*m*L^2*c/((n_high^2-n_low^2)*h)` | particle_in_box_generator.py |
| `BOX_SETUP` | 1, 3 | `BOX_SETUP\|transition_wavelength\|n_low=4, n_high=5\|h=6, c=15` | particle_in_box_generator.py |
| `BRAKET_FORMULA` | 1 | `BRAKET_FORMULA\|U=diag(phases)` | braket_generator.py |
| `BRAKET_SETUP` | 3 | `BRAKET_SETUP\|time_evolution\|psi=[-1,1-i,2]\|phases=[-i,-i,-i]` | braket_generator.py |
| `BRANCH_CLOSE` | 2 | `BRANCH_CLOSE\|1L\|n, ¬n` | semantic_tableau_generator.py |
| `BRANCH_OPEN` | 2 | `BRANCH_OPEN\|1R\|n=F, o=F` | semantic_tableau_generator.py |
| `BRANCH_TEST` | 2 | `BRANCH_TEST\|229 <= 200\|no` | piecewise_evaluation_generator.py |
| `BRANCH_USE` | 1 | `BRANCH_USE\|$8.50` | piecewise_evaluation_generator.py |
| `BRING_DOWN` | 2 | `BRING_DOWN\|group 25\|current = 25` | composite_arithmetic_generator.py, manual_square_root_generator.py |
| `BSC_FORMULA` | 1 | `BSC_FORMULA\|H_b=p*(-log2 p)+(1-p)*(-log2(1-p))` | channel_capacity_generator.py |
| `BSC_SETUP` | 3 | `BSC_SETUP\|p=13/100\|-log2(p)=2.943\|-log2(1-p)=0.201` | channel_capacity_generator.py |
| `BSGS_MATCH` | 3 | `BSGS_MATCH\|i=1\|j=2\|x=8` | baby_step_giant_step_generator.py |
| `BSGS_SETUP` | 4 | `BSGS_SETUP\|p=31\|g=3\|h=20\|m=6` | baby_step_giant_step_generator.py |
| `BS_FORMULA` | 2 | `BS_FORMULA\|C=S*N(d1)-K*df*N(d2)\|P=K*df*N(-d2)-S*N(-d1)` | black_scholes_generator.py |
| `BS_RESULT` | 2 | `BS_RESULT\|call=5.65\|put=4.65` | black_scholes_generator.py |
| `BS_SETUP` | 3 | `BS_SETUP\|S=100,K=110\|df=0.9\|N_d1=0.7,N_d2=0.65` | black_scholes_generator.py |
| `C` | 3 | `C\|1/3\|21\|7/21` | complement_probability_generator.py, experimental_probability_generator.py, fraction_comparison_generator.py, fraction_op_generator.py, mixed_number_operation_generator.py, rational_expr_add_sub_generator.py |
| `CALC` | 1 | `CALC\|x = -9` | systems_elimination_generator.py, systems_substitution_generator.py |
| `CAL_DIVMOD` | 3 | `CAL_DIVMOD\|84\|7\|12 R0` | calendar_arithmetic_generator.py |
| `CAL_FORMULA` | 1 | `CAL_FORMULA\|q=m*c*(T2-T1)` | calorimetry_generator.py |
| `CAL_SETUP` | 3 | `CAL_SETUP\|start 2024-11-22\|end 2024-12-03\|days between` | calendar_arithmetic_generator.py, calorimetry_generator.py |
| `CANCEL` | 2 | `CANCEL\|2x\|7x - 1` | derivative_limit_def_generator.py, derivative_transcendental_generator.py, limit_evaluation_generator.py, power_series_generator.py, rational_expr_mult_div_generator.py, rational_expr_simplify_generator.py, rational_function_features_generator.py, series_convergence_generator.py, trig_identity_verify_generator.py |
| `CANDIDATES` | 1 | `CANDIDATES\|±1, ±2, ±3, ±6` | rational_root_generator.py |
| `CANONICAL_ORDER` | 1 | `CANONICAL_ORDER\|B=2, E=2, A=3, F=3, G=3, C=4, D=4` | kraft_inequality_generator.py |
| `CANONICAL_SHIFT` | 3 | `CANONICAL_SHIFT\|code=0\|left=2\|0` | kraft_inequality_generator.py |
| `CARD_RULE` | 2 | `CARD_RULE\|infinite addition and multiplication\|κ + λ = κ · λ = max(κ, λ)` | cardinal_arithmetic_generator.py |
| `CARRY_FINAL` | 1 | `CARRY_FINAL\|1` | multi_digit_addition_generator.py |
| `CARTESIAN_RESULT` | 1 | `CARTESIAN_RESULT\|{(b, 4), (i, 4)}` | set_operations_generator.py |
| `CART_PAIR` | 3 | `CART_PAIR\|b\|4\|(b, 4)` | set_operations_generator.py |
| `CASE` | 1, 2 | `CASE\|Gia=knight, Ravi=knight` | countability_bijection_generator.py, knights_knaves_generator.py |
| `CASHFLOW_PV` | 2 | `CASHFLOW_PV\|coupon_t1\|2650/13` | bond_pricing_generator.py |
| `CASIMIR_FORCE_SETUP` | 2 | `CASIMIR_FORCE_SETUP\|F/A=-π^2*hbar*c/(240*d^4)\|hbar=8,c=1,d=1` | casimir_force_generator.py |
| `CASIMIR_SETUP` | 3 | `CASIMIR_SETUP\|spin=1\|hbar=22/5\|J^2=Jz^2+(J+J-+J-J+)/2` | casimir_generator.py |
| `CAYLEY_HEADER` | 1 | `CAYLEY_HEADER\|0, 1, 2, 3, 4, 5, 6` | cayley_table_generator.py |
| `CAYLEY_ROW` | 2 | `CAYLEY_ROW\|row 0\|0, 1, 2, 3, 4, 5, 6` | cayley_table_generator.py |
| `CBRT` | 2 | `CBRT\|n^3\|n` | factor_special_forms_generator.py, inverse_function_generator.py, rational_exponent_generator.py |
| `CDF_EVENT` | 3 | `CDF_EVENT\|Y<=y\|X^2<=y\|X<=sqrt(y)` | rv_transform_generator.py |
| `CDF_FORMULA` | 2 | `CDF_FORMULA\|F_Y(y)=sqrt(y)/22\|0<=y<=484` | rv_transform_generator.py |
| `CEIL` | 2 | `CEIL\|10.8241\|11` | confidence_interval_generator.py |
| `CENTER` | 1, 2 | `CENTER\|(-3, 5)` | circle_equation_generator.py, ellipse_features_generator.py, hyperbola_features_generator.py, pca_generator.py |
| `CENTROID_COORD` | 3 | `CENTROID_COORD\|xbar = M_y/A\|(320/3)/(40)\|8/3` | centroid_generator.py |
| `CENTROID_SETUP` | 3 | `CENTROID_SETUP\|0 <= y <= 5*x\|0 <= x <= 4\|centroid` | centroid_generator.py |
| `CENTROID_UPDATE` | 2 | `CENTROID_UPDATE\|C1\|(2/3,-10/3)` | kmeans_step_generator.py |
| `CF_PARTIAL` | 2 | `CF_PARTIAL\|a_0\|5` | continued_fraction_generator.py |
| `CF_RESULT` | 1 | `CF_RESULT\|[5; 1, 1, 9, 1, 6]` | continued_fraction_generator.py |
| `CF_SETUP` | 1 | `CF_SETUP\|801/145` | continued_fraction_generator.py |
| `CG_COEFF` | 2 | `CG_COEFF\|ket(+,-)\|1/sqrt2` | clebsch_gordan_generator.py |
| `CG_SETUP` | 3 | `CG_SETUP\|j1=1/2\|j2=1/2\|phase=+` | clebsch_gordan_generator.py |
| `CG_STATE` | 2 | `CG_STATE\|J=1, M=0\|1/sqrt2*ket(+,-) + 1/sqrt2*ket(-,+)` | clebsch_gordan_generator.py |
| `CHAIN` | 2 | `CHAIN\|{13, 23, 50, 59}\|length 4` | partial_order_generator.py |
| `CHAIN_DERIV` | 2 | `CHAIN_DERIV\|dy/dx\|-3/2` | activation_generator.py |
| `CHAIN_RATE` | 2 | `CHAIN_RATE\|x_s\|3` | multivar_chain_rule_generator.py |
| `CHAIN_SUM` | 3 | `CHAIN_SUM\|f_x*x_s + f_y*y_s\|(-28)*3 + (-24)*1\|-108` | multivar_chain_rule_generator.py |
| `CHAIN_VALUE` | 3 | `CHAIN_VALUE\|x(0,2)\|(-3)*2 + 3\|-3` | multivar_chain_rule_generator.py |
| `CHANGE_BASE` | 1 | `CHANGE_BASE\|log_27(9) = log_3(9)/log_3(27)` | log_conversion_generator.py |
| `CHAR_DIAG` | 2 | `CHAR_DIAG\|diagonal of λI - A\|(λ + 4), λ, (λ + 5)` | eigenvalue_generator.py |
| `CHAR_EQ` | 2 | `CHAR_EQ\|assume y=e^(rx)\|r^2 - 2r - 3 = 0` | ode_system_generator.py, second_order_ode_generator.py, undetermined_coeff_generator.py, variation_parameters_generator.py |
| `CHAR_POLY` | 2 | `CHAR_POLY\|p(λ) = λ^3 + 9λ^2 + 20λ\|(λ + 5)*(λ + 4)*λ` | diagonalization_generator.py, eigenvalue_generator.py, recurrence_generator.py |
| `CHAR_ROOTS` | 2 | `CHAR_ROOTS\|r1 = -1, r2 = 3\|distinct real` | recurrence_generator.py, second_order_ode_generator.py, undetermined_coeff_generator.py, variation_parameters_generator.py |
| `CHAR_SETUP` | 2 | `CHAR_SETUP\|p(λ) = det(λI - A)\|triangular determinant` | eigenvalue_generator.py |
| `CHECK` | 1, 2, 3, 4 | `CHECK\|multiply_back\|23×98+45=2299\|2299` | annuity_generator.py, area_between_curves_generator.py, arithmetic_sequence_generator.py, baby_step_giant_step_generator.py, base_arithmetic_generator.py, bch_generator.py, bitwise_ops_generator.py, boolean_algebra_generator.py, cantor_diagonal_generator.py, cantor_pairing_generator.py, cardinal_arithmetic_generator.py, casimir_generator.py, cauchy_riemann_generator.py, characteristic_vector_generator.py, chi_square_generator.py, cholesky_generator.py, clebsch_gordan_generator.py, combinatory_logic_generator.py, commutator_generator.py, complement_probability_generator.py, completing_square_generator.py, conditional_probability_generator.py, convolutional_code_viterbi_generator.py, coset_generator.py, countability_bijection_generator.py, cramers_rule_generator.py, cyclic_group_generator.py, cyk_parser_generator.py, dedekind_cut_generator.py, dfa_minimization_generator.py, dfa_simulation_generator.py, diagonalization_generator.py, diffie_hellman_generator.py, ecdh_generator.py, ecdsa_generator.py, eigenvalue_generator.py, elliptic_curve_finite_field_generator.py, embedding_similarity_generator.py, equilibrium_ice_generator.py, error_spotting_generator.py, euler_circuit_generator.py, exact_ode_generator.py, expected_value_generator.py, experimental_probability_generator.py, extended_euclid_generator.py, factor_gcf_generator.py, factor_grouping_generator.py, factor_special_forms_generator.py, factor_trinomial_generator.py, feature_map_generator.py, fill_in_step_generator.py, five_number_summary_generator.py, foundations_critic_generator.py, function_inner_product_generator.py, fundamental_counting_principle_generator.py, game_theory_generator.py, gamma_matrix_generator.py, gauss_bonnet_generator.py, gaussian_curvature_generator.py, geometric_mean_generator.py, geometric_probability_generator.py, geometric_sequence_generator.py, godel_numbering_generator.py, gradient_generator.py, gram_schmidt_generator.py, graph_counting_generator.py, hamming_code_generator.py, hereditarily_finite_set_generator.py, hermitian_check_generator.py, hessian_classify_generator.py, hilbert_axiom_derivation_generator.py, horner_evaluation_generator.py, hyperbolic_function_generator.py, hypothesis_test_generator.py, index_gymnastics_generator.py, induction_verify_generator.py, information_gain_generator.py, integers_as_pairs_generator.py, inverse_function_generator.py, kernel_perceptron_generator.py, kernel_validity_generator.py, kmeans_step_generator.py, knights_knaves_generator.py, knn_generator.py, ladder_operator_generator.py, lagrange_multiplier_generator.py, lambda_reduction_generator.py, least_squares_generator.py, legendre_construction_generator.py, lhopital_generator.py, lie_exponential_generator.py, likelihood_language_generator.py, limit_evaluation_generator.py, line_integral_generator.py, linear_fractional_generator.py, lll_reduction_generator.py, log_equation_generator.py, logic_grid_puzzle_generator.py, logical_equivalence_laws_generator.py, long_division_generator.py, low_rank_approx_generator.py, lp_corner_generator.py, lu_decomposition_generator.py, lz_compression_generator.py, manual_square_root_generator.py, markov_chain_generator.py, matrix_exponential_generator.py, matrix_group_check_generator.py, matrix_inverse_generator.py, mean_value_theorem_generator.py, method_of_moments_generator.py, mle_generator.py, mobius_transform_generator.py, modular_arithmetic_generator.py, modular_inverse_generator.py, naive_bayes_generator.py, natural_deduction_generator.py, nfa_simulation_generator.py, ode_system_generator.py, operation_properties_generator.py, or_formula_generator.py, ordinal_arithmetic_generator.py, partial_derivative_generator.py, partial_order_generator.py, partial_trace_generator.py, pauli_algebra_generator.py, pca_generator.py, pda_simulation_generator.py, peano_arithmetic_generator.py, perceptron_generator.py, pollard_factorization_generator.py, polynomial_inequality_generator.py, positive_definite_generator.py, power_series_generator.py, prenex_normal_form_generator.py, prime_factorization_generator.py, projector_generator.py, qr_decomposition_generator.py, quadratic_factoring_generator.py, quadratic_square_root_generator.py, quantifier_negation_generator.py, quaternion_generator.py, radical_variable_simplify_generator.py, ratio_table_generator.py, rationals_as_pairs_generator.py, recursive_explicit_generator.py, regex_to_automaton_generator.py, relation_closure_generator.py, resolution_proof_generator.py, riemann_tensor_generator.py, rotational_dynamics_generator.py, routh_hurwitz_generator.py, rsa_generator.py, running_coupling_generator.py, rv_transform_generator.py, sample_space_list_generator.py, semantic_tableau_generator.py, series_convergence_generator.py, set_algebra_laws_generator.py, shm_generator.py, signal_arithmetic_generator.py, similar_triangles_generator.py, simple_probability_generator.py, simplex_generator.py, special_solution_equation_generator.py, statics_generator.py, stereographic_generator.py, structure_constant_generator.py, structure_isomorphism_generator.py, svd_generator.py, svm_margin_generator.py, syllogism_generator.py, systems_elimination_generator.py, taylor_series_generator.py, tip_bill_split_generator.py, tonelli_shanks_generator.py, totient_generator.py, transportation_generator.py, turing_machine_trace_generator.py, two_sample_test_generator.py, two_step_equation_generator.py, type_theory_generator.py, uncertainty_generator.py, venn_region_count_generator.py, young_tableaux_generator.py, z_score_generator.py, zf_axiom_identify_generator.py |
| `CHECK_POINT` | 3 | `CHECK_POINT\|x=0\|5·0 - 1 = -1\|5·0 - 8 = -8` | special_solution_equation_generator.py |
| `CHINCHILLA` | 2 | `CHINCHILLA\|20N\|1140000000` | scaling_law_generator.py |
| `CHI_FORMULA` | 1 | `CHI_FORMULA\|E = (row·col)/N; χ² = Σ (O - E)^2/E` | chi_square_generator.py |
| `CHI_SETUP` | 2 | `CHI_SETUP\|row 1: 101, 19; row 2: 139, 41; N = 300\|independence; df = 1, critical value = 3.841` | chi_square_generator.py |
| `CHI_TERM` | 3 | `CHI_TERM\|101 - 96 = 5\|5^2 = 25\|25/96 = 25/96` | chi_square_generator.py |
| `CHOLESKY_ENTRY` | 2 | `CHOLESKY_ENTRY\|l11\|3` | cholesky_generator.py |
| `CHOL_SETUP` | 2 | `CHOL_SETUP\|A = [[9, 0, 6], [0, 9, -12], [6, -12, 36]]\|A = L L^T` | cholesky_generator.py |
| `CHRISTOFFEL_FORMULA` | 1 | `CHRISTOFFEL_FORMULA\|Gamma^i_jk = 1/2 g^im(d_j g_mk + d_k g_mj - d_m g_jk)` | christoffel_generator.py |
| `CHRISTOFFEL_SETUP` | 3 | `CHRISTOFFEL_SETUP\|sphere\|g_phiphi=R^2, g_thetatheta=R^2 sin^2(phi)\|R=94, phi=45 deg` | christoffel_generator.py |
| `CHRISTOFFEL_VALUE` | 2 | `CHRISTOFFEL_VALUE\|Gamma^phi_thetatheta\|-420/1369` | riemann_tensor_generator.py |
| `CHURCH_NUMERAL` | 2 | `CHURCH_NUMERAL\|6\|lambda c. (lambda s. (c (c (c (c (c (c s)))))))` | lambda_reduction_generator.py |
| `CIRCLE_ANGLE_SETUP` | 2 | `CIRCLE_ANGLE_SETUP\|triangle inscribed in a circle with one side a diameter; one acute angle is 16°\|the other acute angle` | circle_angle_generator.py |
| `CIRCLE_CALCULATE` | 2 | `CIRCLE_CALCULATE\|radius = diameter / 2 = 32 / 2\|16` | circle_generator.py |
| `CIRCLE_EQ` | 1 | `CIRCLE_EQ\|(x + 1)^2 + (y - 4)^2 = 49` | complex_locus_generator.py |
| `CIRCLE_FORMULA` | 1 | `CIRCLE_FORMULA\|A = πr²` | circle_generator.py |
| `CIRCLE_SETUP` | 2 | `CIRCLE_SETUP\|32\|diameter` | circle_equation_generator.py, circle_generator.py |
| `CIRCLE_SUBSTITUTE` | 1 | `CIRCLE_SUBSTITUTE\|A = π × 16²` | circle_generator.py |
| `CIRCULATION_SUM` | 2 | `CIRCULATION_SUM\|(-1)*12^2*pi\|-144*pi` | vector_theorem_generator.py |
| `CI_FORMULA` | 1 | `CI_FORMULA\|x̄ ± E` | confidence_interval_generator.py |
| `CI_SETUP` | 2 | `CI_SETUP\|σ = 2, E = 1, z* = 1.645\|minimum sample size for the mean` | confidence_interval_generator.py |
| `CLASS` | 2 | `CLASS\|remainder 0\|{10, 15}` | equivalence_relation_generator.py |
| `CLASSIFY` | 2 | `CLASSIFY\|contingency\|T at 3 of 4 rows` | foundations_critic_generator.py, truth_table_generator.py |
| `CLAUSE` | 2 | `CLAUSE\|C1\|(¬P6545)` | resolution_proof_generator.py |
| `CLIFFORD_EXPECT` | 3 | `CLIFFORD_EXPECT\|2*eta=0\|I_entry=0\|0` | gamma_matrix_generator.py |
| `CLOSURE_ADD` | 2 | `CLOSURE_ADD\|(30, 30)\|reflexive` | relation_closure_generator.py |
| `CLUE_APPLY` | 3 | `CLUE_APPLY\|clue 1\|Kira has camera\|6 → 2 candidates` | logic_grid_puzzle_generator.py |
| `CLUSTER_MEMBERS` | 2 | `CLUSTER_MEMBERS\|C1\|P1,P2,P3` | kmeans_step_generator.py |
| `CMP` | 2, 3 | `CMP\|44\|9\|>` | dedekind_cut_generator.py, experimental_probability_generator.py, fraction_comparison_generator.py, graph_interpret_generator.py, integers_as_pairs_generator.py, likelihood_language_generator.py, logical_connective_eval_generator.py, rationals_as_pairs_generator.py, set_builder_roster_generator.py |
| `CMP_DIGIT` | 4 | `CMP_DIGIT\|pos_0\|0\|1\|<` | number_comparison_generator.py |
| `CMP_NUM` | 3 | `CMP_NUM\|46.36\|177.07\|<` | number_comparison_generator.py |
| `CNF` | 1 | `CNF\|ω^3 + ω·5 + 3` | ordinal_arithmetic_generator.py |
| `CNF_FORM` | 1 | `CNF_FORM\|(L OR M OR NOT N) AND (L OR NOT M OR N) AND (L OR NOT M OR NOT N) AND (NOT L OR NOT M OR N) AND (NOT L OR NOT M OR NOT N)` | boolean_algebra_generator.py |
| `CODEWORD` | 1, 3 | `CODEWORD\|1111111` | hamming_code_generator.py, kraft_inequality_generator.py |
| `CODE_LENGTH` | 2 | `CODE_LENGTH\|A\|l=3` | huffman_coding_generator.py |
| `COEFF` | 2 | `COEFF\|a_1\|12600` | laurent_series_generator.py, series_solution_generator.py |
| `COEFFS` | 1, 2 | `COEFFS\|1, -1, -9, -8` | horner_evaluation_generator.py, polynomial_zeros_generator.py, synthetic_division_generator.py |
| `COEFF_MATCH` | 2 | `COEFF_MATCH\|x^n\|(n+1)a_(n+1) = a_n` | series_solution_generator.py |
| `COEFF_PAIR` | 3 | `COEFF_PAIR\|i=2, j=6\|2i + 3j = 22\|accepted` | generating_function_generator.py |
| `COFACTOR` | 2 | `COFACTOR\|(1,1) sign +\|minor [[2, 2], [-4, 1]]` | determinant_generator.py |
| `COLLIDER_SETUP` | 3 | `COLLIDER_SETUP\|luminosity\|N=74 events\|sigma=13 fb` | cross_section_generator.py |
| `COLLISION` | 1 | `COLLISION\|f(e) = f(o) = 15` | function_properties_generator.py |
| `COLLISION_SETUP` | 3 | `COLLISION_SETUP\|elastic_1d\|m1=9, u1=-4\|m2=14, u2=21` | collision_generator.py |
| `COL_BASIS` | 2 | `COL_BASIS\|original columns 1, 2, 3\|[[-17, -2, -45], [9, 1, 24], [-3, 0, -8]]` | subspace_basis_generator.py |
| `COMB` | 2 | `COMB\|C(3,1)\|3` | bec_channel_generator.py |
| `COMBO` | 2 | `COMBO\|x = 44*v1 - 16*v2\|[0, 4]` | diagonalization_generator.py |
| `COMB_CONST` | 3 | `COMB_CONST\|-7\|+7\|0` | derivative_product_quotient_generator.py, equation_from_two_points_generator.py, linear_complex_generator.py, rational_expr_add_sub_generator.py, simplify_expression_generator.py, special_solution_equation_generator.py |
| `COMB_FORMULA` | 1 | `COMB_FORMULA\|C(n, r) = P(n, r)/r!` | permutation_combination_generator.py |
| `COMB_RULE` | 2 | `COMB_RULE\|K x y\|x` | combinatory_logic_generator.py |
| `COMB_SETUP` | 2 | `COMB_SETUP\|choose 6 of 10\|order does not matter` | counting_classics_generator.py, permutation_combination_generator.py, stars_and_bars_generator.py |
| `COMB_X` | 3 | `COMB_X\|3x\|-5x\|-2x` | derivative_product_quotient_generator.py, linear_complex_generator.py, rational_expr_add_sub_generator.py, simplify_expression_generator.py, special_solution_equation_generator.py |
| `COMMON_DIFF` | 2 | `COMMON_DIFF\|-2 - 2\|-4` | arithmetic_sequence_generator.py, recursive_explicit_generator.py |
| `COMMON_RATIO` | 2 | `COMMON_RATIO\|2178/(-2662)\|-9/11` | geometric_sequence_generator.py, recursive_explicit_generator.py |
| `COMMUTATOR` | 2 | `COMMUTATOR\|[A,B]\|[[0, 54], [-54, 0]]` | structure_constant_generator.py |
| `COMM_ENTRY` | 3 | `COMM_ENTRY\|(1,1)\|0 - 0\|0` | structure_constant_generator.py |
| `COMM_FORMULA` | 1 | `COMM_FORMULA\|[A,B]f=A(Bf)-B(Af)` | commutator_generator.py |
| `COMM_RESULT` | 2 | `COMM_RESULT\|[x,p]f\|8i*x^19` | commutator_generator.py |
| `COMM_SETUP` | 3 | `COMM_SETUP\|[x,p]f\|f=x^19\|p=-i*hbar*D, hbar=8` | commutator_generator.py |
| `COMPARE` | 2, 3 | `COMPARE\|0 < 2\|log_b(a) < k` | algorithm_trace_generator.py, equilibrium_ice_generator.py, fixed_point_generator.py, master_theorem_generator.py |
| `COMPLEMENT` | 2, 3 | `COMPLEMENT\|P(Aᶜ) = 1 − P(A)\|1 − 4/13\|9/13` | complement_probability_generator.py, derangement_generator.py |
| `COMPLETE_SQUARE` | 2 | `COMPLETE_SQUARE\|half of 6 = 3\|3^2 = 9` | completing_square_generator.py, conic_standard_form_generator.py, polar_parametric_generator.py |
| `COMPOSE` | 3 | `COMPOSE\|f\|f(f) = 27\|g(27) = L` | function_properties_generator.py |
| `COMPOSE_PAIR` | 3 | `COMPOSE_PAIR\|(b, 22)\|(22, Q)\|(b, Q)` | relation_operations_generator.py |
| `COMPOSITE_FACTOR` | 2 | `COMPOSITE_FACTOR\|5\|73` | divisibility_classification_generator.py |
| `COMPOSITE_SETUP` | 2 | `COMPOSITE_SETUP\|area = length × width with mixed numbers\|convert, multiply, simplify` | composite_arithmetic_generator.py |
| `COMP_INEQ_PART` | 2 | `COMP_INEQ_PART\|Part 1\|2x + 1 < -4 -> x < -5/2` | compound_inequality_generator.py |
| `COMP_INEQ_SETUP` | 1 | `COMP_INEQ_SETUP\|-11 < 3x + 4 < 7` | compound_inequality_generator.py |
| `CONCLUDE` | 1 | `CONCLUDE\|odd` | direct_proof_algebra_generator.py |
| `CONCLUSION_AT` | 2 | `CONCLUSION_AT\|p=T, q=T, r=F, s=F\|F` | argument_form_generator.py |
| `CONCLUSION_CHECK` | 1 | `CONCLUSION_CHECK\|not forced` | syllogism_generator.py |
| `COND_COUNT` | 2 | `COND_COUNT\|club=yes and commute=bike\|27` | conditional_probability_generator.py |
| `COND_ENTROPY` | 1 | `COND_ENTROPY\|H(Y given X)=H(X,Y)-H(X)` | mutual_information_generator.py |
| `COND_FORMULA` | 1 | `COND_FORMULA\|P(A given B) = count(A and B)/count(B)` | conditional_probability_generator.py, joint_distribution_generator.py |
| `COND_PARTS` | 2 | `COND_PARTS\|r ∧ q\|¬((r ∧ q) ∧ ¬p)` | conditional_forms_generator.py |
| `COND_SETUP` | 2 | `COND_SETUP\|yes/bike 27, no/bike 10, yes/bus 15, no/bus 14\|P(club=yes given commute=bike)` | conditional_probability_generator.py |
| `COND_TOTAL` | 2 | `COND_TOTAL\|commute=bike total\|27 + 10 = 37` | conditional_probability_generator.py |
| `CONGRUENCE_REDUCE` | 2 | `CONGRUENCE_REDUCE\|17x congruent to 2\|mod 7` | modular_inverse_generator.py |
| `CONGRUENCE_SOLUTIONS` | 3 | `CONGRUENCE_SOLUTIONS\|base 3\|step 7\|3, 10, 17` | modular_inverse_generator.py |
| `CONIC_SETUP` | 2 | `CONIC_SETUP\|x^2 = 16y\|vertex, focus, directrix` | conic_standard_form_generator.py, ellipse_features_generator.py, hyperbola_features_generator.py, parabola_features_generator.py |
| `CONJ` | 2 | `CONJ\|phi_1=2-i\|2+i` | braket_generator.py |
| `CONJUGATE` | 2 | `CONJUGATE\|-5 + 2i\|-5 - 2i` | complex_division_generator.py, quaternion_generator.py |
| `CONNECTIVE` | 2 | `CONNECTIVE\|¬q\|T` | logical_connective_eval_generator.py |
| `CONSERVATION_SETUP` | 2 | `CONSERVATION_SETUP\|gamma + p + pi0 -> gamma + e+ + gamma\|check=Q,B,Le,Lmu` | conservation_law_generator.py |
| `CONSERVE_CHECK` | 3 | `CONSERVE_CHECK\|Q\|left=1,right=1\|conserved` | conservation_law_generator.py |
| `CONSTRAINT_SUBST` | 3 | `CONSTRAINT_SUBST\|x + 4*y = 108\|lambda*(1/4 + 16/8) = 108\|lambda = 48` | lagrange_multiplier_generator.py |
| `CONST_SOLVE` | 2 | `CONST_SOLVE\|C1 = 3\|C2 = 4` | recurrence_generator.py |
| `CONTOUR_SETUP` | 3 | `CONTOUR_SETUP\|abs(z)=3\|positive orientation\|f=2/(z+7) - 6/(z+8) - 2/(z+6)` | contour_integral_generator.py |
| `CONTRADICTION` | 2 | `CONTRADICTION\|r−d is nonnegative and in S\|r−d < r` | induction_verify_generator.py |
| `CONT_DIST_SETUP` | 3 | `CONT_DIST_SETUP\|f(x)=k*x\|support=[0,19]\|interval=(10,11)` | continuous_distribution_generator.py |
| `CONVERGENT` | 2 | `CONVERGENT\|i=0\|5/1` | continued_fraction_generator.py |
| `CONVERGE_CHECK` | 2 | `CONVERGE_CHECK\|abs(r) = 9/11 < 1\|converges` | geometric_sequence_generator.py, series_convergence_generator.py |
| `CONV_ENCODE_STEP` | 3 | `CONV_ENCODE_STEP\|i=1\|prev=0,u=1\|11` | convolutional_code_viterbi_generator.py |
| `CONV_FACTOR` | 2 | `CONV_FACTOR\|1 hr\|60 min` | cross_section_generator.py, dimensional_analysis_generator.py, multi_step_unit_conversion_generator.py, rate_conversion_generator.py, unit_conversion_generator.py |
| `CONV_INIT` | 2 | `CONV_INIT\|h_-2=0,h_-1=1\|k_-2=1,k_-1=0` | continued_fraction_generator.py |
| `CONV_RECEIVED` | 2 | `CONV_RECEIVED\|111010\|flipped position 5` | convolutional_code_viterbi_generator.py |
| `CONV_RESULT` | 2 | `CONV_RESULT\|41 hr\|2460 min` | dimensional_analysis_generator.py, multi_step_unit_conversion_generator.py, rate_conversion_generator.py, temperature_conversion_generator.py, unit_conversion_generator.py |
| `CONV_SETUP` | 2, 3 | `CONV_SETUP\|x=[0,2,1]\|h=[6,3,5]` | convolution_generator.py, convolutional_code_viterbi_generator.py |
| `CONV_STEP` | 3 | `CONV_STEP\|i=0\|h=5\|k=1` | continued_fraction_generator.py |
| `CONV_SUM` | 2 | `CONV_SUM\|n=0\|0` | convolution_generator.py |
| `CONV_WINDOW` | 2 | `CONV_WINDOW\|n=0\|x0*h0` | convolution_generator.py |
| `COORDS` | 2 | `COORDS\|c = P^-1 x\|[44, -16]` | diagonalization_generator.py |
| `CORRECT_BIT` | 3 | `CORRECT_BIT\|position=5\|0->1\|corrected=1010101` | hamming_code_generator.py |
| `CORR_FORMULA` | 1 | `CORR_FORMULA\|r = Sxy/√(Sxx·Syy)` | joint_distribution_generator.py, regression_generator.py |
| `COS` | 2 | `COS\|2pi/3\|-1/2` | positional_encoding_generator.py |
| `COSET` | 2 | `COSET\|1H\|{1, 13}` | coset_generator.py |
| `COSET_ELEM` | 2 | `COSET_ELEM\|1H\|1` | coset_generator.py |
| `COSET_SKIP` | 2 | `COSET_SKIP\|9\|already listed` | coset_generator.py |
| `COSET_START` | 2 | `COSET_START\|rep 1\|1H` | coset_generator.py |
| `COSINE` | 2 | `COSINE\|A,A\|1` | embedding_similarity_generator.py, lr_schedule_generator.py |
| `COST` | 1 | `COST\|initial` | transportation_generator.py |
| `COUNT` | 2 | `COUNT\|neither\|5` | attribute_sorting_generator.py, bayesian_update_generator.py, equivalence_relation_generator.py, likelihood_language_generator.py, logical_connective_eval_generator.py, method_of_moments_generator.py, mle_generator.py, one_to_one_correspondence_generator.py, probability_addition_rule_generator.py, set_builder_roster_generator.py, set_membership_subset_generator.py, set_operations_generator.py |
| `COUNTEREXAMPLE` | 2, 3 | `COUNTEREXAMPLE\|n = 8\|174 = 2 × 87` | argument_form_generator.py, conditional_forms_generator.py, counterexample_search_generator.py, truth_table_generator.py |
| `COUNTERMODEL` | 1 | `COUNTERMODEL\|writers=TFF, dancers=TFF, orators=FFF` | syllogism_generator.py |
| `COUNT_DP` | 3 | `COUNT_DP\|1\|1\|2` | decimal_mult_generator.py |
| `COUNT_RULE` | 2 | `COUNT_RULE\|k-subsets\|C(n,k) = n(n−1)…(n−k+1)/k!` | function_properties_generator.py, set_counting_generator.py |
| `COUNT_SETUP` | 1, 2 | `COUNT_SETUP\|Catalan C_14` | counting_classics_generator.py |
| `COUPON` | 1 | `COUPON\|212` | bond_pricing_generator.py |
| `COVER` | 3 | `COVER\|41\|58\|no c strictly between` | partial_order_generator.py |
| `COV_ENTRY` | 2 | `COV_ENTRY\|xx\|49/2` | pca_generator.py |
| `COV_FORMULA` | 1 | `COV_FORMULA\|Cov=E[XY]-E[X]E[Y]` | joint_distribution_generator.py |
| `CRC_CHECK` | 3 | `CRC_CHECK\|codeword=1100010011001\|remainder=0000\|valid` | crc_generator.py |
| `CRC_REMAINDER` | 1 | `CRC_REMAINDER\|1001` | crc_generator.py |
| `CRC_SETUP` | 3 | `CRC_SETUP\|data=110001001\|poly=10011\|augmented=1100010010000` | crc_generator.py |
| `CRC_SKIP` | 2 | `CRC_SKIP\|i=2\|leading bit 0` | crc_generator.py |
| `CRC_XOR` | 3 | `CRC_XOR\|i=0\|11000 xor 10011\|01011` | crc_generator.py |
| `CRIT_EQS` | 2 | `CRIT_EQS\|f_x = 0\|-4*x - y + 16 = 0` | hessian_classify_generator.py |
| `CRIT_SOLVE` | 3 | `CRIT_SOLVE\|det\|(-4)*(-4) - (-1)^2\|15` | hessian_classify_generator.py |
| `CROSS_ENTROPY` | 2 | `CROSS_ENTROPY\|target=1\|ln(3)` | perplexity_generator.py, softmax_gradient_generator.py |
| `CROSS_MULT` | 1 | `CROSS_MULT\|20·BC = 5·12` | similar_triangles_generator.py, triangle_solve_generator.py |
| `CROSS_RATIO` | 1 | `CROSS_RATIO\|33/26` | mobius_transform_generator.py |
| `CROSS_RATIO_SETUP` | 4 | `CROSS_RATIO_SETUP\|z1=-6\|z2=-4\|z3=0\|z4=7` | mobius_transform_generator.py |
| `CRT_CHECK` | 3 | `CRT_CHECK\|i=1\|0\|0` | crt_generator.py |
| `CRT_CONGRUENCE` | 3 | `CRT_CONGRUENCE\|i=1\|x=0\|mod 9` | crt_generator.py |
| `CRT_FACTOR` | 3 | `CRT_FACTOR\|i=1\|M_i=13\|mod 9` | crt_generator.py |
| `CRT_SETUP` | 1 | `CRT_SETUP\|2 congruences` | crt_generator.py |
| `CRT_TERM` | 2 | `CRT_TERM\|i=1\|0` | crt_generator.py |
| `CRT_TOTAL_MODULUS` | 2 | `CRT_TOTAL_MODULUS\|9, 13\|117` | crt_generator.py |
| `CR_SETUP` | 2 | `CR_SETUP\|u=3x^2 - 3y^2 - 2y\|v=6xy + 2x` | cauchy_riemann_generator.py |
| `CUM_INTERVAL` | 2 | `CUM_INTERVAL\|A\|[0,1/4)` | arithmetic_coding_generator.py |
| `CURL_COMPONENT` | 3 | `CURL_COMPONENT\|i\|2 + 6\|8` | div_curl_generator.py |
| `CURRENT_YIELD` | 1 | `CURRENT_YIELD\|0.04` | bond_pricing_generator.py |
| `CURVATURE_FORMULA` | 2 | `CURVATURE_FORMULA\|circle\|kappa = 1/R` | curve_geometry_generator.py |
| `CURVE_GEOM_SETUP` | 3 | `CURVE_GEOM_SETUP\|r(t) = <-7*t - 7, 24*t - 3>\|0 <= t <= 12\|arc length` | curve_geometry_generator.py |
| `CURVE_SETUP` | 2 | `CURVE_SETUP\|f(x) = x^3 - 12x^2 + 45x - 8\|critical points and their nature` | curve_analysis_generator.py |
| `CUT_RULE` | 2 | `CUT_RULE\|L(√2)\|q < 0 or q² < 2` | dedekind_cut_generator.py |
| `CW_START` | 2 | `CW_START\|leading 1\|1/1` | countability_bijection_generator.py |
| `CW_STEP` | 3 | `CW_STEP\|bit 1\|1/1\|2/1` | countability_bijection_generator.py |
| `CX_A` | 3 | `CX_A\|56/65\|0\|56/65` | braket_generator.py, spin_half_generator.py |
| `CX_M` | 3 | `CX_M\|1\|56/65\|56/65` | braket_generator.py, spin_half_generator.py |
| `CX_SETUP` | 2 | `CX_SETUP\|(2 + 9i)(7 + 8i)\|multiply` | complex_division_generator.py, complex_number_ops_generator.py |
| `CYCLE` | 1 | `CYCLE\|(1 4)` | permutation_group_generator.py |
| `CYCLE_LENGTHS` | 1 | `CYCLE_LENGTHS\|2, 3` | permutation_group_generator.py |
| `CYCLE_REJECT` | 2 | `CYCLE_REJECT\|AB\|endpoints already connected` | mst_generator.py |
| `CYCLE_TRACE` | 2 | `CYCLE_TRACE\|start 1\|1->4->1` | permutation_group_generator.py |
| `CYCLIC_START` | 2 | `CYCLIC_START\|17\|identity 1` | cyclic_group_generator.py |
| `CYCLIC_SUBGROUP` | 2 | `CYCLIC_SUBGROUP\|{1, 17, 19, 23}\|4` | cyclic_group_generator.py |
| `CYK_CELL` | 2 | `CYK_CELL\|1,2\|{S}` | cyk_parser_generator.py |
| `CYK_COMBINE` | 3 | `CYK_COMBINE\|Y T\|{S}\|cell 1,2` | cyk_parser_generator.py |
| `CYK_RULE` | 2 | `CYK_RULE\|B\|b or d` | cyk_parser_generator.py |
| `CYK_SETUP` | 2 | `CYK_SETUP\|string ddd\|length 3` | cyk_parser_generator.py |
| `CYK_SPAN` | 1 | `CYK_SPAN\|2` | cyk_parser_generator.py |
| `CYK_SPLIT` | 3 | `CYK_SPLIT\|cell 1,2\|1,1 x 2,2\|{B,T,Y} x {B,T,Y}` | cyk_parser_generator.py |
| `CYK_TERMINAL` | 3 | `CYK_TERMINAL\|cell 1,1\|d\|{B,T,Y}` | cyk_parser_generator.py |
| `CYL_BOUNDS` | 2 | `CYL_BOUNDS\|z\|0..9` | triple_integral_generator.py |
| `CYL_CONVERT` | 2 | `CYL_CONVERT\|3*z dV\|3*z*r dz dr dtheta` | triple_integral_generator.py |
| `D` | 3 | `D\|632\|99\|6` | ac_circuit_generator.py, activation_generator.py, adam_step_generator.py, angle_defect_generator.py, annuity_generator.py, antiderivative_generator.py, arithmetic_coding_generator.py, arithmetic_sequence_generator.py, attention_generator.py, backprop_generator.py, bayesian_update_generator.py, bisection_generator.py, blackbody_generator.py, bond_pricing_generator.py, branching_ratio_generator.py, cantor_pairing_generator.py, casimir_force_generator.py, cholesky_generator.py, christoffel_generator.py, circle_angle_generator.py, circle_equation_generator.py, classifier_metrics_generator.py, collision_generator.py, complex_number_ops_generator.py, composite_arithmetic_generator.py, confidence_interval_generator.py, conic_standard_form_generator.py, continuous_distribution_generator.py, coset_generator.py, countability_bijection_generator.py, counting_classics_generator.py, cramers_rule_generator.py, cross_section_generator.py, crt_generator.py, curve_analysis_generator.py, de_moivre_generator.py, decimal_div_generator.py, dedekind_cut_generator.py, definite_integral_generator.py, dimensional_analysis_generator.py, doppler_generator.py, einstein_summation_generator.py, electrostatics_generator.py, embedding_similarity_generator.py, energy_conservation_generator.py, entropy_change_generator.py, entropy_generator.py, equilibrium_ice_generator.py, error_spotting_generator.py, exact_ode_generator.py, exponential_equation_generator.py, exponential_model_generator.py, fill_in_step_generator.py, finite_difference_generator.py, flops_memory_generator.py, fourier_series_generator.py, function_inner_product_generator.py, function_operations_generator.py, game_theory_generator.py, gas_law_generator.py, gas_stoichiometry_generator.py, gauss_bonnet_generator.py, gauss_law_generator.py, gaussian_curvature_generator.py, generating_function_generator.py, geometric_distribution_generator.py, geometric_mean_generator.py, geometric_sequence_generator.py, geometry_area_perimeter_generator.py, gradient_descent_generator.py, gradient_step_generator.py, hamiltonian_generator.py, hawking_generator.py, heat_engine_generator.py, huffman_coding_generator.py, hydrogen_atom_generator.py, hyperbolic_distance_generator.py, hyperbolic_function_generator.py, hypothesis_test_generator.py, information_gain_generator.py, integrating_factor_generator.py, interference_generator.py, interpolation_generator.py, invariant_mass_generator.py, jacobi_symbol_generator.py, joint_distribution_generator.py, kernel_ridge_generator.py, kinematics_generator.py, kl_divergence_generator.py, kmeans_step_generator.py, kraft_inequality_generator.py, ladder_operator_generator.py, lagrangian_generator.py, laplace_ivp_generator.py, laurent_series_generator.py, layer_norm_generator.py, lcm_generator.py, least_squares_generator.py, legendre_construction_generator.py, limit_evaluation_generator.py, linear_simple_generator.py, log_conversion_generator.py, logistic_growth_generator.py, long_division_generator.py, lr_schedule_generator.py, magnetism_generator.py, manual_square_root_generator.py, markov_chain_generator.py, matrix_inverse_generator.py, matrix_norm_generator.py, mean_value_theorem_generator.py, method_of_moments_generator.py, midpoint_generator.py, mle_generator.py, modular_inverse_generator.py, multi_step_unit_conversion_generator.py, naive_bayes_generator.py, named_distribution_generator.py, natural_units_generator.py, nets_surface_area_generator.py, newton_raphson_generator.py, newtons_laws_generator.py, npv_irr_generator.py, ode_substitution_generator.py, optics_generator.py, optimization_generator.py, or_formula_generator.py, orbital_mechanics_generator.py, order_of_operations_generator.py, order_statistics_generator.py, parabola_features_generator.py, param_count_generator.py, parametric_calculus_generator.py, particle_in_box_generator.py, partition_function_generator.py, pca_generator.py, percent_problem_generator.py, permutation_combination_generator.py, perplexity_generator.py, physics_formula_generator.py, planck_units_generator.py, polar_parametric_generator.py, primality_test_generator.py, projectile_motion_generator.py, proportion_word_problem_generator.py, proportional_relationship_generator.py, quadratic_residue_generator.py, quantization_generator.py, quantum_formula_generator.py, radical_rationalize_generator.py, rate_conversion_generator.py, ratio_table_generator.py, recurrence_generator.py, regression_generator.py, regular_polygon_area_generator.py, relativistic_energy_generator.py, repeating_decimal_generator.py, riemann_sum_generator.py, riemann_tensor_generator.py, right_triangle_trig_generator.py, rotational_dynamics_generator.py, round_solids_generator.py, routh_hurwitz_generator.py, runge_kutta_generator.py, running_coupling_generator.py, rv_transform_generator.py, scaling_law_generator.py, schwarzschild_generator.py, second_order_ode_generator.py, segment_partition_generator.py, separable_pde_generator.py, series_convergence_generator.py, series_solution_generator.py, set_counting_generator.py, shm_generator.py, similar_triangles_generator.py, simplex_generator.py, sinusoid_features_generator.py, slope_two_points_generator.py, softmax_gradient_generator.py, solution_chem_generator.py, special_relativity_generator.py, special_right_triangle_generator.py, spherical_excess_generator.py, spherical_triangle_generator.py, spin_half_generator.py, standard_deviation_generator.py, standing_wave_generator.py, stars_and_bars_generator.py, statics_generator.py, stereographic_generator.py, stoichiometry_generator.py, svm_margin_generator.py, taylor_series_generator.py, telescoping_generator.py, temperature_conversion_generator.py, tip_bill_split_generator.py, totient_generator.py, transient_circuit_generator.py, triangle_area_sas_generator.py, triangle_solve_generator.py, trig_identity_eval_generator.py, trig_six_functions_generator.py, two_sample_test_generator.py, u_substitution_generator.py, undetermined_coeff_generator.py, unit_conversion_generator.py, variation_parameters_generator.py, vector_ops_generator.py, wavefunction_generator.py, young_tableaux_generator.py, z_score_generator.py |
| `DALEMBERT` | 1 | `DALEMBERT\|u=(f(x-ct)+f(x+ct))/2` | separable_pde_generator.py |
| `DATA_PRECISION` | 1 | `DATA_PRECISION\|n/sigma^2` | bayesian_update_generator.py |
| `DATE_ORDINAL` | 2 | `DATE_ORDINAL\|2024-11-22\|739212` | calendar_arithmetic_generator.py |
| `DB_FORMULA` | 1 | `DB_FORMULA\|G_dB=10*log10(P2/P1)` | signal_arithmetic_generator.py |
| `DECISION` | 2 | `DECISION\|f(x)\|2` | kernel_perceptron_generator.py, svm_margin_generator.py |
| `DECODE` | 2 | `DECODE\|11011001\|{b, k, o, q, z}` | characteristic_vector_generator.py |
| `DEC_ADD_COL` | 3 | `DEC_ADD_COL\|frac_0\|0+1+0\|->1 (carry 0)` | decimal_add_sub_generator.py |
| `DEC_ALIGN` | 2 | `DEC_ALIGN\|55.60\|69.81` | decimal_add_sub_generator.py |
| `DEC_CARRY_FINAL` | 1 | `DEC_CARRY_FINAL\|1` | decimal_add_sub_generator.py |
| `DEC_SHIFT` | 3 | `DEC_SHIFT\|33.0/0.2\|330/2\|1` | decimal_div_generator.py, percent_problem_generator.py |
| `DEC_SUB_COL` | 3 | `DEC_SUB_COL\|frac_0\|1-0 (borrow_in 0)\|->1 (borrow_out 0)` | decimal_add_sub_generator.py |
| `DEC_TO_FRAC` | 2 | `DEC_TO_FRAC\|4.17\|417/100` | fraction_decimal_percent_converter.py |
| `DEC_TO_PERCENT` | 2 | `DEC_TO_PERCENT\|1.075\|107.5%` | fraction_decimal_percent_converter.py, percent_problem_generator.py, simple_probability_generator.py, tip_bill_split_generator.py |
| `DEC_TYPE` | 2 | `DEC_TYPE\|151/228\|repeating` | repeating_decimal_generator.py |
| `DEC_VALUE` | 2 | `DEC_VALUE\|151/228\|0.66(228070175438596491)` | repeating_decimal_generator.py |
| `DEDUCE` | 3 | `DEDUCE\|Mara\|item = drum\|only solution left` | logic_grid_puzzle_generator.py |
| `DEDUP` | 2 | `DEDUP\|A raw [24, 57, 66, 52, 63, 66]\|{24, 52, 57, 63, 66}` | set_membership_subset_generator.py |
| `DEGREE` | 2, 3 | `DEGREE\|A\|B, E, F\|3` | euler_circuit_generator.py, graph_counting_generator.py |
| `DEGREE_COMPARE` | 2 | `DEGREE_COMPARE\|deg num = 1 < deg den = 2\|y = 0` | limit_evaluation_generator.py, rational_function_features_generator.py, series_convergence_generator.py |
| `DEGREE_SEQUENCE` | 1 | `DEGREE_SEQUENCE\|3, 3, 3, 2, 2, 1` | graph_counting_generator.py |
| `DELTA_VALUE` | 2 | `DELTA_VALUE\|delta_22\|1` | index_gymnastics_generator.py |
| `DEMOIVRE_POWER` | 1 | `DEMOIVRE_POWER\|343 cis(0 deg)` | de_moivre_generator.py |
| `DEMOIVRE_SETUP` | 2, 4 | `DEMOIVRE_SETUP\|power\|r=7\|theta=240 deg\|n=3` | de_moivre_generator.py |
| `DENSITY` | 2 | `DENSITY\|f_X(x)\|1/22` | rv_transform_generator.py |
| `DENSITY_MATRIX` | 1 | `DENSITY_MATRIX\|rho=[[9/17,0],[0,8/17]]` | density_matrix_generator.py |
| `DENSITY_SETUP` | 2, 3 | `DENSITY_SETUP\|state=Schmidt\|psi=(sqrt(183)ket00 + sqrt(202)ket11)/sqrt(385)` | density_matrix_generator.py, partial_trace_generator.py |
| `DEPTH` | 1, 2 | `DEPTH\|3` | wff_parsing_generator.py |
| `DEQUANT_VALUE` | 2 | `DEQUANT_VALUE\|1\|11/25` | quantization_generator.py |
| `DERANGE_PROB` | 2 | `DERANGE_PROB\|D_9/9!\|133496/362880` | derangement_generator.py |
| `DERANGE_SETUP` | 2 | `DERANGE_SETUP\|n = 9\|no item fixed` | derangement_generator.py |
| `DERANGE_VALUE` | 2 | `DERANGE_VALUE\|D_2\|1` | derangement_generator.py |
| `DERIV` | 2, 3 | `DERIV\|d_phi g_thetatheta\|2R^2 sin(phi)cos(phi)` | christoffel_generator.py, gaussian_curvature_generator.py, riemann_tensor_generator.py |
| `DERIVATIVE` | 1, 2 | `DERIVATIVE\|g'(x)\|5/12` | fixed_point_generator.py, mgf_generator.py, mle_generator.py |
| `DERIVED` | 2 | `DERIVED\|C4\|□` | resolution_proof_generator.py |
| `DERIV_FORM` | 2 | `DERIV_FORM\|y'\|-C1e^(-x) + 3C2e^(3x)` | second_order_ode_generator.py, undetermined_coeff_generator.py, variation_parameters_generator.py |
| `DERIV_RULE` | 2 | `DERIV_RULE\|power rule\|d/dx of c·x^n = c·n·x^(n-1)` | chain_rule_generator.py, derivative_power_rule_generator.py, derivative_product_quotient_generator.py, derivative_transcendental_generator.py, lhopital_generator.py, linear_approx_generator.py, log_diff_higher_order_generator.py, multivar_chain_rule_generator.py |
| `DERIV_SERIES` | 2 | `DERIV_SERIES\|y'\|sum (n+1)a_(n+1)x^n` | series_solution_generator.py |
| `DERIV_SETUP` | 2 | `DERIV_SETUP\|f(x) = -7x^3 + 3x^2 - x^(-2)\|f'(x)` | chain_rule_generator.py, derivative_power_rule_generator.py, derivative_product_quotient_generator.py, derivative_transcendental_generator.py, log_diff_higher_order_generator.py, tangent_line_generator.py |
| `DESIGN_MATRIX` | 2 | `DESIGN_MATRIX\|X = [[1, -3], [1, -1], [1, 1], [1, 3]]\|y = [11, 11, 9, 5]` | least_squares_generator.py |
| `DET` | 2 | `DET\|K\|2` | kernel_ridge_generator.py, kernel_validity_generator.py |
| `DET2` | 2 | `DET2\|ad - bc\|-8` | ode_system_generator.py |
| `DET_FORMULA` | 1 | `DET_FORMULA\|det = a11·M11 - a12·M12 + a13·M13` | cramers_rule_generator.py, determinant_generator.py, matrix_inverse_generator.py |
| `DEV_ROW` | 3 | `DEV_ROW\|26\|-1\|1` | standard_deviation_generator.py |
| `DFA_ACCEPT` | 1 | `DFA_ACCEPT\|q2` | dfa_minimization_generator.py, dfa_simulation_generator.py |
| `DFA_INPUT` | 1 | `DFA_INPUT\|1101000` | dfa_simulation_generator.py |
| `DFA_MIN_SETUP` | 3 | `DFA_MIN_SETUP\|states A, B, C\|alphabet 0, 1\|start A` | dfa_minimization_generator.py |
| `DFA_MIN_TRANSITION` | 3 | `DFA_MIN_TRANSITION\|A\|0\|A` | dfa_minimization_generator.py |
| `DFA_READ` | 2 | `DFA_READ\|pos 1\|1` | dfa_simulation_generator.py |
| `DFA_SETUP` | 3 | `DFA_SETUP\|states q0, q1, q2\|alphabet 0, 1\|start q0` | dfa_simulation_generator.py |
| `DFA_STATE` | 2 | `DFA_STATE\|start\|q0` | dfa_simulation_generator.py |
| `DFA_STEP` | 3 | `DFA_STEP\|q0\|1\|q1` | dfa_simulation_generator.py |
| `DFA_TRANSITION` | 3 | `DFA_TRANSITION\|q0\|0\|q0` | dfa_simulation_generator.py |
| `DFS_EDGE` | 2 | `DFS_EDGE\|B->A\|tree` | graph_traversal_generator.py |
| `DFT_BIN` | 1 | `DFT_BIN\|X0=x0+x1+x2+x3` | dft_generator.py |
| `DFT_SETUP` | 2 | `DFT_SETUP\|N=4\|x=[8,-6,-5,-2]` | dft_generator.py |
| `DH_PUBLIC` | 2 | `DH_PUBLIC\|Alice\|23` | diffie_hellman_generator.py |
| `DH_SECRET` | 2 | `DH_SECRET\|Alice\|3` | diffie_hellman_generator.py |
| `DH_SETUP` | 2 | `DH_SETUP\|p=31\|g=12` | diffie_hellman_generator.py |
| `DH_SHARED` | 2 | `DH_SHARED\|Alice\|16` | diffie_hellman_generator.py |
| `DIAG` | 2 | `DIAG\|row 1\|8` | cantor_diagonal_generator.py |
| `DIAGONAL` | 3 | `DIAGONAL\|w=182\|start=16653\|offset=93` | cantor_pairing_generator.py |
| `DIAG_FORM` | 3 | `DIAG_FORM\|P = [[9, 1], [-1, 0]]\|D = [[1, 0], [0, 6]]\|P^-1 = [[0, -1], [1, 9]]` | diagonalization_generator.py, matrix_exponential_generator.py |
| `DIFF_ROW` | 2 | `DIFF_ROW\|Delta y\|[-14, -10, -6]` | finite_difference_generator.py |
| `DIFF_SETUP` | 3 | `DIFF_SETUP\|f(x,y) = 5*x^2 + 4*y^2 + x*y - 2*x - 4*y\|point (4, -1)\|dx=1/2, dy=1/4` | multivar_chain_rule_generator.py |
| `DIFF_SUM` | 3 | `DIFF_SUM\|f_x*dx + f_y*dy\|37*1/2 + (-8)*1/4\|16.5` | multivar_chain_rule_generator.py |
| `DIJKSTRA_INIT` | 2 | `DIJKSTRA_INIT\|start D\|A=inf, B=inf, C=inf, D=0, E=inf` | dijkstra_generator.py |
| `DIM` | 2 | `DIM\|2*1/2+1\|2` | casimir_generator.py |
| `DIRECTRIX` | 1 | `DIRECTRIX\|y = -4` | parabola_features_generator.py |
| `DISC` | 2, 3 | `DISC\|784\|384\|400` | complex_quadratic_generator.py, discriminant_generator.py, polynomial_zeros_generator.py, quadratic_generator.py |
| `DISC_CLASSIFY` | 2 | `DISC_CLASSIFY\|0 = 0\|one repeated rational solution` | complex_quadratic_generator.py, discriminant_generator.py, polynomial_zeros_generator.py |
| `DIST` | 3 | `DIST\|5\|-x-4\|-5x-20` | derivative_limit_def_generator.py, derivative_product_quotient_generator.py, equation_from_two_points_generator.py, function_composition_generator.py, parallel_perpendicular_line_generator.py, point_slope_generator.py, polar_parametric_generator.py, radical_multiply_generator.py, radical_rationalize_generator.py, rational_expr_add_sub_generator.py, recursive_explicit_generator.py, simplify_expression_generator.py, solid_revolution_generator.py, special_solution_equation_generator.py, tangent_line_generator.py |
| `DIST2` | 2, 3 | `DIST2\|P1\|C1\|17` | embedding_similarity_generator.py, kernel_evaluation_generator.py, kmeans_step_generator.py |
| `DIST_COMBINE` | 1 | `DIST_COMBINE\|9y - 90 = -9` | systems_substitution_generator.py |
| `DIST_FORMULA` | 1 | `DIST_FORMULA\|d = √((x2 - x1)^2 + (y2 - y1)^2)` | complex_locus_generator.py, distance_formula_generator.py, hypercube_counting_generator.py |
| `DIST_SETUP` | 3 | `DIST_SETUP\|normal\|mu=-3,sigma=4\|x=-11` | named_distribution_generator.py |
| `DIST_TABLE` | 2 | `DIST_TABLE\|visited D\|A=4, B=inf, C=inf, D=0, E=6` | dijkstra_generator.py |
| `DIST_TERM` | 2 | `DIST_TERM\|-4x\|- 8x^3 - 20x^2 + 16x` | multiplying_polynomials_generator.py |
| `DIVIDE_EQ` | 2 | `DIVIDE_EQ\|divide by y^2\|y^(-2)dy/dx + 5y^(-1) = 5` | ode_substitution_generator.py |
| `DIVMOD` | 3, 4 | `DIVMOD\|8\|2\|4\|r=0` | base_conversion_generator.py, induction_verify_generator.py, recursive_definition_unfold_generator.py |
| `DIV_CHECK` | 3 | `DIV_CHECK\|6\|2\|remainder 0` | conditional_forms_generator.py, counterexample_search_generator.py, divisibility_classification_generator.py, logical_connective_eval_generator.py, set_builder_roster_generator.py |
| `DIV_COEFF` | 3 | `DIV_COEFF\|0\|-2\|x=0` | linear_complex_generator.py |
| `DIV_SETUP` | 2 | `DIV_SETUP\|330\|2` | decimal_div_generator.py, percent_problem_generator.py |
| `DIV_SUM` | 3 | `DIV_SUM\|P_x + Q_y + R_z\|6 - 5 + 4\|5` | div_curl_generator.py |
| `DIV_TERM` | 3 | `DIV_TERM\|10y^4\|5y\|2y^3` | factor_gcf_generator.py, finite_field_generator.py, polynomial_long_division_generator.py |
| `DNF_FORM` | 1 | `DNF_FORM\|(NOT Q AND NOT R AND NOT S AND T) OR (NOT Q AND NOT R AND S AND NOT T)` | boolean_algebra_generator.py |
| `DOMAIN` | 1, 2 | `DOMAIN\|x = 1..15\|{1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15}` | quantifier_finite_domain_generator.py, relation_operations_generator.py, set_builder_roster_generator.py |
| `DOMAIN_COND` | 2 | `DOMAIN_COND\|radicand ≥ 0\|t + 3 ≥ 0` | domain_range_generator.py |
| `DOMAIN_NOTE` | 2 | `DOMAIN_NOTE\|x ≠ 0\|denominator cannot be zero` | domain_range_generator.py, log_equation_generator.py, logistic_growth_generator.py, probability_addition_rule_generator.py, rational_equation_generator.py, unit_circle_generator.py |
| `DOPPLER_FORMULA` | 1 | `DOPPLER_FORMULA\|f_obs=f*(v+v_observer)/(v-v_source)` | doppler_generator.py |
| `DOPPLER_SETUP` | 3 | `DOPPLER_SETUP\|acoustic_toward\|f=178, v=52\|v_observer=10, v_source=7` | doppler_generator.py |
| `DOT` | 2, 3 | `DOT\|(24, 7) · (1, 0)\|24*1 + 7*0\|24` | embedding_similarity_generator.py, feature_map_generator.py, fundamental_form_generator.py, gradient_generator.py, gram_schmidt_generator.py, kernel_evaluation_generator.py, line_integral_generator.py, lll_reduction_generator.py, qr_decomposition_generator.py |
| `DOT4` | 4 | `DOT4\|gamma0gamma1\|(4,3)\|0*-1 + 0*0 + 0*0 + 1*0\|0` | gamma_matrix_generator.py |
| `DOT_FORMULA` | 1 | `DOT_FORMULA\|cos θ = (u·v)/(‖u‖ · ‖v‖)` | dot_product_generator.py |
| `DOUBLE_SETUP` | 2, 3 | `DOUBLE_SETUP\|integrand 6\|x:0..5\|y:0..3*x` | double_integral_generator.py |
| `DPLL_BACKTRACK` | 2 | `DPLL_BACKTRACK\|A\|True` | dpll_trace_generator.py |
| `DPLL_BRANCH` | 3 | `DPLL_BRANCH\|depth 0\|A\|True` | dpll_trace_generator.py |
| `DPLL_CONFLICT` | 1 | `DPLL_CONFLICT\|A=True, B=True` | dpll_trace_generator.py |
| `DPLL_SAT` | 1 | `DPLL_SAT\|A=True, B=True` | dpll_trace_generator.py |
| `DPLL_SETUP` | 3 | `DPLL_SETUP\|(A OR B) AND (A OR not B) AND (not A OR B) AND (not A OR not B)\|variables A, B\|True first` | dpll_trace_generator.py |
| `DPLL_SIMPLIFY` | 2 | `DPLL_SIMPLIFY\|A=True, B=True\|conflict` | dpll_trace_generator.py |
| `DPLL_STATE` | 3 | `DPLL_STATE\|depth 0\|none\|4 clauses left` | dpll_trace_generator.py |
| `DPLL_UNIT` | 2 | `DPLL_UNIT\|(B)\|B=True` | dpll_trace_generator.py |
| `DP_CELL` | 3 | `DP_CELL\|i=1,amount=0\|base empty set\|1` | dp_table_generator.py |
| `DP_COINS` | 1 | `DP_COINS\|1, 4, 6` | dp_table_generator.py |
| `DP_ITEMS` | 1 | `DP_ITEMS\|1:(w=2,v=10); 2:(w=4,v=2); 3:(w=4,v=7)` | dp_table_generator.py |
| `DP_ROW` | 2 | `DP_ROW\|i=0\|1, 0, 0, 0, 0, 0, 0, 0` | dp_table_generator.py |
| `DP_SETUP` | 2, 3 | `DP_SETUP\|coin change\|target 7` | dp_table_generator.py |
| `D_POWER` | 2 | `D_POWER\|D^2\|[[81, 0], [0, 1]]` | diagonalization_generator.py |
| `E` | 3 | `E\|2\|2\|4` | ac_circuit_generator.py, adam_step_generator.py, angle_defect_generator.py, annuity_generator.py, arc_sector_generator.py, backprop_generator.py, bec_channel_generator.py, blackbody_generator.py, bond_pricing_generator.py, casimir_force_generator.py, casimir_generator.py, christoffel_generator.py, circle_equation_generator.py, complex_division_generator.py, complex_locus_generator.py, confidence_interval_generator.py, conic_standard_form_generator.py, continuous_distribution_generator.py, de_moivre_generator.py, dedekind_cut_generator.py, definite_integral_generator.py, density_matrix_generator.py, derivative_limit_def_generator.py, diagonalization_generator.py, distance_formula_generator.py, doppler_generator.py, electrostatics_generator.py, ellipse_features_generator.py, embedding_similarity_generator.py, energy_conservation_generator.py, euler_formula_generator.py, exponential_equation_generator.py, exponential_model_generator.py, factor_special_forms_generator.py, feature_map_generator.py, finance_generator.py, four_vector_generator.py, fractal_iteration_generator.py, function_composition_generator.py, function_evaluation_generator.py, function_operations_generator.py, function_table_generator.py, fundamental_form_generator.py, gauss_bonnet_generator.py, gauss_law_generator.py, gaussian_curvature_generator.py, geometric_mean_generator.py, geometric_sequence_generator.py, gradient_descent_generator.py, gradient_step_generator.py, hamiltonian_generator.py, hawking_generator.py, hermitian_check_generator.py, huffman_coding_generator.py, hydrogen_atom_generator.py, hyperbola_features_generator.py, hyperbolic_function_generator.py, hypercube_counting_generator.py, invariant_mass_generator.py, kernel_evaluation_generator.py, kmeans_step_generator.py, knn_generator.py, kraft_inequality_generator.py, lagrangian_generator.py, laurent_series_generator.py, layer_norm_generator.py, limit_evaluation_generator.py, log_conversion_generator.py, log_equation_generator.py, log_properties_generator.py, low_rank_approx_generator.py, matrix_group_check_generator.py, matrix_norm_generator.py, mean_value_theorem_generator.py, metric_arc_length_generator.py, mgf_generator.py, minkowski_interval_generator.py, mobius_transform_generator.py, named_distribution_generator.py, natural_units_generator.py, npv_irr_generator.py, optimization_generator.py, or_formula_generator.py, orbital_mechanics_generator.py, order_statistics_generator.py, particle_in_box_generator.py, pca_generator.py, piecewise_evaluation_generator.py, planck_units_generator.py, polar_parametric_generator.py, portfolio_generator.py, projectile_motion_generator.py, pythag_hyp_generator.py, radical_equation_generator.py, radical_multiply_generator.py, radical_rationalize_generator.py, rational_exponent_generator.py, recursive_explicit_generator.py, regression_generator.py, related_rates_generator.py, relativistic_energy_generator.py, remainder_factor_theorem_generator.py, riemann_tensor_generator.py, rotational_dynamics_generator.py, round_solids_generator.py, rv_transform_generator.py, schwarzschild_generator.py, set_counting_generator.py, set_operations_generator.py, shm_generator.py, spherical_excess_generator.py, spin_half_generator.py, stereographic_generator.py, svm_margin_generator.py, tangent_line_generator.py, taylor_series_generator.py, triangle_solve_generator.py, trig_identity_eval_generator.py, trig_six_functions_generator.py, uncertainty_generator.py, vector_ops_generator.py, wavefunction_generator.py, z_transform_generator.py |
| `ECDH_SETUP` | 2 | `ECDH_SETUP\|E:y^2=x^3+2x+2 over F_17\|G=(5,1)` | ecdh_generator.py |
| `ECDSA_NONCE` | 2 | `ECDSA_NONCE\|kG=(6,3)\|r=6` | ecdsa_generator.py |
| `ECDSA_PUBLIC` | 1 | `ECDSA_PUBLIC\|Q=dG=(9,16)` | ecdsa_generator.py |
| `ECDSA_SETUP` | 4 | `ECDSA_SETUP\|E/F_17, G=(5,1), n=19\|d=5\|z=5\|k=2` | ecdsa_generator.py |
| `ECDSA_SIGN` | 2 | `ECDSA_SIGN\|s=k^-1(z+rd) mod n\|s=8` | ecdsa_generator.py |
| `ECDSA_VERIFY` | 2 | `ECDSA_VERIFY\|u1=3\|u2=15` | ecdsa_generator.py |
| `EC_ACCUM` | 2 | `EC_ACCUM\|1P\|(14,17)` | elliptic_curve_finite_field_generator.py |
| `EC_ADD` | 1 | `EC_ADD\|(6,3)` | ecdsa_generator.py |
| `EC_IDENTITY` | 2 | `EC_IDENTITY\|O + Q\|(14,17)` | elliptic_curve_finite_field_generator.py |
| `EC_INVERSE` | 3 | *(not observed in sampling)* | elliptic_curve_finite_field_generator.py |
| `EC_POINT_CHECK` | 3 | `EC_POINT_CHECK\|P\|O\|identity` | elliptic_curve_finite_field_generator.py |
| `EC_PUBLIC` | 2 | `EC_PUBLIC\|A=(7,6)\|B=(9,16)` | ecdh_generator.py |
| `EC_SCALAR` | 2 | `EC_SCALAR\|a=9\|aG=(7,6)` | ecdh_generator.py, ecdsa_generator.py |
| `EC_SCALAR_SETUP` | 2 | `EC_SCALAR_SETUP\|k=3\|P=(14,17)` | elliptic_curve_finite_field_generator.py |
| `EC_SETUP` | 3 | `EC_SETUP\|p=19\|a=1\|b=1` | elliptic_curve_finite_field_generator.py |
| `EC_SHARED` | 2 | `EC_SHARED\|aB=(0,6)\|bA=(0,6)` | ecdh_generator.py |
| `EC_SLOPE` | 2 | `EC_SLOPE\|2P\|0` | elliptic_curve_finite_field_generator.py |
| `EC_SLOPE_FORMULA` | 2 | `EC_SLOPE_FORMULA\|2P\|(3x1^2+a)/(2y1)` | elliptic_curve_finite_field_generator.py |
| `EC_X3` | 2 | `EC_X3\|2P\|10` | elliptic_curve_finite_field_generator.py |
| `EC_Y3` | 2 | `EC_Y3\|2P\|2` | elliptic_curve_finite_field_generator.py |
| `EDGE_CHECK` | 3 | `EDGE_CHECK\|(6548, 4788)\|(y, t)\|mismatch` | structure_isomorphism_generator.py |
| `EDGE_CHOOSE` | 3 | `EDGE_CHOOSE\|BD\|weight 7\|add B` | mst_generator.py |
| `EDGE_CONSIDER` | 2 | `EDGE_CONSIDER\|AC\|weight 3` | mst_generator.py |
| `EDGE_COUNT` | 2 | `EDGE_COUNT\|m\|7` | euler_circuit_generator.py, graph_counting_generator.py |
| `EDGE_LIST` | 1 | `EDGE_LIST\|AB, AC, AD, AE, BD, CE` | euler_circuit_generator.py |
| `EDGE_WEIGHT` | 2 | `EDGE_WEIGHT\|AB\|4` | dijkstra_generator.py, mst_generator.py |
| `EIGENPAIR` | 2 | `EIGENPAIR\|lambda = -4\|[2, 1]` | ode_system_generator.py |
| `EIGENVALUE` | 1, 2 | `EIGENVALUE\|λ = -5\|p(-5) = 0` | diagonalization_generator.py, eigenvalue_generator.py, matrix_exponential_generator.py, separable_pde_generator.py, svd_generator.py |
| `EIGENVALUES` | 2 | `EIGENVALUES\|A^T A\|81,64` | low_rank_approx_generator.py, matrix_norm_generator.py, pca_generator.py |
| `EIGENVECTOR` | 2 | `EIGENVECTOR\|A + 5I times v = 0\|[14, 2, -5]` | diagonalization_generator.py, eigenvalue_generator.py, matrix_exponential_generator.py, svd_generator.py |
| `EIGEN_CHECK` | 3 | `EIGEN_CHECK\|sigma_y psi\|1*psi\|lambda=1` | spin_half_generator.py |
| `EIGEN_MATRIX` | 2 | `EIGEN_MATRIX\|A + 5I\|[[1, 3, 4], [0, 5, 2], [0, 0, 0]]` | eigenvalue_generator.py |
| `EINSTEIN_SETUP` | 2, 3 | `EINSTEIN_SETUP\|symmetrize\|T_ij=[[-5, 1], [-4, 4]]` | einstein_summation_generator.py |
| `ELEC_FORMULA` | 1 | `ELEC_FORMULA\|left charge: E1=q1/r1^2` | electrostatics_generator.py |
| `ELEC_SETUP` | 2, 3 | `ELEC_SETUP\|field_axis\|q1=-2, x1=-3\|q2=5, x2=2` | electrostatics_generator.py |
| `ELEMENT_ORDER` | 2 | `ELEMENT_ORDER\|5\|7` | cayley_table_generator.py |
| `ELEMENT_SCAN` | 3 | `ELEMENT_SCAN\|30\|A\|found` | set_expression_generator.py, set_membership_subset_generator.py, set_operations_generator.py |
| `ELIMINATE` | 1, 3 | `ELIMINATE\|clue 1\|Mara: camera; Oona: drum; Kira: spoon\|violates clue` | logic_grid_puzzle_generator.py, newtons_laws_generator.py |
| `ELIMINATE_LAMBDA` | 2 | `ELIMINATE_LAMBDA\|f_x = f_y\|3*y = x` | lagrange_multiplier_generator.py |
| `EL_EQUATION` | 1 | `EL_EQUATION\|mL^2*thetaddot+mgL*sin(theta)=0` | lagrangian_generator.py |
| `EL_SOLVE` | 2 | `EL_SOLVE\|thetaddot\|-(10/9)*sin(theta)` | lagrangian_generator.py |
| `EMBED_SETUP` | 1 | `EMBED_SETUP\|A=(-3,4), B=(8,15), C=(12,5)` | embedding_similarity_generator.py |
| `ENERGY_FORMULA` | 1 | `ENERGY_FORMULA\|vf^2=vi^2+2W/m` | energy_conservation_generator.py |
| `ENERGY_LEVEL` | 2 | `ENERGY_LEVEL\|E_20=hbar*omega*(n+1/2)\|328` | ladder_operator_generator.py |
| `ENERGY_SETUP` | 3 | `ENERGY_SETUP\|work_energy\|m=17\|vi=5, W=6936` | energy_conservation_generator.py |
| `ENERGY_TERM` | 1 | `ENERGY_TERM\|T=1/2*m*L^2*thetadot^2` | lagrangian_generator.py |
| `ENGINE_FORMULA` | 1 | `ENGINE_FORMULA\|eta_C=1-Tc/Th=(Th-Tc)/Th` | heat_engine_generator.py |
| `ENGINE_SETUP` | 3 | `ENGINE_SETUP\|carnot_efficiency\|Th=601\|Tc=433` | heat_engine_generator.py |
| `ENQUEUE` | 3 | `ENQUEUE\|A\|from D\|A` | graph_traversal_generator.py |
| `ENTER` | 2 | `ENTER\|x\|most negative reduced cost -15` | simplex_generator.py |
| `ENTROPY_FORMULA` | 1 | `ENTROPY_FORMULA\|DeltaS=nR*ln(V2/V1)` | entropy_change_generator.py |
| `ENTROPY_SETUP` | 2, 3 | `ENTROPY_SETUP\|eigenvalues=[1/8,1/64,1/128,1/128,1/16,1/8,1/16,1/64,1/32,1/8,1/32,1/8,1/8,1/64,1/8]\|S=-sum lambda log2(lambda)` | entropy_change_generator.py, entropy_generator.py, huffman_coding_generator.py, information_gain_generator.py, mutual_information_generator.py, von_neumann_entropy_generator.py |
| `ENTROPY_SKIP` | 2 | `ENTROPY_SKIP\|H(X,Y)\|p=0` | mutual_information_generator.py |
| `ENTROPY_TERM` | 4 | `ENTROPY_TERM\|row 0\|p=3/4\|I=0.415\|249/800` | entropy_rate_markov_generator.py |
| `ENTROPY_VALUE` | 2 | `ENTROPY_VALUE\|parent\|0.543875` | information_gain_generator.py |
| `ENTROPY_ZERO` | 2 | `ENTROPY_ZERO\|source_left\|count=0` | information_gain_generator.py |
| `EPSILON_VALUE` | 2 | `EPSILON_VALUE\|eps_121\|0` | index_gymnastics_generator.py |
| `EPS_CLOSURE` | 2 | `EPS_CLOSURE\|{q1}\|{q1}` | nfa_simulation_generator.py |
| `EQUATE_EXP` | 1 | `EQUATE_EXP\|3x = 4` | exponential_equation_generator.py |
| `EQUILIBRIA` | 2 | `EQUILIBRIA\|f(y) = 0\|y=0, y=11` | stability_generator.py |
| `EQ_2PT_SETUP` | 2 | `EQ_2PT_SETUP\|(7, 1)\|(6, -3)` | equation_from_two_points_generator.py |
| `EQ_OP_BOTH` | 3, 4 | `EQ_OP_BOTH\|divide\|11\|x\|5` | absolute_value_equation_generator.py, area_between_curves_generator.py, completing_square_generator.py, curve_analysis_generator.py, error_spotting_generator.py, exponential_equation_generator.py, fill_in_step_generator.py, implicit_diff_generator.py, inverse_function_generator.py, linear_fractional_generator.py, log_diff_higher_order_generator.py, log_equation_generator.py, mean_value_theorem_generator.py, one_step_equation_generator.py, optimization_generator.py, partial_fractions_generator.py, polar_parametric_generator.py, quadratic_factoring_generator.py, quadratic_square_root_generator.py, radical_equation_generator.py, rational_equation_generator.py, related_rates_generator.py, remainder_factor_theorem_generator.py, separable_ode_generator.py, special_solution_equation_generator.py, systems_elimination_generator.py, systems_substitution_generator.py, trig_equation_generator.py, two_step_equation_generator.py |
| `EQ_OP_NOTE` | 3 | `EQ_OP_NOTE\|subtract\|2w\|from both sides` | equation_from_two_points_generator.py, literal_equation_generator.py, parallel_perpendicular_line_generator.py, point_slope_generator.py, standard_form_conversion_generator.py |
| `EQ_RESULT` | 2 | `EQ_RESULT\|x\|5` | completing_square_generator.py, error_spotting_generator.py, fill_in_step_generator.py, linear_fractional_generator.py, linear_simple_generator.py, one_step_equation_generator.py, quadratic_factoring_generator.py, quadratic_square_root_generator.py, radical_equation_generator.py, rational_equation_generator.py, special_solution_equation_generator.py, two_step_equation_generator.py |
| `EQ_SETUP` | 1, 2 | `EQ_SETUP\|x = 6/2` | area_between_curves_generator.py, completing_square_generator.py, complex_quadratic_generator.py, cramers_rule_generator.py, discriminant_generator.py, error_spotting_generator.py, exponential_equation_generator.py, fill_in_step_generator.py, linear_fractional_generator.py, literal_equation_generator.py, log_equation_generator.py, one_step_equation_generator.py, polynomial_zeros_generator.py, proportion_word_problem_generator.py, proportional_relationship_generator.py, quadratic_factoring_generator.py, quadratic_generator.py, quadratic_square_root_generator.py, radical_equation_generator.py, rational_equation_generator.py, remainder_factor_theorem_generator.py, special_solution_equation_generator.py, standard_form_conversion_generator.py, trig_equation_generator.py, two_step_equation_generator.py |
| `EQ_SIMPLIFY` | 1 | `EQ_SIMPLIFY\|x + 10 = 7` | error_spotting_generator.py, fill_in_step_generator.py, linear_fractional_generator.py, two_step_equation_generator.py |
| `ESCAPE_CHECK` | 3 | `ESCAPE_CHECK\|n=1\|norm2=1\|bounded` | fractal_iteration_generator.py |
| `ESTIMATE` | 2 | `ESTIMATE\|83196 × 21041 ≈ 80000 × 20000\|1600000000` | long_division_generator.py, multi_digit_multiplication_generator.py |
| `ESTIMATE_CHECK` | 3 | `ESTIMATE_CHECK\|4.9 × 10^4\|48600\|rounded estimate` | fermi_estimation_generator.py, long_division_generator.py, multi_digit_multiplication_generator.py |
| `EUCLID_DIV` | 4 | `EUCLID_DIV\|174\|166\|1\|8` | continued_fraction_generator.py, extended_euclid_generator.py, modular_inverse_generator.py, rsa_generator.py |
| `EULER_BACKTRACK` | 3 | `EULER_BACKTRACK\|A\|route suffix A\|stack A-B-D-A-C-E` | euler_circuit_generator.py |
| `EULER_CRITERION` | 2 | `EULER_CRITERION\|28^14 mod 29\|1` | quadratic_residue_generator.py |
| `EULER_FORMULA` | 1 | `EULER_FORMULA\|χ = V - E + F` | euler_characteristic_generator.py, euler_formula_generator.py |
| `EULER_NOTE` | 2 | `EULER_NOTE\|2\|sphere-family polyhedron: χ is always 2` | euler_characteristic_generator.py |
| `EULER_ROUTE` | 2 | `EULER_ROUTE\|A-B-D-A-C-E-A\|uses 6 edges` | euler_circuit_generator.py |
| `EULER_SETUP` | 2, 3 | `EULER_SETUP\|triangular prism: V = 6, E = 9, F = 5\|V - E + F` | euler_characteristic_generator.py, euler_formula_generator.py |
| `EULER_STACK` | 2 | `EULER_STACK\|initial\|A` | euler_circuit_generator.py |
| `EULER_START` | 2 | `EULER_START\|A\|alphabetically first vertex` | euler_circuit_generator.py |
| `EULER_TRAVERSE` | 3 | `EULER_TRAVERSE\|A->B\|AB\|stack A-B` | euler_circuit_generator.py |
| `EVAL` | 1, 2, 3 | `EVAL\|f(3)\|0` | arc_length_generator.py, area_between_curves_generator.py, circle_equation_generator.py, complex_division_generator.py, composite_arithmetic_generator.py, conic_standard_form_generator.py, cramers_rule_generator.py, definite_integral_generator.py, derivative_limit_def_generator.py, determinant_generator.py, dot_product_generator.py, ellipse_features_generator.py, euler_method_generator.py, exact_ode_generator.py, five_number_summary_generator.py, function_composition_generator.py, function_operations_generator.py, horner_evaluation_generator.py, hyperbola_features_generator.py, improper_integral_generator.py, lagrange_multiplier_generator.py, legendre_construction_generator.py, limit_evaluation_generator.py, line_integral_generator.py, linear_approx_generator.py, log_conversion_generator.py, log_properties_generator.py, matrix_inverse_generator.py, mean_value_theorem_generator.py, ode_substitution_generator.py, parabola_features_generator.py, parametric_calculus_generator.py, partial_fractions_generator.py, power_series_generator.py, recursive_explicit_generator.py, regular_polygon_area_generator.py, related_rates_generator.py, remainder_factor_theorem_generator.py, riemann_sum_generator.py, row_reduction_generator.py, runge_kutta_generator.py, solid_revolution_generator.py, standard_deviation_generator.py, tangent_line_generator.py, taylor_series_generator.py, triangle_solve_generator.py, trig_equation_generator.py, trig_identity_eval_generator.py, trig_six_functions_generator.py, vector_ops_generator.py |
| `EVAL_AT_ZERO` | 2 | `EVAL_AT_ZERO\|e^0=1\|e^(2*0)=1` | mgf_generator.py |
| `EVAL_PARTIAL` | 3 | `EVAL_PARTIAL\|f_x\|10*3\|30` | gradient_generator.py, multivar_chain_rule_generator.py |
| `EVAL_SUB` | 3 | `EVAL_SUB\|p=T, q=T\|formula: q ∨ p\|T` | set_identity_membership_table_generator.py, truth_table_generator.py |
| `EVENT` | 2, 3 | `EVENT\|A\|first 11 tickets\|11` | complement_probability_generator.py, fundamental_counting_principle_generator.py, sample_space_list_generator.py, simple_probability_generator.py |
| `EV_FORMULA` | 1 | `EV_FORMULA\|E[X] = Σ x·P(x)` | expected_value_generator.py |
| `EV_SETUP` | 2 | `EV_SETUP\|P(X=2) = 1/4; P(X=5) = 1/4; P(X=6) = 1/2\|E[X]` | expected_value_generator.py |
| `EXACT_MATCH` | 2 | `EXACT_MATCH\|F_y = N\|x + g'(y) = x + 8*y + 2` | exact_ode_generator.py |
| `EXPAND` | 1, 2 | `EXPAND\|d + u\|2w + 2s + 1` | complex_locus_generator.py, direct_proof_algebra_generator.py, mobius_transform_generator.py, zf_axiom_identify_generator.py |
| `EXPECTATION` | 3 | `EXPECTATION\|E[X]=8/49\|E[Y]=8/49\|E[XY]=146/2401` | joint_distribution_generator.py |
| `EXPECTED_PAYOFF` | 1 | `EXPECTED_PAYOFF\|row1 against q` | game_theory_generator.py |
| `EXP_APPLY` | 2 | `EXP_APPLY\|x(t) = e^(At)x(0)\|x(0) = [2, -5]` | matrix_exponential_generator.py |
| `EXP_CELL` | 2 | `EXP_CELL\|(120·240)/300\|96` | chi_square_generator.py |
| `EXP_DIAG` | 2 | `EXP_DIAG\|e^(Dt)\|[[e^(4t), 0], [0, e^(5t)]]` | matrix_exponential_generator.py |
| `EXP_ENTRY` | 3 | `EXP_ENTRY\|(1,1)\|-7*e^(4t) + 8*e^(5t)\|-7*e^(4t) + 8*e^(5t)` | matrix_exponential_generator.py |
| `EXP_EXPAND` | 1 | `EXP_EXPAND\|(-15) × (-15)` | exponent_generator.py |
| `EXP_FORM` | 1 | `EXP_FORM\|e^(At) = P*e^(Dt)*P^-1` | euler_formula_generator.py, matrix_exponential_generator.py |
| `EXP_PARTIAL` | 3 | `EXP_PARTIAL\|-15\|-15\|225` | exponent_generator.py |
| `EXP_RULE_APPLY` | 3, 4 | `EXP_RULE_APPLY\|subtract\|12\|6\|6` | exponent_generator.py, exponent_mixed_rules_generator.py |
| `EXP_RULE_IDENTIFY` | 2 | `EXP_RULE_IDENTIFY\|zero_exponent\|x^0 = 1 (for x ≠ 0)` | exponent_generator.py, exponent_mixed_rules_generator.py, rational_exponent_generator.py |
| `EXP_RULE_SETUP` | 1 | `EXP_RULE_SETUP\|(sp)^0` | exponent_generator.py, exponent_mixed_rules_generator.py, rational_exponent_generator.py |
| `EXP_RULE_SIMPLIFY` | 1 | `EXP_RULE_SIMPLIFY\|1` | exponent_generator.py, exponent_mixed_rules_generator.py |
| `EXP_SETUP` | 2 | `EXP_SETUP\|-15\|2` | exponent_generator.py |
| `EXP_SUB` | 3 | `EXP_SUB\|t/tau\|6\|e^-6` | transient_circuit_generator.py |
| `EXP_VALUE` | 2 | `EXP_VALUE\|exp(-z)\|1` | activation_generator.py |
| `EXT_GCD_SETUP` | 2 | `EXT_GCD_SETUP\|174\|166` | extended_euclid_generator.py, modular_inverse_generator.py, rsa_generator.py |
| `F` | 2, 3 | `F\|4/6\|2/3` | complement_probability_generator.py, composite_arithmetic_generator.py, derangement_generator.py, fraction_decimal_percent_converter.py, fraction_op_generator.py, fundamental_counting_principle_generator.py, likelihood_language_generator.py, mixed_number_operation_generator.py, mobius_transform_generator.py, order_of_operations_generator.py, quaternion_generator.py, radical_rationalize_generator.py, rational_exponent_generator.py, rational_expr_add_sub_generator.py, repeating_decimal_generator.py, sample_space_list_generator.py, simple_probability_generator.py, slope_two_points_generator.py |
| `FACT` | 2 | `FACT\|9\|362880` | derangement_generator.py, named_distribution_generator.py, order_statistics_generator.py, young_tableaux_generator.py |
| `FACTOR` | 1, 2 | `FACTOR\|2(w + s) + 1` | direct_proof_algebra_generator.py, polynomial_inequality_generator.py, second_order_ode_generator.py, transfer_function_generator.py, undetermined_coeff_generator.py, variation_parameters_generator.py |
| `FACTOR_FORM` | 2 | `FACTOR_FORM\|42\|2 * 3 * 7` | totient_generator.py |
| `FACTOR_FOUND` | 2 | `FACTOR_FOUND\|2\|1` | totient_generator.py |
| `FACTOR_GROUP` | 3 | `FACTOR_GROUP\|4x^2 + 12x\|4x\|(x + 3)` | conic_standard_form_generator.py, curve_analysis_generator.py, derivative_limit_def_generator.py, factor_grouping_generator.py, factor_trinomial_generator.py |
| `FACTOR_PAIR_GOAL` | 2 | `FACTOR_PAIR_GOAL\|m·n = 6\|m + n = -7` | factor_trinomial_generator.py |
| `FACTOR_SETUP` | 1 | `FACTOR_SETUP\|42` | totient_generator.py |
| `FACT_CHECK` | 3 | `FACT_CHECK\|375\|1\|0` | factors_generator.py |
| `FACT_FORMULA` | 1 | `FACT_FORMULA\|6! = 1·2·3·4·5·6` | derangement_generator.py, permutation_combination_generator.py |
| `FACT_PAIR` | 2 | `FACT_PAIR\|1\|375` | factors_generator.py |
| `FACT_SETUP` | 2 | `FACT_SETUP\|6!\|expand the factorial` | permutation_combination_generator.py |
| `FACT_VALUE` | 2 | `FACT_VALUE\|16!\|20922789888000` | stars_and_bars_generator.py |
| `FCP` | 3 | `FCP\|fruits\|11\|11` | fundamental_counting_principle_generator.py |
| `FEATURE_MAP_SETUP` | 3 | `FEATURE_MAP_SETUP\|K(x,z)=(xz+2)^2\|phi(t)=(t^2,2t,2)\|x=-14,z=8` | feature_map_generator.py |
| `FEATURE_VECTOR` | 2 | `FEATURE_VECTOR\|phi(x)\|(196,-28,2)` | feature_map_generator.py |
| `FEEDBACK` | 1 | `FEEDBACK\|T=G/(1+G)` | transfer_function_generator.py |
| `FERMAT_SETUP` | 3 | `FERMAT_SETUP\|prime 19\|base 55\|exponent 89` | totient_generator.py |
| `FERMI_FACTOR` | 2 | `FERMI_FACTOR\|students\|450` | fermi_estimation_generator.py |
| `FERMI_SETUP` | 2 | `FERMI_SETUP\|school pizza slices\|slices/year` | fermi_estimation_generator.py |
| `FIELD_SETUP` | 2 | `FIELD_SETUP\|GF(2)[x]\|addition is XOR` | finite_field_generator.py |
| `FIND_SLOPE` | 2 | `FIND_SLOPE\|Given slope (m1)\|1/3` | parallel_perpendicular_line_generator.py |
| `FINITE_DIFF_SETUP` | 3 | `FINITE_DIFF_SETUP\|forward_derivative\|x0=3,h=1\|f0=16,f1=23` | finite_difference_generator.py |
| `FIN_FORMULA` | 1 | `FIN_FORMULA\|A = P(1+r)^t` | finance_generator.py |
| `FIN_SETUP` | 3 | `FIN_SETUP\|compound interest P = 2000\|r = 25%, t = 3\|ending balance` | finance_generator.py |
| `FIRSTLAW_FORMULA` | 1 | `FIRSTLAW_FORMULA\|DeltaU=Q-W` | first_law_generator.py |
| `FIRSTLAW_SETUP` | 3 | `FIRSTLAW_SETUP\|adiabatic\|Q=0\|W=12` | first_law_generator.py |
| `FIXED_CHECK` | 3 | `FIXED_CHECK\|a\|f(a) = p\|not fixed` | function_properties_generator.py |
| `FIXED_EQ` | 1 | `FIXED_EQ\|z=(az+b)/(cz+d)` | mobius_transform_generator.py |
| `FIXED_POINT` | 1 | `FIXED_POINT\|-5` | mobius_transform_generator.py |
| `FIXED_POINT_SETUP` | 3 | `FIXED_POINT_SETUP\|g(x)=5/12*x-3/2\|x0=1\|iterations=4` | fixed_point_generator.py |
| `FIXED_POINT_UPDATE` | 3 | `FIXED_POINT_UPDATE\|1\|x_0=1\|x_1=-13/12` | fixed_point_generator.py |
| `FLAG` | 2 | `FLAG\|8\|T` | error_spotting_generator.py, foundations_critic_generator.py |
| `FLIP` | 2 | `FLIP\|1\|8 → 1` | cantor_diagonal_generator.py |
| `FLOOR_DIV` | 3 | `FLOOR_DIV\|7\|2\|3` | algorithm_trace_generator.py |
| `FLOPS_SETUP` | 2 | `FLOPS_SETUP\|rule=2mnk\|m=128,d=512,h=512,o=32` | flops_memory_generator.py |
| `FLUX_SUM` | 2 | `FLUX_SUM\|(-2 - 2 + 4)*36\|0` | vector_theorem_generator.py |
| `FOCUS` | 1 | `FOCUS\|(0, 4)` | ellipse_features_generator.py, hyperbola_features_generator.py, parabola_features_generator.py |
| `FOIL_F` | 2 | `FOIL_F\|First: 2 * 7\|14` | complex_division_generator.py, complex_number_ops_generator.py, multiplying_binomials_generator.py |
| `FOIL_I` | 2 | `FOIL_I\|Inner: 9i * 7\|63i` | complex_division_generator.py, complex_number_ops_generator.py, multiplying_binomials_generator.py |
| `FOIL_L` | 2 | `FOIL_L\|Last: 9i * 8i\|72i^2` | complex_division_generator.py, complex_number_ops_generator.py, multiplying_binomials_generator.py |
| `FOIL_O` | 2 | `FOIL_O\|Outer: 2 * 8i\|16i` | complex_division_generator.py, complex_number_ops_generator.py, multiplying_binomials_generator.py |
| `FOIL_SETUP` | 1 | `FOIL_SETUP\|(2 + √3)(1 + √3)` | complex_division_generator.py, complex_number_ops_generator.py, multiplying_binomials_generator.py, radical_multiply_generator.py, trig_identity_verify_generator.py |
| `FOLD` | 2 | `FOLD\|rev("e")\|e` | peano_arithmetic_generator.py, recursive_definition_unfold_generator.py |
| `FORCE_COMPONENT` | 1 | `FORCE_COMPONENT\|parallel=m*g*sin` | newtons_laws_generator.py |
| `FORCE_EQ` | 1 | `FORCE_EQ\|T-m1*g=m1*a` | newtons_laws_generator.py |
| `FORM` | 2 | `FORM\|contrapositive\|¬¬((r ∧ q) ∧ ¬p) → ¬(r ∧ q)` | conditional_forms_generator.py, zf_axiom_identify_generator.py |
| `FORMULA` | 1, 2 | `FORMULA\|sinh x = (e^x - e^(-x))/2` | collision_generator.py, gaussian_curvature_generator.py, hyperbolic_distance_generator.py, hyperbolic_function_generator.py, or_formula_generator.py, projectile_motion_generator.py, stereographic_generator.py, uncertainty_generator.py |
| `FORM_IDENTIFY` | 2 | `FORM_IDENTIFY\|perfect_square_trinomial\|a^2 - 2ab + b^2 = (a - b)^2` | completing_square_generator.py, conic_standard_form_generator.py, ellipse_features_generator.py, factor_special_forms_generator.py, hyperbola_features_generator.py, parabola_features_generator.py, radical_multiply_generator.py, radical_rationalize_generator.py, rational_equation_generator.py, rational_exponent_generator.py, rational_expr_add_sub_generator.py, rational_expr_mult_div_generator.py |
| `FOURIER_COEF` | 1 | `FOURIER_COEF\|b_11=4/11` | fourier_series_generator.py |
| `FOURIER_SETUP` | 3 | `FOURIER_SETUP\|sawtooth\|A=2\|n=11` | fourier_series_generator.py |
| `FOUR_VECTOR_SETUP` | 3 | `FOUR_VECTOR_SETUP\|signature=+---\|p=[-7,1,0,7]\|q=[2,-2,-1,-5]` | four_vector_generator.py |
| `FRACTAL_SETUP` | 4 | `FRACTAL_SETUP\|mandelbrot\|z0=(0,0)\|c=(-1,0)\|N=5` | fractal_iteration_generator.py |
| `FRAC_BUILD` | 2 | `FRAC_BUILD\|30/56\|15/28` | conditional_probability_generator.py, geometric_probability_generator.py |
| `FRAC_REDUCE` | 2 | `FRAC_REDUCE\|-22/20\|-11/10` | angle_measure_generator.py, arc_length_generator.py, arc_sector_generator.py, complex_division_generator.py, frequency_table_generator.py, function_operations_generator.py, hyperbola_features_generator.py, implicit_diff_generator.py, improper_integral_generator.py, probability_addition_rule_generator.py, related_rates_generator.py, right_triangle_trig_generator.py |
| `FRAC_TO_DEC` | 2 | `FRAC_TO_DEC\|43/40\|1.075` | fraction_decimal_percent_converter.py, simple_probability_generator.py |
| `FREQ_SETUP` | 2 | `FREQ_SETUP\|histogram — 50-59: 8, 60-69: 14, 70-79: 4, 80-89: 2\|cumulative count up to 80-89` | frequency_table_generator.py |
| `FUNC_OP` | 2 | `FUNC_OP\|(f/g)(3)\|f(3)/g(3)` | function_composition_generator.py, function_operations_generator.py |
| `FUNC_SETUP` | 2 | `FUNC_SETUP\|t: -3, 4, 6, 7, 8; f(t): -10, 12, -11, 2, 3\|f(-3)` | domain_range_generator.py, function_composition_generator.py, function_evaluation_generator.py, function_operations_generator.py, function_table_generator.py, inverse_function_generator.py, piecewise_evaluation_generator.py, rational_function_features_generator.py |
| `FUNDAMENTAL_FORM_SETUP` | 3 | `FUNDAMENTAL_FORM_SETUP\|cylinder\|R=7\|u in [0,pi/3], v in [0,8]` | fundamental_form_generator.py |
| `GAME_SETUP` | 2 | `GAME_SETUP\|payoffs=(4,8;6,2)\|row player maximizes, column player minimizes` | game_theory_generator.py |
| `GAMMA_SETUP` | 3 | `GAMMA_SETUP\|anticommutator_entry\|gamma0,gamma1\|entry=(4,3)` | gamma_matrix_generator.py |
| `GAS_FORMULA` | 1 | `GAS_FORMULA\|P1*V1/T1=P2*V2/T2` | gas_law_generator.py, gas_stoichiometry_generator.py |
| `GAS_SETUP` | 3 | `GAS_SETUP\|combined_pressure\|P1=28, V1=29, T1=30\|V2=26, T2=8` | gas_law_generator.py |
| `GAS_STOICH_SETUP` | 3 | `GAS_STOICH_SETUP\|mass_to_gas_pressure\|CaCO3 -> CaO + CO2\|given=500 g CaCO3, gas=CO2` | gas_stoichiometry_generator.py |
| `GATE_MATRIX` | 2 | `GATE_MATRIX\|Z\|[[1,0],[0,-1]]` | quantum_gate_generator.py |
| `GAUSSIAN_CURVATURE_SETUP` | 2, 3 | `GAUSSIAN_CURVATURE_SETUP\|saddle\|z=(12x^2-23y^2)/2\|point=(0,0)` | gaussian_curvature_generator.py |
| `GAUSS_BONNET_SETUP` | 3 | `GAUSS_BONNET_SETUP\|flat_torus\|width=8, height=25\|chi=0` | gauss_bonnet_generator.py |
| `GAUSS_FORMULA` | 1 | `GAUSS_FORMULA\|E*(4πr^2)=Q` | gauss_law_generator.py |
| `GAUSS_SETUP` | 3 | `GAUSS_SETUP\|sphere\|Q=22\|r=7` | gauss_law_generator.py |
| `GCD` | 2 | `GCD\|gcd(133496,362880)\|8` | derangement_generator.py, pollard_factorization_generator.py |
| `GCD_DIV` | 4 | `GCD_DIV\|57\|43\|1\|14` | rationals_as_pairs_generator.py |
| `GCD_DONE` | 1 | `GCD_DONE\|1` | rationals_as_pairs_generator.py |
| `GCD_RESULT` | 1, 2 | `GCD_RESULT\|1` | lcm_generator.py, modular_inverse_generator.py, permutation_group_generator.py, rsa_generator.py, totient_generator.py |
| `GCD_START` | 2 | `GCD_START\|45\|118` | gcf_generator.py, lcm_generator.py, rationals_as_pairs_generator.py |
| `GCD_STEP` | 3 | `GCD_STEP\|45\|118\|45` | gcf_generator.py, lcm_generator.py |
| `GCF_COEFF` | 2 | `GCF_COEFF\|10, 35, 25\|5` | factor_gcf_generator.py, quadratic_factoring_generator.py, rational_expr_simplify_generator.py |
| `GCF_RESULT` | 1 | `GCF_RESULT\|5y` | factor_gcf_generator.py, quadratic_factoring_generator.py, rational_expr_simplify_generator.py |
| `GCF_VAR` | 2 | `GCF_VAR\|y^4, y^2, y\|y` | factor_gcf_generator.py, quadratic_factoring_generator.py, rational_expr_simplify_generator.py |
| `GD_SETUP` | 3 | `GD_SETUP\|f(x,y)=1/2*(6x^2+6y^2)\|start=(4,5)\|eta=1/11` | gradient_descent_generator.py |
| `GD_UPDATE` | 3 | `GD_UPDATE\|w_old=(-1,0)\|eta=1/4\|w_new=(7/3,37/6)` | gradient_step_generator.py |
| `GELLMANN_IDENTITY` | 3 | `GELLMANN_IDENTITY\|Tr(lambda_4 lambda_5)\|2 delta_ab\|0` | pauli_algebra_generator.py |
| `GELLMANN_SETUP` | 3 | `GELLMANN_SETUP\|trace\|A=3lambda_4\|B=2lambda_5` | pauli_algebra_generator.py |
| `GENERAL` | 2 | `GENERAL\|a_n\|C1(-2)^n + C2(-3)^n + 2` | recurrence_generator.py |
| `GEOMETRIC_FORMULA` | 2 | `GEOMETRIC_FORMULA\|c_n = A*(-1)^n/d^(n+1)\|A=6, d=-2` | laurent_series_generator.py |
| `GEOM_FORMULA` | 1 | `GEOM_FORMULA\|P(X=k) = (1-p)^(k-1) * p` | geometric_distribution_generator.py |
| `GEOM_SETUP` | 2 | `GEOM_SETUP\|p = 3/10, q = 7/10\|P(X = 2)` | geometric_distribution_generator.py |
| `GEO_PROB_FORMULA` | 1 | `GEO_PROB_FORMULA\|probability = favorable length / total length` | geometric_probability_generator.py |
| `GEO_PROB_SETUP` | 2 | `GEO_PROB_SETUP\|number line from 0 to 56\|lands between 24 and 54` | geometric_probability_generator.py |
| `GEO_SETUP` | 2 | `GEO_SETUP\|right triangle, altitude to hypotenuse; the altitude splits the hypotenuse into p = 40 and q = 52\|altitude h` | geometric_mean_generator.py |
| `GF2_XOR` | 3 | `GF2_XOR\|quotient x^4\|0 xor 1\|1` | finite_field_generator.py |
| `GF_DIV_CHECK` | 3 | `GF_DIV_CHECK\|22 / 3\|not integer\|reject` | generating_function_generator.py |
| `GF_EXPAND` | 2 | `GF_EXPAND\|1/(1 - x^2)\|sum x^(2i), i >= 0` | generating_function_generator.py |
| `GF_SETUP` | 2 | `GF_SETUP\|[x^22]\|1/((1 - x^2)(1 - x^3))` | generating_function_generator.py |
| `GIANT_FACTOR` | 2 | `GIANT_FACTOR\|g^-m mod p\|2` | baby_step_giant_step_generator.py |
| `GIANT_STEP` | 2 | `GIANT_STEP\|i=0\|20` | baby_step_giant_step_generator.py |
| `GLB` | 1 | `GLB\|none` | partial_order_generator.py |
| `GOAL` | 1 | `GOAL\|show d + 1 is even` | direct_proof_algebra_generator.py, point_slope_generator.py, standard_form_conversion_generator.py |
| `GODEL_DECODE` | 2 | `GODEL_DECODE\|1, 5, 4\|p ) q` | godel_numbering_generator.py |
| `GODEL_TERM` | 2 | `GODEL_TERM\|2^3\|8` | godel_numbering_generator.py |
| `GRAD` | 2 | `GRAD\|1\|-2/3` | softmax_gradient_generator.py |
| `GRADIENT_FORMULA` | 1 | `GRADIENT_FORMULA\|grad=(6x,6y)` | gradient_descent_generator.py, matrix_calculus_generator.py |
| `GRAD_ENTRY` | 2 | `GRAD_ENTRY\|g1\|16` | matrix_calculus_generator.py |
| `GRAD_RESULT` | 2 | `GRAD_RESULT\|grad g\|(1, 4)` | lagrange_multiplier_generator.py |
| `GRAD_SETUP` | 3 | `GRAD_SETUP\|f(x,y) = 5*x^2 + 4*y^2 + 3*x*y + 2*y\|point (3, 0)\|tangent` | gradient_generator.py |
| `GRAPH_CHANGE` | 3 | `GRAPH_CHANGE\|Mon\|Tue\|4` | graph_interpret_generator.py |
| `GRAPH_DATA` | 2 | `GRAPH_DATA\|pictograph\|key:■=10` | graph_interpret_generator.py |
| `GRAPH_MAX` | 2 | `GRAPH_MAX\|Salad\|12` | graph_interpret_generator.py |
| `GRAPH_MAX_CHANGE` | 3 | `GRAPH_MAX_CHANGE\|Wed\|Thu\|8` | graph_interpret_generator.py |
| `GRAPH_MIN` | 2 | `GRAPH_MIN\|Bananas\|13` | graph_interpret_generator.py |
| `GRAPH_READ` | 2 | `GRAPH_READ\|Mon\|17` | graph_interpret_generator.py |
| `GRAPH_SETUP` | 2 | `GRAPH_SETUP\|directed adjacency matrix\|3 vertices` | dijkstra_generator.py, euler_circuit_generator.py, graph_counting_generator.py, graph_traversal_generator.py |
| `GRASSMANN_RESULT` | 3 | `GRASSMANN_RESULT\|constant=1\|theta=6\|1 + 6theta` | grassmann_generator.py |
| `GRASSMANN_SETUP` | 3 | `GRASSMANN_SETUP\|integrate\|expr=7 + 8theta\|int1=0,inttheta=1` | grassmann_generator.py |
| `GREATEST` | 1 | `GREATEST\|none` | partial_order_generator.py |
| `GREAT_CIRCLE_SETUP` | 3 | `GREAT_CIRCLE_SETUP\|R=18\|A=(0,-120)\|B=(60,-120)` | great_circle_generator.py |
| `GROUP` | 2 | `GROUP\|(4x^2 + 12x)\|(3x + 9)` | factor_grouping_generator.py, factor_trinomial_generator.py |
| `GROUP_MULT` | 3 | `GROUP_MULT\|e\|e\|e` | coset_generator.py |
| `GROUP_SETUP` | 2, 3 | `GROUP_SETUP\|Z_7\|addition mod n` | cayley_table_generator.py, coset_generator.py, cyclic_group_generator.py |
| `GS_SETUP` | 2 | `GS_SETUP\|vectors [[2, 1], [-5, 0]]\|orthogonal basis, not normalized` | gram_schmidt_generator.py |
| `GS_SUBTRACT` | 2 | `GS_SUBTRACT\|remove projection on u1\|[-1, 2]` | gram_schmidt_generator.py, qr_decomposition_generator.py |
| `GS_VECTOR` | 2 | `GS_VECTOR\|u1 = v1\|[2, 1]` | gram_schmidt_generator.py |
| `HA` | 1 | `HA\|y = 0` | rational_function_features_generator.py |
| `HAMILTON` | 2 | `HAMILTON\|i*i\|-1` | quaternion_generator.py |
| `HAMILTONIAN` | 1 | `HAMILTONIAN\|H=p_y^2/(2(m1+m2))+(m1-m2)g*y` | hamiltonian_generator.py |
| `HAMMING_PLACE` | 2 | `HAMMING_PLACE\|positions 1,2,3,4,5,6,7\|p1,p2,d1,p4,d2,d3,d4` | hamming_code_generator.py |
| `HAMMING_RECEIVED` | 1 | `HAMMING_RECEIVED\|r=1010001` | hamming_code_generator.py |
| `HAMMING_SETUP` | 2 | `HAMMING_SETUP\|data=1111\|even parity` | hamming_code_generator.py |
| `HAM_EQ` | 2 | `HAM_EQ\|ydot=dH/dp_y\|ydot=p_y/24` | hamiltonian_generator.py |
| `HAM_SETUP` | 3 | `HAM_SETUP\|atwood\|m1=11, m2=13\|g=10, q=y, p=p_y` | hamiltonian_generator.py |
| `HARMONIC_SETUP` | 1 | `HARMONIC_SETUP\|u=x^2 - y^2 - x - y` | cauchy_riemann_generator.py |
| `HAWKING_SETUP` | 3 | `HAWKING_SETUP\|entropy\|S_BH=k_B*c^3*A/(4*hbar*G)\|k_B=1,c=4,A=13,hbar=11,G=1` | hawking_generator.py |
| `HESSIAN_DET` | 3 | `HESSIAN_DET\|D = f_xx*f_yy - f_xy^2\|(-4)*(-4) - (-1)^2\|15` | hessian_classify_generator.py |
| `HESSIAN_SETUP` | 2 | `HESSIAN_SETUP\|f(x,y) = -2*x^2 - 2*y^2 - x*y + 16*x + 4*y\|find and classify the critical point` | hessian_classify_generator.py |
| `HESSIAN_TEST` | 3 | `HESSIAN_TEST\|D = 15\|f_xx = -4\|local maximum` | hessian_classify_generator.py |
| `HIDDEN_PRE` | 2 | `HIDDEN_PRE\|h1\|z=1` | backprop_generator.py |
| `HIT_EQ` | 2 | `HIT_EQ\|t0=1+p00*t0+p01*t1\|t1=1+p10*t0+p11*t1` | markov_chain_generator.py |
| `HMM_SETUP` | 2 | `HMM_SETUP\|states H,L\|observations AAB` | viterbi_generator.py |
| `HMM_START` | 1 | `HMM_START\|H=1/2, L=1/2` | viterbi_generator.py |
| `HOLE` | 1 | `HOLE\|x = 1` | rational_function_features_generator.py |
| `HOM_SOL` | 2 | `HOM_SOL\|y_h\|y_h = C1e^(-4x) + C2e^(-3x)` | undetermined_coeff_generator.py, variation_parameters_generator.py |
| `HOOK` | 4 | `HOOK\|(1,1)\|right=3\|below=3\|hook=7` | young_tableaux_generator.py |
| `HORNER_SETUP` | 2 | `HORNER_SETUP\|3x^3 + x^2 + 2x - 5\|x = 2` | horner_evaluation_generator.py |
| `HT_SETUP` | 2 | `HT_SETUP\|H0: p = 0.5; Ha: p ≠ 0.5\|n = 25, 17 successes, critical value = 1.645` | hypothesis_test_generator.py, two_sample_test_generator.py |
| `HUFFMAN_FORMULA` | 1 | `HUFFMAN_FORMULA\|L=sum p_i*l_i` | huffman_coding_generator.py |
| `HUFFMAN_MERGE` | 2 | `HUFFMAN_MERGE\|A:1/8 + B:1/8\|AB:1/4` | huffman_coding_generator.py |
| `HUFFMAN_SETUP` | 1 | `HUFFMAN_SETUP\|A=1/8, B=1/8, C=1/8, D=1/8, E=1/4, F=1/8, G=1/8` | huffman_coding_generator.py |
| `HYDROGEN_FORMULA` | 1 | `HYDROGEN_FORMULA\|1/lambda=R_L*(1/n_low^2-1/n_high^2)` | hydrogen_atom_generator.py |
| `HYDROGEN_SETUP` | 3 | `HYDROGEN_SETUP\|transition_wavelength\|n_low=4, n_high=9\|R_L=2 1/m` | hydrogen_atom_generator.py |
| `HYPERBOLIC_DISTANCE_SETUP` | 3 | `HYPERBOLIC_DISTANCE_SETUP\|half-plane\|P=(6,12)\|Q=(6,264/17)` | hyperbolic_distance_generator.py |
| `HYPERBOLIC_SETUP` | 2 | `HYPERBOLIC_SETUP\|e^x=31/17\|e^(-x)=17/31` | hyperbolic_function_generator.py |
| `HYPERCUBE_FORMULA` | 1 | `HYPERCUBE_FORMULA\|diagonal = s·√n` | hypercube_counting_generator.py |
| `HYPERCUBE_SETUP` | 2 | `HYPERCUBE_SETUP\|2-cube with side 8\|main diagonal` | hypercube_counting_generator.py |
| `I` | 2 | `I\|7/2\|2/7` | fraction_op_generator.py, mixed_number_operation_generator.py, rational_expr_mult_div_generator.py |
| `ICE_ROW` | 2 | `ICE_ROW\|initial\|[A]=6, [B]=0` | equilibrium_ice_generator.py |
| `IDENTIFY` | 2 | `IDENTIFY\|order does not matter\|use C(n, r)` | permutation_combination_generator.py |
| `IDENTITY` | 2 | `IDENTITY\|hockey-stick\|Σ i=10..88 C(i,10) = C(89,11)` | counting_classics_generator.py, function_inner_product_generator.py, index_gymnastics_generator.py |
| `IDENTITY_SETUP` | 2 | `IDENTITY_SETUP\|verify: 1/(1 - cos x) + 1/(1 + cos x) = 2/sin^2 x\|transform the left side` | trig_identity_verify_generator.py |
| `IDENT_MATCH` | 1 | `IDENT_MATCH\|2/sin^2 x = 2/sin^2 x` | trig_identity_verify_generator.py |
| `IDENT_SUB` | 1, 2 | `IDENT_SUB\|1 - cos^2 x = sin^2 x` | parametric_calculus_generator.py, trig_identity_verify_generator.py |
| `IE_FORMULA` | 2 | `IE_FORMULA\|n(A union B union C)\|n(A)+n(B)+n(C) - n(AB)-n(AC)-n(BC) + n(ABC)` | inclusion_exclusion_generator.py |
| `IE_SETUP` | 2 | `IE_SETUP\|n(A)=46, n(B)=31, n(C)=29\|n(AB)=10, n(AC)=16, n(BC)=8, n(ABC)=5` | inclusion_exclusion_generator.py |
| `IFACTOR` | 2 | `IFACTOR\|mu = e^(∫ 3 dx)\|e^(3x)` | integrating_factor_generator.py, ode_substitution_generator.py |
| `IG_SETUP` | 3 | `IG_SETUP\|parent pos=2, neg=14\|total=16\|splits=source,region` | information_gain_generator.py |
| `IMAGE` | 2 | `IMAGE\|n\|24` | function_properties_generator.py, mobius_transform_generator.py |
| `IMPLICIT_DIFF` | 2 | `IMPLICIT_DIFF\|d/dx of x^2\|2x` | implicit_diff_generator.py, log_diff_higher_order_generator.py, related_rates_generator.py |
| `IMPLICIT_SETUP` | 2 | `IMPLICIT_SETUP\|x^2 + y^2 = 36\|dy/dx` | implicit_diff_generator.py |
| `IMPROPER_TO_MIX` | 2 | `IMPROPER_TO_MIX\|477/55\|8 37/55` | composite_arithmetic_generator.py, mixed_number_operation_generator.py, order_of_operations_generator.py |
| `INDEGREE` | 2 | `INDEGREE\|A\|0` | graph_traversal_generator.py |
| `INDEGREE_UPDATE` | 2 | `INDEGREE_UPDATE\|B\|0` | graph_traversal_generator.py |
| `INDEP_CHECK` | 3 | `INDEP_CHECK\|P11=146/2401\|product=64/2401\|no` | joint_distribution_generator.py |
| `INDEP_FORMULA` | 1 | `INDEP_FORMULA\|independent iff P11=P(X=1)P(Y=1)` | joint_distribution_generator.py |
| `INDEX` | 3 | `INDEX\|G size 24\|H size 2\|12` | coset_generator.py |
| `INDEX_METRIC` | 3 | `INDEX_METRIC\|lower\|Minkowski\|g_ii=[-1,1,1,1]` | index_raising_generator.py |
| `INDEX_SETUP` | 3 | `INDEX_SETUP\|c=-4\|j=2, k=1\|l=2, m=1` | index_gymnastics_generator.py |
| `INDUCT_ASSUME` | 1, 2 | `INDUCT_ASSUME\|n = 4a + 5b\|a,b nonnegative` | induction_verify_generator.py |
| `INDUCT_BASE` | 2 | `INDUCT_BASE\|n=12\|12 = 4·3 + 5·0` | induction_verify_generator.py |
| `INDUCT_STEP` | 1, 2 | `INDUCT_STEP\|n → n+4\|n+4 = 4(a+1) + 5b` | induction_verify_generator.py |
| `INEQ_FLIP` | 1 | `INEQ_FLIP\|Multiplying by negative number reverses inequality` | domain_range_generator.py, linear_fractional_generator.py, one_step_inequality_generator.py, two_step_inequality_generator.py |
| `INEQ_OP_ALL` | 3 | `INEQ_OP_ALL\|subtract\|3\|-21 < 3x < 15` | absolute_value_inequality_generator.py, compound_inequality_generator.py |
| `INEQ_OP_BOTH` | 4 | `INEQ_OP_BOTH\|multiply\|8\|x\|32` | domain_range_generator.py, linear_fractional_generator.py, one_step_inequality_generator.py, two_step_inequality_generator.py |
| `INEQ_RESULT` | 3 | `INEQ_RESULT\|x\|<\|32` | domain_range_generator.py, linear_fractional_generator.py, one_step_inequality_generator.py, two_step_inequality_generator.py |
| `INEQ_SETUP` | 1 | `INEQ_SETUP\|x/8 < 4` | linear_fractional_generator.py, one_step_inequality_generator.py, polynomial_inequality_generator.py, two_step_inequality_generator.py |
| `INEQ_SIMPLIFY` | 1 | `INEQ_SIMPLIFY\|x/-2 ≥ -2` | domain_range_generator.py, linear_fractional_generator.py, two_step_inequality_generator.py |
| `INEX_TERM` | 3 | `INEX_TERM\|0\|1×2^6\|64` | function_properties_generator.py |
| `INFO_GAIN` | 2 | `INFO_GAIN\|source\|0.13825` | information_gain_generator.py |
| `INFO_SETUP` | 2 | `INFO_SETUP\|p=1/32768\|I=-log2(p)` | entropy_generator.py |
| `INFO_TABLE` | 1 | `INFO_TABLE\|1/8=3, 1/4=2, 3/4=0.415, 7/8=0.193, 1=0` | information_gain_generator.py |
| `INFO_VALUE` | 2 | `INFO_VALUE\|p=1/8\|I=3` | information_gain_generator.py |
| `INITIAL` | 2 | `INITIAL\|D_0 = 1\|D_1 = 0` | derangement_generator.py |
| `INITIAL_COEFF` | 2 | `INITIAL_COEFF\|a_0\|12600` | series_solution_generator.py |
| `INITIAL_EQ` | 2 | `INITIAL_EQ\|C1 + C2\|7` | recurrence_generator.py |
| `INITIAL_SYSTEM` | 2 | `INITIAL_SYSTEM\|C1[2, 1] + C2[1, 0]\|[6, 1]` | ode_system_generator.py |
| `INNER_ANTIDERIV` | 2 | `INNER_ANTIDERIV\|dx\|6*x` | double_integral_generator.py, triple_integral_generator.py |
| `INNER_EVAL` | 2, 3 | `INNER_EVAL\|x=y/3..5\|6*(5 - y/3)` | double_integral_generator.py, triple_integral_generator.py |
| `INNER_PRODUCT` | 2 | `INNER_PRODUCT\|inner(phi,psi)\|6+2i` | braket_generator.py |
| `INNER_PRODUCT_SETUP` | 3 | `INNER_PRODUCT_SETUP\|interval=[0,2pi]\|f=sin(31x)\|g=cos(16x)` | function_inner_product_generator.py |
| `INSERT_KEY` | 3 | `INSERT_KEY\|pass 1\|4\|index 1` | algorithm_trace_generator.py |
| `INSERT_PLACE` | 2 | `INSERT_PLACE\|index 0\|4, 17, 31, 13, 25` | algorithm_trace_generator.py |
| `INTEGRAL` | 1, 2 | `INTEGRAL\|integral sin(47x) on [0,2pi]\|0` | fourier_series_generator.py, function_inner_product_generator.py, legendre_construction_generator.py |
| `INTEGRAL_SETUP` | 1 | `INTEGRAL_SETUP\|L = integral from r0 to r1 of 1 dr` | metric_arc_length_generator.py |
| `INTEGRATE` | 2 | `INTEGRATE\|v_y = u_x\|v=2xy + x - y + phi(x)` | cauchy_riemann_generator.py |
| `INTEGRATION_BY_PARTS` | 2 | `INTEGRATION_BY_PARTS\|u=x\|dv=sin(nx)dx` | fourier_series_generator.py |
| `INTEG_RULE` | 2 | `INTEG_RULE\|exponential rule\|∫ e^(kx) dx = e^(kx)/k + C` | antiderivative_generator.py, definite_integral_generator.py, ode_substitution_generator.py, partial_fractions_generator.py, separable_ode_generator.py, solid_revolution_generator.py, u_substitution_generator.py |
| `INTEG_SETUP` | 2 | `INTEG_SETUP\|∫ -15e^(3x) dx\|antiderivative` | antiderivative_generator.py, arc_length_generator.py, definite_integral_generator.py, improper_integral_generator.py, integration_by_parts_generator.py, parametric_calculus_generator.py, partial_fractions_generator.py, u_substitution_generator.py |
| `INTERCEPT_FORMULA` | 1 | `INTERCEPT_FORMULA\|a = ȳ - b·x̄` | regression_generator.py |
| `INTERFERENCE_FORMULA` | 1 | `INTERFERENCE_FORMULA\|d*sin(theta)=m*lambda` | interference_generator.py |
| `INTERFERENCE_SETUP` | 3 | `INTERFERENCE_SETUP\|diffraction_grating\|m=5, lambda=10\|d=95` | interference_generator.py |
| `INTERP_SETUP` | 3 | `INTERP_SETUP\|newton\|points=(-4,34), (-1,1), (3,41)\|x=-6` | interpolation_generator.py |
| `INTERVAL_CLASS` | 2 | `INTERVAL_CLASS\|s2=851\|timelike` | minkowski_interval_generator.py |
| `INT_ABS` | 2 | `INT_ABS\|-18\|18` | integer_operations_generator.py |
| `INT_ALIGN` | 2 | `INT_ALIGN\|82320\|65750` | multi_digit_addition_generator.py, multi_digit_subtraction_generator.py |
| `INT_APPLY_SIGN` | 3 | `INT_APPLY_SIGN\|12\|negative\|-12` | integer_operations_generator.py |
| `INT_OP` | 4 | `INT_OP\|-\|18\|6\|12` | integer_operations_generator.py |
| `INT_REWRITE` | 2 | `INT_REWRITE\|-9 - (-5)\|-9 + 5` | integer_operations_generator.py |
| `INT_SIGN_RULE` | 2 | `INT_SIGN_RULE\|different_signs\|Different signs: subtract absolute values, take sign of larger absolute value` | integer_operations_generator.py |
| `INVARIANT` | 3 | `INVARIANT\|sizes\|3\|4` | structure_isomorphism_generator.py |
| `INVERSE_LAPLACE` | 2 | `INVERSE_LAPLACE\|-2/(s + 5)\|-2e^(-5t)` | laplace_ivp_generator.py |
| `INVERSE_MAP` | 2 | `INVERSE_MAP\|x=(u+v)/2\|y=(u-v)/2` | rv_transform_generator.py |
| `INVERSE_METRIC` | 2 | `INVERSE_METRIC\|g^phiphi=1/R^2\|g^thetatheta=1/(R^2 sin^2(phi))` | christoffel_generator.py, riemann_tensor_generator.py |
| `INVERSE_PAIR` | 2 | `INVERSE_PAIR\|(g, 23)\|(23, g)` | function_properties_generator.py, relation_operations_generator.py |
| `INV_FORMULA` | 1 | `INV_FORMULA\|A⁻¹ = (1/det)·[[d, -b], [-c, a]]` | matrix_inverse_generator.py |
| `IRR_SETUP` | 2 | `IRR_SETUP\|c0=-2900,c1=7250\|r0=0,iterations=2` | npv_irr_generator.py |
| `IRR_VALUE` | 2 | `IRR_VALUE\|f1\|4350` | npv_irr_generator.py |
| `ITERATE` | 2 | `ITERATE\|n=1\|z=(-1,0)` | fractal_iteration_generator.py, gradient_descent_generator.py |
| `IVT_SETUP` | 2 | `IVT_SETUP\|f(x) = x^3 + x + 1 on [2, 4]\|does the IVT guarantee a root?` | mean_value_theorem_generator.py |
| `I_CYCLE` | 2 | `I_CYCLE\|i^1\|i` | complex_number_ops_generator.py |
| `I_SQUARE` | 2 | `I_SQUARE\|72i^2\|-72` | complex_division_generator.py, complex_log_generator.py, complex_number_ops_generator.py |
| `JACOBIAN` | 2 | `JACOBIAN\|dA\|r dr dtheta` | double_integral_generator.py |
| `JACOBI_END` | 2 | `JACOBI_END\|a=1\|sign -1` | jacobi_symbol_generator.py |
| `JACOBI_RECIPROCITY` | 3 | `JACOBI_RECIPROCITY\|a mod 4 = 1\|n mod 4 = 1\|keep sign` | jacobi_symbol_generator.py |
| `JACOBI_SETUP` | 3 | `JACOBI_SETUP\|a=58\|n=45\|n odd` | jacobi_symbol_generator.py |
| `JACOBI_SWAP` | 3 | `JACOBI_SWAP\|a=45\|n=13\|sign 1` | jacobi_symbol_generator.py |
| `JACOBI_TWO_RULE` | 3 | `JACOBI_TWO_RULE\|n mod 8 = 5\|flip sign\|sign -1` | jacobi_symbol_generator.py |
| `JAC_DET` | 3 | `JAC_DET\|x_u*y_v - x_v*y_u\|3*3 - 2*0\|9` | jacobian_generator.py |
| `JAC_MATRIX` | 2 | `JAC_MATRIX\|[[x_u, x_v], [y_u, y_v]]\|[[3, 2], [0, 3]]` | jacobian_generator.py, rv_transform_generator.py |
| `JAC_SETUP` | 3 | `JAC_SETUP\|x = 3*u + 2*v\|y = 3*v\|d(x,y)/d(u,v)` | jacobian_generator.py |
| `JOINT_SETUP` | 3 | `JOINT_SETUP\|X,Y in {0,1}\|p00=1763/2401, p01=246/2401\|p10=246/2401, p11=146/2401` | joint_distribution_generator.py |
| `KERNEL_BASE` | 3 | `KERNEL_BASE\|A,A\|dot+c=2+1\|3` | feature_map_generator.py, kernel_evaluation_generator.py |
| `KERNEL_EXPONENT` | 2 | `KERNEL_EXPONENT\|A,A\|0` | kernel_evaluation_generator.py |
| `KERNEL_SETUP` | 3 | `KERNEL_SETUP\|type=rbf\|points=A=(-1,-2), B=(3,-1), C=(-1,-1)\|gamma=1/2` | kernel_evaluation_generator.py |
| `KERNEL_VALIDITY` | 1 | `KERNEL_VALIDITY\|psd=true` | kernel_validity_generator.py |
| `KERNEL_VALUE` | 2 | `KERNEL_VALUE\|A,A\|1` | feature_map_generator.py, kernel_evaluation_generator.py, kernel_perceptron_generator.py, kernel_ridge_generator.py |
| `KIN_FORMULA` | 1 | `KIN_FORMULA\|v = d/t` | invariant_mass_generator.py, kinematics_generator.py |
| `KIN_SETUP` | 3, 4 | `KIN_SETUP\|d = 184 kilometers\|t = 8 hours\|speed` | invariant_mass_generator.py, kinematics_generator.py |
| `KL_FORMULA` | 1 | `KL_FORMULA\|D=sum source_i*log2(source_i/target_i)` | kl_divergence_generator.py |
| `KL_SETUP` | 3 | `KL_SETUP\|P=[508/1023,7/2046,1/2]\|Q=[127/2046,448/1023,1/2]\|direction=P to Q` | kl_divergence_generator.py |
| `KMAP_GROUP` | 2 | `KMAP_GROUP\|0100, 0101\|NOT P AND Q AND NOT R` | boolean_algebra_generator.py |
| `KMAP_ROW` | 2 | `KMAP_ROW\|PQ=00\|0, 0, 0, 1` | boolean_algebra_generator.py |
| `KMAP_SETUP` | 2 | `KMAP_SETUP\|rows PQ=00,PQ=01,PQ=11,PQ=10\|columns RS=00,RS=01,RS=11,RS=10` | boolean_algebra_generator.py |
| `KMAP_SIMPLIFY` | 1 | `KMAP_SIMPLIFY\|(NOT P AND Q AND NOT R) OR (P AND NOT R AND NOT S) OR (NOT P AND NOT Q AND R AND NOT S) OR (P AND NOT Q AND R AND S)` | boolean_algebra_generator.py |
| `KMEANS_SETUP` | 2 | `KMEANS_SETUP\|points=P1=(-3,-3), P2=(5,-5), P3=(0,-2), P4=(-2,5)\|centroids=C1=(1,-2), C2=(0,0)` | kmeans_step_generator.py |
| `KNN_DISTANCE` | 3 | `KNN_DISTANCE\|P1\|label=A\|d2=13` | knn_generator.py |
| `KNN_NEIGHBORS` | 1 | `KNN_NEIGHBORS\|P1:13:A,P4:45:B,P5:74:B` | knn_generator.py |
| `KNN_SETUP` | 3 | `KNN_SETUP\|q=(-5,2)\|k=3\|training=P1=(-2,4,A), P2=(5,-4,A), P3=(4,-1,B), P4=(-2,-4,B), P5=(2,-3,B)` | knn_generator.py |
| `KNN_SORT` | 1 | `KNN_SORT\|P1:13:A,P4:45:B,P5:74:B,P3:90:B,P2:136:A` | knn_generator.py |
| `KP_EXAMPLE` | 3 | `KP_EXAMPLE\|1\|x=7,y=1\|alpha=(0,0,0)` | kernel_perceptron_generator.py |
| `KP_SETUP` | 3 | `KP_SETUP\|kernel=linear\|data=[(7,1), (3,1), (-5,-1)]\|alpha0=(0,0,0)` | kernel_perceptron_generator.py |
| `KP_TERM` | 2 | `KP_TERM\|j=1\|0` | kernel_perceptron_generator.py |
| `KRAFT_CHECK` | 2, 3 | `KRAFT_CHECK\|sum=1\|complete` | huffman_coding_generator.py, kraft_inequality_generator.py |
| `KRAFT_CLASSIFY` | 2 | `KRAFT_CLASSIFY\|slack=0\|complete` | kraft_inequality_generator.py |
| `KRAFT_FORMULA` | 1 | `KRAFT_FORMULA\|sum 2^-l_i` | huffman_coding_generator.py, kraft_inequality_generator.py |
| `KRAFT_SETUP` | 2 | `KRAFT_SETUP\|A=3, B=2, C=4, D=4, E=2, F=3, G=3\|binary prefix code` | kraft_inequality_generator.py |
| `KRAFT_TERM` | 3 | `KRAFT_TERM\|A\|l=3\|1/8` | kraft_inequality_generator.py |
| `KRR_SETUP` | 3 | `KRR_SETUP\|kernel=linear\|data=[(-6,2), (-2,-2)]\|lambda=2,x*=5` | kernel_ridge_generator.py |
| `KV_CACHE` | 2 | `KV_CACHE\|values\|18874368` | flops_memory_generator.py |
| `K_EXPR` | 1, 2 | `K_EXPR\|K = [B]^2/[A]\|0.8 = (2x)^2/(6-x)` | equilibrium_ice_generator.py |
| `L` | 2, 3 | `L\|3\|7\|21` | complement_probability_generator.py, experimental_probability_generator.py, fraction_comparison_generator.py, fraction_op_generator.py, linear_fractional_generator.py, mixed_number_operation_generator.py, rational_expr_add_sub_generator.py |
| `LABEL_COUNT` | 2 | `LABEL_COUNT\|A\|1` | knn_generator.py |
| `LADDER_APPLY` | 2 | `LADDER_APPLY\|a ket20\|sqrt(20) ket19` | ladder_operator_generator.py |
| `LADDER_COMM` | 2 | `LADDER_COMM\|[a,adag] ketn\|ket4` | ladder_operator_generator.py |
| `LADDER_RULE` | 2 | `LADDER_RULE\|J_- = J1_- + J2_-\|lower from highest weights` | clebsch_gordan_generator.py, ladder_operator_generator.py |
| `LADDER_SETUP` | 3 | `LADDER_SETUP\|number_energy\|state=ket20\|hbar=4, omega=4` | ladder_operator_generator.py |
| `LAGRANGE_EQ` | 2 | `LAGRANGE_EQ\|4*x = lambda*1\|x = lambda/4` | lagrange_multiplier_generator.py |
| `LAGRANGE_FACTOR` | 3 | `LAGRANGE_FACTOR\|L_0\|j=1\|4/3` | interpolation_generator.py |
| `LAGRANGE_SETUP` | 3 | `LAGRANGE_SETUP\|f(x,y) = 2*x^2 + 4*y^2\|constraint x + 4*y = 108\|minimize` | lagrange_multiplier_generator.py |
| `LAGRANGIAN` | 1, 2 | `LAGRANGIAN\|L=T-V` | lagrangian_generator.py |
| `LAG_SETUP` | 3 | `LAG_SETUP\|pendulum\|m=4, L=9\|g=10, q=theta` | lagrangian_generator.py |
| `LAMBDA_SETUP` | 2 | `LAMBDA_SETUP\|(((lambda d. h) (lambda c. (h c))) (h h))\|leftmost-outermost` | lambda_reduction_generator.py |
| `LAPLACE` | 2 | `LAPLACE\|L[y' + 5y]\|(sY + 1) + 5Y` | laplace_ivp_generator.py, transfer_function_generator.py |
| `LAPLACE_TABLE` | 1 | `LAPLACE_TABLE\|L{y'} = sY - y(0); L{e^(kt)} = 1/(s-k); L^-1{1/(s-k)} = e^(kt)` | laplace_ivp_generator.py |
| `LATTICE_PAIR` | 3 | `LATTICE_PAIR\|(4, 4)\|lub 4\|glb 4` | partial_order_generator.py |
| `LAURENT_SETUP` | 3 | `LAURENT_SETUP\|center a=2\|w=(z-2)\|f=6/(z-4)` | laurent_series_generator.py |
| `LAURENT_TERM` | 1 | `LAURENT_TERM\|4(z-3)^-3` | residue_generator.py |
| `LAW` | 3 | `LAW\|distributive ∧ over ∨\|p ∧ (u ∨ ¬r)\|(p ∧ u) ∨ (p ∧ ¬r)` | logical_equivalence_laws_generator.py, set_algebra_laws_generator.py |
| `LAYERNORM_SETUP` | 3 | `LAYERNORM_SETUP\|x=(5,13)\|gamma=(1,3)\|beta=(-2,0)` | layer_norm_generator.py |
| `LB` | 2 | `LB\|{14, 35}\|∅` | partial_order_generator.py |
| `LCM_FROM_GCD` | 3 | `LCM_FROM_GCD\|90*53\|1\|4770` | lcm_generator.py |
| `LCM_STEP` | 3 | `LCM_STEP\|1\|2\|2` | permutation_group_generator.py, pollard_factorization_generator.py |
| `LEADING_MINOR` | 2 | `LEADING_MINOR\|Delta1\|25` | positive_definite_generator.py |
| `LEAST` | 1 | `LEAST\|none` | induction_verify_generator.py, partial_order_generator.py |
| `LEGENDRE_RESULT` | 3 | `LEGENDRE_RESULT\|1\|1\|quadratic residue` | quadratic_residue_generator.py |
| `LEGENDRE_SETUP` | 2 | `LEGENDRE_SETUP\|a=28\|p=29` | legendre_construction_generator.py, quadratic_residue_generator.py |
| `LEVEL` | 2 | `LEVEL\|d\|7398` | type_theory_generator.py |
| `LIE_EXP_FORM` | 2 | `LIE_EXP_FORM\|e^(theta J)\|cos(theta)I + sin(theta)J` | lie_exponential_generator.py |
| `LIE_EXP_SETUP` | 4 | `LIE_EXP_SETUP\|SO3\|axis=y\|theta=1035 deg\|K=[[0, 0, 1], [0, 0, 0], [-1, 0, 0]]` | lie_exponential_generator.py |
| `LIKELIHOOD` | 2 | `LIKELIHOOD\|1/2\|even chance` | likelihood_language_generator.py |
| `LIMITING_REAGENT` | 2 | `LIMITING_REAGENT\|H2\|NH3=26/3 mol` | stoichiometry_generator.py |
| `LIMIT_CHECK` | 2 | `LIMIT_CHECK\|NH3 from N2=18 mol\|NH3 from H2=26/3 mol` | stoichiometry_generator.py |
| `LIMIT_SETUP` | 1, 2 | `LIMIT_SETUP\|lim x→0 of (√(x + 25) - 5)/x\|0/0: rationalize` | derivative_limit_def_generator.py, improper_integral_generator.py, lhopital_generator.py, limit_evaluation_generator.py, power_series_generator.py, series_convergence_generator.py |
| `LINEAR_SYSTEM` | 2 | `LINEAR_SYSTEM\|a=13/15, b=-1/5\|c=-2/9, d=1` | markov_chain_generator.py |
| `LINE_EQ` | 1 | `LINE_EQ\|-2x - 6y - 24 = 0` | complex_locus_generator.py |
| `LINE_INTEGRAL` | 3 | `LINE_INTEGRAL\|int_0^1 dot dt\|-100/2 + 50\|0` | line_integral_generator.py |
| `LINE_RELATION_SETUP` | 3 | `LINE_RELATION_SETUP\|parallel\|y = 1/3x - 4\|(-7, 6)` | parallel_perpendicular_line_generator.py |
| `LINE_SETUP` | 2 | `LINE_SETUP\|F(x,y) = <2*x - 3*y, 2*y - 3*x>\|from (3, -2) to (-2, 3)` | line_integral_generator.py |
| `LIST_MAX` | 2 | `LIST_MAX\|42/59, 9/11, 7/8\|7/8` | dedekind_cut_generator.py |
| `LLL_DONE` | 1 | `LLL_DONE\|[(2,7),(-13,0)]` | lll_reduction_generator.py |
| `LLL_SETUP` | 1 | `LLL_SETUP\|[(-11,7),(2,7)]` | lll_reduction_generator.py |
| `LOCUS_SETUP` | 3 | `LOCUS_SETUP\|z=x+iy\|p=(-4,-1)\|q=(-5,-4)` | complex_locus_generator.py |
| `LOG2` | 2 | `LOG2\|1/8\|-3` | entropy_generator.py, huffman_coding_generator.py, mutual_information_generator.py, von_neumann_entropy_generator.py |
| `LOG2_RATIO` | 3 | `LOG2_RATIO\|i=0\|ratio=8\|log=3` | kl_divergence_generator.py |
| `LOG_BOTH_SIDES` | 1 | `LOG_BOTH_SIDES\|log_10(10^x) = log_10(20)` | exponential_equation_generator.py, log_diff_higher_order_generator.py, separable_ode_generator.py |
| `LOG_EVAL` | 2 | `LOG_EVAL\|22/17\|ln(22/17)` | hyperbolic_distance_generator.py |
| `LOG_EXACT` | 2 | `LOG_EXACT\|log_8(1)\|0` | master_theorem_generator.py |
| `LOG_FORM` | 1 | `LOG_FORM\|log_b(x) = y ⟺ b^y = x` | log_conversion_generator.py, log_equation_generator.py |
| `LOG_FORMULA` | 1 | `LOG_FORMULA\|log z = ln r + i(arg + 2pi*k)` | complex_log_generator.py |
| `LOG_IDENT` | 2 | `LOG_IDENT\|ln(e) = 1\|1` | exponential_equation_generator.py, log_conversion_generator.py |
| `LOG_LIKELIHOOD` | 1 | `LOG_LIKELIHOOD\|ell(p)=8*log(p)+4*log(1-p)` | mle_generator.py |
| `LOG_ONE_TO_ONE` | 1 | `LOG_ONE_TO_ONE\|2x - 5 = x + 6` | log_equation_generator.py |
| `LOG_POWER` | 2 | `LOG_POWER\|4log_2(x)\|log_2(x^4)` | derivative_transcendental_generator.py, log_diff_higher_order_generator.py, log_properties_generator.py, ph_calculation_generator.py |
| `LOG_PRODUCT` | 1, 2 | `LOG_PRODUCT\|log_5(x) + log_5(y^3)\|log_5(xy^3)` | log_equation_generator.py, log_properties_generator.py, ph_calculation_generator.py |
| `LOG_QUOTIENT` | 2 | `LOG_QUOTIENT\|log_2(x^4) - log_2(y^4)\|log_2(x^4/y^4)` | log_properties_generator.py |
| `LOG_SETUP` | 1, 2 | `LOG_SETUP\|4log_2(x) - 4log_2(y)\|condense` | complex_log_generator.py, log_properties_generator.py |
| `LOG_SOFTMAX` | 2 | `LOG_SOFTMAX\|1\|ln(1/3)` | softmax_gradient_generator.py |
| `LOG_SUPPLIED` | 2 | `LOG_SUPPLIED\|log10(1/100)\|-2` | signal_arithmetic_generator.py |
| `LOG_TERM` | 3 | `LOG_TERM\|6\|ln(9)\|6*ln(9)` | entropy_change_generator.py |
| `LOOKUP_SUPPLIED` | 2 | `LOOKUP_SUPPLIED\|Phi(-2)\|57/2500` | named_distribution_generator.py |
| `LORA_COUNT` | 2 | `LORA_COUNT\|r*(d_in+d_out)\|134784` | param_count_generator.py |
| `LOWRANK_SETUP` | 2 | `LOWRANK_SETUP\|A=[[15,0], [0,3]]\|rank=1` | low_rank_approx_generator.py |
| `LP_CORNER_SETUP` | 3 | `LP_CORNER_SETUP\|max z=10x+7y\|0<=x<=16, 0<=y<=21\|x+y<=33` | lp_corner_generator.py |
| `LR_PHASE` | 1 | `LR_PHASE\|warmup` | lr_schedule_generator.py |
| `LR_SETUP` | 3 | `LR_SETUP\|base=3/100\|min=0\|warmup=100,total=500,t=35` | lr_schedule_generator.py |
| `LR_VALUE` | 1 | `LR_VALUE\|21/2000` | lr_schedule_generator.py |
| `LS_LINE` | 2 | `LS_LINE\|a = 9, b = -1\|ŷ = 9 - x` | least_squares_generator.py |
| `LS_SETUP` | 2 | `LS_SETUP\|points [(-3, 11), (-1, 11), (1, 9), (3, 5)]\|model y = a + bx` | least_squares_generator.py |
| `LUB` | 1 | `LUB\|none` | partial_order_generator.py |
| `LUHN_DIGIT` | 3 | `LUHN_DIGIT\|digit 1\|keep\|1 -> 1` | modular_arithmetic_generator.py |
| `LU_ENTRY` | 3 | `LU_ENTRY\|u11\|a11 = -5\|-5` | lu_decomposition_generator.py |
| `LU_RESULT` | 2 | `LU_RESULT\|L\|[[1, 0, 0], [-3, 1, 0], [0, -3, 1]]` | lu_decomposition_generator.py |
| `LU_SETUP` | 2 | `LU_SETUP\|A = [[-5, 3, -4], [15, -10, 12], [0, 3, -3]]\|unit lower L` | lu_decomposition_generator.py |
| `LZ77_EMIT` | 1 | `LZ77_EMIT\|(0,0,s)` | lz_compression_generator.py |
| `LZ77_EXPAND` | 4 | `LZ77_EXPAND\|(0,0,d)\|no copy\|then add d\|out = d` | lz_compression_generator.py |
| `LZ77_MATCH` | 4 | `LZ77_MATCH\|pos 0\|literal\|offset 0, len 0\|next s` | lz_compression_generator.py |
| `LZ77_SEARCH` | 3 | `LZ77_SEARCH\|pos 1\|start 0\|len 0` | lz_compression_generator.py |
| `LZ78_APPEND` | 2 | `LZ78_APPEND\|empty + h\|out = h` | lz_compression_generator.py |
| `LZ78_DICT` | 2 | `LZ78_DICT\|0\|empty` | lz_compression_generator.py |
| `LZ78_EMIT` | 1 | `LZ78_EMIT\|(0,m)` | lz_compression_generator.py |
| `LZ78_LOOKUP` | 2 | `LZ78_LOOKUP\|index 0\|phrase empty` | lz_compression_generator.py |
| `LZ78_MATCH` | 4 | `LZ78_MATCH\|pos 0\|phrase empty\|index 0\|next m` | lz_compression_generator.py |
| `LZ_SETUP` | 2 | `LZ_SETUP\|LZ78\|mmmmmmhhm` | lz_compression_generator.py |
| `M` | 3 | `M\|6\|99\|594` | ac_circuit_generator.py, activation_generator.py, adam_step_generator.py, angle_defect_generator.py, angle_measure_generator.py, annuity_generator.py, arc_length_generator.py, arc_sector_generator.py, arithmetic_coding_generator.py, arithmetic_sequence_generator.py, attention_generator.py, backprop_generator.py, bec_channel_generator.py, binomial_probability_generator.py, bisection_generator.py, black_scholes_generator.py, blackbody_generator.py, bond_pricing_generator.py, calorimetry_generator.py, cantor_pairing_generator.py, cardinal_arithmetic_generator.py, casimir_force_generator.py, casimir_generator.py, cayley_table_generator.py, chain_rule_generator.py, channel_capacity_generator.py, christoffel_generator.py, circle_angle_generator.py, classifier_metrics_generator.py, collision_generator.py, commutator_generator.py, complement_probability_generator.py, complex_locus_generator.py, complex_log_generator.py, composite_arithmetic_generator.py, confidence_interval_generator.py, conic_standard_form_generator.py, continued_fraction_generator.py, continuous_distribution_generator.py, contour_integral_generator.py, convolution_generator.py, coset_generator.py, countability_bijection_generator.py, counterexample_search_generator.py, counting_classics_generator.py, cramers_rule_generator.py, cross_section_generator.py, crt_generator.py, curve_analysis_generator.py, cyclic_group_generator.py, de_moivre_generator.py, decimal_div_generator.py, definite_integral_generator.py, density_matrix_generator.py, derangement_generator.py, derivative_limit_def_generator.py, derivative_power_rule_generator.py, derivative_transcendental_generator.py, determinant_generator.py, dimensional_analysis_generator.py, doppler_generator.py, dot_product_generator.py, einstein_summation_generator.py, electrostatics_generator.py, elliptic_curve_finite_field_generator.py, embedding_similarity_generator.py, energy_conservation_generator.py, entropy_change_generator.py, entropy_generator.py, entropy_rate_markov_generator.py, equilibrium_ice_generator.py, equivalence_relation_generator.py, error_spotting_generator.py, euler_method_generator.py, evaluate_expression_generator.py, expected_value_generator.py, experimental_probability_generator.py, exponential_model_generator.py, extended_euclid_generator.py, factor_special_forms_generator.py, feature_map_generator.py, fermi_estimation_generator.py, fill_in_step_generator.py, finance_generator.py, finite_difference_generator.py, finite_field_generator.py, first_law_generator.py, five_number_summary_generator.py, fixed_point_generator.py, flops_memory_generator.py, four_vector_generator.py, fourier_series_generator.py, fractal_iteration_generator.py, fraction_op_generator.py, function_composition_generator.py, function_evaluation_generator.py, function_operations_generator.py, function_properties_generator.py, function_table_generator.py, fundamental_form_generator.py, game_theory_generator.py, gas_law_generator.py, gas_stoichiometry_generator.py, gauss_bonnet_generator.py, gauss_law_generator.py, gaussian_curvature_generator.py, generating_function_generator.py, geometric_distribution_generator.py, geometric_mean_generator.py, geometric_sequence_generator.py, geometry_area_perimeter_generator.py, godel_numbering_generator.py, gradient_descent_generator.py, gradient_step_generator.py, graph_counting_generator.py, graph_interpret_generator.py, grassmann_generator.py, great_circle_generator.py, hamiltonian_generator.py, hawking_generator.py, hermitian_check_generator.py, horner_evaluation_generator.py, huffman_coding_generator.py, hydrogen_atom_generator.py, hypercube_counting_generator.py, hypothesis_test_generator.py, index_gymnastics_generator.py, index_raising_generator.py, information_gain_generator.py, integers_as_pairs_generator.py, interference_generator.py, interpolation_generator.py, invariant_mass_generator.py, joint_distribution_generator.py, kernel_evaluation_generator.py, kernel_perceptron_generator.py, kernel_ridge_generator.py, kernel_validity_generator.py, kinematics_generator.py, kl_divergence_generator.py, ladder_operator_generator.py, lagrangian_generator.py, laplace_ivp_generator.py, laurent_series_generator.py, layer_norm_generator.py, lcm_generator.py, legendre_construction_generator.py, lhopital_generator.py, limit_evaluation_generator.py, linear_approx_generator.py, log_conversion_generator.py, log_diff_higher_order_generator.py, logistic_growth_generator.py, long_division_generator.py, lp_corner_generator.py, lr_schedule_generator.py, magnetism_generator.py, markov_chain_generator.py, matrix_calculus_generator.py, matrix_group_check_generator.py, matrix_inverse_generator.py, matrix_ops_generator.py, mean_value_theorem_generator.py, method_of_moments_generator.py, metric_arc_length_generator.py, mgf_generator.py, midpoint_generator.py, mixed_number_operation_generator.py, mobius_transform_generator.py, mod_exp_generator.py, modular_inverse_generator.py, multi_step_unit_conversion_generator.py, mutual_information_generator.py, naive_bayes_generator.py, named_distribution_generator.py, natural_units_generator.py, nets_surface_area_generator.py, newton_raphson_generator.py, newtons_laws_generator.py, npv_irr_generator.py, ode_system_generator.py, operation_properties_generator.py, optics_generator.py, optimization_generator.py, or_formula_generator.py, orbital_mechanics_generator.py, order_of_operations_generator.py, order_statistics_generator.py, ordinal_arithmetic_generator.py, param_count_generator.py, parametric_calculus_generator.py, particle_in_box_generator.py, partition_function_generator.py, pca_generator.py, percent_problem_generator.py, percent_word_problem_generator.py, perceptron_generator.py, permutation_combination_generator.py, physics_formula_generator.py, piecewise_evaluation_generator.py, planck_units_generator.py, polar_parametric_generator.py, polynomial_zeros_generator.py, portfolio_generator.py, positive_definite_generator.py, primality_test_generator.py, projectile_motion_generator.py, proportion_word_problem_generator.py, proportional_relationship_generator.py, quadratic_residue_generator.py, quantization_generator.py, quantum_formula_generator.py, quark_composition_generator.py, quaternion_generator.py, radical_multiply_generator.py, radical_rationalize_generator.py, rate_conversion_generator.py, ratio_table_generator.py, rational_equation_generator.py, rational_exponent_generator.py, rationals_as_pairs_generator.py, recurrence_generator.py, recursive_definition_unfold_generator.py, recursive_explicit_generator.py, reed_solomon_generator.py, regression_generator.py, regular_polygon_area_generator.py, related_rates_generator.py, relativistic_energy_generator.py, remainder_factor_theorem_generator.py, riemann_sum_generator.py, riemann_tensor_generator.py, right_triangle_trig_generator.py, rotational_dynamics_generator.py, round_solids_generator.py, routh_hurwitz_generator.py, row_reduction_generator.py, rsa_generator.py, runge_kutta_generator.py, running_coupling_generator.py, rv_transform_generator.py, scaling_law_generator.py, schwarzschild_generator.py, second_order_ode_generator.py, segment_partition_generator.py, separable_pde_generator.py, series_solution_generator.py, set_builder_roster_generator.py, set_counting_generator.py, set_operations_generator.py, shm_generator.py, signal_arithmetic_generator.py, similar_triangles_generator.py, simplex_generator.py, solid_revolution_generator.py, solution_chem_generator.py, special_relativity_generator.py, special_right_triangle_generator.py, spherical_excess_generator.py, spherical_triangle_generator.py, standing_wave_generator.py, stars_and_bars_generator.py, statics_generator.py, stereographic_generator.py, stoichiometry_generator.py, svm_margin_generator.py, synthetic_division_generator.py, tangent_line_generator.py, taxicab_geometry_generator.py, taylor_series_generator.py, temperature_conversion_generator.py, tensor_product_generator.py, tip_bill_split_generator.py, totient_generator.py, transfer_function_generator.py, transformation_generator.py, transient_circuit_generator.py, transportation_generator.py, triangle_area_sas_generator.py, triangle_solve_generator.py, trig_identity_eval_generator.py, two_sample_test_generator.py, uncertainty_generator.py, undetermined_coeff_generator.py, unit_circle_generator.py, unit_conversion_generator.py, vector_ops_generator.py, volume_rect_prism_generator.py, von_neumann_entropy_generator.py, wavefunction_generator.py, young_tableaux_generator.py, z_score_generator.py, z_transform_generator.py |
| `MAG_FORMULA` | 1 | `MAG_FORMULA\|magnitude = √(x^2 + y^2)` | magnetism_generator.py, vector_ops_generator.py |
| `MAG_SETUP` | 3 | `MAG_SETUP\|force\|q=4, v=27\|B=3, sin=7/25` | magnetism_generator.py |
| `MAIN_CONNECTIVE` | 1 | `MAIN_CONNECTIVE\|∨` | wff_parsing_generator.py |
| `MAP` | 2 | `MAP\|a\|f(a) = p` | function_properties_generator.py |
| `MARGIN` | 2 | `MARGIN\|2/norm(w)\|2/5` | svm_margin_generator.py |
| `MARGINAL` | 1 | `MARGINAL\|P(X=0)=p00+p01` | joint_distribution_generator.py, mutual_information_generator.py |
| `MARKOV_SETUP` | 2, 3 | `MARKOV_SETUP\|two_state\|P00=3/8, P01=5/8\|P10=2/7, P11=5/7` | entropy_rate_markov_generator.py, markov_chain_generator.py |
| `MASTER_CASE` | 2 | `MASTER_CASE\|case 1\|Θ(n^2)` | master_theorem_generator.py |
| `MATMUL_FLOPS` | 2 | `MATMUL_FLOPS\|XW1\|67108864` | flops_memory_generator.py |
| `MATRIX_ADD` | 2 | `MATRIX_ADD\|P0+P1\|[[1,0],[0,1]]` | bch_generator.py, casimir_generator.py, projector_generator.py |
| `MATRIX_ENTRY` | 1 | `MATRIX_ENTRY\|P2_01=P00*P01 + P01*P11` | markov_chain_generator.py |
| `MATRIX_ENTRY_SUM` | 3 | `MATRIX_ENTRY_SUM\|(4,3)\|0 + 0\|0` | gamma_matrix_generator.py |
| `MATRIX_EXP` | 3 | `MATRIX_EXP\|e^A\|I + A\|[[1, 1, 0], [0, 1, 0], [0, 0, 1]]` | bch_generator.py |
| `MATRIX_GROUP_SETUP` | 2 | `MATRIX_GROUP_SETUP\|SL2Z\|M=[[-6,-7],[12,4]]` | matrix_group_check_generator.py |
| `MATRIX_MULT` | 2, 3 | `MATRIX_MULT\|row1 dot col1\|423801/554555401*423801/554555401+15324540/554555401*15324540/554555401\|423801/554555401` | projector_generator.py |
| `MATRIX_POWER` | 2 | `MATRIX_POWER\|K^2\|[[-1, 0, 0], [0, 0, 0], [0, 0, -1]]` | lie_exponential_generator.py |
| `MATRIX_PRODUCT` | 2 | `MATRIX_PRODUCT\|AB\|[[0, 27], [-27, 0]]` | bch_generator.py, casimir_generator.py, gamma_matrix_generator.py, pauli_algebra_generator.py, structure_constant_generator.py |
| `MATRIX_ROW` | 2 | `MATRIX_ROW\|g\|0 1` | graph_counting_generator.py, relation_operations_generator.py |
| `MATRIX_SCALE` | 2 | `MATRIX_SCALE\|1/2 ladder sum\|[[484/25, 0, 0], [0, 968/25, 0], [0, 0, 484/25]]` | bch_generator.py, casimir_generator.py |
| `MATRIX_SETUP` | 2 | `MATRIX_SETUP\|hermitian\|A=[[-19,6],[6,-19]]` | hermitian_check_generator.py |
| `MATRIX_SUB` | 2 | `MATRIX_SUB\|AB - BA\|[[0, 0, 0], [0, 0, 0], [0, -4, 0]]` | bch_generator.py |
| `MATRIX_SUM` | 1 | `MATRIX_SUM\|B=A+A^T` | matrix_calculus_generator.py |
| `MATRIX_VALUE` | 2 | `MATRIX_VALUE\|A\|[[0, -9], [-9, 0]]` | pauli_algebra_generator.py, structure_constant_generator.py |
| `MAT_ENTRY` | 2, 3 | `MAT_ENTRY\|(1,1)\|12` | lie_exponential_generator.py, matrix_calculus_generator.py, matrix_ops_generator.py |
| `MAT_SETUP` | 2 | `MAT_SETUP\|A = [[-6, -3], [-5, 1]]\|-2A` | determinant_generator.py, diagonalization_generator.py, eigenvalue_generator.py, matrix_exponential_generator.py, matrix_inverse_generator.py, matrix_ops_generator.py, row_reduction_generator.py, subspace_basis_generator.py, svd_generator.py |
| `MAX` | 2, 3 | `MAX\|10, 9\|10` | dp_table_generator.py, matrix_norm_generator.py, taxicab_geometry_generator.py |
| `MAXIMAL` | 1 | `MAXIMAL\|{12, 14, 55, 56}` | partial_order_generator.py |
| `MAXTERM` | 2 | `MAXTERM\|001\|L OR M OR NOT N` | boolean_algebra_generator.py |
| `MC_SETUP` | 3 | `MC_SETUP\|expression=x^T A x\|A=[[-2,1], [3,2]]\|x=(-4,0)` | matrix_calculus_generator.py |
| `MEAN` | 1 | `MEAN\|9` | layer_norm_generator.py |
| `MEAN_DIV` | 3 | `MEAN_DIV\|63\|9\|7` | composite_arithmetic_generator.py, five_number_summary_generator.py, regression_generator.py, simple_stats_generator.py, standard_deviation_generator.py |
| `MEASURE_BASIS` | 3 | `MEASURE_BASIS\|x\|ket+x=(ket0+ket1)/sqrt(2)\|ket-x=(ket0-ket1)/sqrt(2)` | spin_half_generator.py |
| `MEASURE_FAVORABLE` | 2 | `MEASURE_FAVORABLE\|interval length\|54 - 24 = 30` | geometric_probability_generator.py |
| `MEASURE_PROB` | 3 | `MEASURE_PROB\|computational basis\|P(0)=1/2\|P(1)=1/2` | quantum_gate_generator.py |
| `MEASURE_TOTAL` | 2 | `MEASURE_TOTAL\|total length\|56` | geometric_probability_generator.py |
| `MEDIAN_PAIR` | 2 | `MEDIAN_PAIR\|7\|8` | five_number_summary_generator.py, simple_stats_generator.py |
| `MEDIAN_PICK` | 1, 2 | `MEDIAN_PICK\|9` | five_number_summary_generator.py, simple_stats_generator.py |
| `MEMBER` | 1 | `MEMBER\|−17/41 ∈ L(√2)` | dedekind_cut_generator.py |
| `MEMBERSHIP_BAD` | 2 | `MEMBERSHIP_BAD\|type(d) = type(d) + 1\|impossible` | type_theory_generator.py |
| `MEMBERSHIP_OK` | 1 | `MEMBERSHIP_OK\|type(v) = type(h) + 1` | type_theory_generator.py |
| `MEMBER_ROW` | 1, 3 | `MEMBER_ROW\|x∈V, x∈Y, x∈Z` | foundations_critic_generator.py, set_identity_membership_table_generator.py |
| `MEMORY_SETUP` | 3 | `MEMORY_SETUP\|kv_cache\|L=24,h=4,d_k=96\|seq=1024,precision_bytes=2` | flops_memory_generator.py |
| `MEMORY_UNIT` | 2 | `MEMORY_UNIT\|MiB\|36` | flops_memory_generator.py |
| `MERGE_BEGIN` | 3 | `MERGE_BEGIN\|merge 1\|lo=0,mid=1,hi=2\|left 23; right 33` | algorithm_trace_generator.py |
| `MERGE_COMPARE` | 3 | `MERGE_COMPARE\|23\|33\|take left` | algorithm_trace_generator.py |
| `MERGE_DONE` | 3 | `MERGE_DONE\|merge 1\|range 0-1\|array 23, 33, 12, 21, 6` | algorithm_trace_generator.py |
| `MERGE_TAKE` | 2 | `MERGE_TAKE\|23\|merged 23` | algorithm_trace_generator.py |
| `METRIC` | 2 | `METRIC\|Chebyshev\|d = max(abs(x2 - x1), abs(y2 - y1))` | taxicab_geometry_generator.py |
| `METRICS_SETUP` | 1 | `METRICS_SETUP\|TP=29, FP=28, FN=17, TN=44` | classifier_metrics_generator.py |
| `METRIC_ARC_SETUP` | 3 | `METRIC_ARC_SETUP\|polar metric\|ds^2=dr^2+r^2 dtheta^2\|theta=120 deg, r:20->36` | metric_arc_length_generator.py |
| `METRIC_FORMULA` | 1 | `METRIC_FORMULA\|precision=TP/(TP+FP)` | classifier_metrics_generator.py |
| `METRIC_RESTRICT` | 2 | `METRIC_RESTRICT\|dtheta=0\|ds^2=dr^2` | metric_arc_length_generator.py |
| `MGF_SETUP` | 3 | `MGF_SETUP\|P(X=0)=8/23\|P(X=1)=2/23\|P(X=2)=13/23` | mgf_generator.py |
| `MGF_TERM` | 3 | `MGF_TERM\|x=0\|p0*e^(0t)\|8/23` | mgf_generator.py |
| `MIDDLE_EVAL` | 3 | `MIDDLE_EVAL\|phi=0..pi\|int sin(phi) dphi = 2\|2` | triple_integral_generator.py |
| `MIDLINE` | 1 | `MIDLINE\|y = -6` | sinusoid_features_generator.py |
| `MIDPOINT` | 2 | `MIDPOINT\|iter 1\|3` | algorithm_trace_generator.py |
| `MID_FORMULA` | 1 | `MID_FORMULA\|M = ((x1 + x2)/2, (y1 + y2)/2)` | circle_equation_generator.py, midpoint_generator.py |
| `MIN` | 2 | `MIN\|81,64\|64` | matrix_norm_generator.py |
| `MIN3` | 4 | `MIN3\|2\|2\|1\|1` | dp_table_generator.py |
| `MINIMAL` | 1 | `MINIMAL\|{12, 14, 44}` | partial_order_generator.py |
| `MINKOWSKI_FORMULA` | 1 | `MINKOWSKI_FORMULA\|s2=ct^2-x^2` | minkowski_interval_generator.py |
| `MINKOWSKI_SETUP` | 3 | `MINKOWSKI_SETUP\|interval_classification\|ct=-30\|x=7` | minkowski_interval_generator.py |
| `MINTERM` | 2 | `MINTERM\|0001\|NOT Q AND NOT R AND NOT S AND T` | boolean_algebra_generator.py |
| `MIN_INITIAL` | 3 | `MIN_INITIAL\|nonaccept A, B\|accept C\|{A,B}, {C}` | dfa_minimization_generator.py |
| `MIN_REFINE` | 2 | `MIN_REFINE\|round 1\|{A}, {B}, {C}` | dfa_minimization_generator.py |
| `MIN_SIGNATURE` | 3 | `MIN_SIGNATURE\|round 1\|A\|0->B0,1->B0` | dfa_minimization_generator.py |
| `MIN_STABLE` | 1 | `MIN_STABLE\|{A}, {B}, {C}` | dfa_minimization_generator.py |
| `MIN_TRANSITION` | 3 | `MIN_TRANSITION\|{A}\|0\|{A}` | dfa_minimization_generator.py |
| `MISSED` | 1 | `MISSED\|4` | function_properties_generator.py |
| `MIX_FORMULA` | 2 | `MIX_FORMULA\|q=(d-b)/(a-b-c+d)\|p=(d-c)/(a-b-c+d)` | game_theory_generator.py |
| `MIX_IMPROPER` | 2 | `MIX_IMPROPER\|2 2/7\|16/7` | composite_arithmetic_generator.py, mixed_number_operation_generator.py, order_of_operations_generator.py |
| `MI_FORMULA` | 1 | `MI_FORMULA\|I=H(X)+H(Y)-H(X,Y)` | mutual_information_generator.py |
| `MI_SETUP` | 2 | `MI_SETUP\|rows=[[0,1/4,0,0];[1/8,0,0,1/8];[0,0,1/2,0]]\|task=I(X;Y)` | mutual_information_generator.py |
| `MLE_SETUP` | 2, 3 | `MLE_SETUP\|bernoulli\|parameter=p\|data=[0,1,0,0,1,1,1,1,0,1,1,1]` | mle_generator.py |
| `MOBIUS_SETUP` | 2 | `MOBIUS_SETUP\|T(z)=(-4z + 1)/(3z - 5)\|z0=-5` | mobius_transform_generator.py |
| `MODE` | 2 | `MODE\|2\|10, 13` | frequency_table_generator.py, simple_stats_generator.py |
| `MODEL` | 1 | `MODEL\|A = P(1 + r)^t` | exponential_model_generator.py |
| `MODEL_APPLY` | 1 | `MODEL_APPLY\|A = 39800 · (1 + 0.63)^2` | exponential_model_generator.py |
| `MODEL_OUTPUT` | 1 | `MODEL_OUTPUT\|3` | activation_generator.py |
| `MODEXP_MULTIPLY` | 2 | `MODEXP_MULTIPLY\|bit 1=1\|41` | mod_exp_generator.py, quadratic_residue_generator.py |
| `MODEXP_SETUP` | 3 | `MODEXP_SETUP\|base 41\|exponent 57\|modulus 58` | mod_exp_generator.py |
| `MODEXP_SQUARE` | 2 | `MODEXP_SQUARE\|bit 1=1\|1` | mod_exp_generator.py, quadratic_residue_generator.py |
| `MODEXP_STATE` | 2 | `MODEXP_STATE\|after bit 1\|41` | mod_exp_generator.py, quadratic_residue_generator.py |
| `MODE_COUNT` | 2 | `MODE_COUNT\|1\|1` | simple_stats_generator.py |
| `MOD_INVERSE` | 2 | `MOD_INVERSE\|17 mod 7\|5` | crt_generator.py, ecdsa_generator.py, elliptic_curve_finite_field_generator.py, modular_inverse_generator.py, rsa_generator.py |
| `MOD_NORMALIZE` | 3 | `MOD_NORMALIZE\|-2\|mod 7\|5` | modular_inverse_generator.py, rsa_generator.py |
| `MOD_POWER` | 3 | `MOD_POWER\|5^0\|mod 42\|1` | diffie_hellman_generator.py, pollard_factorization_generator.py, primality_test_generator.py, rsa_generator.py, tonelli_shanks_generator.py, totient_generator.py |
| `MOD_REDUCE` | 3 | `MOD_REDUCE\|202\|mod 11\|4` | calendar_arithmetic_generator.py, cayley_table_generator.py, coset_generator.py, crt_generator.py, cyclic_group_generator.py, de_moivre_generator.py, elliptic_curve_finite_field_generator.py, finite_field_generator.py, jacobi_symbol_generator.py, lie_exponential_generator.py, mod_exp_generator.py, modular_arithmetic_generator.py, modular_inverse_generator.py, primality_test_generator.py, quadratic_residue_generator.py, reed_solomon_generator.py, rsa_generator.py, totient_generator.py |
| `MOD_SETUP` | 2, 3, 4 | `MOD_SETUP\|ISBN-10 modulus 11\|prefix 644154034` | modular_arithmetic_generator.py, modular_inverse_generator.py |
| `MOD_SOLVE` | 2 | `MOD_SOLVE\|d ≡ -4 mod 11\|7` | modular_arithmetic_generator.py |
| `MOD_TERM` | 2 | `MOD_TERM\|10 * 6\|60` | modular_arithmetic_generator.py |
| `MOE_FORMULA` | 1 | `MOE_FORMULA\|E = z*·σ/√n` | confidence_interval_generator.py |
| `MOLAR_MASS` | 2 | `MOLAR_MASS\|H2\|2 g/mol` | gas_stoichiometry_generator.py, stoichiometry_generator.py |
| `MOLAR_VOLUME` | 2 | `MOLAR_VOLUME\|1 mol gas\|24 L` | stoichiometry_generator.py |
| `MOMENT` | 2 | `MOMENT\|m1\|-9/10` | adam_step_generator.py |
| `MOMENTUM` | 1 | `MOMENTUM\|x components` | collision_generator.py |
| `MOMENT_X` | 3 | `MOMENT_X\|M_x = 1/2 int y^2 dx\|5^2*4^3/6\|800/3` | centroid_generator.py |
| `MOMENT_Y` | 3 | `MOMENT_Y\|M_y = int x*y dx\|5*4^3/3\|320/3` | centroid_generator.py |
| `MOM_EQUATION` | 2 | `MOM_EQUATION\|E[X]=theta/2\|xbar=theta/2` | method_of_moments_generator.py |
| `MOM_SETUP` | 3 | `MOM_SETUP\|uniform_zero_theta\|parameter=theta\|data=[11,16,3,9,8,6,11,16,18]` | method_of_moments_generator.py |
| `MONO_ADD_EXP` | 2 | `MONO_ADD_EXP\|x^9 * x^9 = x^(9+9)\|x^18` | monomial_mult_div_generator.py |
| `MONO_DIV_COEFF` | 2 | `MONO_DIV_COEFF\|-4 / -1\|4` | monomial_mult_div_generator.py |
| `MONO_MULT_COEFF` | 2 | `MONO_MULT_COEFF\|-7 * -9\|63` | monomial_mult_div_generator.py |
| `MONO_SETUP` | 1 | `MONO_SETUP\|(-4x^6) / (-x^3)` | monomial_mult_div_generator.py |
| `MONO_SUB_EXP` | 2 | `MONO_SUB_EXP\|x^6 / x^3 = x^(6-3)\|x^3` | monomial_mult_div_generator.py |
| `MOOD` | 2 | `MOOD\|AII\|figure 4` | syllogism_generator.py |
| `MOVE_TERM` | 2, 3 | `MOVE_TERM\|+5x\|left\|3x-7-5x = -7` | area_between_curves_generator.py, completing_square_generator.py, conic_standard_form_generator.py, linear_complex_generator.py, polar_parametric_generator.py, quadratic_factoring_generator.py, quadratic_square_root_generator.py, radical_equation_generator.py, special_solution_equation_generator.py, standard_form_conversion_generator.py |
| `MP` | 2 | `MP\|lines 1,2\|(d → ¬j) → (¬e → ((k ∨ n) → ¬e))` | hilbert_axiom_derivation_generator.py |
| `MR_DECOMPOSE` | 2 | `MR_DECOMPOSE\|220\|2^2 * 55` | primality_test_generator.py |
| `MR_SETUP` | 2 | `MR_SETUP\|n=221\|witnesses 3, 9` | primality_test_generator.py |
| `MR_SQUARE` | 2 | `MR_SQUARE\|r=1\|87` | primality_test_generator.py |
| `MR_WITNESS` | 1 | `MR_WITNESS\|3` | primality_test_generator.py |
| `MR_WITNESS_RESULT` | 2 | `MR_WITNESS_RESULT\|3\|composite` | primality_test_generator.py |
| `MSE_FORMULA` | 2 | `MSE_FORMULA\|L=(1/n) sum r_i^2\|grad=(2/n) sum r_i*[1,x_i]` | gradient_step_generator.py |
| `MSE_GRADIENT` | 2 | `MSE_GRADIENT\|g0=-40/3\|g1=-74/3` | gradient_step_generator.py |
| `MSE_SAMPLE` | 3 | `MSE_SAMPLE\|i=1\|pred=-1\|r=-8` | gradient_step_generator.py |
| `MSE_SETUP` | 3 | `MSE_SETUP\|model y_hat=w0+w1*x\|samples=[(2,7), (3,6), (0,4)]\|w=(-1,0), eta=1/4` | gradient_step_generator.py |
| `MST_ADD` | 2 | `MST_ADD\|AC\|total 3` | mst_generator.py |
| `MST_SET` | 1 | `MST_SET\|AC` | mst_generator.py |
| `MST_SETUP` | 2 | `MST_SETUP\|weighted undirected graph\|vertices A, B, C, D` | mst_generator.py |
| `MU` | 2 | `MU\|27/170\|round=0` | lll_reduction_generator.py |
| `MULTIPLY_IF` | 2 | `MULTIPLY_IF\|e^(3x)y' + 3e^(3x)y\|18e^(6x)` | integrating_factor_generator.py, ode_substitution_generator.py |
| `MULTIVALUED_LOG` | 2 | `MULTIVALUED_LOG\|ln(7) + i*(79pi/180 + 2pi*k)\|k in Z` | complex_log_generator.py |
| `MULTI_FORMULA` | 2 | `MULTI_FORMULA\|n!/(a!b!c!...)\|16! / repeats` | stars_and_bars_generator.py |
| `MULTI_SETUP` | 2 | `MULTI_SETUP\|4 P's, 3 R's, 4 N's, 5 C's\|total 16` | stars_and_bars_generator.py |
| `MUL_PARTIAL` | 3 | `MUL_PARTIAL\|6\|68395\|410370` | decimal_mult_generator.py, multi_digit_multiplication_generator.py |
| `MUL_SETUP` | 2 | `MUL_SETUP\|68395\|1956` | decimal_mult_generator.py, multi_digit_multiplication_generator.py |
| `MUL_TERM` | 3 | `MUL_TERM\|10\|2.8x\|28x` | linear_fractional_generator.py, polynomial_long_division_generator.py, rational_equation_generator.py |
| `MVT_SETUP` | 2 | `MVT_SETUP\|f(x) = x^2 - 3x - 6 on [-3, 3]\|find the c guaranteed by the MVT` | mean_value_theorem_generator.py |
| `MV_CHAIN_SETUP` | 3 | `MV_CHAIN_SETUP\|z = f(x,y) = 5*x^2 + 3*y^2 - x*y - 2*x - 3*y\|x = 3*s - 3*t + 3, y = s - 3*t + 2\|(s,t) = (0, 2)` | multivar_chain_rule_generator.py |
| `NATURAL_SETUP` | 3 | `NATURAL_SETUP\|length\|hbar=1,c=1\|L=32/39 keV^-1` | natural_units_generator.py |
| `NB_FEATURE_COUNT` | 3 | `NB_FEATURE_COUNT\|Spam\|long=1\|count=6` | naive_bayes_generator.py |
| `NB_LIKELIHOOD` | 3 | `NB_LIKELIHOOD\|Spam\|long=1\|7/20` | naive_bayes_generator.py |
| `NB_PRIOR` | 2 | `NB_PRIOR\|Spam\|18/37` | naive_bayes_generator.py |
| `NB_SCORE` | 2 | `NB_SCORE\|Spam\|start=18/37` | naive_bayes_generator.py |
| `NB_SETUP` | 3 | `NB_SETUP\|query=long=1, money=0\|alpha=1\|classes=Spam,Ham` | naive_bayes_generator.py |
| `NCR` | 2 | `NCR\|C(5,2)\|10` | binomial_probability_generator.py, derangement_generator.py, generating_function_generator.py, hypercube_counting_generator.py |
| `NEAREST` | 2 | `NEAREST\|queen\|(-6,-2)` | embedding_similarity_generator.py |
| `NEED` | 2 | `NEED\|line 2 gives the base ratio 3:10\|line 4 multiplies 3 by 5` | fill_in_step_generator.py |
| `NEGATE` | 2 | `NEGATE\|379\|-379` | countability_bijection_generator.py |
| `NEG_CONNECTIVE` | 2 | `NEG_CONNECTIVE\|¬(U(z) ∨ D(z))\|¬U(z) ∧ ¬D(z)` | prenex_normal_form_generator.py, quantifier_negation_generator.py |
| `NEG_LOG` | 2 | `NEG_LOG\|p=1/8\|ln(8)` | perplexity_generator.py |
| `NEG_QUANT` | 2 | `NEG_QUANT\|¬∀z\|∃z ¬` | prenex_normal_form_generator.py, quantifier_negation_generator.py |
| `NEST` | 2 | `NEST\|block 1\|{{∅, {{∅}, {∅, {∅}}, {{{∅}}}}}, {{{∅}}, {∅, {∅, {∅}}, {{∅}}, {{{∅}}}}, {{∅}, {∅, {∅}}, {{∅}}, {{{∅}}}}}}` | hereditarily_finite_set_generator.py |
| `NET_SETUP` | 2 | `NET_SETUP\|2 right triangles with legs 12 and 16; rectangles 12 by 12, 16 by 12, and 20 by 12\|total surface area` | nets_surface_area_generator.py |
| `NEWTON_DD` | 2 | `NEWTON_DD\|f[x0,x1]\|-11` | interpolation_generator.py |
| `NEWTON_SETUP` | 2, 3 | `NEWTON_SETUP\|f(x)=x^2-38\|f'(x)=2x\|x0=6,iterations=3` | newton_raphson_generator.py, newtons_laws_generator.py |
| `NEWTON_STEP` | 2 | `NEWTON_STEP\|1\|3/5` | npv_irr_generator.py |
| `NEWTON_UPDATE` | 3 | `NEWTON_UPDATE\|1\|x_0=6\|x_1=37/6` | newton_raphson_generator.py |
| `NEW_SLOPE` | 2 | `NEW_SLOPE\|New slope (m2) = 1/3\|Parallel lines have the same slope` | parallel_perpendicular_line_generator.py |
| `NEW_STRING` | 1 | `NEW_STRING\|11111121` | cantor_diagonal_generator.py |
| `NFA_ACCEPT` | 1 | `NFA_ACCEPT\|q4` | nfa_simulation_generator.py |
| `NFA_ACTIVE` | 2 | `NFA_ACTIVE\|start\|{q1}` | nfa_simulation_generator.py |
| `NFA_EPSILON` | 2 | `NFA_EPSILON\|q3\|{q6}` | nfa_simulation_generator.py |
| `NFA_INPUT` | 1 | `NFA_INPUT\|bab` | nfa_simulation_generator.py |
| `NFA_MOVE` | 4 | `NFA_MOVE\|{q1}\|b\|q1->{q4}\|{q4}` | nfa_simulation_generator.py |
| `NFA_READ` | 2 | `NFA_READ\|pos 1\|b` | nfa_simulation_generator.py |
| `NFA_SETUP` | 3 | `NFA_SETUP\|states q1, q4, q8\|alphabet a, b\|start q1` | nfa_simulation_generator.py |
| `NFA_TRANSITION` | 3 | `NFA_TRANSITION\|q1\|a\|{q4,q8}` | nfa_simulation_generator.py |
| `NILPOTENT` | 3 | `NILPOTENT\|n>=2\|theta^2=0\|0` | grassmann_generator.py |
| `NLL` | 2 | `NLL\|111 tokens\|111*ln(8)` | perplexity_generator.py |
| `NORM2` | 2 | `NORM2\|b1\|170` | lll_reduction_generator.py |
| `NORMALIZE` | 2 | `NORMALIZE\|1/2 + 1/2\|1` | clebsch_gordan_generator.py, layer_norm_generator.py |
| `NORMALIZE_SIGN` | 2 | `NORMALIZE_SIGN\|(-4,4)\|(4,-4)` | lll_reduction_generator.py |
| `NORMAL_EQ` | 2 | `NORMAL_EQ\|X^T X\|[[4, 0], [0, 20]]` | least_squares_generator.py |
| `NORMAL_SLOPE` | 2 | `NORMAL_SLOPE\|-1/(9)\|-1/9` | tangent_line_generator.py |
| `NORMAL_SYMMETRY` | 2 | `NORMAL_SYMMETRY\|N_neg_d1=0.3\|N_neg_d2=0.35` | black_scholes_generator.py |
| `NORM_CHECK` | 2 | `NORM_CHECK\|P(+x)+P(-x)\|1` | spin_half_generator.py |
| `NORM_SETUP` | 2 | `NORM_SETUP\|A: 56 in N(53, 4)\|compare relative standing` | matrix_norm_generator.py, normal_table_generator.py, z_score_generator.py |
| `NORM_SQUARED` | 2 | `NORM_SQUARED\|q\|1` | quaternion_generator.py |
| `NO_COLLISION` | 1 | `NO_COLLISION\|all outputs distinct` | function_properties_generator.py |
| `NO_MISSED` | 1 | `NO_MISSED\|all codomain values hit` | function_properties_generator.py |
| `NO_REDEX` | 2 | `NO_REDEX\|(h (h h))\|no beta redex remains` | lambda_reduction_generator.py |
| `NO_WITNESS` | 2, 3 | `NO_WITNESS\|x=6\|fails y=6\|6 < 6` | peano_arithmetic_generator.py, quantifier_finite_domain_generator.py |
| `NPV_SETUP` | 2 | `NPV_SETUP\|c0=-700,c1=1350,c2=350,c3=200\|rate=20%` | npv_irr_generator.py |
| `NPV_TERM` | 2 | `NPV_TERM\|t=0\|-700` | npv_irr_generator.py |
| `NULL_REL` | 2 | `NULL_REL\|x1 = 0\|x1 = 0` | subspace_basis_generator.py |
| `NULL_VECTOR` | 2 | `NULL_VECTOR\|x4=1\|[0, 1, 1, 1]` | subspace_basis_generator.py |
| `NUMBER_OPERATOR` | 2 | `NUMBER_OPERATOR\|N ket20\|20 ket20` | ladder_operator_generator.py |
| `NW_ALLOC` | 1, 3 | `NW_ALLOC\|cell x11\|min(23,9)\|9` | transportation_generator.py |
| `NYQUIST` | 1 | `NYQUIST\|required rate = 2*f_max` | signal_arithmetic_generator.py |
| `OBJECTIVE` | 1 | `OBJECTIVE\|at (0,0)` | lp_corner_generator.py |
| `OCCURS_CHECK` | 3 | `OCCURS_CHECK\|X\|f(X)\|fail` | unification_generator.py |
| `ODD_VERTICES` | 2 | `ODD_VERTICES\|none\|0` | euler_circuit_generator.py |
| `ODE_SETUP` | 2, 3 | `ODE_SETUP\|dy/dt = ky; y doubles every 150 hours\|find k exactly` | euler_method_generator.py, exact_ode_generator.py, integrating_factor_generator.py, laplace_ivp_generator.py, logistic_growth_generator.py, ode_substitution_generator.py, ode_system_generator.py, runge_kutta_generator.py, second_order_ode_generator.py, separable_ode_generator.py, series_solution_generator.py, stability_generator.py, undetermined_coeff_generator.py, variation_parameters_generator.py |
| `OPTICS_FORMULA` | 1 | `OPTICS_FORMULA\|1/f=1/d_o+1/d_i` | optics_generator.py |
| `OPTICS_SETUP` | 3 | `OPTICS_SETUP\|thin_lens\|f=20\|d_o=39` | optics_generator.py |
| `OPT_SETUP` | 2 | `OPT_SETUP\|x + y = 327, x, y > 0\|maximize P = x·y^2` | optimization_generator.py |
| `ORBIT_FORMULA` | 1 | `ORBIT_FORMULA\|(T2/T1)^2=(a2/a1)^3` | orbital_mechanics_generator.py |
| `ORBIT_SETUP` | 3 | `ORBIT_SETUP\|kepler_third\|T1=46, a1=3\|a2=75` | orbital_mechanics_generator.py |
| `ORDER_PAIR` | 2 | `ORDER_PAIR\|41 ≤ 58\|reachable in H` | partial_order_generator.py |
| `ORDER_PDF` | 1 | `ORDER_PDF\|f_{1:6}(x)=6*(1-x)^5` | order_statistics_generator.py |
| `ORDER_SETUP` | 3 | `ORDER_SETUP\|n=6\|k=1\|q=2/3` | order_statistics_generator.py |
| `ORDER_START` | 2 | `ORDER_START\|5\|identity 0` | cayley_table_generator.py |
| `ORDER_STEP` | 2 | `ORDER_STEP\|k=1\|5` | cayley_table_generator.py |
| `ORD_CMP` | 2 | `ORD_CMP\|coefficients at exponent 3\|1 < 4` | ordinal_arithmetic_generator.py |
| `ORD_RULE` | 2, 3 | `ORD_RULE\|normalization\|expand the finite right factor` | ordinal_arithmetic_generator.py |
| `ORTHOGONALITY` | 2 | `ORTHOGONALITY\|lower multiplet\|orthogonal to higher J` | clebsch_gordan_generator.py |
| `OR_SETUP` | 3 | `OR_SETUP\|M/M/1\|lambda=5\|mu=25` | or_formula_generator.py |
| `OUTCOME_CHECK` | 3 | `OUTCOME_CHECK\|17\|the two-digit number is greater than 81\|no` | sample_space_list_generator.py |
| `OUTER_ANTIDERIV` | 2 | `OUTER_ANTIDERIV\|dx\|4*x^2 + 11*x` | double_integral_generator.py |
| `OUTER_EVAL` | 3 | `OUTER_EVAL\|y=0..15\|6*3*5^2/2\|225` | double_integral_generator.py |
| `OUTER_PRODUCT` | 1 | `OUTER_PRODUCT\|rho=183/385ket00bra00 + sqrt(36966)/385(ket00bra11+ket11bra00) + 202/385ket11bra11` | partial_trace_generator.py |
| `OUTPUT` | 1 | `OUTPUT\|y_hat=-4` | backprop_generator.py |
| `PAIR` | 2 | `PAIR\|apricot\|badger` | one_to_one_correspondence_generator.py |
| `PAIRING` | 2 | `PAIRING\|(89, 93)\|(m + n)(m + n + 1)/2 + n` | cantor_pairing_generator.py |
| `PAIR_RULE` | 1, 2 | `PAIR_RULE\|[a, b] ≤ [c, d]\|a + d ≤ b + c` | integers_as_pairs_generator.py, rationals_as_pairs_generator.py |
| `PARALLEL_RELATION` | 1 | `PARALLEL_RELATION\|2x + 30 = 5x - 30` | angle_relationships_generator.py |
| `PARALLEL_SETUP` | 2 | `PARALLEL_SETUP\|alternate_exterior\|Alternate exterior angles are equal` | angle_relationships_generator.py |
| `PARALLEL_SOLVE` | 2 | `PARALLEL_SOLVE\|-3x = -60\|x = 20` | angle_relationships_generator.py |
| `PARAMS` | 3 | `PARAMS\|W1=[[-2,2], [-2,1]]\|b1=(1,1)\|v=(-2,-2), c=2` | backprop_generator.py |
| `PARAM_PART` | 2 | `PARAM_PART\|full_matrix\|3504128` | param_count_generator.py |
| `PARAM_PATH` | 3 | `PARAM_PATH\|r(t)\|(5*t - 2, 5*t - 4)\|0 <= t <= 1` | line_integral_generator.py |
| `PARAM_SETUP` | 2, 3 | `PARAM_SETUP\|x = 6t - 4, y = 10t - 1\|eliminate t` | param_count_generator.py, parametric_calculus_generator.py, polar_parametric_generator.py |
| `PARITY` | 1, 2 | `PARITY\|transpositions 3\|odd` | fourier_series_generator.py, permutation_group_generator.py |
| `PARITY_CALC` | 2 | `PARITY_CALC\|p1=d1 xor d2 xor d4\|1 xor 1 xor 1=1` | hamming_code_generator.py |
| `PARSE` | 2, 3 | `PARSE\|p\|atom` | wff_parsing_generator.py |
| `PARTFRAC_SETUP` | 1 | `PARTFRAC_SETUP\|(x + 7)/((x + 1)(x - 1)) = A/(x + 1) + B/(x - 1)` | partial_fractions_generator.py, telescoping_generator.py |
| `PARTIAL` | 2 | `PARTIAL\|u_x\|6x` | cauchy_riemann_generator.py, fundamental_form_generator.py, hamiltonian_generator.py, lagrangian_generator.py |
| `PARTIAL_FRAC` | 2 | `PARTIAL_FRAC\|Y(s)\|-2/(s + 5) + 1/(s - 1)` | laplace_ivp_generator.py |
| `PARTIAL_RESULT` | 2 | `PARTIAL_RESULT\|f_x\|28*x^3*y + 9*x^2*y^4` | div_curl_generator.py, exact_ode_generator.py, gradient_generator.py, hessian_classify_generator.py, jacobian_generator.py, lagrange_multiplier_generator.py, line_integral_generator.py, multivar_chain_rule_generator.py, partial_derivative_generator.py, vector_theorem_generator.py |
| `PARTIAL_RULE` | 3 | `PARTIAL_RULE\|7*x^4*y\|d/dx\|28*x^3*y` | partial_derivative_generator.py |
| `PARTIAL_SETUP` | 2 | `PARTIAL_SETUP\|f(x,y) = 7*x^4*y + 3*x^3*y^4\|f_x` | partial_derivative_generator.py |
| `PARTIAL_TRACE` | 2 | `PARTIAL_TRACE\|ket00bra00\|ket0bra0` | partial_trace_generator.py |
| `PARTICLE_TABLE` | 1 | `PARTICLE_TABLE\|gamma(Q=0,B=0,Le=0,Lmu=0); p(Q=1,B=1,Le=0,Lmu=0); pi0(Q=0,B=0,Le=0,Lmu=0); e+(Q=1,B=0,Le=-1,Lmu=0)` | conservation_law_generator.py |
| `PARTICULAR` | 2 | `PARTICULAR\|y_p\|-2` | undetermined_coeff_generator.py, variation_parameters_generator.py |
| `PARTICULAR_CHECK` | 2 | `PARTICULAR_CHECK\|K = 2\|-5K - 6K + 24 = K` | recurrence_generator.py |
| `PARTICULAR_TRY` | 2 | `PARTICULAR_TRY\|a_n = K\|constant forcing` | recurrence_generator.py |
| `PARTITION` | 1 | `PARTITION\|{{10, 15}, {11, 16}, {12, 17}, {13}, {14}}` | equivalence_relation_generator.py |
| `PARTITION_FORMULA` | 1 | `PARTITION_FORMULA\|Z=g0+g1*b` | partition_function_generator.py |
| `PARTITION_SETUP` | 3 | `PARTITION_SETUP\|degenerate_two_level\|g0=5, g1=2\|epsilon=10, b=1/5` | partition_function_generator.py |
| `PARTS_CHOOSE` | 2 | `PARTS_CHOOSE\|u = ln(x), dv = -204 dx\|du = dx/x, v = -204x` | integration_by_parts_generator.py |
| `PARTS_FORMULA` | 1 | `PARTS_FORMULA\|∫ u dv = uv - ∫ v du` | integration_by_parts_generator.py |
| `PASCAL_ROW` | 2 | `PASCAL_ROW\|0\|1` | pascal_triangle_generator.py |
| `PASCAL_SETUP` | 1 | `PASCAL_SETUP\|8C3` | pascal_triangle_generator.py |
| `PATH` | 2 | `PATH\|4→31→2\|add (4, 2)` | relation_closure_generator.py |
| `PATH_DERIV` | 2 | `PATH_DERIV\|r'(t)\|(5, 5)` | curve_geometry_generator.py, line_integral_generator.py |
| `PAULI_IDENTITY` | 3 | `PAULI_IDENTITY\|{sigma_x,sigma_z}\|2 delta_ij I\|0` | pauli_algebra_generator.py |
| `PAULI_MATRIX` | 2 | `PAULI_MATRIX\|sigma_z\|[[1,0],[0,-1]]` | spin_half_generator.py |
| `PAULI_SETUP` | 3 | `PAULI_SETUP\|anticommutator\|A=-2sigma_x\|B=-3sigma_z` | pauli_algebra_generator.py |
| `PCA_SETUP` | 2 | `PCA_SETUP\|points=[(10,-2), (-4,-2), (3,3), (3,-7)]\|population covariance` | pca_generator.py |
| `PC_VECTOR` | 2 | `PC_VECTOR\|e1\|(1,0)` | pca_generator.py |
| `PDA_POP` | 2 | `PDA_POP\|(\|stack=$(` | pda_simulation_generator.py |
| `PDA_PUSH` | 2 | `PDA_PUSH\|(\|stack=$(` | pda_simulation_generator.py |
| `PDA_READ` | 1 | `PDA_READ\|(` | pda_simulation_generator.py |
| `PDA_REJECT` | 1 | `PDA_REJECT\|pop from bottom` | pda_simulation_generator.py |
| `PDA_SETUP` | 2 | `PDA_SETUP\|balanced_parentheses\|stack=$` | pda_simulation_generator.py |
| `PDA_STATE` | 3 | `PDA_STATE\|pos 1\|q\|stack=$` | pda_simulation_generator.py |
| `PDE_SETUP` | 2 | `PDE_SETUP\|u_tt = 25u_xx\|u(x,0)=x^2, u_t(x,0)=0` | separable_pde_generator.py |
| `PDF_FORMULA` | 1 | `PDF_FORMULA\|f_Y(y)=1/(44*sqrt(y))` | rv_transform_generator.py |
| `PD_SETUP` | 2 | `PD_SETUP\|A=[[25,-10], [-10,13]]\|Sylvester criterion` | positive_definite_generator.py |
| `PEANO_BASE` | 2 | `PEANO_BASE\|SS0 + 0\|SS0` | peano_arithmetic_generator.py |
| `PEANO_EQ` | 2 | `PEANO_EQ\|SS0 + SSS0\|S(SS0 + SS0)` | peano_arithmetic_generator.py |
| `PERCENT_CALC_PART` | 3 | `PERCENT_CALC_PART\|0.12\|605\|72.6` | percent_problem_generator.py |
| `PERCENT_TO_DEC` | 2 | `PERCENT_TO_DEC\|87%\|0.87` | annuity_generator.py, bond_pricing_generator.py, composite_arithmetic_generator.py, exponential_model_generator.py, fill_in_step_generator.py, finance_generator.py, fraction_decimal_percent_converter.py, npv_irr_generator.py, percent_problem_generator.py, percent_word_problem_generator.py, piecewise_evaluation_generator.py, portfolio_generator.py, tip_bill_split_generator.py |
| `PERCEPTRON_RULE` | 2 | `PERCEPTRON_RULE\|score=w0+w1*x1+w2*x2\|if y*score <= 0 update` | perceptron_generator.py |
| `PERCEPTRON_SAMPLE` | 3 | `PERCEPTRON_SAMPLE\|i=1\|x=(-1,0)\|y=1` | perceptron_generator.py |
| `PERCEPTRON_SCORE` | 2 | `PERCEPTRON_SCORE\|i=1\|score=3` | perceptron_generator.py |
| `PERCEPTRON_SETUP` | 3 | `PERCEPTRON_SETUP\|eta=1\|w=(2,-1,0)\|samples=[(-1,0,1), (1,3,1), (-2,-1,1), (1,-2,-1)]` | perceptron_generator.py |
| `PERCEPTRON_UPDATE` | 2, 3 | `PERCEPTRON_UPDATE\|i=1\|no change\|w=(2,-1,0)` | perceptron_generator.py |
| `PERIM` | 1 | `PERIM\|42` | geometry_area_perimeter_generator.py, polygon_perimeter_generator.py |
| `PERIOD` | 1 | `PERIOD\|120°` | sinusoid_features_generator.py |
| `PERM_COMPOSE` | 3 | `PERM_COMPOSE\|i=1\|tau(i)=1\|sigma(tau(i))=4` | permutation_group_generator.py |
| `PERM_FORMULA` | 1 | `PERM_FORMULA\|P(n, r) = n·(n-1)···(n-r+1), 2 factors` | permutation_combination_generator.py |
| `PERM_RESULT` | 1 | `PERM_RESULT\|[4, 3, 5, 1, 2]` | permutation_group_generator.py |
| `PERM_SETUP` | 2, 3 | `PERM_SETUP\|arrange 2 of 4\|order matters` | permutation_combination_generator.py, permutation_group_generator.py |
| `PERPLEXITY` | 2 | `PERPLEXITY\|exp(CE)\|8` | perplexity_generator.py |
| `PERPLEXITY_SETUP` | 2 | `PERPLEXITY_SETUP\|tokens=111\|p=1/8` | perplexity_generator.py |
| `PE_ENTRY` | 2 | `PE_ENTRY\|0\|sqrt(3)/2` | positional_encoding_generator.py |
| `PE_SETUP` | 3 | `PE_SETUP\|position=64\|d=2\|theta=2pi/3` | positional_encoding_generator.py |
| `PF_PRIME` | 1 | `PF_PRIME\|347` | godel_numbering_generator.py, prime_factorization_generator.py, repeating_decimal_generator.py |
| `PF_STEP` | 3 | `PF_STEP\|1041\|3\|347` | godel_numbering_generator.py, prime_factorization_generator.py, repeating_decimal_generator.py |
| `PHASE_SHIFT` | 1 | `PHASE_SHIFT\|45° right` | sinusoid_features_generator.py |
| `PHI_STEP` | 2 | `PHI_STEP\|p=2\|21` | totient_generator.py |
| `PHYS_FORMULA` | 1 | `PHYS_FORMULA\|P = W/t` | physics_formula_generator.py |
| `PHYS_SETUP` | 3 | `PHYS_SETUP\|W = 30660 joules\|t = 7 minutes\|power` | physics_formula_generator.py |
| `PH_FORMULA` | 1 | `PH_FORMULA\|pOH=-log10([OH-]), pH=14-pOH` | ph_calculation_generator.py |
| `PH_SETUP` | 2, 3 | `PH_SETUP\|hydroxide_with_log\|[OH-]=4*10^-4\|log10(4)=0.6` | ph_calculation_generator.py |
| `PI2_NUM` | 3 | `PI2_NUM\|-1/30\|π^2\|-π^2/30` | casimir_force_generator.py |
| `PICTO_COUNT` | 2 | `PICTO_COUNT\|Fish\|5` | graph_interpret_generator.py |
| `PICTO_KEY` | 2 | `PICTO_KEY\|■\|10` | graph_interpret_generator.py |
| `PIVOT` | 3 | `PIVOT\|row=s1\|column=x\|pivot=1` | simplex_generator.py |
| `PIVOT_COLS` | 2 | `PIVOT_COLS\|columns 1, 2, 3\|rank = 3` | subspace_basis_generator.py |
| `PI_COEFF` | 2 | `PI_COEFF\|11π/8\|11/8` | arc_sector_generator.py |
| `PI_DEN` | 3 | `PI_DEN\|11/12\|π\|11/(12π)` | gauss_law_generator.py, hawking_generator.py, magnetism_generator.py |
| `PI_MULT` | 3 | `PI_MULT\|2/5\|π\|2π/5` | shm_generator.py |
| `PLACE_DP` | 3 | `PLACE_DP\|2262\|2\|22.62` | decimal_mult_generator.py |
| `PLACE_DP_Q` | 3 | `PLACE_DP_Q\|165\|3\|165` | decimal_div_generator.py, percent_problem_generator.py |
| `PLACE_VALUE` | 2 | `PLACE_VALUE\|B * 16^0\|11` | base_conversion_generator.py |
| `PLANCK_SETUP` | 4 | `PLANCK_SETUP\|time\|hbar=144\|G=36\|c=16` | planck_units_generator.py |
| `PLUS_MINUS` | 2 | `PLUS_MINUS\|x = ±15\|x = 15 or x = -15` | completing_square_generator.py, quadratic_square_root_generator.py, rational_equation_generator.py |
| `POINT_FROM_LAMBDA` | 3 | `POINT_FROM_LAMBDA\|x\|48/4\|12` | lagrange_multiplier_generator.py |
| `POINT_SLOPE_SETUP` | 1 | `POINT_SLOPE_SETUP\|y - 1 = 4(x - 7)` | equation_from_two_points_generator.py, parallel_perpendicular_line_generator.py, point_slope_generator.py |
| `POLAR_AREA_FORMULA` | 1 | `POLAR_AREA_FORMULA\|A = (1/2) ∫ r^2 dθ` | parametric_calculus_generator.py |
| `POLAR_BOUNDS` | 2 | `POLAR_BOUNDS\|r\|0..5` | double_integral_generator.py |
| `POLAR_CONVERT` | 2 | `POLAR_CONVERT\|x^2 + y^2\|r^2` | double_integral_generator.py |
| `POLAR_EVAL` | 3 | `POLAR_EVAL\|theta range * radial integral\|pi/2 * 625/4\|625/8*pi` | double_integral_generator.py |
| `POLAR_FORM` | 1 | `POLAR_FORM\|10sqrt2 cis(315 deg)` | euler_formula_generator.py |
| `POLAR_FORMULA` | 1 | `POLAR_FORMULA\|x = r cos θ, y = r sin θ` | polar_parametric_generator.py |
| `POLAR_SETUP` | 2, 3 | `POLAR_SETUP\|r = 27\|pole=(3, 20)\|rectangular equation` | parametric_calculus_generator.py, polar_parametric_generator.py |
| `POLES` | 1 | `POLES\|s=-9, -12` | transfer_function_generator.py |
| `POLE_ORDER` | 1 | `POLE_ORDER\|3` | residue_generator.py |
| `POLE_TEST` | 3 | `POLE_TEST\|pole -7\|abs(-7) < 3\|outside` | contour_integral_generator.py |
| `POLISH` | 1 | `POLISH\|AKrrKErqCqp` | wff_parsing_generator.py |
| `POLLARD_FACTOR` | 2 | `POLLARD_FACTOR\|13\|17` | pollard_factorization_generator.py |
| `POLLARD_PM1_SETUP` | 3 | `POLLARD_PM1_SETUP\|n=221\|base=5\|B=5` | pollard_factorization_generator.py |
| `POLLARD_RHO_SETUP` | 3 | `POLLARD_RHO_SETUP\|n=143\|c=2\|x0=4` | pollard_factorization_generator.py |
| `POLYDIV_SETUP` | 2 | `POLYDIV_SETUP\|3y^3 - 2y^2 - 3y - 2\|y - 1` | finite_field_generator.py, polynomial_long_division_generator.py |
| `POLY_ACCUM` | 2 | `POLY_ACCUM\|x^0\|4` | finite_field_generator.py |
| `POLY_ADD_START` | 1 | `POLY_ADD_START\|max degree 3` | finite_field_generator.py |
| `POLY_COEFF` | 3 | `POLY_COEFF\|sum\|x^0\|5` | finite_field_generator.py |
| `POLY_COMBINE` | 1 | `POLY_COMBINE\|x^3 - 5x^2 - 11x - 2` | multiplying_binomials_generator.py, polynomial_add_sub_generator.py |
| `POLY_DIST_NEG` | 1 | `POLY_DIST_NEG\|Distribute negative sign to second polynomial` | polynomial_add_sub_generator.py |
| `POLY_DIV_SETUP` | 1 | `POLY_DIV_SETUP\|(20x^6 - 5x^2) / (-5x^2)` | polynomial_div_monomial_generator.py |
| `POLY_DIV_SPLIT` | 1 | `POLY_DIV_SPLIT\|(20x^6) / (-5x^2) + (-5x^2) / (-5x^2)` | polynomial_div_monomial_generator.py |
| `POLY_FORMULA` | 1 | `POLY_FORMULA\|A = (1/2)·a·P` | regular_polygon_area_generator.py |
| `POLY_GROUP_LIKE` | 1 | `POLY_GROUP_LIKE\|(x^3) + (-5x^2) + (-3x -8x) + (2 -4)` | multiplying_polynomials_generator.py, polynomial_add_sub_generator.py |
| `POLY_INPUT` | 2 | `POLY_INPUT\|f(x)\|3x^2 + 3x + 1` | finite_field_generator.py |
| `POLY_MULT_SETUP` | 1 | `POLY_MULT_SETUP\|(-4x + 1)(2x^2 + 5x - 4)` | multiplying_polynomials_generator.py |
| `POLY_MUL_START` | 2 | `POLY_MUL_START\|degree 2\|degree 3` | finite_field_generator.py |
| `POLY_REMAINDER` | 1 | `POLY_REMAINDER\|x^4 + x^3` | finite_field_generator.py |
| `POLY_SCALE` | 3 | `POLY_SCALE\|x^2 - 1/3\|3/2\|(3x^2 - 1)/2` | legendre_construction_generator.py |
| `POLY_SETUP` | 1, 2 | `POLY_SETUP\|(x^3 - 5x^2 - 3x + 2) + (-8x - 4)` | factor_gcf_generator.py, factor_grouping_generator.py, factor_special_forms_generator.py, factor_trinomial_generator.py, polynomial_add_sub_generator.py, rational_expr_add_sub_generator.py, rational_expr_mult_div_generator.py, rational_expr_simplify_generator.py, regular_polygon_area_generator.py |
| `POLY_SUB` | 2, 3 | `POLY_SUB\|(3y^3 - 2y^2) - (3y^3 - 3y^2)\|y^2` | legendre_construction_generator.py, polynomial_long_division_generator.py |
| `PORT_FORMULA` | 2 | `PORT_FORMULA\|E=wA*rA+wB*rB\|Var=wA^2*varA+wB^2*varB+2*wA*wB*cov` | portfolio_generator.py |
| `PORT_RESULT` | 2 | `PORT_RESULT\|expected_return=0.12\|variance=0.01125` | portfolio_generator.py |
| `PORT_SETUP` | 3 | `PORT_SETUP\|wA=0.5,wB=0.5\|rA=6%,rB=18%\|varA=0.0225,varB=0.0225,cov=0` | portfolio_generator.py |
| `POSTERIOR_PARAM` | 1 | `POSTERIOR_PARAM\|alpha' = alpha + successes` | bayesian_update_generator.py |
| `POST_PRECISION` | 1 | `POST_PRECISION\|prior precision + data precision` | bayesian_update_generator.py |
| `POTENTIAL_BUILD` | 3 | `POTENTIAL_BUILD\|integrate P dx\|x^2 - 3*x*y + g(y)\|g'(y) remains` | exact_ode_generator.py, line_integral_generator.py |
| `POTENTIAL_RESULT` | 2 | `POTENTIAL_RESULT\|phi(x,y)\|x^2 + y^2 - 3*x*y` | exact_ode_generator.py, line_integral_generator.py |
| `POW` | 2 | `POW\|(1/5)^5\|0.00032` | binomial_probability_generator.py, geometric_distribution_generator.py, recurrence_generator.py |
| `POWER_ENTRY` | 3 | `POWER_ENTRY\|(1,1)\|(-81) + 2\|-79` | diagonalization_generator.py |
| `POWER_FORM` | 1 | `POWER_FORM\|A^2 = P*D^2*P^-1` | diagonalization_generator.py |
| `POWER_INTEGRAL` | 2 | `POWER_INTEGRAL\|int_0^a x dx\|a^2/2` | continuous_distribution_generator.py, wavefunction_generator.py |
| `POWER_REDUCE` | 2 | `POWER_REDUCE\|5^120\|5^0 mod 42` | totient_generator.py |
| `POWER_RULE` | 2 | `POWER_RULE\|-7x^3\|-21x^2` | chain_rule_generator.py, commutator_generator.py, curve_analysis_generator.py, derivative_power_rule_generator.py, derivative_product_quotient_generator.py, derivative_transcendental_generator.py, lhopital_generator.py, linear_approx_generator.py, log_diff_higher_order_generator.py, mean_value_theorem_generator.py, optimization_generator.py, tangent_line_generator.py |
| `POWER_SETUP` | 2 | `POWER_SETUP\|cis(167 deg)^(9i)\|principal logarithm` | complex_log_generator.py |
| `POWER_SET_RESULT` | 1 | `POWER_SET_RESULT\|{∅, {e}, {t}, {e, t}}` | set_operations_generator.py |
| `POWER_SHIFT` | 3 | `POWER_SHIFT\|k=0\|0-2\|-2` | laurent_series_generator.py |
| `PREDICATES` | 1 | `PREDICATES\|K(x): x is a dancer; M(x): x is generous` | english_to_logic_generator.py |
| `PREDICT` | 2 | `PREDICT\|x*\|-20/21` | kernel_ridge_generator.py |
| `PREIMAGE` | 2 | `PREIMAGE\|7\|{r}` | function_properties_generator.py |
| `PREMISE` | 2 | `PREMISE\|1\|m` | natural_deduction_generator.py |
| `PREMISES_ALL_T` | 2 | `PREMISES_ALL_T\|p=T, q=T, r=T, s=T\|no` | argument_form_generator.py |
| `PRIME` | 1 | `PRIME\|41` | divisibility_classification_generator.py |
| `PRIM_CANDIDATES` | 2 | `PRIM_CANDIDATES\|visited D\|BD=7, DF=16, CD=20, DE=22` | mst_generator.py |
| `PRIM_START` | 1 | `PRIM_START\|D` | mst_generator.py |
| `PRINCIPAL_LOG` | 1 | `PRINCIPAL_LOG\|ln(7) + i*79pi/180` | complex_log_generator.py |
| `PRINCIPAL_MINOR` | 2 | `PRINCIPAL_MINOR\|K11\|1` | kernel_validity_generator.py |
| `PRIOR_PRECISION` | 1 | `PRIOR_PRECISION\|1/tau^2` | bayesian_update_generator.py |
| `PROBABILITY` | 2 | `PROBABILITY\|P(+x)\|16129/25538` | spin_half_generator.py |
| `PROB_CONDITIONAL` | 2 | `PROB_CONDITIONAL\|P(multiple of 3 given first was multiple of 3)\|14/45` | compound_probability_generator.py |
| `PROB_DEPENDENT` | 1 | `PROB_DEPENDENT\|Drawing without replacement means dependent events` | compound_probability_generator.py |
| `PROB_DESCRIBE` | 1 | `PROB_DESCRIBE\|Two dice: d7=1, d15=8` | compound_probability_generator.py |
| `PROB_IDENTIFY` | 2 | `PROB_IDENTIFY\|P(first die is 1)\|1/7` | compound_probability_generator.py |
| `PROB_INDEPENDENT` | 1 | `PROB_INDEPENDENT\|The two dice are independent events` | compound_probability_generator.py |
| `PROB_MULTIPLY` | 3 | `PROB_MULTIPLY\|1/7\|1/15\|1/105` | compound_probability_generator.py |
| `PROB_SETUP` | 2 | `PROB_SETUP\|11\|16` | complement_probability_generator.py, fundamental_counting_principle_generator.py, likelihood_language_generator.py, sample_space_list_generator.py, simple_probability_generator.py |
| `PROB_SIMPLIFY` | 2 | `PROB_SIMPLIFY\|210/2070\|7/69` | compound_probability_generator.py |
| `PROB_WEIGHT` | 2 | `PROB_WEIGHT\|1/sqrt2^2\|1/2` | clebsch_gordan_generator.py |
| `PRODUCT` | 2 | `PRODUCT\|Delta x^2 * Delta p^2\|1156pi^2/12 - 1/2` | uncertainty_generator.py |
| `PROJECT` | 2 | `PROJECT\|P1\|7` | pca_generator.py |
| `PROJECTILE_SETUP` | 3 | `PROJECTILE_SETUP\|vx=18\|vy=27\|g=10` | projectile_motion_generator.py |
| `PROJECTION` | 2 | `PROJECTION\|X*beta\|[12, 10, 8, 6]` | least_squares_generator.py, legendre_construction_generator.py |
| `PROJECTOR_SETUP` | 2 | `PROJECTOR_SETUP\|v=(651/23549, 23540/23549)\|P=vv^T=[[423801/554555401,15324540/554555401],[15324540/554555401,554131600/554555401]]` | projector_generator.py |
| `PROJ_COEFF` | 3 | `PROJ_COEFF\|v2 on u1\|-10/5\|-2` | gram_schmidt_generator.py |
| `PROJ_VECTOR` | 2 | `PROJ_VECTOR\|-2*u1\|[-4, -2]` | gram_schmidt_generator.py |
| `PROPERTY_MATCH` | 3 | `PROPERTY_MATCH\|multiplicative identity property\|a × 1 = a\|5771 × 1` | operation_properties_generator.py |
| `PROPERTY_RESULT` | 2 | `PROPERTY_RESULT\|reflexive\|yes` | relation_check_generator.py |
| `PROP_SETUP` | 1 | `PROP_SETUP\|2/2 = x/3` | proportion_word_problem_generator.py, proportional_relationship_generator.py, similar_triangles_generator.py, triangle_solve_generator.py |
| `PSD_SETUP` | 2 | `PSD_SETUP\|K=[[1,-1], [-1,3]]\|criterion=all principal minors >= 0` | kernel_validity_generator.py |
| `PULL` | 2 | `PULL\|∃y\|from left past ∧` | prenex_normal_form_generator.py |
| `PURITY` | 1 | `PURITY\|Tr(rho^2)=145/289` | density_matrix_generator.py |
| `PYTHAG_CALCULATE` | 2 | `PYTHAG_CALCULATE\|h² = 33489 - 32400 = 1089\|1089` | pythag_leg_generator.py |
| `PYTHAG_CONTEXT` | 3 | `PYTHAG_CONTEXT\|ladder\|ladder=183ft, given=180ft\|diagram=FGQ` | pythag_leg_generator.py |
| `PYTHAG_FORMULA` | 1 | `PYTHAG_FORMULA\|a² + b² = c²` | pythag_hyp_generator.py, pythag_leg_generator.py |
| `PYTHAG_MODEL` | 3 | `PYTHAG_MODEL\|ground=180\|wall=?\|ladder=183` | pythag_leg_generator.py |
| `PYTHAG_ROOT` | 2 | `PYTHAG_ROOT\|36864\|192` | pythag_leg_generator.py |
| `PYTHAG_SETUP` | 2, 3 | `PYTHAG_SETUP\|legs=1056,92\|hypotenuse ZB=?` | pythag_hyp_generator.py, pythag_leg_generator.py |
| `PYTHAG_SOLVE` | 2 | `PYTHAG_SOLVE\|b² = 85264 - 48400\|36864` | pythag_leg_generator.py |
| `PYTHAG_SQUARE` | 2 | `PYTHAG_SQUARE\|220\|48400` | pythag_leg_generator.py |
| `PYTHAG_SUBSTITUTE` | 1 | `PYTHAG_SUBSTITUTE\|220² + b² = 292²` | pythag_leg_generator.py |
| `Q1` | 4 | `Q1\|28\|20\|2\|24` | complex_quadratic_generator.py, polynomial_zeros_generator.py, quadratic_generator.py |
| `Q2` | 4 | `Q2\|28\|20\|2\|4` | complex_quadratic_generator.py, polynomial_zeros_generator.py, quadratic_generator.py |
| `QN_ADD` | 4 | `QN_ADD\|Q\|left\|0 + gamma(0)\|0` | conservation_law_generator.py |
| `QR_ENTRY` | 2 | `QR_ENTRY\|q1\|[1, 0, 0]` | qr_decomposition_generator.py |
| `QR_SETUP` | 2 | `QR_SETUP\|A = [[4, 1, 0], [0, 5, -3], [0, 0, 4]]\|Gram-Schmidt columns` | qr_decomposition_generator.py |
| `QUADRANT` | 2 | `QUADRANT\|164°\|quadrant II` | angle_measure_generator.py, polar_parametric_generator.py, unit_circle_generator.py |
| `QUADRATIC` | 3 | `QUADRATIC\|2\|16\|30` | mobius_transform_generator.py |
| `QUANTUM_FORMULA` | 1 | `QUANTUM_FORMULA\|lambda=h/p` | quantum_formula_generator.py |
| `QUANTUM_SETUP` | 2, 3 | `QUANTUM_SETUP\|gates=Z then H then Y\|input=e^(i103π/114)·ket1` | quantum_formula_generator.py, quantum_gate_generator.py |
| `QUANT_CASE` | 1, 2 | `QUANT_CASE\|x=6` | quantifier_finite_domain_generator.py |
| `QUANT_CHOICE` | 1 | `QUANT_CHOICE\|some/there is → ∃` | english_to_logic_generator.py |
| `QUANT_RESULT` | 2, 3 | `QUANT_RESULT\|∃x ∀y\|false` | quantifier_finite_domain_generator.py |
| `QUANT_SETUP` | 3 | `QUANT_SETUP\|x=(21/50,27/100,-42/25)\|scale=1/25\|zero_point=8` | quantization_generator.py |
| `QUANT_VALUE` | 2 | `QUANT_VALUE\|1\|19` | quantization_generator.py |
| `QUARK_CHARGE` | 2 | `QUARK_CHARGE\|anti_u\|-2/3` | quark_composition_generator.py |
| `QUARK_SETUP` | 3 | `QUARK_SETUP\|meson,count=812\|anti_u d\|u=2/3,d=-1/3,s=-1/3,c=2/3,b=-1/3; anti=-charge` | quark_composition_generator.py |
| `QUARTILE` | 3 | `QUARTILE\|Q1\|9,20,21\|20` | five_number_summary_generator.py |
| `QUAT_COMPONENT` | 3 | `QUAT_COMPONENT\|q*v\|real\|0` | quaternion_generator.py |
| `QUAT_INVERSE` | 2 | `QUAT_INVERSE\|q\|(0,0,-1,0)` | quaternion_generator.py |
| `QUAT_MUL_START` | 3 | `QUAT_MUL_START\|q*v\|q\|v` | quaternion_generator.py |
| `QUAT_RESULT` | 2 | `QUAT_RESULT\|q*v\|(0,-4,0,-4)` | quaternion_generator.py |
| `QUAT_SETUP` | 2 | `QUAT_SETUP\|q=(0,0,1,0)\|v=(0,4,0,-4)` | quaternion_generator.py |
| `QUEUE_STATE` | 2 | `QUEUE_STATE\|initial\|D` | graph_traversal_generator.py |
| `QUOTIENT` | 1 | `QUOTIENT\|x^4 + x^2 + 1` | finite_field_generator.py |
| `Q_EXPR` | 1 | `Q_EXPR\|Q = [B]/[A]` | equilibrium_ice_generator.py |
| `R` | 1 | `R\|21` | complex_number_ops_generator.py, finite_field_generator.py, long_division_generator.py, polynomial_long_division_generator.py, polynomial_zeros_generator.py, synthetic_division_generator.py |
| `RANGE` | 1 | `RANGE\|{5, 18}` | relation_operations_generator.py |
| `RANK` | 2 | `RANK\|∅\|0` | hereditarily_finite_set_generator.py |
| `RAPIDITY_SUM` | 2 | `RAPIDITY_SUM\|collinear boosts\|2` | minkowski_interval_generator.py |
| `RATE_MONTHLY` | 2 | `RATE_MONTHLY\|12% / 12\|0.01` | finance_generator.py |
| `RATE_SETUP` | 2 | `RATE_SETUP\|conical tank, radius = height/2; water in at dV/dt = 7 m³/min; depth h = 16 m\|dh/dt` | related_rates_generator.py |
| `RATIO` | 2, 3 | `RATIO\|3*y = x\|y = x/3` | lagrange_multiplier_generator.py, simplex_generator.py |
| `RATIONALIZE` | 1 | `RATIONALIZE\|√190/√190` | dot_product_generator.py, limit_evaluation_generator.py, radical_rationalize_generator.py, special_right_triangle_generator.py |
| `RATIO_BASE` | 3 | `RATIO_BASE\|10:18\|2\|5:9` | error_spotting_generator.py, fill_in_step_generator.py, ratio_table_generator.py |
| `RATIO_TABLE` | 2 | `RATIO_TABLE\|Trees: ?, 10, 40, 60\|Rows: 9, 18, 72, 108` | error_spotting_generator.py, fill_in_step_generator.py, ratio_table_generator.py |
| `RAW_FORMULA` | 1 | `RAW_FORMULA\|x = μ + z·σ` | z_score_generator.py |
| `REARRANGE_EQ` | 1 | `REARRANGE_EQ\|whole = 810 / 0.36` | percent_problem_generator.py |
| `RECIPROCAL` | 2 | `RECIPROCAL\|csc θ = 1/sin θ\|-5/3` | trig_six_functions_generator.py |
| `RECOVER_DATA` | 2 | `RECOVER_DATA\|positions 3,5,6,7\|1101` | hamming_code_generator.py |
| `RECT_FORM` | 1 | `RECT_FORM\|-11i` | de_moivre_generator.py, euler_formula_generator.py |
| `RECUR` | 3 | `RECUR\|5P_5 = 9x P_4 - 4P_3\|P_4 = (35x^4 - 30x^2 + 3)/8\|P_3 = (5x^3 - 3x)/2` | legendre_construction_generator.py |
| `RECURRENCE` | 2 | `RECURRENCE\|a_(n+1)\|a_n/(n+1)` | derangement_generator.py, series_solution_generator.py |
| `REC_SETUP` | 1, 2 | `REC_SETUP\|a_n = -5 a_(n-1) - 6 a_(n-2) + 24\|a_0 = 9, a_1 = -16` | master_theorem_generator.py, recurrence_generator.py |
| `REDUCE` | 2, 3 | `REDUCE\|(18, 14)\|(4, 0)` | integers_as_pairs_generator.py, rationals_as_pairs_generator.py |
| `REDUCED_DENSITY` | 1 | `REDUCED_DENSITY\|rho_A=[[183/385,0],[0,202/385]]` | partial_trace_generator.py |
| `REFLEXIVE_CHECK` | 2 | `REFLEXIVE_CHECK\|(15, 15)\|present` | equivalence_relation_generator.py, relation_check_generator.py |
| `REGEX_ACCEPT` | 1 | `REGEX_ACCEPT\|q4757_3, q4757_4` | regex_to_automaton_generator.py |
| `REGEX_SETUP` | 3 | `REGEX_SETUP\|(a or b)*(ab or ba)\|alphabet a,b\|canonical progress DFA` | regex_to_automaton_generator.py |
| `REGEX_STATE` | 2 | `REGEX_STATE\|q4757_0\|start` | regex_to_automaton_generator.py |
| `REGEX_TRANSITION` | 3 | `REGEX_TRANSITION\|q4757_0\|a\|q4757_1` | regex_to_automaton_generator.py |
| `REGION` | 2 | `REGION\|both\|{17, 19, 25}` | attribute_sorting_generator.py, venn_region_count_generator.py |
| `REGION_EQ` | 2 | `REGION_EQ\|A ∩ B\|30` | venn_region_count_generator.py |
| `REGION_MEASURE` | 3 | `REGION_MEASURE\|disk area\|12^2*pi\|144*pi` | vector_theorem_generator.py |
| `REGION_REWRITE` | 2 | `REGION_REWRITE\|0 <= y <= 15\|y/3 <= x <= 5` | double_integral_generator.py |
| `REG_ROW` | 3 | `REG_ROW\|x-x̄=-2\|y-ȳ=-3\|product=6` | regression_generator.py |
| `REG_SETUP` | 2 | `REG_SETUP\|line ŷ = 50.6 - 1.2x\|predict ŷ at x = 10` | regression_generator.py |
| `REJECT` | 1, 2 | `REJECT\|x = 1` | cantor_pairing_generator.py, conditional_forms_generator.py, counterexample_search_generator.py, factor_trinomial_generator.py, knights_knaves_generator.py, log_conversion_generator.py, log_equation_generator.py, optimization_generator.py, polynomial_inequality_generator.py, radical_equation_generator.py, rational_equation_generator.py, rational_root_generator.py, set_builder_roster_generator.py, structure_isomorphism_generator.py |
| `RELAX` | 3 | `RELAX\|D->A\|update inf to 4\|via weight 4` | dijkstra_generator.py |
| `RELU` | 3 | `RELU\|z=1\|h=1\|deriv=1` | backprop_generator.py |
| `REL_ENERGY_FORMULA` | 1 | `REL_ENERGY_FORMULA\|w=(u+v)/(1+u*v), c=1` | relativistic_energy_generator.py |
| `REL_ENERGY_SETUP` | 3 | `REL_ENERGY_SETUP\|velocity_addition\|u=4/5\|v=1/3` | relativistic_energy_generator.py |
| `REL_FORMULA` | 1 | `REL_FORMULA\|L=L0/gamma` | special_relativity_generator.py |
| `REL_FREQ` | 3 | `REL_FREQ\|amber\|33/57\|11/19` | experimental_probability_generator.py |
| `REL_PAIR` | 2 | `REL_PAIR\|(3, 3)\|same block` | equivalence_relation_generator.py |
| `REL_SETUP` | 2, 3 | `REL_SETUP\|A = {15, 16, 47, 58, 59}\|R = {(15, 15), (16, 16), (47, 47), (47, 58), (47, 59), (58, 47), (58, 58), (58, 59), (59, 47), (59, 58), (59, 59)}` | equivalence_relation_generator.py, relation_check_generator.py, relation_closure_generator.py, relation_operations_generator.py, special_relativity_generator.py |
| `RENAME` | 2 | `RENAME\|∀w\|∀w1` | prenex_normal_form_generator.py |
| `REPEAT_DETECT` | 2 | `REPEAT_DETECT\|remainder 52 repeats\|repetend 228070175438596491` | repeating_decimal_generator.py |
| `REPRESENT` | 2 | `REPRESENT\|even d\|d = 2w` | direct_proof_algebra_generator.py |
| `REP_DIM` | 2 | `REP_DIM\|8\|8` | young_tableaux_generator.py |
| `RESIDUAL` | 2 | `RESIDUAL\|y - X*beta\|[-1, 1, 1, -1]` | least_squares_generator.py |
| `RESIDUE` | 1, 3 | `RESIDUE\|-6` | contour_integral_generator.py, residue_generator.py |
| `RESIDUE_SETUP` | 2 | `RESIDUE_SETUP\|a=3\|f=(4 - 4(z-3) - 6(z-3)^2 + 2(z-3)^3 + 5(z-3)^4)/(z-3)^3` | residue_generator.py |
| `RESIDUE_SUM` | 1 | `RESIDUE_SUM\|0` | contour_integral_generator.py |
| `RESID_SETUP` | 2 | `RESID_SETUP\|point (1, 33), line ŷ = 36.9 - 0.3x\|residual = observed − predicted` | regression_generator.py |
| `RESOLVE` | 3 | `RESOLVE\|C1\|C2\|¬P6545` | resolution_proof_generator.py |
| `RESTRICT_CHECK` | 3 | `RESTRICT_CHECK\|(e, 2)\|e in D=yes\|keep` | relation_operations_generator.py |
| `RES_EMPTY` | 1 | `RES_EMPTY\|C4` | resolution_proof_generator.py |
| `RES_SETUP` | 1 | `RES_SETUP\|C1=(¬P6545), C2=(P6545), C3=(P83639)` | resolution_proof_generator.py |
| `RES_SKIP` | 3 | `RES_SKIP\|C1\|C3\|(P3284)` | resolution_proof_generator.py |
| `REVERSE` | 2 | `REVERSE\|0,0,0,1\|1000` | base_arithmetic_generator.py, base_conversion_generator.py, bitwise_ops_generator.py |
| `REWRITE` | 1, 2 | `REWRITE\|5771 × 1\|5771` | antiderivative_generator.py, arc_length_generator.py, area_between_curves_generator.py, cardinal_arithmetic_generator.py, chain_rule_generator.py, circle_equation_generator.py, combinatory_logic_generator.py, completing_square_generator.py, complex_division_generator.py, complex_log_generator.py, complex_number_ops_generator.py, complex_quadratic_generator.py, confidence_interval_generator.py, conic_standard_form_generator.py, cramers_rule_generator.py, curve_analysis_generator.py, definite_integral_generator.py, derivative_limit_def_generator.py, derivative_power_rule_generator.py, derivative_product_quotient_generator.py, derivative_transcendental_generator.py, domain_range_generator.py, dot_product_generator.py, english_to_logic_generator.py, euler_formula_generator.py, evaluate_expression_generator.py, exponent_generator.py, exponent_mixed_rules_generator.py, exponential_equation_generator.py, factor_gcf_generator.py, factor_grouping_generator.py, factor_special_forms_generator.py, factor_trinomial_generator.py, frequency_table_generator.py, function_composition_generator.py, function_operations_generator.py, horner_evaluation_generator.py, implicit_diff_generator.py, improper_integral_generator.py, induction_verify_generator.py, integrating_factor_generator.py, integration_by_parts_generator.py, inverse_function_generator.py, lambda_reduction_generator.py, laurent_series_generator.py, lhopital_generator.py, limit_evaluation_generator.py, linear_approx_generator.py, linear_complex_generator.py, linear_fractional_generator.py, literal_equation_generator.py, log_conversion_generator.py, log_diff_higher_order_generator.py, log_equation_generator.py, log_properties_generator.py, logical_equivalence_laws_generator.py, logistic_growth_generator.py, master_theorem_generator.py, matrix_inverse_generator.py, method_of_moments_generator.py, mgf_generator.py, midpoint_generator.py, mle_generator.py, normal_table_generator.py, ode_substitution_generator.py, operation_properties_generator.py, optimization_generator.py, order_of_operations_generator.py, ordinal_arithmetic_generator.py, parametric_calculus_generator.py, partial_fractions_generator.py, permutation_combination_generator.py, polar_parametric_generator.py, polynomial_zeros_generator.py, power_series_generator.py, prenex_normal_form_generator.py, quadratic_factoring_generator.py, quantifier_negation_generator.py, radical_add_sub_generator.py, radical_equation_generator.py, radical_multiply_generator.py, radical_rationalize_generator.py, radical_variable_simplify_generator.py, rational_equation_generator.py, rational_exponent_generator.py, rational_expr_add_sub_generator.py, rational_expr_mult_div_generator.py, rational_expr_simplify_generator.py, rational_function_features_generator.py, recursive_explicit_generator.py, regression_generator.py, related_rates_generator.py, right_triangle_trig_generator.py, row_reduction_generator.py, separable_ode_generator.py, separable_pde_generator.py, series_convergence_generator.py, series_solution_generator.py, set_algebra_laws_generator.py, set_expression_generator.py, set_operations_generator.py, simplify_expression_generator.py, sinusoid_features_generator.py, solid_revolution_generator.py, special_right_triangle_generator.py, special_solution_equation_generator.py, spin_half_generator.py, standard_form_conversion_generator.py, stars_and_bars_generator.py, synthetic_division_generator.py, tangent_line_generator.py, taxicab_geometry_generator.py, taylor_series_generator.py, trig_equation_generator.py, trig_identity_eval_generator.py, trig_identity_verify_generator.py, trig_six_functions_generator.py, u_substitution_generator.py, vector_ops_generator.py, z_transform_generator.py |
| `RG_SETUP` | 3 | `RG_SETUP\|one_loop\|alpha0=1/10\|beta=7,L=1/2` | running_coupling_generator.py |
| `RHO_ITER` | 4 | `RHO_ITER\|1\|x=18, y=40\|abs(r)=22\|gcd=11` | pollard_factorization_generator.py |
| `RICCI_ENTRY` | 2 | `RICCI_ENTRY\|R_phiphi\|1` | riemann_tensor_generator.py |
| `RIDGE_ENTRY` | 2 | `RIDGE_ENTRY\|K\|[[36,12], [12,4]]` | kernel_ridge_generator.py |
| `RIEMANN_ENTRY` | 2 | `RIEMANN_ENTRY\|R^phi_theta phi theta\|144/1369` | riemann_tensor_generator.py |
| `RIEMANN_SETUP` | 2, 3 | `RIEMANN_SETUP\|f(x) = x^2 + 4 on [-2, 6], n = 4\|midpoint Riemann sum` | riemann_sum_generator.py, riemann_tensor_generator.py |
| `RK_COMBINE` | 2 | `RK_COMBINE\|k1+2k2+2k3+k4\|-2553/32` | runge_kutta_generator.py |
| `RK_STAGE` | 3 | `RK_STAGE\|k1\|t=5/2\|v=5` | runge_kutta_generator.py |
| `RODRIGUES_FORM` | 2 | `RODRIGUES_FORM\|e^(theta K)\|I + sin(theta)K + (1-cos(theta))K^2` | lie_exponential_generator.py |
| `ROOT` | 1, 2, 3 | `ROOT\|1156\|34` | ac_circuit_generator.py, adam_step_generator.py, cholesky_generator.py, completing_square_generator.py, confidence_interval_generator.py, countability_bijection_generator.py, de_moivre_generator.py, doppler_generator.py, embedding_similarity_generator.py, energy_conservation_generator.py, factor_special_forms_generator.py, four_vector_generator.py, fundamental_form_generator.py, hypothesis_test_generator.py, invariant_mass_generator.py, joint_distribution_generator.py, ladder_operator_generator.py, layer_norm_generator.py, low_rank_approx_generator.py, matrix_norm_generator.py, metric_arc_length_generator.py, or_formula_generator.py, orbital_mechanics_generator.py, planck_units_generator.py, pythag_hyp_generator.py, qr_decomposition_generator.py, quadratic_generator.py, quadratic_square_root_generator.py, radical_add_sub_generator.py, radical_multiply_generator.py, radical_rationalize_generator.py, radical_variable_simplify_generator.py, rational_equation_generator.py, rational_exponent_generator.py, regression_generator.py, relativistic_energy_generator.py, round_solids_generator.py, rv_transform_generator.py, schwarzschild_generator.py, shm_generator.py, svd_generator.py, svm_margin_generator.py, two_sample_test_generator.py |
| `ROOT_ANGLE` | 2 | `ROOT_ANGLE\|k=0\|135 deg` | de_moivre_generator.py |
| `ROOT_EXTRACT` | 2 | `ROOT_EXTRACT\|15` | exponent_generator.py |
| `ROOT_IDENTIFY` | 3 | `ROOT_IDENTIFY\|225\|perfect_square\|15` | exponent_generator.py |
| `ROOT_SETUP` | 1 | `ROOT_SETUP\|√225` | exponent_generator.py, radical_add_sub_generator.py, radical_multiply_generator.py, radical_rationalize_generator.py, radical_variable_simplify_generator.py |
| `ROOT_SIMPLIFY` | 1, 2 | `ROOT_SIMPLIFY\|3√5` | complex_quadratic_generator.py, distance_formula_generator.py, dot_product_generator.py, euler_formula_generator.py, exponent_generator.py, geometric_mean_generator.py, hypercube_counting_generator.py, polar_parametric_generator.py, vector_ops_generator.py |
| `ROSTER` | 2 | `ROSTER\|S\|{2, 3, 5, 7, 11, 13}` | set_builder_roster_generator.py |
| `ROTATED_VECTOR` | 1 | `ROTATED_VECTOR\|(-4,0,4)` | quaternion_generator.py |
| `ROT_FORMULA` | 1 | `ROT_FORMULA\|I=I_cm+m*d^2` | rotational_dynamics_generator.py |
| `ROT_SETUP` | 3 | `ROT_SETUP\|parallel_axis\|I_cm=2, m=26\|d=7` | rotational_dynamics_generator.py |
| `ROUND` | 2 | `ROUND\|37/2\|19` | quantization_generator.py |
| `ROUNDTRIP_ERROR` | 2 | `ROUNDTRIP_ERROR\|sum_abs\|3/100` | quantization_generator.py |
| `ROUND_CHECK` | 3 | `ROUND_CHECK\|4\|8\|>=5` | place_value_rounding_generator.py |
| `ROUND_RESULT` | 2 | `ROUND_RESULT\|19148\|19150` | place_value_rounding_generator.py |
| `ROUTH_ROW` | 2 | `ROUTH_ROW\|s^3\|1, 2` | routh_hurwitz_generator.py |
| `ROUTH_SETUP` | 1 | `ROUTH_SETUP\|p(s)=s^3+6s^2+2s+19` | routh_hurwitz_generator.py |
| `ROW` | 2 | `ROW\|c=F, g=F, k=F\|T` | foundations_critic_generator.py |
| `ROW_ENTROPY` | 2 | `ROW_ENTROPY\|H0\|649/800` | entropy_rate_markov_generator.py |
| `ROW_OP` | 1, 2 | `ROW_OP\|R2 → R2 + R1\|[0, 1, 4]` | row_reduction_generator.py, simplex_generator.py, subspace_basis_generator.py |
| `RREF_RESULT` | 2 | `RREF_RESULT\|RREF(A)\|[[1, 0, 0, 0], [0, 1, 0, -1], [0, 0, 1, -1]]` | subspace_basis_generator.py |
| `RSA_DECRYPT` | 2 | `RSA_DECRYPT\|101\|24` | rsa_generator.py |
| `RSA_ENCRYPT` | 2 | `RSA_ENCRYPT\|24\|101` | rsa_generator.py |
| `RSA_PRIVATE_KEY` | 1 | `RSA_PRIVATE_KEY\|d=131` | rsa_generator.py |
| `RSA_PUBLIC_KEY` | 2 | `RSA_PUBLIC_KEY\|n=209\|e=11` | rsa_generator.py |
| `RSA_SETUP` | 3 | `RSA_SETUP\|p=11\|q=19\|message=24` | rsa_generator.py |
| `RSQ_FORMULA` | 1 | `RSQ_FORMULA\|r^2 = Sxy^2/(Sxx·Syy)` | regression_generator.py |
| `RS_CORRECT` | 2 | `RS_CORRECT\|position=1\|[79,63,93,43]` | reed_solomon_generator.py |
| `RS_EVAL` | 2 | `RS_EVAL\|x=74\|44` | reed_solomon_generator.py |
| `RS_LINE` | 3 | `RS_LINE\|m0=21\|m1=83\|agree=2` | reed_solomon_generator.py |
| `RS_PAIR` | 2 | `RS_PAIR\|x=4,70\|y=44,63` | reed_solomon_generator.py |
| `RS_RECEIVED` | 1 | `RS_RECEIVED\|[44,63,93,43]` | reed_solomon_generator.py |
| `RS_SETUP` | 3 | `RS_SETUP\|F_163\|m(x)=35+64x\|points 74,107,111,153` | reed_solomon_generator.py |
| `RUNNING_TOTAL` | 3 | `RUNNING_TOTAL\|0\|64\|64` | function_properties_generator.py |
| `S` | 3 | `S\|632\|594\|38` | ac_circuit_generator.py, activation_generator.py, adam_step_generator.py, angle_defect_generator.py, angle_measure_generator.py, annuity_generator.py, arc_length_generator.py, area_between_curves_generator.py, arithmetic_coding_generator.py, arithmetic_sequence_generator.py, backprop_generator.py, bayesian_update_generator.py, bec_channel_generator.py, binomial_probability_generator.py, bisection_generator.py, black_scholes_generator.py, calendar_arithmetic_generator.py, calorimetry_generator.py, cantor_pairing_generator.py, casimir_force_generator.py, casimir_generator.py, channel_capacity_generator.py, cholesky_generator.py, circle_angle_generator.py, circle_equation_generator.py, collision_generator.py, commutator_generator.py, complement_probability_generator.py, complex_locus_generator.py, complex_log_generator.py, complex_number_ops_generator.py, complex_quadratic_generator.py, composite_arithmetic_generator.py, confidence_interval_generator.py, continued_fraction_generator.py, continuous_distribution_generator.py, countability_bijection_generator.py, counting_classics_generator.py, cramers_rule_generator.py, decimal_div_generator.py, definite_integral_generator.py, density_matrix_generator.py, derangement_generator.py, determinant_generator.py, dft_generator.py, distance_formula_generator.py, doppler_generator.py, ellipse_features_generator.py, elliptic_curve_finite_field_generator.py, embedding_similarity_generator.py, entropy_generator.py, equilibrium_ice_generator.py, euler_characteristic_generator.py, euler_circuit_generator.py, euler_method_generator.py, expected_value_generator.py, exponential_model_generator.py, extended_euclid_generator.py, finance_generator.py, finite_difference_generator.py, first_law_generator.py, five_number_summary_generator.py, four_vector_generator.py, fourier_series_generator.py, fractal_iteration_generator.py, fraction_op_generator.py, function_inner_product_generator.py, function_operations_generator.py, fundamental_counting_principle_generator.py, fundamental_form_generator.py, game_theory_generator.py, gaussian_curvature_generator.py, generating_function_generator.py, geometric_distribution_generator.py, geometric_sequence_generator.py, gradient_descent_generator.py, gradient_step_generator.py, graph_interpret_generator.py, graph_traversal_generator.py, hamiltonian_generator.py, heat_engine_generator.py, hermitian_check_generator.py, hydrogen_atom_generator.py, hyperbola_features_generator.py, hyperbolic_distance_generator.py, hyperbolic_function_generator.py, hypercube_counting_generator.py, hypothesis_test_generator.py, inclusion_exclusion_generator.py, index_gymnastics_generator.py, information_gain_generator.py, integrating_factor_generator.py, interpolation_generator.py, invariant_mass_generator.py, joint_distribution_generator.py, kernel_evaluation_generator.py, kernel_ridge_generator.py, kernel_validity_generator.py, kinematics_generator.py, kmeans_step_generator.py, knn_generator.py, kraft_inequality_generator.py, ladder_operator_generator.py, lagrangian_generator.py, layer_norm_generator.py, legendre_construction_generator.py, linear_simple_generator.py, logistic_growth_generator.py, long_division_generator.py, low_rank_approx_generator.py, lp_corner_generator.py, lr_schedule_generator.py, manual_square_root_generator.py, markov_chain_generator.py, matrix_group_check_generator.py, matrix_inverse_generator.py, matrix_ops_generator.py, mean_value_theorem_generator.py, metric_arc_length_generator.py, mgf_generator.py, midpoint_generator.py, minkowski_interval_generator.py, mixed_number_operation_generator.py, mle_generator.py, mobius_transform_generator.py, modular_inverse_generator.py, mutual_information_generator.py, naive_bayes_generator.py, named_distribution_generator.py, newton_raphson_generator.py, newtons_laws_generator.py, normal_table_generator.py, npv_irr_generator.py, ode_substitution_generator.py, ode_system_generator.py, optics_generator.py, optimization_generator.py, or_formula_generator.py, order_of_operations_generator.py, order_statistics_generator.py, parabola_features_generator.py, parametric_calculus_generator.py, particle_in_box_generator.py, pca_generator.py, percent_problem_generator.py, percent_word_problem_generator.py, permutation_group_generator.py, ph_calculation_generator.py, piecewise_evaluation_generator.py, polar_parametric_generator.py, pollard_factorization_generator.py, positive_definite_generator.py, probability_addition_rule_generator.py, quadratic_residue_generator.py, quantization_generator.py, quantum_formula_generator.py, quaternion_generator.py, radical_add_sub_generator.py, radical_rationalize_generator.py, rational_expr_add_sub_generator.py, recurrence_generator.py, regression_generator.py, related_rates_generator.py, riemann_sum_generator.py, riemann_tensor_generator.py, rotational_dynamics_generator.py, routh_hurwitz_generator.py, row_reduction_generator.py, rsa_generator.py, runge_kutta_generator.py, rv_transform_generator.py, schwarzschild_generator.py, second_order_ode_generator.py, segment_partition_generator.py, separable_pde_generator.py, series_convergence_generator.py, set_counting_generator.py, shm_generator.py, signal_arithmetic_generator.py, slope_two_points_generator.py, softmax_gradient_generator.py, solid_revolution_generator.py, special_relativity_generator.py, spherical_excess_generator.py, spin_half_generator.py, standing_wave_generator.py, stars_and_bars_generator.py, statics_generator.py, stereographic_generator.py, taxicab_geometry_generator.py, taylor_series_generator.py, telescoping_generator.py, temperature_conversion_generator.py, tip_bill_split_generator.py, totient_generator.py, transformation_generator.py, transportation_generator.py, triangle_solve_generator.py, trig_identity_eval_generator.py, trig_six_functions_generator.py, two_sample_test_generator.py, undetermined_coeff_generator.py, unit_circle_generator.py, vector_ops_generator.py, venn_region_count_generator.py, z_score_generator.py |
| `SAMPLE_MOMENT` | 2 | `SAMPLE_MOMENT\|xbar\|98/9` | method_of_moments_generator.py |
| `SAMPLE_SIZE_FORMULA` | 1 | `SAMPLE_SIZE_FORMULA\|n = (z*·σ/E)^2` | confidence_interval_generator.py |
| `SAMPLE_SPACE` | 3 | `SAMPLE_SPACE\|ordered digit cards\|17, 18, 71, 78, 81, 87\|6` | sample_space_list_generator.py |
| `SA_BASES` | 2 | `SA_BASES\|2π(50)² = 2π × 2500\|5000π` | volume_3d_generator.py |
| `SA_FACES` | 3 | `SA_FACES\|top/bottom\|8 × 5\|40` | volume_3d_generator.py |
| `SA_FORMULA` | 1 | `SA_FORMULA\|SA = 2(lw + lh + wh)` | round_solids_generator.py, volume_3d_generator.py |
| `SA_LATERAL` | 2 | `SA_LATERAL\|2π × 50 × 11\|1100π` | volume_3d_generator.py |
| `SA_SETUP` | 2 | `SA_SETUP\|rectangular_prism\|l=8, w=5, h=5` | volume_3d_generator.py |
| `SA_TOTAL` | 2 | `SA_TOTAL\|SA = 2(40 + 40 + 25)\|210` | round_solids_generator.py, volume_3d_generator.py |
| `SB_FORMULA` | 1 | `SB_FORMULA\|C(n-1, k-1)` | stars_and_bars_generator.py |
| `SB_SETUP` | 2 | `SB_SETUP\|x1+...+x4 = 16\|xi >= 1` | stars_and_bars_generator.py |
| `SCALE_DIV` | 3 | `SCALE_DIV\|1232\|28\|44` | scaling_generator.py |
| `SCALE_EXACT` | 2 | `SCALE_EXACT\|11*cos\|0` | de_moivre_generator.py, euler_formula_generator.py |
| `SCALE_IDENTIFY` | 2 | `SCALE_IDENTIFY\|17.25 centimeters\|actual_dimension` | scaling_generator.py |
| `SCALE_MODE` | 3 | `SCALE_MODE\|λ = -6\|36*44\|1584` | diagonalization_generator.py |
| `SCALE_MULT` | 3 | `SCALE_MULT\|17.25\|35\|603.75` | scaling_generator.py |
| `SCALE_SETUP` | 3 | `SCALE_SETUP\|1 centimeter\|35 meters\|35` | scaling_generator.py |
| `SCALE_SHIFT` | 2 | `SCALE_SHIFT\|1\|-3` | layer_norm_generator.py |
| `SCALING_COMPUTE` | 2 | `SCALING_COMPUTE\|6ND\|17442000000000000000` | scaling_law_generator.py |
| `SCALING_SETUP` | 3 | `SCALING_SETUP\|N=57000000\|D=51000000000\|F=36000000000000000` | scaling_law_generator.py |
| `SCAN` | 2 | `SCAN\|(\|parenthesis depth 1` | wff_parsing_generator.py |
| `SCHWARZSCHILD_SETUP` | 3, 4 | `SCHWARZSCHILD_SETUP\|radius\|G=7\|M=10\|c=1` | schwarzschild_generator.py |
| `SCI_IDENTIFY` | 2 | `SCI_IDENTIFY\|1.49\|-9` | exponent_generator.py |
| `SCI_MOVE_DECIMAL` | 2 | `SCI_MOVE_DECIMAL\|right\|9` | exponent_generator.py |
| `SCI_OPERATION` | 4 | `SCI_OPERATION\|divide_coefficients\|7.14\|1.4\|5.1` | exponent_generator.py |
| `SCI_SETUP` | 1 | `SCI_SETUP\|(7.14 × 10^6) ÷ (1.4 × 10^-6)` | exponent_generator.py |
| `SCORE_EQ` | 1 | `SCORE_EQ\|8/p=4/(1-p)` | mle_generator.py |
| `SEARCH_BOUNDS` | 3 | `SEARCH_BOUNDS\|iter 1\|lo=0\|hi=7` | algorithm_trace_generator.py |
| `SEARCH_STATE` | 2 | `SEARCH_STATE\|lo=0\|hi=2` | algorithm_trace_generator.py |
| `SECOND_DERIV_TEST` | 2 | `SECOND_DERIV_TEST\|f''(3) = -6 < 0\|local maximum at x = 3` | curve_analysis_generator.py, optimization_generator.py |
| `SECOND_PARTIAL` | 2 | `SECOND_PARTIAL\|f_xx\|-4` | hessian_classify_generator.py |
| `SECTION_FORMULA` | 1 | `SECTION_FORMULA\|P = (x1 + m/(m+n)·(x2 - x1), y1 + m/(m+n)·(y2 - y1))` | segment_partition_generator.py |
| `SECTION_SETUP` | 2 | `SECTION_SETUP\|A(8, 2), B(36, 23); ratio 3:4 from A\|point P` | segment_partition_generator.py |
| `SECTOR_FORMULA` | 1 | `SECTOR_FORMULA\|A = (θ/360)·πr^2` | arc_sector_generator.py |
| `SELECT_MIN` | 2 | `SELECT_MIN\|D\|0` | dijkstra_generator.py |
| `SELECT_RELEVANT` | 2 | `SELECT_RELEVANT\|base = 47, rate = 15%\|ignore 44 (irrelevant)` | percent_word_problem_generator.py, proportion_word_problem_generator.py |
| `SEPARATE` | 1, 2 | `SEPARATE\|y^2 dy = x^2 dx` | ode_substitution_generator.py, separable_ode_generator.py, separable_pde_generator.py |
| `SEPARATOR` | 3 | `SEPARATOR\|89/61\|in L(3/2)\|not in L(√2)` | dedekind_cut_generator.py |
| `SEQ_APPLY` | 1 | `SEQ_APPLY\|a_26 = 2 + (26 - 1)·-4` | arithmetic_sequence_generator.py, geometric_sequence_generator.py, recursive_explicit_generator.py |
| `SEQ_FORMULA` | 1 | `SEQ_FORMULA\|a_n = a_1 + (n - 1)d` | arithmetic_sequence_generator.py, geometric_sequence_generator.py, recursive_explicit_generator.py |
| `SEQ_SETUP` | 2 | `SEQ_SETUP\|2, -2, -6, -10, ...\|26th term` | arithmetic_sequence_generator.py, geometric_sequence_generator.py, recursive_explicit_generator.py |
| `SERIES` | 1 | `SERIES\|G=G1*G2` | transfer_function_generator.py |
| `SERIES_ASSUME` | 2 | `SERIES_ASSUME\|y\|sum a_n x^n` | series_solution_generator.py |
| `SERIES_GROUP` | 2 | `SERIES_GROUP\|even powers\|cos(theta)I` | lie_exponential_generator.py |
| `SERIES_SETUP` | 2 | `SERIES_SETUP\|Σ 1/n^(2/3), n ≥ 1\|converge or diverge?` | legendre_construction_generator.py, power_series_generator.py, series_convergence_generator.py |
| `SERIES_TERM` | 3 | `SERIES_TERM\|n=0\|1\|1` | grassmann_generator.py |
| `SETUP` | 1, 2 | `SETUP\|assume √5 = g/v in lowest terms; derive 5v² = g²` | direct_proof_algebra_generator.py, induction_verify_generator.py |
| `SETUP_PERCENT_EQ` | 1 | `SETUP_PERCENT_EQ\|810 = 0.36 * whole` | percent_problem_generator.py |
| `SET_SETUP` | 2, 3, 4 | `SET_SETUP\|A = {9, 14, 36}\|B = {1, 2, 5, 17, 31}\|C = {7, 14, 25}` | set_expression_generator.py, set_operations_generator.py |
| `SET_SIDE` | 2 | `SET_SIDE\|left\|∅` | counterexample_search_generator.py |
| `SHAPE` | 1 | `SHAPE\|existential restriction → conjunction` | english_to_logic_generator.py |
| `SHIFT` | 1, 2 | `SHIFT\|yi = xi - 1\|y1+...+y4 = 12` | algorithm_trace_generator.py, recurrence_generator.py, stars_and_bars_generator.py, z_transform_generator.py |
| `SHM_FORMULA` | 1 | `SHM_FORMULA\|omega^2=g/L` | shm_generator.py |
| `SHM_SETUP` | 3 | `SHM_SETUP\|pendulum_period\|g=10\|L=2/5` | shm_generator.py |
| `SHORTEST` | 2 | `SHORTEST\|(4,-4)\|norm^2=32` | lll_reduction_generator.py |
| `SIDE` | 2 | `SIDE\|left\|∉` | set_identity_membership_table_generator.py |
| `SIGFIG_ROUND` | 3 | `SIGFIG_ROUND\|48600\|2 significant figures\|4.9 × 10^4` | fermi_estimation_generator.py |
| `SIGMA_EXPAND` | 1 | `SIGMA_EXPAND\|30 + 31 + 32` | sigma_notation_generator.py |
| `SIGMA_SETUP` | 2 | `SIGMA_SETUP\|Σ_(k=10)^(12) (k + 20)\|expand and evaluate` | sigma_notation_generator.py |
| `SIGMA_TERM` | 3 | `SIGMA_TERM\|k=10\|(10) + 20\|30` | sigma_notation_generator.py |
| `SIGN` | 3 | `SIGN\|left\|-16\|negative` | bisection_generator.py |
| `SIGNAL_SETUP` | 2, 3 | `SIGNAL_SETUP\|sampling\|f_max=897 Hz\|f_s=978 Hz` | signal_arithmetic_generator.py |
| `SIGN_CHART` | 2 | `SIGN_CHART\|critical values\|-6, 4` | polynomial_inequality_generator.py |
| `SIGN_RULE` | 2 | `SIGN_RULE\|arcsin of a negative\|negative angle` | trig_equation_generator.py, trig_identity_eval_generator.py, trig_six_functions_generator.py, unit_circle_generator.py |
| `SIGN_TEST` | 4 | `SIGN_TEST\|(-inf, 0)\|y = -1\|f(y) = 12 (positive)\|up` | stability_generator.py |
| `SIMILAR_APPLY` | 3 | `SIMILAR_APPLY\|3\|0.5\|1.5` | scaling_generator.py |
| `SIMILAR_SCALE` | 3 | `SIMILAR_SCALE\|4\|8\|0.5` | scaling_generator.py |
| `SIMILAR_SETUP` | 3 | `SIMILAR_SETUP\|triangle\|3,8,3\|4 (others unknown)` | scaling_generator.py |
| `SIMPLEX_SETUP` | 3 | `SIMPLEX_SETUP\|max z=15x+12y\|x<=11\|y<=13` | simplex_generator.py |
| `SIM_SETUP` | 2 | `SIM_SETUP\|△ABC ~ △DEF; DE = 20, AB = 5, EF = 12\|find BC` | similar_triangles_generator.py |
| `SIN` | 2 | `SIN\|2pi/3\|sqrt(3)/2` | positional_encoding_generator.py |
| `SINGULAR_VALUE` | 2 | `SINGULAR_VALUE\|sigma1\|15` | low_rank_approx_generator.py |
| `SINUSOID_SETUP` | 2 | `SINUSOID_SETUP\|y = 3cos(3(x - 45°)) - 6\|amplitude, period, phase shift, midline` | sinusoid_features_generator.py |
| `SIZE_REDUCE` | 2 | `SIZE_REDUCE\|b2=(-11, 7)\|b2-1b1=(-13, 0)` | lll_reduction_generator.py |
| `SLOPE_CALC` | 2 | *(not observed in sampling)* | equation_from_two_points_generator.py |
| `SLOPE_FORMULA` | 1 | `SLOPE_FORMULA\|m = (y2 - y1) / (x2 - x1)` | equation_from_two_points_generator.py, regression_generator.py, slope_two_points_generator.py |
| `SLOPE_INT_IDENTIFY` | 2 | `SLOPE_INT_IDENTIFY\|Slope (m)\|-27` | slope_intercept_form_generator.py |
| `SLOPE_INT_MATCH` | 2 | `SLOPE_INT_MATCH\|Compare to Slope-Intercept Form\|y = mx + b` | slope_intercept_form_generator.py |
| `SLOPE_INT_SETUP` | 1 | `SLOPE_INT_SETUP\|y = -27x + 32` | slope_intercept_form_generator.py |
| `SLOPE_RESULT` | 1 | `SLOPE_RESULT\|4` | equation_from_two_points_generator.py |
| `SLOPE_SETUP` | 2 | `SLOPE_SETUP\|(4, -2)\|(5, 2)` | slope_two_points_generator.py |
| `SLOPE_SUBST` | 1 | `SLOPE_SUBST\|m = (2 - (-2)) / (5 - 4)` | equation_from_two_points_generator.py, slope_two_points_generator.py |
| `SLOPE_UNDEFINED` | 1 | `SLOPE_UNDEFINED\|Division by zero` | slope_two_points_generator.py |
| `SOFTMAX_EXP` | 2 | `SOFTMAX_EXP\|1,1\|1` | attention_generator.py, softmax_gradient_generator.py |
| `SOFTMAX_PROB` | 2 | `SOFTMAX_PROB\|1\|1/3` | softmax_gradient_generator.py |
| `SOFTMAX_SETUP` | 3 | `SOFTMAX_SETUP\|z=(2*ln(5),2*ln(7),2*ln(3))\|T=2\|target=1` | softmax_gradient_generator.py |
| `SOFTMAX_WEIGHT` | 2 | `SOFTMAX_WEIGHT\|1,1\|1/2` | attention_generator.py |
| `SOLUTIONS` | 2 | `SOLUTIONS\|cos x = √2/2\|45°, 315°, 405°, 675°, 765°, 1035°, 1125°, 1395°, 1485°, 1755°, 1845°, 2115°, 2205°, 2475°, 2565°, 2835°, 2925°, 3195°, 3285°, 3555°, 3645°, 3915°, 4005°, 4275°, 4365°, 4635°, 4725°, 4995°, 5085°, 5355°, 5445°, 5715°, 5805°, 6075°, 6165°, 6435°, 6525°, 6795°, 6885°, 7155°, 7245°, 7515°, 7605°, 7875°` | trig_equation_generator.py |
| `SOLUTION_FORMULA` | 1 | `SOLUTION_FORMULA\|M_final=(Ma*Va+Mb*Vb)/(Va+Vb)` | solution_chem_generator.py |
| `SOLUTION_SETUP` | 3 | `SOLUTION_SETUP\|mixing_molarity\|Ma=3/2, Va=26\|Mb=5, Vb=142` | solution_chem_generator.py |
| `SOLVE_CONST` | 2 | `SOLVE_CONST\|C1 = -4\|C2 = 4` | ode_system_generator.py, second_order_ode_generator.py, undetermined_coeff_generator.py |
| `SOLVE_U` | 2 | `SOLVE_U\|e^(-5x)u = e^(-5x) + C\|u = 1 + Ce^(5x)` | ode_substitution_generator.py |
| `SOLVE_Y` | 2 | `SOLVE_Y\|e^(3x)y = 3e^(6x) + C\|y = 3e^(3x) + Ce^(-3x)` | integrating_factor_generator.py, laplace_ivp_generator.py, ode_substitution_generator.py |
| `SOL_ENTRY` | 3 | `SOL_ENTRY\|x1(t)\|(-7*e^(4t) + 8*e^(5t))*2 + (-8*e^(4t) + 8*e^(5t))*(-5)\|26*e^(4t) - 24*e^(5t)` | matrix_exponential_generator.py |
| `SOL_FORM` | 1, 2 | `SOL_FORM\|y = C1e^(-x) + C2e^(3x)` | ode_system_generator.py, second_order_ode_generator.py, undetermined_coeff_generator.py, variation_parameters_generator.py |
| `SORT` | 2 | `SORT\|9,15,20,2,1\|1,2,9,15,20` | five_number_summary_generator.py, simple_stats_generator.py |
| `SORT_EDGES` | 1 | `SORT_EDGES\|AC=3, BC=5, AB=6, BD=18` | mst_generator.py |
| `SPECIAL_SOLUTION` | 2 | `SPECIAL_SOLUTION\|-1 = -8\|contradiction: no value of x works` | radical_equation_generator.py, special_solution_equation_generator.py |
| `SPEED` | 2, 3 | `SPEED\|sqrt(a^2 + b^2)\|sqrt((-7)^2 + 24^2)\|25` | curve_geometry_generator.py |
| `SPHERICAL_BOUNDS` | 2 | `SPHERICAL_BOUNDS\|rho\|0..2` | triple_integral_generator.py |
| `SPHERICAL_CONVERT` | 2 | `SPHERICAL_CONVERT\|3 dV\|3*rho^2*sin(phi) drho dphi dtheta` | triple_integral_generator.py |
| `SPHERICAL_COSINES` | 1 | `SPHERICAL_COSINES\|cos(c)=sin(lat1)sin(lat2)+cos(lat1)cos(lat2)cos(dlon)` | great_circle_generator.py |
| `SPHERICAL_COSINE_LAW` | 1 | `SPHERICAL_COSINE_LAW\|cos(a)=cos(b)cos(c)+sin(b)sin(c)cos(A)` | spherical_triangle_generator.py |
| `SPHERICAL_EXCESS_SETUP` | 2 | `SPHERICAL_EXCESS_SETUP\|R=20\|angles=150,135,90` | spherical_excess_generator.py |
| `SPHERICAL_SINE_LAW` | 1 | `SPHERICAL_SINE_LAW\|sin(A)/sin(a)=sin(B)/sin(b)` | spherical_triangle_generator.py |
| `SPHERICAL_TRIANGLE_SETUP` | 2 | `SPHERICAL_TRIANGLE_SETUP\|a=150 deg, b=135 deg, A=150 deg\|find sin(B)` | spherical_triangle_generator.py |
| `SPIN_COMPONENT` | 2 | `SPIN_COMPONENT\|row=1\|56/65` | spin_half_generator.py |
| `SPIN_SETUP` | 3 | `SPIN_SETUP\|measurement_probability\|axis=x\|psi=[-112/113,-15/113]` | spin_half_generator.py |
| `SPLIT_MIDDLE` | 2 | `SPLIT_MIDDLE\|15x = 12x + 3x\|4x^2 + 12x + 3x + 9` | factor_trinomial_generator.py |
| `SPLIT_SETUP` | 3 | `SPLIT_SETUP\|source\|left pos=0, neg=8\|right pos=2, neg=6` | information_gain_generator.py |
| `SQRT_BOTH_SIDES` | 2 | `SQRT_BOTH_SIDES\|x^2 = 225\|x = ±15` | completing_square_generator.py, quadratic_square_root_generator.py, rational_equation_generator.py |
| `SQRT_DIGIT` | 2 | `SQRT_DIGIT\|5\|root = 5` | manual_square_root_generator.py |
| `SQRT_NEG` | 2 | `SQRT_NEG\|√(-1332)\|i√1332` | complex_quadratic_generator.py, polynomial_zeros_generator.py |
| `SQRT_SETUP` | 2 | `SQRT_SETUP\|N = 258064\|groups 25, 80, 64` | manual_square_root_generator.py |
| `SQRT_TRIAL` | 3 | `SQRT_TRIAL\|x = 5\|(0 + 5)*5 = 25\|fits` | manual_square_root_generator.py |
| `SQUARE_BOTH_SIDES` | 2 | `SQUARE_BOTH_SIDES\|√(x + 8) = x - 4\|x + 8 = (x - 4)^2` | radical_equation_generator.py |
| `SQUARE_FACTOR` | 3 | `SQUARE_FACTOR\|53429\|529 × 101\|529` | radical_add_sub_generator.py, radical_multiply_generator.py, radical_rationalize_generator.py, radical_variable_simplify_generator.py |
| `SQUARE_TEST` | 3 | `SQUARE_TEST\|44\|6^2 = 36, 7^2 = 49\|not a perfect square` | discriminant_generator.py |
| `STABILITY` | 3 | `STABILITY\|y=0\|left up, right down\|stable` | stability_generator.py |
| `STANDING_BOUNDARY` | 1 | `STANDING_BOUNDARY\|open-open pipe allows n=1,2,3,...` | standing_wave_generator.py |
| `STANDING_FORMULA` | 1 | `STANDING_FORMULA\|lambda=2L/n, f=v/lambda` | standing_wave_generator.py |
| `STANDING_SETUP` | 3 | `STANDING_SETUP\|open_pipe\|n=5\|L=6, v=135` | standing_wave_generator.py |
| `STATEMENT_EVAL` | 3 | `STATEMENT_EVAL\|Gia says Gia and Ravi are different types\|F\|contradiction` | knights_knaves_generator.py |
| `STATICS_FORMULA` | 1 | `STATICS_FORMULA\|sum_tau_left=0 => RB*L=W*x` | statics_generator.py |
| `STATICS_SETUP` | 3 | `STATICS_SETUP\|supported_beam\|W=144, L=6\|x=1` | statics_generator.py |
| `STATIONARY` | 2 | `STATIONARY\|pi0=1/2\|pi1=1/2` | entropy_rate_markov_generator.py |
| `STAT_ABS_DEV` | 2 | `STAT_ABS_DEV\|5\|5` | statistics_generator.py |
| `STAT_AVERAGE` | 2 | `STAT_AVERAGE\|(67 + 72) / 2\|69.5` | statistics_generator.py |
| `STAT_COUNT` | 1 | `STAT_COUNT\|10` | statistics_generator.py |
| `STAT_DEVIATION` | 3 | `STAT_DEVIATION\|51\|46\|5` | statistics_generator.py |
| `STAT_DIVIDE` | 2 | `STAT_DIVIDE\|380 / 10\|38` | statistics_generator.py |
| `STAT_FREQUENCY` | 2 | `STAT_FREQUENCY\|11\|1` | statistics_generator.py |
| `STAT_MAD` | 3 | `STAT_MAD\|20\|5\|4` | statistics_generator.py |
| `STAT_MAX` | 1 | `STAT_MAX\|92` | statistics_generator.py |
| `STAT_MEAN` | 2 | `STAT_MEAN\|230 / 5\|46` | statistics_generator.py |
| `STAT_MIDDLE` | 2 | `STAT_MIDDLE\|position 5\|43` | statistics_generator.py |
| `STAT_MIN` | 1 | `STAT_MIN\|13` | statistics_generator.py |
| `STAT_MODE` | 2 | `STAT_MODE\|No mode\|All values appear with same frequency` | statistics_generator.py |
| `STAT_ORDER` | 1 | `STAT_ORDER\|10, 25, 35, 40, 43, 62, 70, 96, 99` | statistics_generator.py |
| `STAT_RANGE` | 2 | `STAT_RANGE\|92 - 13\|79` | statistics_generator.py |
| `STAT_SETUP` | 1 | `STAT_SETUP\|30, 14, 16, 55, 36, 28, 26, 63, 51, 61` | statistics_generator.py |
| `STAT_SUM` | 2 | `STAT_SUM\|30 + 14 + 16 + 55 + 36 + 28 + 26 + 63 + 51 + 61\|380` | statistics_generator.py |
| `STD` | 1 | `STD\|4` | layer_norm_generator.py |
| `STEADY_EQUATION` | 2 | `STEADY_EQUATION\|pi0*pi01=pi1*pi10\|pi0+pi1=1` | markov_chain_generator.py |
| `STEPPING_STONE` | 2 | `STEPPING_STONE\|enter x21\|+x21 -x22 +x12 -x11` | transportation_generator.py |
| `STEREO_SETUP` | 3, 4 | `STEREO_SETUP\|sphere_to_plane\|X=36/241\|Y=168/241\|Z=169/241` | stereographic_generator.py |
| `STIRLING_CELL` | 3 | `STIRLING_CELL\|S(1,1)\|1×0+1\|1` | set_counting_generator.py |
| `STMT_EVAL` | 3 | `STMT_EVAL\|p\|6 is prime\|F` | logical_connective_eval_generator.py |
| `STOICH_RATIO` | 2 | `STOICH_RATIO\|H2->NH3\|2/3=2/3` | gas_stoichiometry_generator.py, stoichiometry_generator.py |
| `STOICH_SETUP` | 2, 3 | `STOICH_SETUP\|mass_to_mass\|N2 + 3 H2 -> 2 NH3\|given=8 g H2, target=NH3` | stoichiometry_generator.py |
| `STRUCTURE_CONSTANT` | 3 | `STRUCTURE_CONSTANT\|epsilon_xzy\|-1\|108iJy` | structure_constant_generator.py |
| `STRUCTURE_SETUP` | 3 | `STRUCTURE_SETUP\|A=-18Jx\|B=6Jz\|epsilon_xzy=-1` | structure_constant_generator.py |
| `SU3_SETUP` | 2 | `SU3_SETUP\|left=3\|right=3bar` | young_tableaux_generator.py |
| `SUBEXPR` | 2 | `SUBEXPR\|A ∪ B\|{1, 2, 5, 9, 14, 17, 31, 36}` | set_expression_generator.py, set_operations_generator.py |
| `SUBGROUP` | 2 | `SUBGROUP\|H={1, 13}\|size 2` | coset_generator.py |
| `SUBGROUP_ELEM` | 2 | `SUBGROUP_ELEM\|k=1\|17` | coset_generator.py, cyclic_group_generator.py |
| `SUBGROUP_START` | 2 | `SUBGROUP_START\|H=<13>\|identity 1` | coset_generator.py |
| `SUBPROOF_CLOSE` | 3 | `SUBPROOF_CLOSE\|→I\|lines 2–3\|v → t` | natural_deduction_generator.py |
| `SUBPROOF_OPEN` | 2 | `SUBPROOF_OPEN\|assume\|v` | natural_deduction_generator.py |
| `SUBSET_CHECK` | 3 | `SUBSET_CHECK\|{26}\|subset of A?\|yes` | set_membership_subset_generator.py |
| `SUBSET_SIZE` | 2 | `SUBSET_SIZE\|0\|∅` | set_operations_generator.py |
| `SUBST` | 2, 3 | `SUBST\|x\|-1\|-5(-1)-4y-8` | arc_length_generator.py, chain_rule_generator.py, curve_analysis_generator.py, derivative_limit_def_generator.py, evaluate_expression_generator.py, function_composition_generator.py, function_evaluation_generator.py, function_operations_generator.py, function_table_generator.py, implicit_diff_generator.py, integrating_factor_generator.py, legendre_construction_generator.py, lhopital_generator.py, limit_evaluation_generator.py, line_integral_generator.py, linear_approx_generator.py, log_diff_higher_order_generator.py, logistic_growth_generator.py, mean_value_theorem_generator.py, ode_substitution_generator.py, optimization_generator.py, parametric_calculus_generator.py, partial_fractions_generator.py, piecewise_evaluation_generator.py, polar_parametric_generator.py, power_series_generator.py, recursive_explicit_generator.py, related_rates_generator.py, remainder_factor_theorem_generator.py, second_order_ode_generator.py, separable_ode_generator.py, tangent_line_generator.py, taylor_series_generator.py, trig_equation_generator.py, u_substitution_generator.py, undetermined_coeff_generator.py |
| `SUBSTITUTE` | 2, 3 | `SUBSTITUTE\|(p ∨ (q ∨ r)) → (q ∨ (p ∨ r))\|p := a ∨ ¬d; q := j → b; r := (k ∨ h) → (n ∨ h)\|((a ∨ ¬d) ∨ ((j → b) ∨ ((k ∨ h) → (n ∨ h)))) → ((j → b) ∨ ((a ∨ ¬d) ∨ ((k ∨ h) → (n ∨ h))))` | hilbert_axiom_derivation_generator.py, lambda_reduction_generator.py |
| `SUBSTITUTION` | 2 | `SUBSTITUTION\|y = vx\|dy/dx = v + x dv/dx` | ode_substitution_generator.py |
| `SUB_COL` | 3 | `SUB_COL\|col_1\|5-6-borrow0\|->9 (borrow_out 1)` | multi_digit_subtraction_generator.py |
| `SUM` | 2, 3 | `SUM\|20 + 16 + 26\|62` | bayesian_update_generator.py, experimental_probability_generator.py, likelihood_language_generator.py, method_of_moments_generator.py, mle_generator.py, regression_generator.py |
| `SUM_ORDER` | 2 | `SUM_ORDER\|Σ i^8\|n^9` | master_theorem_generator.py |
| `SUPPORT` | 2 | `SUPPORT\|0<=x<=22\|0<=y<=484` | rv_transform_generator.py |
| `SUPPORT_TERM` | 2 | `SUPPORT_TERM\|1\|(-3,0)` | svm_margin_generator.py |
| `SVM_SETUP` | 3 | `SVM_SETUP\|x1=(3,0),y1=-1,alpha1=1\|x2=(0,4),y2=-1,alpha2=1\|b=1,x=(1,-1)` | svm_margin_generator.py |
| `SWAP` | 2 | `SWAP\|norm b2=53\|norm b1=170` | lll_reduction_generator.py |
| `SWAP_VARS` | 1 | `SWAP_VARS\|x = 4y - 3` | inverse_function_generator.py |
| `SYMBOL_CODE` | 2 | `SYMBOL_CODE\|position 1: )\|3` | godel_numbering_generator.py |
| `SYMMETRIC_CHECK` | 3 | `SYMMETRIC_CHECK\|(15, 15)\|reverse (15, 15)\|present` | equivalence_relation_generator.py, relation_check_generator.py |
| `SYMMETRY` | 2 | `SYMMETRY\|odd function\|a0=0, a_n=0` | fourier_series_generator.py |
| `SYNDIV_SETUP` | 2 | `SYNDIV_SETUP\|x^3 - x^2 - 9x - 8\|r = -2` | polynomial_zeros_generator.py, synthetic_division_generator.py |
| `SYNDROME_CALC` | 2 | `SYNDROME_CALC\|s1=b1 xor b3 xor b5 xor b7\|1 xor 1 xor 0 xor 1=1` | hamming_code_generator.py |
| `SYNDROME_VALUE` | 2 | `SYNDROME_VALUE\|s1=1, s2=0, s4=1\|position=5` | hamming_code_generator.py |
| `SYN_DROP` | 1 | `SYN_DROP\|1` | horner_evaluation_generator.py, polynomial_zeros_generator.py, synthetic_division_generator.py |
| `SYN_ROW` | 1 | `SYN_ROW\|1, -3, -3, -2` | polynomial_zeros_generator.py, synthetic_division_generator.py |
| `SYS_ADD` | 1 | `SYS_ADD\|Add equations: -7y = -14` | systems_elimination_generator.py |
| `SYS_EQ_NEW` | 1 | `SYS_EQ_NEW\|New equation with y only` | systems_substitution_generator.py |
| `SYS_ISOLATE` | 2 | `SYS_ISOLATE\|Isolate x in Eq 1\|x = 3y - 12` | systems_substitution_generator.py |
| `SYS_MULT` | 1 | `SYS_MULT\|Eq2 * -1` | systems_elimination_generator.py |
| `SYS_REWRITE` | 2 | `SYS_REWRITE\|x - 2y = -11\|-x - 5y = -3` | systems_elimination_generator.py |
| `SYS_SETUP` | 2 | `SYS_SETUP\|x = y - 18\|5x + 4y = -9` | systems_elimination_generator.py, systems_substitution_generator.py |
| `SYS_SUBST` | 1 | `SYS_SUBST\|Substitute (y - 18) for x in Eq 2` | systems_substitution_generator.py |
| `SYS_SUBST_BACK` | 1 | `SYS_SUBST_BACK\|Substitute y=9 into Eq 1` | systems_elimination_generator.py, systems_substitution_generator.py |
| `TABLEAU` | 2, 3 | `TABLEAU\|initial\|s1: x + s1 = 11\|s2: y + s2 = 13` | simplex_generator.py |
| `TABLEAU_ROOT` | 1 | `TABLEAU_ROOT\|((n ∧ o) ∨ ¬n) ∧ ¬n` | semantic_tableau_generator.py |
| `TABLEAU_RULE` | 3 | `TABLEAU_RULE\|3 x 3bar\|box plus antibox gives adjoint plus singlet\|8 + 1` | young_tableaux_generator.py |
| `TABLE_COMPARE` | 1, 2 | `TABLE_COMPARE\|match` | foundations_critic_generator.py, set_identity_membership_table_generator.py |
| `TABLE_ENTRY` | 2 | `TABLE_ENTRY\|g(-3)\|13` | euler_method_generator.py, function_table_generator.py, taylor_series_generator.py |
| `TABLE_LOOKUP` | 2 | `TABLE_LOOKUP\|f(-3)\|-10` | de_moivre_generator.py, dot_product_generator.py, euler_formula_generator.py, function_evaluation_generator.py, lie_exponential_generator.py, normal_table_generator.py, pascal_triangle_generator.py, polar_parametric_generator.py, right_triangle_trig_generator.py, triangle_solve_generator.py, trig_equation_generator.py, trig_identity_eval_generator.py, unit_circle_generator.py |
| `TALLY` | 2 | `TALLY\|amber\|33` | experimental_probability_generator.py |
| `TANGENT_PLANE` | 2 | `TANGENT_PLANE\|z = z0 + fx(x-a) + fy(y-b)\|z = 45 + 30*(x - 3) + 11*(y - 0)` | gradient_generator.py |
| `TARGET_STATE` | 2 | `TARGET_STATE\|J=1\|M=0` | clebsch_gordan_generator.py |
| `TAYLOR_FORMULA` | 1 | `TAYLOR_FORMULA\|P_n(x) = Σ f^(k)(a)/k!·(x - a)^k` | taylor_series_generator.py |
| `TAYLOR_SETUP` | 2 | `TAYLOR_SETUP\|f(x) = e^x, P_1 around 0\|bound the error at x = 2/3` | taylor_series_generator.py |
| `TELESCOPE_CANCEL` | 2 | `TELESCOPE_CANCEL\|all middle factors cancel\|8/152` | telescoping_generator.py |
| `TELE_SETUP` | 1 | `TELE_SETUP\|Π k=8..151 k/(k+1)` | telescoping_generator.py |
| `TEMP_SCALE` | 2 | `TEMP_SCALE\|z1/T\|ln(5)` | softmax_gradient_generator.py |
| `TENSOR_ENTRY` | 2 | `TENSOR_ENTRY\|S_11\|-5` | einstein_summation_generator.py, index_raising_generator.py |
| `TENSOR_RULE` | 1 | `TENSOR_RULE\|diag(a,b) tensor diag(c,d)=diag(ac,ad,bc,bd)` | tensor_product_generator.py |
| `TENSOR_SETUP` | 3 | `TENSOR_SETUP\|A=diag(-2,4)\|B=diag(5,2)\|u=[-4,2], v=[-3,0]` | tensor_product_generator.py |
| `TENSOR_STATE` | 2 | `TENSOR_STATE\|u tensor v\|[12,0,-6,0]` | tensor_product_generator.py |
| `TERM` | 2 | `TERM\|i=0: 1·(1/2)^0·(1/2)^5\|0.03125` | binomial_probability_generator.py |
| `TERMS` | 1 | `TERMS\|y[0..4]=[1,3,9,27,81]` | z_transform_generator.py |
| `TEST_CHOOSE` | 2 | `TEST_CHOOSE\|p-series\|Σ 1/n^p with p = 2/3` | power_series_generator.py, series_convergence_generator.py |
| `TEST_STAT_FORMULA` | 1 | `TEST_STAT_FORMULA\|z = (p̂ - p0)/√(p0(1-p0)/n)` | hypothesis_test_generator.py, two_sample_test_generator.py |
| `TF_SETUP` | 3 | `TF_SETUP\|ode\|y''+21y'+108y=3x'+27x\|zero initial conditions` | transfer_function_generator.py |
| `THEOREM` | 1, 2 | `THEOREM\|quadratic formula\|t = (-b ± √(b^2 - 4ac))/(2a)` | angle_defect_generator.py, circle_angle_generator.py, gauss_bonnet_generator.py, geometric_mean_generator.py, logistic_growth_generator.py, mean_value_theorem_generator.py, parametric_calculus_generator.py, polar_parametric_generator.py, quadratic_generator.py, rational_root_generator.py, remainder_factor_theorem_generator.py, series_convergence_generator.py, special_right_triangle_generator.py, spherical_excess_generator.py, taylor_series_generator.py, triangle_solve_generator.py, trig_identity_eval_generator.py, trig_six_functions_generator.py |
| `THEOREM_REWRITE` | 2 | `THEOREM_REWRITE\|circulation\|surface integral of curl F dot n` | vector_theorem_generator.py |
| `THEOREM_SETUP` | 3 | `THEOREM_SETUP\|Stokes\|F=<y, 0, 0>\|disk radius 12 in z=0` | vector_theorem_generator.py |
| `THETA` | 2 | `THETA\|min(11,9)\|9` | transportation_generator.py |
| `THROUGHPUT` | 2 | `THROUGHPUT\|tokens_per_second\|2000000000/19` | scaling_law_generator.py |
| `TIME_COMPONENT` | 2 | `TIME_COMPONENT\|k=1\|i` | braket_generator.py |
| `TIME_DERIV` | 2 | `TIME_DERIV\|d/dt(m*L^2*thetadot)\|m*L^2*thetaddot` | lagrangian_generator.py |
| `TIME_EVOLVE` | 2 | `TIME_EVOLVE\|U psi\|[i,-1-i,-2i]` | braket_generator.py |
| `TM_CONFIG` | 4 | `TM_CONFIG\|step 0\|state=q0\|head=0\|tape=11` | turing_machine_trace_generator.py |
| `TM_HALT` | 2 | `TM_HALT\|step 3\|halted` | turing_machine_trace_generator.py |
| `TM_MOVE` | 3 | `TM_MOVE\|0\|R\|1` | turing_machine_trace_generator.py |
| `TM_READ` | 2 | `TM_READ\|head=0\|1` | turing_machine_trace_generator.py |
| `TM_RULE` | 2 | `TM_RULE\|q0,1\|q0,_,R` | turing_machine_trace_generator.py |
| `TM_SETUP` | 3 | `TM_SETUP\|erase_ones\|input=11\|limit=5` | turing_machine_trace_generator.py |
| `TM_WRITE` | 2 | `TM_WRITE\|head=0\|_` | turing_machine_trace_generator.py |
| `TOPO_AVAILABLE` | 1 | `TOPO_AVAILABLE\|A` | graph_traversal_generator.py |
| `TOPO_PICK` | 2 | `TOPO_PICK\|available {6, 44, 47}\|pick 6` | partial_order_generator.py |
| `TOPO_READY` | 1 | `TOPO_READY\|B` | graph_traversal_generator.py |
| `TOPO_SELECT` | 2 | `TOPO_SELECT\|A\|A` | graph_traversal_generator.py |
| `TOTIENT_RESULT` | 2 | `TOTIENT_RESULT\|phi(42)\|12` | totient_generator.py |
| `TRACE` | 2 | `TRACE\|2 - 4\|-2` | ode_system_generator.py |
| `TRACE_ADD` | 4 | `TRACE_ADD\|gamma3gamma3\|(1,1)\|0 + -1\|-1` | gamma_matrix_generator.py |
| `TRACE_ENTRY` | 2 | `TRACE_ENTRY\|(1,1)\|8` | einstein_summation_generator.py, pauli_algebra_generator.py |
| `TRACE_EXPECT` | 1, 3 | `TRACE_EXPECT\|Tr(rho A)=p0*a+p1*b` | density_matrix_generator.py, gamma_matrix_generator.py |
| `TRACE_SUM` | 2 | `TRACE_SUM\|8 + 8\|16` | pauli_algebra_generator.py |
| `TRANSFER` | 1 | `TRANSFER\|H(s)=(3s+27)/(s^2+21s+108)` | transfer_function_generator.py |
| `TRANSFORM_APPLY` | 2 | `TRANSFORM_APPLY\|(-(3), -(-5))\|(-3, 5)` | transformation_generator.py |
| `TRANSFORM_RULE` | 1 | `TRANSFORM_RULE\|(x, y) → (-x, -y)` | transformation_generator.py |
| `TRANSFORM_SETUP` | 2, 3 | `TRANSFORM_SETUP\|P(3, -5)\|rotation 180° about the origin, then reflection over the y-axis` | rv_transform_generator.py, transformation_generator.py |
| `TRANSIENT_FORMULA` | 1 | `TRANSIENT_FORMULA\|tau=L/R` | transient_circuit_generator.py |
| `TRANSIENT_SETUP` | 3 | `TRANSIENT_SETUP\|rl_rise\|R=12, L=12\|V=30, t=6` | transient_circuit_generator.py |
| `TRANSITIVE_CHECK` | 2, 3 | `TRANSITIVE_CHECK\|(15, 15) and (15, 15)\|need (15, 15)\|present` | equivalence_relation_generator.py, hereditarily_finite_set_generator.py, relation_check_generator.py |
| `TRANSLATE` | 2 | `TRANSLATE\|Some pilot is vigilant\|∃w (T(w) ∧ Z(w))` | quantifier_negation_generator.py |
| `TRANSPORT_SETUP` | 3 | `TRANSPORT_SETUP\|supply=(23,11)\|demand=(9,25)\|costs=(4,7;3,7)` | transportation_generator.py |
| `TRIG_RATIO` | 2 | `TRIG_RATIO\|sin\|opposite/hypotenuse` | right_triangle_trig_generator.py |
| `TRIG_SETUP` | 2 | `TRIG_SETUP\|right triangle, angle 30°, hypotenuse = 92; given sin 30° ≈ 0.5\|the opposite side` | right_triangle_trig_generator.py, trig_identity_eval_generator.py, trig_six_functions_generator.py, unit_circle_generator.py |
| `TRIG_VALUE` | 2, 3 | `TRIG_VALUE\|sin(lat1)=0\|sin(lat2)=sqrt(3)/2\|cos(dlon)=1` | christoffel_generator.py, great_circle_generator.py, spherical_triangle_generator.py |
| `TRIPLE_EVAL` | 3 | `TRIPLE_EVAL\|rho_part * phi_part * angle\|3*8/3*2*2*pi\|32*pi` | triple_integral_generator.py |
| `TRIPLE_SETUP` | 3 | `TRIPLE_SETUP\|integrand 3\|ball radius 2\|spherical` | triple_integral_generator.py |
| `TRI_ANGLE_SETUP` | 3 | `TRI_ANGLE_SETUP\|34\|66\|x` | angle_relationships_generator.py |
| `TRI_ANGLE_SOLVE` | 2 | `TRI_ANGLE_SOLVE\|x = 180 - 34 - 66\|80` | angle_relationships_generator.py |
| `TRI_ANGLE_SUM` | 1 | `TRI_ANGLE_SUM\|34 + 66 + x = 180` | angle_relationships_generator.py |
| `TRI_AREA_FORMULA` | 1 | `TRI_AREA_FORMULA\|Area = (1/2)·a·b·sin C` | triangle_area_sas_generator.py |
| `TRI_SETUP` | 2 | `TRI_SETUP\|30-60-90 triangle, longer leg = 249√3\|shorter leg and hypotenuse` | special_right_triangle_generator.py, triangle_area_sas_generator.py, triangle_solve_generator.py |
| `TRUNCATE` | 2 | `TRUNCATE\|rank=1\|discard=3` | low_rank_approx_generator.py |
| `TRUTH_ROW` | 1, 2 | `TRUTH_ROW\|row 1\|p=T, q=T` | argument_form_generator.py, boolean_algebra_generator.py, truth_table_generator.py |
| `TRY` | 1, 2, 3 | `TRY\|x = 1\|0 < x ≤ 15 and x is prime\|false` | cantor_pairing_generator.py, conditional_forms_generator.py, counterexample_search_generator.py, factor_trinomial_generator.py, log_conversion_generator.py, log_equation_generator.py, polynomial_inequality_generator.py, radical_equation_generator.py, rational_equation_generator.py, rational_root_generator.py, set_builder_roster_generator.py, structure_isomorphism_generator.py |
| `TS_FACTOR` | 3 | `TS_FACTOR\|p-1=72\|q=9\|s=3` | tonelli_shanks_generator.py |
| `TS_INIT` | 4 | `TS_INIT\|m=3\|c=10\|t=72\|r=57` | tonelli_shanks_generator.py |
| `TS_LOOP` | 2 | `TS_LOOP\|i=1\|b=27` | tonelli_shanks_generator.py |
| `TS_NONRESIDUE` | 1 | `TS_NONRESIDUE\|5` | tonelli_shanks_generator.py |
| `TS_SETUP` | 2 | `TS_SETUP\|a=36\|p=73` | tonelli_shanks_generator.py |
| `TT_COLUMN` | 2 | `TT_COLUMN\|formula\|FFFF` | truth_table_generator.py |
| `TT_SETUP` | 2 | `TT_SETUP\|variables p, q\|4` | truth_table_generator.py |
| `TWIDDLE` | 1, 3 | `TWIDDLE\|W4=-i\|W4^2=-1\|W4^3=i` | dft_generator.py |
| `TWOS_SETUP` | 2 | `TWOS_SETUP\|8-bit two's complement\|offset = 2^8 = 256` | base_conversion_generator.py |
| `TYPE_ABS` | 2 | `TYPE_ABS\|lambda u\|c → e` | type_theory_generator.py |
| `TYPE_APP` | 3 | `TYPE_APP\|(y u)\|unify\|d → e` | type_theory_generator.py |
| `TYPE_ASSIGN` | 2 | `TYPE_ASSIGN\|m\|a` | type_theory_generator.py |
| `UB` | 2 | `UB\|{14, 35}\|∅` | partial_order_generator.py |
| `UC_GUESS` | 2 | `UC_GUESS\|constant forcing\|y_p = A` | undetermined_coeff_generator.py |
| `UC_POINT` | 2 | `UC_POINT\|270°\|(0, -1)` | unit_circle_generator.py |
| `UNCERTAINTY_SETUP` | 3 | `UNCERTAINTY_SETUP\|particle in a box\|L=1, hbar=1\|n=34` | uncertainty_generator.py |
| `UNFOLD` | 2 | `UNFOLD\|rev("deebbebdeede")\|rev("eebbebdeede") + "d"` | recursive_definition_unfold_generator.py |
| `UNIFY_BIND` | 3 | `UNIFY_BIND\|X\|b\|{X=b}` | unification_generator.py |
| `UNIFY_DECOMPOSE` | 2 | `UNIFY_DECOMPOSE\|f\|2 arguments` | unification_generator.py |
| `UNIFY_FAIL` | 1 | `UNIFY_FAIL\|occurs-check X in f(X)` | unification_generator.py |
| `UNIFY_PAIR` | 2 | `UNIFY_PAIR\|f(X,a)\|f(b,Y)` | unification_generator.py |
| `UNIFY_SETUP` | 3 | `UNIFY_SETUP\|f(X,a)\|f(b,Y)\|occurs-check` | unification_generator.py |
| `UNION_ELEMENT` | 2 | `UNION_ELEMENT\|{{∅, {∅}, {∅, {∅}}}, {∅, {∅}, {∅, {∅}}, {{∅}}}, {{∅}, {∅, {∅}}, {{∅}}}, {{∅}, {∅, {∅}}, {{{∅}}}}}\|contributes {{∅, {∅}, {∅, {∅}}}, {∅, {∅}, {∅, {∅}}, {{∅}}}, {{∅}, {∅, {∅}}, {{∅}}}, {{∅}, {∅, {∅}}, {{{∅}}}}}` | hereditarily_finite_set_generator.py |
| `UNIT_ATTACH` | 3 | `UNIT_ATTACH\|23\|km/hour\|23 km/hour` | cross_section_generator.py, kinematics_generator.py, physics_formula_generator.py |
| `UNIT_CONVERT` | 2 | `UNIT_CONVERT\|7 minutes\|420 seconds` | physics_formula_generator.py |
| `UNIT_NORMAL` | 2 | `UNIT_NORMAL\|T'(0)/norm T'(0)\|<-1, 0>` | curve_geometry_generator.py |
| `UNIT_RATE_DIV` | 3 | `UNIT_RATE_DIV\|$20.00\|10\|$2.00` | unit_rate_generator.py |
| `UNIT_RATE_PICK` | 2 | `UNIT_RATE_PICK\|3\|75` | unit_rate_generator.py |
| `UNIT_RATE_SETUP` | 3 | `UNIT_RATE_SETUP\|10\|apples\|$20.00` | unit_rate_generator.py |
| `UNIT_RATE_TABLE` | 2 | `UNIT_RATE_TABLE\|3,4,7,8\|75,100,175,200` | unit_rate_generator.py |
| `UNIT_RULE` | 3 | `UNIT_RULE\|hbar=1\|E=1/L\|keV` | natural_units_generator.py |
| `UNIT_TANGENT` | 2 | `UNIT_TANGENT\|r'(0)/speed\|<0, 1>` | curve_geometry_generator.py |
| `UNLIKE_RADICALS` | 2 | `UNLIKE_RADICALS\|√3 ≠ √13\|unlike radicands — cannot combine` | radical_add_sub_generator.py |
| `UNPAIR` | 2 | `UNPAIR\|13157\|(45, 116)` | cantor_pairing_generator.py |
| `UNPAIRED` | 2 | `UNPAIRED\|neither\|∅` | one_to_one_correspondence_generator.py |
| `UNROLL` | 2 | `UNROLL\|-9, 54, -324, 1944\|geometric, r = -6` | recursive_explicit_generator.py |
| `UPDATE` | 2 | `UPDATE\|W1_11\|2/3` | backprop_generator.py, kernel_perceptron_generator.py |
| `U_VECTOR` | 2 | `U_VECTOR\|u1 = A*v1/σ1\|[1/√2, 1/√2]` | svd_generator.py |
| `VA` | 1 | `VA\|x = -5` | rational_function_features_generator.py |
| `VALIDITY` | 2 | `VALIDITY\|invalid\|denying the antecedent` | argument_form_generator.py |
| `VALUE_FORMULA` | 1 | `VALUE_FORMULA\|v=(ad-bc)/(a-b-c+d)` | game_theory_generator.py |
| `VARIANCE` | 1, 2 | `VARIANCE\|Delta x^2\|1/12 - 1/(2312pi^2)` | layer_norm_generator.py, uncertainty_generator.py |
| `VAR_FORMULA` | 1 | `VAR_FORMULA\|Var(X) = Σ P(x)·(x - μ)^2` | expected_value_generator.py |
| `VAR_ROW` | 3 | `VAR_ROW\|5 - 3.6 = 1.4\|(1.4)^2 = 1.96\|2/5·1.96 = 0.784` | expected_value_generator.py |
| `VECTOR_NORM` | 2 | `VECTOR_NORM\|A\|5` | embedding_similarity_generator.py |
| `VECTOR_SETUP` | 2 | `VECTOR_SETUP\|F(x,y,z) = <6*x + 4*y, 3*x - 5*y - 6*z, x + 2*y + 4*z>\|divergence and curl` | div_curl_generator.py |
| `VEC_ENTRY` | 3 | `VEC_ENTRY\|(1)\|1584*4 + (-400)*11\|1936` | diagonalization_generator.py |
| `VEC_SETUP` | 2 | `VEC_SETUP\|v = ⟨3, 7⟩\|magnitude` | dot_product_generator.py, vector_ops_generator.py |
| `VENN_MARK` | 2 | `VENN_MARK\|dancers ∩ writers\|x2` | syllogism_generator.py |
| `VENN_SHADE` | 2 | `VENN_SHADE\|orators − dancers\|empty` | syllogism_generator.py |
| `VERIFY` | 2 | `VERIFY\|1\|ok` | error_spotting_generator.py, foundations_critic_generator.py |
| `VERTEX` | 1 | `VERTEX\|(0, 0)` | ellipse_features_generator.py, hyperbola_features_generator.py, lp_corner_generator.py, parabola_features_generator.py |
| `VERTEX_SOLVE` | 2 | `VERTEX_SOLVE\|x=0\|y=0` | lp_corner_generator.py |
| `VISIT` | 2 | `VISIT\|D\|D` | graph_traversal_generator.py |
| `VITERBI_BACKTRACE` | 2 | `VITERBI_BACKTRACE\|H->H->L\|81/2048` | viterbi_generator.py |
| `VITERBI_CAND` | 3 | `VITERBI_CAND\|t=2,state=H\|from H\|27/128` | convolutional_code_viterbi_generator.py, viterbi_generator.py |
| `VITERBI_INIT` | 3 | `VITERBI_INIT\|H\|obs=A\|3/8` | viterbi_generator.py |
| `VITERBI_PICK` | 2, 3 | `VITERBI_PICK\|t=2,state=H\|from H\|27/128` | convolutional_code_viterbi_generator.py, viterbi_generator.py |
| `VOLUME` | 1 | `VOLUME\|200` | volume_rect_prism_generator.py |
| `VOLUME_SETUP` | 2 | `VOLUME_SETUP\|region between y = 82x (outer) and y = 82x^2 (inner) on [0, 1], about the x-axis\|washer method` | solid_revolution_generator.py |
| `VOL_BASE_AREA` | 2 | `VOL_BASE_AREA\|Base Area = (1/2) × 9 × 9\|40.5` | round_solids_generator.py, volume_3d_generator.py |
| `VOL_CALCULATE` | 2 | `VOL_CALCULATE\|V = 12 × 11 × 7\|924` | round_solids_generator.py, volume_3d_generator.py |
| `VOL_FORMULA` | 1 | `VOL_FORMULA\|V = l × w × h` | round_solids_generator.py, solid_revolution_generator.py, volume_3d_generator.py |
| `VOL_SETUP` | 2 | `VOL_SETUP\|rectangular_prism\|l=12, w=11, h=7` | volume_3d_generator.py |
| `VOP_FORM` | 2 | `VOP_FORM\|u1' = -y2*g/W\|140/7 * e^(2x)` | variation_parameters_generator.py |
| `WALK_ENTRY` | 2 | `WALK_ENTRY\|A^2[3,1]\|1` | graph_counting_generator.py |
| `WALK_GOAL` | 2 | `WALK_GOAL\|length 2\|3 to 1` | graph_counting_generator.py |
| `WALK_TERM` | 3 | `WALK_TERM\|via 1\|A[3,1]*A[1,1]\|0` | graph_counting_generator.py |
| `WARSHALL_K` | 2 | `WARSHALL_K\|k=3\|0 0 1 0 0; 0 1 0 0 1; 1 0 1 0 1; 0 1 0 0 0; 1 1 1 0 0` | relation_closure_generator.py |
| `WAVE_FORMULA` | 1 | `WAVE_FORMULA\|1=N^2*integral_0^L (x/L)^(2k) dx` | wavefunction_generator.py |
| `WAVE_SETUP` | 3 | `WAVE_SETUP\|power_interval\|psi=N*(x/L)^5\|0<=x<=29` | wavefunction_generator.py |
| `WEEKDAY_SCAN` | 2, 3 | `WEEKDAY_SCAN\|index 6\|Sunday` | calendar_arithmetic_generator.py |
| `WEIGHT` | 2 | `WEIGHT\|blue\|57/98` | complement_probability_generator.py |
| `WEIGHT_VECTOR` | 2 | `WEIGHT_VECTOR\|w\|(-3,-4)` | svm_margin_generator.py |
| `WIDTH_SETUP` | 3 | `WIDTH_SETUP\|lifetime\|hbar=7\|Gamma=30` | branching_ratio_generator.py |
| `WITNESS` | 2, 3 | `WITNESS\|n=2\|Prime(2)=T\|Odd(2)=F` | induction_verify_generator.py, peano_arithmetic_generator.py, quantifier_finite_domain_generator.py, quantifier_negation_generator.py |
| `WORK_DIFF` | 3 | `WORK_DIFF\|phi(end) - phi(start)\|31 - 31\|0` | line_integral_generator.py |
| `WRONSKIAN` | 2 | `WRONSKIAN\|y1*y2' - y1'*y2\|7e^x` | variation_parameters_generator.py |
| `XOR` | 3 | `XOR\|control=1\|target=1\|0` | quantum_gate_generator.py |
| `YOUNG_SETUP` | 3 | `YOUNG_SETUP\|partition=[4,3,3,1]\|n=11\|group=S_11` | young_tableaux_generator.py |
| `Z` | 1 | `Z\|63 R84` | abacus_addition_generator.py, absolute_value_equation_generator.py, absolute_value_inequality_generator.py, ac_circuit_generator.py, activation_generator.py, adam_step_generator.py, algorithm_trace_generator.py, angle_defect_generator.py, angle_measure_generator.py, angle_relationships_generator.py, annuity_generator.py, antiderivative_generator.py, arc_length_generator.py, arc_sector_generator.py, area_between_curves_generator.py, argument_form_generator.py, arithmetic_coding_generator.py, arithmetic_sequence_generator.py, attention_generator.py, attribute_sorting_generator.py, baby_step_giant_step_generator.py, backprop_generator.py, base_arithmetic_generator.py, base_conversion_generator.py, bayesian_update_generator.py, bch_generator.py, bec_channel_generator.py, binomial_probability_generator.py, bisection_generator.py, bitwise_ops_generator.py, black_scholes_generator.py, blackbody_generator.py, bond_pricing_generator.py, boolean_algebra_generator.py, braket_generator.py, branching_ratio_generator.py, calendar_arithmetic_generator.py, calorimetry_generator.py, cantor_diagonal_generator.py, cantor_pairing_generator.py, cardinal_arithmetic_generator.py, casimir_force_generator.py, casimir_generator.py, cauchy_riemann_generator.py, cayley_table_generator.py, centroid_generator.py, chain_rule_generator.py, channel_capacity_generator.py, characteristic_vector_generator.py, chi_square_generator.py, cholesky_generator.py, christoffel_generator.py, circle_angle_generator.py, circle_equation_generator.py, circle_generator.py, classifier_metrics_generator.py, clebsch_gordan_generator.py, collision_generator.py, combinatory_logic_generator.py, commutator_generator.py, complement_probability_generator.py, completing_square_generator.py, complex_division_generator.py, complex_locus_generator.py, complex_log_generator.py, complex_number_ops_generator.py, complex_quadratic_generator.py, composite_arithmetic_generator.py, compound_inequality_generator.py, compound_probability_generator.py, conditional_forms_generator.py, conditional_probability_generator.py, confidence_interval_generator.py, conic_standard_form_generator.py, conservation_law_generator.py, continued_fraction_generator.py, continuous_distribution_generator.py, contour_integral_generator.py, convolution_generator.py, convolutional_code_viterbi_generator.py, coset_generator.py, countability_bijection_generator.py, counterexample_search_generator.py, counting_classics_generator.py, cramers_rule_generator.py, crc_generator.py, cross_section_generator.py, crt_generator.py, curve_analysis_generator.py, curve_geometry_generator.py, cyclic_group_generator.py, cyk_parser_generator.py, de_moivre_generator.py, decimal_add_sub_generator.py, decimal_div_generator.py, decimal_mult_generator.py, dedekind_cut_generator.py, definite_integral_generator.py, density_matrix_generator.py, derangement_generator.py, derivative_limit_def_generator.py, derivative_power_rule_generator.py, derivative_product_quotient_generator.py, derivative_transcendental_generator.py, determinant_generator.py, dfa_minimization_generator.py, dfa_simulation_generator.py, dft_generator.py, diagonalization_generator.py, diffie_hellman_generator.py, dijkstra_generator.py, dimensional_analysis_generator.py, direct_proof_algebra_generator.py, discriminant_generator.py, distance_formula_generator.py, div_curl_generator.py, divisibility_classification_generator.py, domain_range_generator.py, doppler_generator.py, dot_product_generator.py, double_integral_generator.py, dp_table_generator.py, dpll_trace_generator.py, ecdh_generator.py, ecdsa_generator.py, eigenvalue_generator.py, einstein_summation_generator.py, electrostatics_generator.py, ellipse_features_generator.py, elliptic_curve_finite_field_generator.py, embedding_similarity_generator.py, energy_conservation_generator.py, english_to_logic_generator.py, entropy_change_generator.py, entropy_generator.py, entropy_rate_markov_generator.py, equation_from_two_points_generator.py, equilibrium_ice_generator.py, equivalence_relation_generator.py, error_spotting_generator.py, euler_characteristic_generator.py, euler_circuit_generator.py, euler_formula_generator.py, euler_method_generator.py, evaluate_expression_generator.py, exact_ode_generator.py, expected_value_generator.py, experimental_probability_generator.py, exponent_generator.py, exponent_mixed_rules_generator.py, exponential_equation_generator.py, exponential_model_generator.py, extended_euclid_generator.py, factor_gcf_generator.py, factor_grouping_generator.py, factor_special_forms_generator.py, factor_trinomial_generator.py, factors_generator.py, feature_map_generator.py, fermi_estimation_generator.py, fill_in_step_generator.py, finance_generator.py, finite_difference_generator.py, finite_field_generator.py, first_law_generator.py, five_number_summary_generator.py, fixed_point_generator.py, flops_memory_generator.py, foundations_critic_generator.py, four_vector_generator.py, fourier_series_generator.py, fractal_iteration_generator.py, fraction_comparison_generator.py, fraction_decimal_percent_converter.py, fraction_op_generator.py, frequency_table_generator.py, function_composition_generator.py, function_evaluation_generator.py, function_inner_product_generator.py, function_operations_generator.py, function_properties_generator.py, function_table_generator.py, fundamental_counting_principle_generator.py, fundamental_form_generator.py, game_theory_generator.py, gamma_matrix_generator.py, gas_law_generator.py, gas_stoichiometry_generator.py, gauss_bonnet_generator.py, gauss_law_generator.py, gaussian_curvature_generator.py, gcf_generator.py, generating_function_generator.py, geometric_distribution_generator.py, geometric_mean_generator.py, geometric_probability_generator.py, geometric_sequence_generator.py, geometry_area_perimeter_generator.py, godel_numbering_generator.py, gradient_descent_generator.py, gradient_generator.py, gradient_step_generator.py, gram_schmidt_generator.py, graph_counting_generator.py, graph_interpret_generator.py, graph_traversal_generator.py, grassmann_generator.py, great_circle_generator.py, hamiltonian_generator.py, hamming_code_generator.py, hawking_generator.py, heat_engine_generator.py, hereditarily_finite_set_generator.py, hermitian_check_generator.py, hessian_classify_generator.py, hilbert_axiom_derivation_generator.py, horner_evaluation_generator.py, huffman_coding_generator.py, hydrogen_atom_generator.py, hyperbola_features_generator.py, hyperbolic_distance_generator.py, hyperbolic_function_generator.py, hypercube_counting_generator.py, hypothesis_test_generator.py, implicit_diff_generator.py, improper_integral_generator.py, inclusion_exclusion_generator.py, index_gymnastics_generator.py, index_raising_generator.py, induction_verify_generator.py, information_gain_generator.py, integer_operations_generator.py, integers_as_pairs_generator.py, integrating_factor_generator.py, integration_by_parts_generator.py, interference_generator.py, interpolation_generator.py, invariant_mass_generator.py, inverse_function_generator.py, jacobi_symbol_generator.py, jacobian_generator.py, joint_distribution_generator.py, kernel_evaluation_generator.py, kernel_perceptron_generator.py, kernel_ridge_generator.py, kernel_validity_generator.py, kinematics_generator.py, kl_divergence_generator.py, kmeans_step_generator.py, knights_knaves_generator.py, knn_generator.py, kraft_inequality_generator.py, ladder_operator_generator.py, lagrange_multiplier_generator.py, lagrangian_generator.py, lambda_reduction_generator.py, laplace_ivp_generator.py, laurent_series_generator.py, layer_norm_generator.py, lcm_generator.py, least_squares_generator.py, legendre_construction_generator.py, lhopital_generator.py, lie_exponential_generator.py, likelihood_language_generator.py, limit_evaluation_generator.py, line_integral_generator.py, linear_approx_generator.py, linear_complex_generator.py, linear_fractional_generator.py, linear_simple_generator.py, literal_equation_generator.py, lll_reduction_generator.py, log_conversion_generator.py, log_diff_higher_order_generator.py, log_equation_generator.py, log_properties_generator.py, logic_grid_puzzle_generator.py, logical_connective_eval_generator.py, logical_equivalence_laws_generator.py, logistic_growth_generator.py, long_division_generator.py, low_rank_approx_generator.py, lp_corner_generator.py, lr_schedule_generator.py, lu_decomposition_generator.py, lz_compression_generator.py, magnetism_generator.py, manual_square_root_generator.py, markov_chain_generator.py, master_theorem_generator.py, matrix_calculus_generator.py, matrix_exponential_generator.py, matrix_group_check_generator.py, matrix_inverse_generator.py, matrix_norm_generator.py, matrix_ops_generator.py, mean_value_theorem_generator.py, method_of_moments_generator.py, metric_arc_length_generator.py, mgf_generator.py, midpoint_generator.py, minkowski_interval_generator.py, mixed_number_operation_generator.py, mle_generator.py, mobius_transform_generator.py, mod_exp_generator.py, modular_arithmetic_generator.py, modular_inverse_generator.py, monomial_mult_div_generator.py, mst_generator.py, multi_digit_addition_generator.py, multi_digit_multiplication_generator.py, multi_digit_subtraction_generator.py, multi_step_unit_conversion_generator.py, multiplying_binomials_generator.py, multiplying_polynomials_generator.py, multivar_chain_rule_generator.py, mutual_information_generator.py, naive_bayes_generator.py, named_distribution_generator.py, natural_deduction_generator.py, natural_units_generator.py, nets_surface_area_generator.py, newton_raphson_generator.py, newtons_laws_generator.py, nfa_simulation_generator.py, normal_table_generator.py, npv_irr_generator.py, number_comparison_generator.py, ode_substitution_generator.py, ode_system_generator.py, one_step_equation_generator.py, one_step_inequality_generator.py, one_to_one_correspondence_generator.py, operation_properties_generator.py, optics_generator.py, optimization_generator.py, or_formula_generator.py, orbital_mechanics_generator.py, order_of_operations_generator.py, order_statistics_generator.py, ordinal_arithmetic_generator.py, parabola_features_generator.py, parallel_perpendicular_line_generator.py, param_count_generator.py, parametric_calculus_generator.py, partial_derivative_generator.py, partial_fractions_generator.py, partial_order_generator.py, partial_trace_generator.py, particle_in_box_generator.py, partition_function_generator.py, pascal_triangle_generator.py, pauli_algebra_generator.py, pca_generator.py, pda_simulation_generator.py, peano_arithmetic_generator.py, percent_problem_generator.py, percent_word_problem_generator.py, perceptron_generator.py, permutation_combination_generator.py, permutation_group_generator.py, perplexity_generator.py, ph_calculation_generator.py, physics_formula_generator.py, piecewise_evaluation_generator.py, place_value_rounding_generator.py, planck_units_generator.py, point_slope_generator.py, polar_parametric_generator.py, pollard_factorization_generator.py, polygon_perimeter_generator.py, polynomial_add_sub_generator.py, polynomial_div_monomial_generator.py, polynomial_inequality_generator.py, polynomial_long_division_generator.py, polynomial_zeros_generator.py, portfolio_generator.py, positional_encoding_generator.py, positive_definite_generator.py, power_series_generator.py, prenex_normal_form_generator.py, primality_test_generator.py, prime_factorization_generator.py, probability_addition_rule_generator.py, projectile_motion_generator.py, projector_generator.py, proportion_word_problem_generator.py, proportional_relationship_generator.py, pythag_hyp_generator.py, pythag_leg_generator.py, qr_decomposition_generator.py, quadratic_factoring_generator.py, quadratic_generator.py, quadratic_residue_generator.py, quadratic_square_root_generator.py, quantifier_finite_domain_generator.py, quantifier_negation_generator.py, quantization_generator.py, quantum_formula_generator.py, quantum_gate_generator.py, quark_composition_generator.py, quaternion_generator.py, radical_add_sub_generator.py, radical_equation_generator.py, radical_multiply_generator.py, radical_rationalize_generator.py, radical_variable_simplify_generator.py, rate_conversion_generator.py, ratio_table_generator.py, rational_equation_generator.py, rational_exponent_generator.py, rational_expr_add_sub_generator.py, rational_expr_mult_div_generator.py, rational_expr_simplify_generator.py, rational_function_features_generator.py, rational_root_generator.py, rationals_as_pairs_generator.py, recurrence_generator.py, recursive_definition_unfold_generator.py, recursive_explicit_generator.py, reed_solomon_generator.py, regex_to_automaton_generator.py, regression_generator.py, regular_polygon_area_generator.py, related_rates_generator.py, relation_check_generator.py, relation_closure_generator.py, relation_operations_generator.py, relativistic_energy_generator.py, remainder_factor_theorem_generator.py, repeating_decimal_generator.py, residue_generator.py, resolution_proof_generator.py, riemann_sum_generator.py, riemann_tensor_generator.py, right_triangle_trig_generator.py, rotational_dynamics_generator.py, round_solids_generator.py, routh_hurwitz_generator.py, row_reduction_generator.py, rsa_generator.py, runge_kutta_generator.py, running_coupling_generator.py, rv_transform_generator.py, sample_space_list_generator.py, scaling_generator.py, scaling_law_generator.py, schwarzschild_generator.py, second_order_ode_generator.py, segment_partition_generator.py, semantic_tableau_generator.py, separable_ode_generator.py, separable_pde_generator.py, series_convergence_generator.py, series_solution_generator.py, set_algebra_laws_generator.py, set_builder_roster_generator.py, set_counting_generator.py, set_expression_generator.py, set_identity_membership_table_generator.py, set_membership_subset_generator.py, set_operations_generator.py, shm_generator.py, sigma_notation_generator.py, signal_arithmetic_generator.py, similar_triangles_generator.py, simple_probability_generator.py, simple_stats_generator.py, simplex_generator.py, simplify_expression_generator.py, sinusoid_features_generator.py, slope_intercept_form_generator.py, slope_two_points_generator.py, softmax_gradient_generator.py, solid_revolution_generator.py, solution_chem_generator.py, special_relativity_generator.py, special_right_triangle_generator.py, special_solution_equation_generator.py, spherical_excess_generator.py, spherical_triangle_generator.py, spin_half_generator.py, stability_generator.py, standard_deviation_generator.py, standard_form_conversion_generator.py, standing_wave_generator.py, stars_and_bars_generator.py, statics_generator.py, statistics_generator.py, stereographic_generator.py, stoichiometry_generator.py, structure_constant_generator.py, structure_isomorphism_generator.py, subspace_basis_generator.py, svd_generator.py, svm_margin_generator.py, syllogism_generator.py, synthetic_division_generator.py, systems_elimination_generator.py, systems_substitution_generator.py, tangent_line_generator.py, taxicab_geometry_generator.py, taylor_series_generator.py, telescoping_generator.py, temperature_conversion_generator.py, tensor_product_generator.py, tip_bill_split_generator.py, tonelli_shanks_generator.py, totient_generator.py, transfer_function_generator.py, transformation_generator.py, transient_circuit_generator.py, transportation_generator.py, triangle_area_sas_generator.py, triangle_solve_generator.py, trig_equation_generator.py, trig_identity_eval_generator.py, trig_identity_verify_generator.py, trig_six_functions_generator.py, triple_integral_generator.py, truth_table_generator.py, turing_machine_trace_generator.py, two_sample_test_generator.py, two_step_equation_generator.py, two_step_inequality_generator.py, type_theory_generator.py, u_substitution_generator.py, uncertainty_generator.py, undetermined_coeff_generator.py, unification_generator.py, unit_circle_generator.py, unit_conversion_generator.py, unit_rate_generator.py, variation_parameters_generator.py, vector_ops_generator.py, vector_theorem_generator.py, venn_region_count_generator.py, viterbi_generator.py, volume_3d_generator.py, volume_rect_prism_generator.py, von_neumann_entropy_generator.py, wavefunction_generator.py, wff_parsing_generator.py, young_tableaux_generator.py, z_score_generator.py, z_transform_generator.py, zf_axiom_identify_generator.py |
| `ZERO` | 1 | `ZERO\|s=-9` | transfer_function_generator.py |
| `ZERO_PRODUCT` | 2 | `ZERO_PRODUCT\|(x - 4) = 0\|x = 4` | area_between_curves_generator.py, curve_analysis_generator.py, domain_range_generator.py, log_equation_generator.py, optimization_generator.py, polynomial_inequality_generator.py, polynomial_zeros_generator.py, quadratic_factoring_generator.py, radical_equation_generator.py, trig_equation_generator.py |
| `ZSCORE` | 2 | `ZSCORE\|(56 - 53)/4\|0.75` | normal_table_generator.py, z_score_generator.py |
| `ZSCORE_FORMULA` | 1 | `ZSCORE_FORMULA\|z = (x - μ)/σ` | z_score_generator.py |
| `ZT_PAIR` | 1 | `ZT_PAIR\|Z{r^n u[n]}=1/(1-r z^-1)` | z_transform_generator.py |
| `ZT_SETUP` | 2, 3 | `ZT_SETUP\|difference\|y[n]-3y[n-1]=delta[n]\|y[-1]=0` | z_transform_generator.py |
