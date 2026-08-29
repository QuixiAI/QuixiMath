# Op-Code Legend

**Generated file — do not hand-edit.** Regenerate with `python tools/gen_opcode_legend.py` (verify freshness with `--check`).

The scratchpad vocabulary belongs to the model and evolves organically: generators may introduce new op-codes freely, and this legend is *descriptive*, not prescriptive. Steps are pipe-delimited strings (`CODE|field|field|...`, at most 4 payload fields) built with `helpers.step()`; the final step of every problem is `Z|<final_answer>`.

2057 distinct op-codes observed.

| Code | Payload fields | Example | Used by |
|---|---|---|---|
| `A` | 2, 3 | `A\|43\|45\|88` | ac_circuit_generator.py, activation_generator.py, adam_step_generator.py, algorithm_trace_generator.py, alternative_means_generator.py, angle_defect_generator.py, angle_measure_generator.py, annuity_generator.py, arithmetic_coding_generator.py, arithmetic_sequence_generator.py, assumption_check_generator.py, attention_generator.py, backprop_generator.py, ballot_reflection_generator.py, base_conversion_generator.py, bayes_multiple_hypotheses_generator.py, bayesian_update_generator.py, binomial_probability_generator.py, bisection_generator.py, bond_pricing_generator.py, branching_ratio_generator.py, calendar_arithmetic_generator.py, calorimetry_generator.py, cantor_pairing_generator.py, cardinal_arithmetic_generator.py, casimir_generator.py, cayley_table_generator.py, channel_capacity_generator.py, chi_square_generator.py, circle_equation_generator.py, classifier_metrics_generator.py, collision_generator.py, commutator_generator.py, complement_probability_generator.py, complex_division_generator.py, complex_locus_generator.py, complex_number_ops_generator.py, composite_arithmetic_generator.py, conditional_expectation_generator.py, conditional_probability_generator.py, confidence_interval_generator.py, conic_standard_form_generator.py, continued_fraction_generator.py, contour_integral_generator.py, convolution_generator.py, coset_generator.py, countability_bijection_generator.py, counterexample_search_generator.py, counting_classics_generator.py, covariance_algebra_generator.py, crt_generator.py, curve_analysis_generator.py, cyclic_group_generator.py, de_moivre_generator.py, dedekind_cut_generator.py, definite_integral_generator.py, density_matrix_generator.py, derangement_generator.py, derivative_limit_def_generator.py, determinant_generator.py, dft_generator.py, dijkstra_generator.py, discrete_posterior_generator.py, discrete_uniform_bernoulli_generator.py, distance_formula_generator.py, distribution_of_sum_generator.py, doppler_generator.py, dot_plot_generator.py, dot_product_generator.py, dp_table_generator.py, einstein_summation_generator.py, electrostatics_generator.py, ellipse_features_generator.py, embedding_similarity_generator.py, empirical_rule_generator.py, energy_conservation_generator.py, entropy_change_generator.py, entropy_generator.py, entropy_rate_markov_generator.py, equivalence_relation_generator.py, euler_characteristic_generator.py, euler_formula_generator.py, euler_method_generator.py, evaluate_expression_generator.py, expectation_of_function_generator.py, expected_value_classics_generator.py, expected_value_generator.py, exponential_model_generator.py, extended_euclid_generator.py, feature_map_generator.py, fill_in_step_generator.py, finance_generator.py, finite_field_generator.py, finite_sigma_algebra_generator.py, fisher_information_generator.py, five_number_summary_generator.py, fixed_point_generator.py, flops_memory_generator.py, formula_derivation_generator.py, four_vector_generator.py, fractal_iteration_generator.py, fraction_op_generator.py, frequency_table_generator.py, function_composition_generator.py, function_evaluation_generator.py, function_inner_product_generator.py, function_operations_generator.py, function_table_generator.py, game_theory_generator.py, gaussian_curvature_generator.py, generating_function_generator.py, geometric_mean_generator.py, geometry_area_perimeter_generator.py, geometry_in_context_generator.py, gradient_descent_generator.py, gradient_step_generator.py, graph_counting_generator.py, graph_interpret_generator.py, grassmann_generator.py, great_circle_generator.py, grouped_data_generator.py, growth_comparison_generator.py, hamiltonian_generator.py, heat_engine_generator.py, hermitian_check_generator.py, horner_evaluation_generator.py, huffman_coding_generator.py, hyperbola_features_generator.py, hyperbolic_distance_generator.py, hyperbolic_function_generator.py, hypercube_counting_generator.py, hypergeometric_generator.py, inclusion_exclusion_generator.py, index_gymnastics_generator.py, information_gain_generator.py, integer_puzzle_word_generator.py, integers_as_pairs_generator.py, integrating_factor_generator.py, interpolation_generator.py, invariant_mass_generator.py, inverse_normal_generator.py, joint_distribution_generator.py, kernel_evaluation_generator.py, kernel_perceptron_generator.py, kernel_ridge_generator.py, kl_divergence_generator.py, kmeans_step_generator.py, knn_generator.py, kraft_inequality_generator.py, ladder_operator_generator.py, lagrangian_generator.py, laplace_ivp_generator.py, law_of_total_probability_generator.py, layer_norm_generator.py, legendre_construction_generator.py, lhopital_generator.py, likelihood_ratio_test_generator.py, limit_evaluation_generator.py, linear_approx_generator.py, linear_model_word_generator.py, linear_transform_effect_generator.py, linearity_of_expectation_generator.py, low_rank_approx_generator.py, lp_corner_generator.py, lr_schedule_generator.py, magnitude_comparison_generator.py, manual_square_root_generator.py, markov_chain_generator.py, martingale_check_generator.py, matrix_calculus_generator.py, matrix_group_check_generator.py, matrix_norm_generator.py, matrix_ops_generator.py, mean_adjustment_generator.py, mean_value_theorem_generator.py, measurement_uncertainty_generator.py, mental_strategy_generator.py, method_discrimination_generator.py, method_of_moments_generator.py, mgf_generator.py, midpoint_generator.py, minkowski_interval_generator.py, missing_information_generator.py, mixed_number_operation_generator.py, mixture_generator.py, mobius_transform_generator.py, modular_arithmetic_generator.py, money_life_generator.py, monte_carlo_arithmetic_generator.py, motion_word_generator.py, mse_decomposition_generator.py, mst_generator.py, multi_state_markov_generator.py, multi_step_word_generator.py, mutual_information_generator.py, naive_bayes_generator.py, named_distribution_generator.py, negative_binomial_generator.py, nets_surface_area_generator.py, newtons_laws_generator.py, nonparametric_test_generator.py, normal_table_generator.py, npv_irr_generator.py, odds_probability_generator.py, operation_properties_generator.py, optimization_in_context_generator.py, or_formula_generator.py, order_of_operations_generator.py, order_statistics_generator.py, ordinal_arithmetic_generator.py, parabola_features_generator.py, param_count_generator.py, partition_function_generator.py, pascal_triangle_generator.py, pca_generator.py, percent_chain_generator.py, percent_word_problem_generator.py, percentile_generator.py, perceptron_generator.py, permutation_group_generator.py, pgf_generator.py, piecewise_evaluation_generator.py, pmf_cdf_quantile_generator.py, poisson_process_generator.py, polar_parametric_generator.py, polya_urn_generator.py, polygon_perimeter_generator.py, polynomial_zeros_generator.py, portfolio_generator.py, probability_addition_rule_generator.py, probability_axioms_finite_generator.py, probability_critic_generator.py, probability_inequality_generator.py, probability_measure_generator.py, pythag_hyp_generator.py, quadratic_word_generator.py, qualitative_reasoning_generator.py, quantization_generator.py, quark_composition_generator.py, quaternion_generator.py, radical_add_sub_generator.py, radical_multiply_generator.py, rate_of_change_interpret_generator.py, rational_expr_add_sub_generator.py, rationals_as_pairs_generator.py, recurrence_generator.py, recursive_definition_unfold_generator.py, recursive_explicit_generator.py, reed_solomon_generator.py, regression_generator.py, relativistic_energy_generator.py, reliability_system_generator.py, remainder_factor_theorem_generator.py, representation_translation_generator.py, riemann_sum_generator.py, riemann_tensor_generator.py, rotational_dynamics_generator.py, round_solids_generator.py, rounding_effect_generator.py, runge_kutta_generator.py, running_coupling_generator.py, rv_transform_generator.py, scatter_plot_describe_generator.py, scenario_generator.py, segment_partition_generator.py, separable_pde_generator.py, set_counting_generator.py, shm_generator.py, sigma_notation_generator.py, simple_stats_generator.py, simplex_generator.py, slope_inference_generator.py, softmax_gradient_generator.py, solution_chem_generator.py, spatial_description_generator.py, spherical_excess_generator.py, spherical_triangle_generator.py, spin_half_generator.py, standard_deviation_generator.py, stars_and_bars_generator.py, statics_generator.py, stereographic_generator.py, study_design_generator.py, svm_margin_generator.py, synthetic_division_generator.py, systems_word_generator.py, t_interval_generator.py, tangent_line_generator.py, taxicab_geometry_generator.py, taylor_series_generator.py, temperature_conversion_generator.py, tip_bill_split_generator.py, transfer_function_generator.py, transformation_generator.py, transportation_generator.py, triangle_solve_generator.py, trig_identity_eval_generator.py, trig_six_functions_generator.py, two_sample_test_generator.py, two_way_table_probability_generator.py, type_error_power_generator.py, undetermined_coeff_generator.py, variation_parameters_generator.py, vector_ops_generator.py, venn_probability_generator.py, venn_region_count_generator.py, von_neumann_entropy_generator.py, wavefunction_generator.py, work_rate_generator.py, young_tableaux_generator.py, z_score_generator.py |
| `ABS` | 2 | `ABS\|-4/9\|4/9` | fixed_point_generator.py, matrix_norm_generator.py, rv_transform_generator.py, scatter_plot_describe_generator.py |
| `ABSORBING_CHECK` | 3 | `ABSORBING_CHECK\|state 1\|outgoing {2, 3, 4}\|no` | markov_state_classification_generator.py |
| `ABSORB_EQ` | 2 | `ABSORB_EQ\|u0=p0A+p00*u0+p01*u1\|u1=p1A+p10*u0+p11*u1` | markov_chain_generator.py |
| `ABS_CASE` | 2 | `ABS_CASE\|Case 1\|2x - 2 = 20` | absolute_value_equation_generator.py |
| `ABS_CHECK` | 2 | `ABS_CHECK\|-8 < 0\|Absolute value cannot be negative` | absolute_value_equation_generator.py |
| `ABS_ERROR` | 2 | `ABS_ERROR\|1\|1/100` | quantization_generator.py |
| `ABS_INEQ_CHECK` | 2 | `ABS_INEQ_CHECK\|-3 < 0\|Absolute value is always non-negative` | absolute_value_inequality_generator.py |
| `ABS_INEQ_PART` | 2 | `ABS_INEQ_PART\|Part 1\|4x ≥ 12 -> x ≥ 3` | absolute_value_inequality_generator.py |
| `ABS_INEQ_SETUP` | 1 | `ABS_INEQ_SETUP\|abs(5x - 4) ≤ 6` | absolute_value_inequality_generator.py |
| `ABS_INEQ_SPECIAL` | 2 | `ABS_INEQ_SPECIAL\|c = 0\|Check logic for <` | absolute_value_inequality_generator.py |
| `ABS_INEQ_SPLIT` | 2 | `ABS_INEQ_SPLIT\|AND case\|-6 ≤ 5x - 4 ≤ 6` | absolute_value_inequality_generator.py |
| `ABS_SETUP` | 1 | `ABS_SETUP\|abs(2x - 2) = 20` | absolute_value_equation_generator.py |
| `ABS_SPLIT` | 2, 3 | `ABS_SPLIT\|Two cases\|2x - 2 = 20\|2x - 2 = -20` | absolute_value_equation_generator.py |
| `ABS_VAL` | 2 | `ABS_VAL\|(-8)\|8` | taxicab_geometry_generator.py |
| `AB_ADD` | 3 | `AB_ADD\|+9000\|5543\|14543` | abacus_addition_generator.py |
| `AB_SET` | 1 | `AB_SET\|5543` | abacus_addition_generator.py |
| `ACCEPT` | 1, 2 | `ACCEPT\|x = 25` | conditional_forms_generator.py, counterexample_search_generator.py, factor_trinomial_generator.py, growth_comparison_generator.py, knights_knaves_generator.py, log_conversion_generator.py, log_equation_generator.py, optimization_generator.py, optimization_in_context_generator.py, polynomial_inequality_generator.py, quadratic_word_generator.py, radical_equation_generator.py, rational_equation_generator.py, rational_root_generator.py, set_builder_roster_generator.py, structure_isomorphism_generator.py |
| `ACT_DERIV` | 3 | `ACT_DERIV\|sigmoid\|0\|1/4` | activation_generator.py |
| `ACT_SETUP` | 3 | `ACT_SETUP\|activation=sigmoid\|x=4\|w1=1,b1=-4,w2=-1,b2=4` | activation_generator.py |
| `ACT_VALUE` | 3 | `ACT_VALUE\|sigmoid\|0\|1/2` | activation_generator.py |
| `AC_COMPLEX` | 3 | `AC_COMPLEX\|Z\|13\|5j` | ac_circuit_generator.py |
| `AC_FORMULA` | 1 | `AC_FORMULA\|Z=R+j(XL-XC)` | ac_circuit_generator.py |
| `AC_PRODUCT` | 2 | `AC_PRODUCT\|4 × 1\|4` | factor_trinomial_generator.py |
| `AC_SETUP` | 3 | `AC_SETUP\|series_rlc\|R=13, XL=40\|XC=35, V=6` | ac_circuit_generator.py |
| `ADAM_SETUP` | 3 | `ADAM_SETUP\|theta=13/4,g=5\|beta1=9/10,beta2=99/100\|lr=1/100,epsilon=0` | adam_step_generator.py |
| `ADAM_UPDATE` | 2 | `ADAM_UPDATE\|theta_new\|81/25` | adam_step_generator.py |
| `ADD_COL` | 3 | `ADD_COL\|col_1\|4+1+0\|->5 (carry 0)` | multi_digit_addition_generator.py |
| `ADD_FORMULA` | 1 | `ADD_FORMULA\|P(A ∪ B) = P(A) + P(B)` | probability_addition_rule_generator.py |
| `ADD_PARTIALS` | 2 | `ADD_PARTIALS\|429215 + 7725870 + 60090100 + 686744000\|754989185` | decimal_mult_generator.py, multi_digit_multiplication_generator.py |
| `ADD_SETUP` | 2 | `ADD_SETUP\|P(A) = 6/10, P(B) = 2/10, mutually exclusive\|P(A ∪ B)` | probability_addition_rule_generator.py |
| `ADJOINT` | 1 | `ADJOINT\|A^dagger=[[-17,7],[7,-17]]` | hermitian_check_generator.py |
| `ADJ_LIST` | 2 | `ADJ_LIST\|A\|B, C, D` | euler_circuit_generator.py, graph_traversal_generator.py |
| `ALG_SETUP` | 3 | `ALG_SETUP\|merge sort\|merges 6\|values 40, 32, 6, 20, 24, 21, 19` | algorithm_trace_generator.py |
| `ALIGN_NUM` | 2 | `ALIGN_NUM\|903.19\|102.54` | number_comparison_generator.py |
| `ALLOCATE` | 3 | `ALLOCATE\|freshmen\|96/168 × 21\|12` | study_design_generator.py |
| `ALPHA` | 2 | `ALPHA\|line 2\|4: g; 5: ¬f ∨ ¬f` | kernel_ridge_generator.py, semantic_tableau_generator.py |
| `ALPHA_RENAME` | 2 | `ALPHA_RENAME\|lambda s. m\|lambda z. m` | lambda_reduction_generator.py |
| `AMORT_ROW` | 3 | `AMORT_ROW\|1\|interest=$10300.00\|principal=$1750.00,balance=$18850.00` | annuity_generator.py |
| `AMOUNT` | 2 | `AMOUNT\|dye initially\|1.05` | mixture_generator.py |
| `AMPLITUDE` | 2 | `AMPLITUDE\|abs(-3)\|3` | sinusoid_features_generator.py |
| `ANALOGY_SETUP` | 3 | `ANALOGY_SETUP\|man=(2,3)\|woman=(2,1)\|king=(2,6)` | embedding_similarity_generator.py |
| `ANALOGY_VECTOR` | 2 | `ANALOGY_VECTOR\|king-man+woman\|(2,4)` | embedding_similarity_generator.py |
| `ANGLE` | 2 | `ANGLE\|theta\|pi` | positional_encoding_generator.py |
| `ANGLE_DEFECT_SETUP` | 2 | `ANGLE_DEFECT_SETUP\|R=16\|angles=75,30,30` | angle_defect_generator.py |
| `ANGLE_EVAL` | 2 | `ANGLE_EVAL\|theta=0..2*pi\|2*pi` | triple_integral_generator.py |
| `ANGLE_FORMULA` | 1 | `ANGLE_FORMULA\|degrees = radians · 180/π` | angle_measure_generator.py |
| `ANGLE_RELATION` | 1 | `ANGLE_RELATION\|5x + 29 = 6x + 19` | angle_relationships_generator.py |
| `ANGLE_SETUP` | 2 | `ANGLE_SETUP\|vertical\|Vertical angles are equal` | angle_relationships_generator.py |
| `ANGLE_SOLVE` | 2 | `ANGLE_SOLVE\|-1x = -10\|x = 10` | angle_relationships_generator.py |
| `ANGLE_WRAP` | 2 | `ANGLE_WRAP\|191 deg\|-169 deg` | complex_log_generator.py |
| `ANNUITY_FORMULA` | 1 | `ANNUITY_FORMULA\|FV = PMT*((1+r)^n - 1)/r` | annuity_generator.py |
| `ANNUITY_SETUP` | 2, 3 | `ANNUITY_SETUP\|ordinary annuity future value\|PMT=4470,r=8%,n=2` | annuity_generator.py |
| `ANOVA_ROW` | 3 | `ANOVA_ROW\|A\|mean 68\|SS 20` | anova_generator.py |
| `ANOVA_SETUP` | 2 | `ANOVA_SETUP\|k = 4, n = 4\|one-way ANOVA; equal group sizes` | anova_generator.py |
| `ANTICHAIN` | 2 | `ANTICHAIN\|{1, 9, 46}\|size 3` | partial_order_generator.py |
| `ANTICOMM_ENTRY` | 3 | `ANTICOMM_ENTRY\|(1,1)\|0 + 0\|0` | pauli_algebra_generator.py |
| `ANTIDERIV` | 2 | `ANTIDERIV\|16x^3\|4x^4` | antiderivative_generator.py, arc_length_generator.py, area_between_curves_generator.py, definite_integral_generator.py, improper_integral_generator.py, integrating_factor_generator.py, integration_by_parts_generator.py, ode_substitution_generator.py, parametric_calculus_generator.py, partial_fractions_generator.py, separable_ode_generator.py, solid_revolution_generator.py, u_substitution_generator.py, variation_parameters_generator.py |
| `ANTIDERIVATIVE` | 1 | `ANTIDERIVATIVE\|-A*cos(nx)/n` | fourier_series_generator.py |
| `ANTISYM_CHECK` | 3 | `ANTISYM_CHECK\|(1, 3)\|reverse (3, 1)\|ok` | relation_check_generator.py |
| `APPLY` | 3 | `APPLY\|∧I\|1,2\|b ∧ s` | natural_deduction_generator.py |
| `APPLY_GATE` | 3 | `APPLY_GATE\|CNOT\|e^(i369π/187)·ket10\|e^(i369π/187)·ket11` | quantum_gate_generator.py |
| `APPLY_OPERATOR` | 2 | `APPLY_OPERATOR\|L[A]\|-6A = -12` | commutator_generator.py, undetermined_coeff_generator.py |
| `APPLY_PAULI` | 2 | `APPLY_PAULI\|sigma_y ket0\|i ket1` | spin_half_generator.py |
| `APPLY_SUBST` | 1 | *(not observed in sampling)* | unification_generator.py |
| `APPROX` | 2 | `APPROX\|lora/full\|145/672` | param_count_generator.py |
| `APPROX_ENTRY` | 2 | `APPROX_ENTRY\|(1,1)\|19` | low_rank_approx_generator.py |
| `APPROX_SETUP` | 2 | `APPROX_SETUP\|estimate √52\|linearize f(x) = √x at a = 49` | linear_approx_generator.py |
| `ARCCOS` | 2 | `ARCCOS\|cos(c)=1/2\|c=pi/3` | great_circle_generator.py |
| `ARCLEN_FORMULA` | 1 | `ARCLEN_FORMULA\|L = ∫ √((dx/dt)^2 + (dy/dt)^2) dt` | arc_length_generator.py, parametric_calculus_generator.py |
| `ARC_FORMULA` | 1 | `ARC_FORMULA\|L = (θ/360)·2πr` | arc_sector_generator.py |
| `ARC_LENGTH` | 3 | `ARC_LENGTH\|int_0^T speed dt\|25*5\|125` | curve_geometry_generator.py |
| `ARC_SETUP` | 2 | `ARC_SETUP\|circle r = 36, central angle 85°\|sector area` | arc_sector_generator.py |
| `AREA` | 2 | `AREA\|10 × 8\|80` | geometry_area_perimeter_generator.py, geometry_in_context_generator.py, optimization_in_context_generator.py, spatial_packing_generator.py |
| `AREA_INT` | 3 | `AREA_INT\|A = int y dx\|3*13^2/2\|507/2` | centroid_generator.py |
| `AREA_INTEGRAL` | 2 | `AREA_INTEGRAL\|sqrt(EG-F^2)=R^2 sin(phi)\|area = R^2*theta*(cos phi1 - cos phi2)` | fundamental_form_generator.py |
| `AREA_SCALE` | 3 | `AREA_SCALE\|uv rectangle area\|4*7\|28` | jacobian_generator.py |
| `AREA_SETUP` | 2 | `AREA_SETUP\|y = x^2 + 6x + 1 and y = 3x - 1\|area between the curves` | area_between_curves_generator.py |
| `ARGUMENT` | 2 | `ARGUMENT\|(-11,0)\|180 deg` | complex_log_generator.py, euler_formula_generator.py |
| `ARG_SETUP` | 2 | `ARG_SETUP\|(¬(q ∨ s) → ((p ∨ r) ∧ (s ∨ p))) ∧ (¬(r ∧ p) → ((s ∨ p) ∧ (r ∨ r))); ¬(q ∨ s) ∨ ¬(r ∧ p)\|((p ∨ r) ∧ (s ∨ p)) ∨ ((s ∨ p) ∧ (r ∨ r))` | argument_form_generator.py |
| `ARITH_INTERVAL` | 1 | `ARITH_INTERVAL\|[0,1/4)` | arithmetic_coding_generator.py |
| `ARITH_SETUP` | 2 | `ARITH_SETUP\|A=1/4, B=1/4, C=1/4, D=1/4\|message=AABCA` | arithmetic_coding_generator.py |
| `ARITH_SYMBOL` | 2 | `ARITH_SYMBOL\|A\|cum=[0,1/4)` | arithmetic_coding_generator.py |
| `ARRAY_STATE` | 2 | `ARRAY_STATE\|pass 1\|13, 24, 20, 11, 8, 10` | algorithm_trace_generator.py |
| `ASSIGN` | 2 | `ASSIGN\|P1\|C1` | kmeans_step_generator.py |
| `ASSUME` | 1 | `ASSUME\|assume u is the greatest integer` | direct_proof_algebra_generator.py, induction_verify_generator.py |
| `ASSUMPTION` | 3 | `ASSUMPTION\|unchanged second chance\|holds\|first token is returned` | assumption_check_generator.py |
| `ASYMPTOTE` | 1 | `ASYMPTOTE\|y = 3 ± (3/5)(x + 2)` | hyperbola_features_generator.py |
| `ATA` | 2 | `ATA\|A^T A\|[[2789, 1700], [1700, 2789]]` | svd_generator.py |
| `ATOM` | 1 | `ATOM\|{1}` | finite_sigma_algebra_generator.py |
| `ATOM_CHECK` | 3 | `ATOM_CHECK\|Al\|left=4\|right=4` | stoichiometry_generator.py |
| `ATOM_SPLIT` | 2 | `ATOM_SPLIT\|{7, 8}\|A intersection atom={7}` | finite_sigma_algebra_generator.py |
| `ATTN_OUTPUT` | 2 | `ATTN_OUTPUT\|1\|[[-7/3,-13/3]]` | attention_generator.py |
| `ATTN_SCORE` | 2 | `ATTN_SCORE\|1,1\|0` | attention_generator.py |
| `ATTN_SETUP` | 1, 3 | `ATTN_SETUP\|tokens=3,d=2\|Q=[[0,0], [0,0], [0,0]]\|K=[[0,0], [0,0], [0,0]]` | attention_generator.py |
| `ATTR_CHECK` | 3 | `ATTR_CHECK\|4\|A: multiple of 3\|no` | attribute_sorting_generator.py |
| `AVG` | 2 | `AVG\|(90% + 86.25%)/2\|88.125%` | statistical_literacy_generator.py |
| `AVG_RATE` | 2 | `AVG_RATE\|(106 − 34)/(15 − 7)\|9` | rate_of_change_interpret_generator.py |
| `AV_VECTOR` | 2 | `AV_VECTOR\|A*v1\|[67/√2, 67/√2]` | svd_generator.py |
| `AXIOM` | 2 | `AXIOM\|nonnegativity\|every weight ≥ 0` | probability_axioms_finite_generator.py, probability_measure_generator.py |
| `AXIOM_MATCH` | 2 | `AXIOM_MATCH\|L1\|p := ((n ∨ g) → ¬g), q := (d ∨ e)` | hilbert_axiom_derivation_generator.py |
| `B` | 1, 3 | `B\|49\|0\|490` | decimal_div_generator.py, long_division_generator.py, percent_problem_generator.py, polynomial_long_division_generator.py |
| `BABY_STEP` | 2 | `BABY_STEP\|j=0\|1` | baby_step_giant_step_generator.py |
| `BACKPROP_DELTA` | 2 | `BACKPROP_DELTA\|h1\|delta=2` | backprop_generator.py |
| `BACKPROP_GRAD` | 2 | `BACKPROP_GRAD\|dL/dy_hat\|-2` | backprop_generator.py |
| `BACKPROP_SETUP` | 3 | `BACKPROP_SETUP\|x=(1,-2)\|y=1\|eta=1/3` | backprop_generator.py |
| `BACK_SUB` | 2 | `BACK_SUB\|u = 1/y\|y = 1/(2 + 6e^(2x))` | ode_substitution_generator.py |
| `BACK_SUB_ROW` | 3 | `BACK_SUB_ROW\|r=354\|x=1\|y=0` | extended_euclid_generator.py, modular_inverse_generator.py, rsa_generator.py |
| `BALANCED_EQ` | 1 | `BALANCED_EQ\|4 Al + 3 O2 -> 2 Al2O3` | stoichiometry_generator.py |
| `BALANCE_COEFFS` | 2 | `BALANCE_COEFFS\|reactants=4,3\|products=2` | stoichiometry_generator.py |
| `BALLOT_FORMULA` | 1 | `BALLOT_FORMULA\|strict lead probability=(a-b)/(a+b)` | ballot_reflection_generator.py |
| `BASE` | 2 | `BASE\|count_c(ε)\|0` | recursive_definition_unfold_generator.py |
| `BASE_ADD_COL` | 3 | `BASE_ADD_COL\|col 0\|1 + 1 + carry 0\|2 -> digit 2, carry 0` | base_arithmetic_generator.py |
| `BASE_ARITH_SETUP` | 2 | `BASE_ARITH_SETUP\|base 16\|93B * B` | base_arithmetic_generator.py |
| `BASE_CARRY` | 2 | `BASE_CARRY\|carry 6\|digit 6, carry 0` | base_arithmetic_generator.py |
| `BASE_MUL_COL` | 3 | `BASE_MUL_COL\|col 0\|B * B + carry 0\|121 -> digit 9, carry 7` | base_arithmetic_generator.py |
| `BASE_SETUP` | 2 | `BASE_SETUP\|2218_10\|hexadecimal` | base_conversion_generator.py |
| `BAYES_CELL` | 3 | `BAYES_CELL\|true positive\|119 × 1/7\|17` | conditional_probability_generator.py |
| `BAYES_EVIDENCE` | 2 | `BAYES_EVIDENCE\|sum of Bayes terms\|17/36` | bayes_multiple_hypotheses_generator.py, probability_critic_generator.py |
| `BAYES_FACTOR` | 2 | `BAYES_FACTOR\|L(0.2)/L(0.6)\|2` | discrete_posterior_generator.py |
| `BAYES_FORMULA` | 1 | `BAYES_FORMULA\|P(disease=no given negative) = TN/(TN + FN)` | conditional_probability_generator.py |
| `BAYES_ROW` | 3 | `BAYES_ROW\|0.2\|1/4 · 0.04 · 0.4096\|0.004096` | discrete_posterior_generator.py |
| `BAYES_SETUP` | 3 | `BAYES_SETUP\|disease=yes 119, disease=no 2040\|sensitivity 1/7, specificity 13/30\|P(disease=no given test negative)` | conditional_probability_generator.py |
| `BAYES_STAGE` | 2 | `BAYES_STAGE\|observe orange\|prior × likelihood for every hypothesis` | bayes_multiple_hypotheses_generator.py |
| `BAYES_TERM` | 3 | `BAYES_TERM\|U1\|1/10 × 1/2\|1/20` | bayes_multiple_hypotheses_generator.py, probability_critic_generator.py |
| `BAYES_UPDATE_SETUP` | 2, 3 | `BAYES_UPDATE_SETUP\|beta_binomial\|prior=Beta(11,4)\|successes=4, trials=9` | bayesian_update_generator.py, discrete_posterior_generator.py |
| `BCH_FORM` | 2 | `BCH_FORM\|A+B+1/2[A,B]\|[[0, 0, 0], [1/2, 0, -1], [-1, 0, 0]]` | bch_generator.py |
| `BCH_SETUP` | 3 | `BCH_SETUP\|A=-E23\|B=-E31\|order=2` | bch_generator.py |
| `BEARING` | 2 | `BEARING\|left 30\|130°` | spatial_description_generator.py |
| `BEC_FORMULA` | 1 | `BEC_FORMULA\|P(exactly one)=C(n,1)*epsilon*(1-epsilon)^(n-1)` | bec_channel_generator.py |
| `BEC_SETUP` | 1 | `BEC_SETUP\|epsilon=1/4` | bec_channel_generator.py |
| `BELL_ROW` | 3 | `BELL_ROW\|n=1\|1\|1` | set_counting_generator.py |
| `BEREZIN_RULE` | 2 | `BEREZIN_RULE\|int dtheta 1\|0` | grassmann_generator.py |
| `BETA` | 1, 3 | `BETA\|line 1\|1L: 2: g ∧ (¬f ∨ ¬f)\|1R: 3: g ∨ t` | lambda_reduction_generator.py, semantic_tableau_generator.py |
| `BETA_COUNT` | 1 | `BETA_COUNT\|1` | lambda_reduction_generator.py |
| `BEZOUT_CHECK` | 2 | `BEZOUT_CHECK\|354*-1 + 180*2\|6` | extended_euclid_generator.py |
| `BIAS` | 3 | `BIAS\|E[max] = 3.125\|N = 4\|-0.875` | estimator_bias_enum_generator.py, mse_decomposition_generator.py |
| `BIAS_CORRECT` | 2 | `BIAS_CORRECT\|m_hat\|5` | adam_step_generator.py |
| `BIJECTION_RULE` | 2 | `BIJECTION_RULE\|s(n)\|n²` | countability_bijection_generator.py |
| `BINARY` | 2 | `BINARY\|35984\|1000110010010000` | countability_bijection_generator.py |
| `BINARY_EXPONENT` | 2 | `BINARY_EXPONENT\|84\|1010100` | mod_exp_generator.py, quadratic_residue_generator.py |
| `BINOMIAL_MARGINAL` | 2 | `BINOMIAL_MARGINAL\|X_A ~ Binomial(n,p_A)\|B and C combine as not-A` | multinomial_probability_generator.py |
| `BINOM_FORMULA` | 1 | `BINOM_FORMULA\|P(X ≤ k) = Σ C(n,i)·p^i·(1-p)^(n-i)` | binomial_probability_generator.py, nonparametric_test_generator.py |
| `BINOM_SETUP` | 2 | `BINOM_SETUP\|n = 180, p = 5/6\|P(X ≥ 162)` | binomial_probability_generator.py, normal_approx_binomial_generator.py |
| `BIN_ASSIGN` | 2 | `BIN_ASSIGN\|75\|70-79` | histogram_construct_generator.py |
| `BIN_COUNT` | 2 | `BIN_COUNT\|40-49\|5` | grouped_data_generator.py, histogram_construct_generator.py |
| `BISECTION_SETUP` | 3 | `BISECTION_SETUP\|f(x)=x^2-168\|interval=[12, 13]\|iterations=3` | bisection_generator.py |
| `BISECT_UPDATE` | 3 | `BISECT_UPDATE\|1\|product > 0\|[25/2, 13]` | bisection_generator.py |
| `BIT` | 1, 2 | `BIT\|c\|A=0` | characteristic_vector_generator.py |
| `BITWISE` | 1 | `BITWISE\|⊕\|0110001111\|1011011010\|1101010101` | characteristic_vector_generator.py |
| `BIT_ROW` | 2, 3 | `BIT_ROW\|bit 0\|0 OR 1\|1` | bitwise_ops_generator.py |
| `BIT_RULE` | 2 | `BIT_RULE\|OR\|1 when at least one bit is 1` | bitwise_ops_generator.py |
| `BIT_SETUP` | 2 | `BIT_SETUP\|0010 OR 0101\|4-bit mask` | bitwise_ops_generator.py |
| `BLACKBODY_FORMULA` | 1 | `BLACKBODY_FORMULA\|lambda_max=b/T` | blackbody_generator.py |
| `BLACKBODY_SETUP` | 3 | `BLACKBODY_SETUP\|wien_peak\|b=27666\|T=954` | blackbody_generator.py |
| `BOND_FORMULA` | 1 | `BOND_FORMULA\|price=sum coupon/(1+y)^t + face/(1+y)^n` | bond_pricing_generator.py |
| `BOND_PRICE` | 1 | `BOND_PRICE\|$8500.00` | bond_pricing_generator.py |
| `BOND_SETUP` | 2 | `BOND_SETUP\|face=8500\|coupon=8%,ytm=8%,years=4` | bond_pricing_generator.py |
| `BOOL_SETUP` | 2 | `BOOL_SETUP\|variables A, B, C\|DNF from G=1 rows` | boolean_algebra_generator.py |
| `BORROW` | 3 | `BORROW\|col_3\|from_left\|1` | multi_digit_subtraction_generator.py |
| `BOUND` | 3 | `BOUND\|claim 10^7\|upper 20800000\|within` | fermi_estimation_generator.py, magnitude_comparison_generator.py, plausibility_critic_generator.py |
| `BOUNDARY_MLE` | 2 | `BOUNDARY_MLE\|smallest allowed theta\|20` | mle_generator.py |
| `BOX_FORMULA` | 1 | `BOX_FORMULA\|lambda=8*m*L^2*c/((n_high^2-n_low^2)*h)` | particle_in_box_generator.py |
| `BOX_SETUP` | 1, 3 | `BOX_SETUP\|transition_wavelength\|n_low=3, n_high=6\|h=2, c=10` | particle_in_box_generator.py |
| `BOX_SURFACE` | 2 | `BOX_SURFACE\|11×11×11\|726` | optimization_in_context_generator.py |
| `BRAKET_FORMULA` | 1 | `BRAKET_FORMULA\|inner(phi,psi)=sum conj(phi_k)*psi_k` | braket_generator.py |
| `BRAKET_SETUP` | 3 | `BRAKET_SETUP\|inner_product\|phi=[0,0,-1]\|psi=[0,1-i,2]` | braket_generator.py |
| `BRANCH_CLOSE` | 2 | `BRANCH_CLOSE\|1L\|c, ¬c` | semantic_tableau_generator.py |
| `BRANCH_OPEN` | 2 | `BRANCH_OPEN\|1LL\|f=F, g=T, t=F` | semantic_tableau_generator.py |
| `BRANCH_SUM` | 3 | `BRANCH_SUM\|AB + BA\|33/595 + 33/595\|66/595` | probability_critic_generator.py, tree_diagram_probability_generator.py |
| `BRANCH_TEST` | 2 | `BRANCH_TEST\|19000 <= 10000\|no` | piecewise_evaluation_generator.py |
| `BRANCH_USE` | 1 | `BRANCH_USE\|$6.25` | piecewise_evaluation_generator.py |
| `BREAK_EVEN` | 2 | `BREAK_EVEN\|1485 = (30 − 15)·u\|99` | scenario_generator.py |
| `BRING_DOWN` | 2 | `BRING_DOWN\|group 04\|current = 4` | composite_arithmetic_generator.py, manual_square_root_generator.py |
| `BSC_FORMULA` | 1 | `BSC_FORMULA\|H_b=p*(-log2 p)+(1-p)*(-log2(1-p))` | channel_capacity_generator.py |
| `BSC_SETUP` | 3 | `BSC_SETUP\|p=43/100\|-log2(p)=1.218\|-log2(1-p)=0.811` | channel_capacity_generator.py |
| `BSGS_MATCH` | 3 | `BSGS_MATCH\|i=2\|j=3\|x=15` | baby_step_giant_step_generator.py |
| `BSGS_SETUP` | 4 | `BSGS_SETUP\|p=29\|g=2\|h=27\|m=6` | baby_step_giant_step_generator.py |
| `BS_FORMULA` | 2 | `BS_FORMULA\|C=S*N(d1)-K*df*N(d2)\|P=K*df*N(-d2)-S*N(-d1)` | black_scholes_generator.py |
| `BS_RESULT` | 2 | `BS_RESULT\|call=0.95\|put=7.95` | black_scholes_generator.py |
| `BS_SETUP` | 3 | `BS_SETUP\|S=110,K=120\|df=0.975\|N_d1=0.7,N_d2=0.65` | black_scholes_generator.py |
| `BUDGET` | 3 | `BUDGET\|rent\|35%\|$2065.00` | money_life_generator.py |
| `BUFFON_FORMULA` | 1, 2 | `BUFFON_FORMULA\|P(cross)=2L/(pi*d)` | expected_value_classics_generator.py |
| `C` | 2, 3 | `C\|1/2\|14\|7/14` | alternative_means_generator.py, complement_probability_generator.py, experimental_probability_generator.py, fraction_comparison_generator.py, fraction_op_generator.py, mixed_number_operation_generator.py, rational_expr_add_sub_generator.py |
| `CAGR` | 2 | `CAGR\|(25/16)^(1/2)\|1.25` | index_and_growth_generator.py |
| `CALC` | 1 | `CALC\|x = 5` | systems_elimination_generator.py, systems_substitution_generator.py |
| `CAL_DIVMOD` | 3 | `CAL_DIVMOD\|22\|7\|3 R1` | calendar_arithmetic_generator.py |
| `CAL_FORMULA` | 1 | `CAL_FORMULA\|warm ice: q1=m*c_ice*(0-Ti)` | calorimetry_generator.py |
| `CAL_SETUP` | 3 | `CAL_SETUP\|start 2027-05-03\|end 2027-10-24\|days between` | calendar_arithmetic_generator.py, calorimetry_generator.py |
| `CANCEL` | 2 | `CANCEL\|5n\|5n - 2` | derivative_limit_def_generator.py, derivative_transcendental_generator.py, limit_evaluation_generator.py, power_series_generator.py, rational_expr_mult_div_generator.py, rational_expr_simplify_generator.py, rational_function_features_generator.py, series_convergence_generator.py, trig_identity_verify_generator.py |
| `CANDIDATES` | 1 | `CANDIDATES\|±1, ±3, ±9` | rational_root_generator.py |
| `CANONICAL_ORDER` | 1 | `CANONICAL_ORDER\|B=2, C=2, D=4, A=5` | kraft_inequality_generator.py |
| `CANONICAL_SHIFT` | 3 | `CANONICAL_SHIFT\|code=0\|left=2\|0` | kraft_inequality_generator.py |
| `CARD_RULE` | 2 | `CARD_RULE\|continuum to countable power\|c^ℵ0 = c` | cardinal_arithmetic_generator.py |
| `CARRY_FINAL` | 1 | `CARRY_FINAL\|1` | multi_digit_addition_generator.py |
| `CARTESIAN_RESULT` | 1 | `CARTESIAN_RESULT\|{(b, 15)}` | set_operations_generator.py |
| `CART_PAIR` | 3 | `CART_PAIR\|b\|15\|(b, 15)` | set_operations_generator.py |
| `CASE` | 1, 2, 3 | `CASE\|prize behind initial choice\|1/3\|stay wins` | classic_probability_puzzles_generator.py, countability_bijection_generator.py, knights_knaves_generator.py |
| `CASHFLOW_PV` | 2 | `CASHFLOW_PV\|coupon_t1\|17000/27` | bond_pricing_generator.py |
| `CASIMIR_FORCE_SETUP` | 2 | `CASIMIR_FORCE_SETUP\|F/A=-π^2*hbar*c/(240*d^4)\|hbar=19,c=18,d=8` | casimir_force_generator.py |
| `CASIMIR_SETUP` | 3 | `CASIMIR_SETUP\|spin=2\|hbar=46/9\|J^2=Jz^2+(J+J-+J-J+)/2` | casimir_generator.py |
| `CATALAN_FORMULA` | 1 | `CATALAN_FORMULA\|C_m=C(2m,m)/(m+1)` | ballot_reflection_generator.py |
| `CAYLEY_HEADER` | 1 | `CAYLEY_HEADER\|e, r, r2, s, rs, r2s` | cayley_table_generator.py |
| `CAYLEY_ROW` | 2 | `CAYLEY_ROW\|row e\|e, r, r2, s, rs, r2s` | cayley_table_generator.py |
| `CBRT` | 2 | `CBRT\|125p^3\|5p` | factor_special_forms_generator.py, inverse_function_generator.py, rational_exponent_generator.py |
| `CDF_EVENT` | 3 | `CDF_EVENT\|Y<=y\|X^2<=y\|X<=sqrt(y)` | rv_transform_generator.py |
| `CDF_FORMULA` | 2 | `CDF_FORMULA\|F_Y(y)=sqrt(y)/12\|0<=y<=144` | rv_transform_generator.py |
| `CDF_ROW` | 2 | `CDF_ROW\|-10\|103/256` | distribution_of_sum_generator.py, pmf_cdf_quantile_generator.py |
| `CDF_TABLE` | 2 | `CDF_TABLE\|outcomes 1,2,3,4\|F(1)=1/8, F(2)=5/8, F(3)=3/4, F(4)=1` | monte_carlo_arithmetic_generator.py |
| `CEIL` | 2 | `CEIL\|8000\|8000` | confidence_interval_generator.py, geometry_in_context_generator.py, inference_setup_generator.py, nonparametric_test_generator.py, percentile_generator.py, probability_inequality_generator.py, scenario_generator.py |
| `CENTER` | 1, 2 | `CENTER\|(4, 1)` | circle_equation_generator.py, ellipse_features_generator.py, hyperbola_features_generator.py, pca_generator.py |
| `CENTROID_COORD` | 3 | `CENTROID_COORD\|xbar = M_y/A\|(2197)/(507/2)\|26/3` | centroid_generator.py |
| `CENTROID_SETUP` | 3 | `CENTROID_SETUP\|0 <= y <= 3*x\|0 <= x <= 13\|centroid` | centroid_generator.py |
| `CENTROID_UPDATE` | 2 | `CENTROID_UPDATE\|C1\|(-3,5/3)` | kmeans_step_generator.py |
| `CF_PARTIAL` | 2 | `CF_PARTIAL\|a_0\|4` | continued_fraction_generator.py |
| `CF_RESULT` | 1 | `CF_RESULT\|[4; 1, 16, 1, 1, 2]` | continued_fraction_generator.py |
| `CF_SETUP` | 1 | `CF_SETUP\|435/88` | continued_fraction_generator.py |
| `CG_COEFF` | 2 | `CG_COEFF\|ket(+,-)\|0` | clebsch_gordan_generator.py |
| `CG_SETUP` | 3 | `CG_SETUP\|j1=1/2\|j2=1/2\|phase=+` | clebsch_gordan_generator.py |
| `CG_STATE` | 2 | `CG_STATE\|J=1, M=-1\|ket(-,-)` | clebsch_gordan_generator.py |
| `CHAIN` | 2 | `CHAIN\|{1, 3, 25, 57}\|length 4` | partial_order_generator.py |
| `CHAIN_DERIV` | 2 | `CHAIN_DERIV\|dy/dx\|-1/4` | activation_generator.py |
| `CHAIN_PERIOD` | 3 | `CHAIN_PERIOD\|{1, 2, 3, 4}\|return lengths {4, 5, 6, 7, 8}\|1` | markov_state_classification_generator.py |
| `CHAIN_RATE` | 2 | `CHAIN_RATE\|dx/dt\|4` | multivar_chain_rule_generator.py |
| `CHAIN_SUM` | 3 | `CHAIN_SUM\|f_x*dx/dt + f_y*dy/dt\|18*4 + (-6)*(-2)\|84` | multivar_chain_rule_generator.py |
| `CHAIN_VALUE` | 3 | `CHAIN_VALUE\|x(1)\|4*1 + (-1)\|3` | multivar_chain_rule_generator.py |
| `CHANGE_BASE` | 1 | `CHANGE_BASE\|log_4(64) = log_2(64)/log_2(4)` | log_conversion_generator.py |
| `CHANGE_ROW` | 3 | `CHANGE_ROW\|mean\|52.2 to 66.2\|changed` | linear_transform_effect_generator.py |
| `CHAR_DIAG` | 2 | `CHAR_DIAG\|diagonal of λI - A\|(λ + 4), (λ - 3)` | eigenvalue_generator.py |
| `CHAR_EQ` | 2 | `CHAR_EQ\|assume y=e^(rx)\|r^2 + 4r + 4 = 0` | ode_system_generator.py, second_order_ode_generator.py, undetermined_coeff_generator.py, variation_parameters_generator.py |
| `CHAR_POLY` | 2 | `CHAR_POLY\|p(λ) = λ^2 + λ - 12\|(λ + 4)*(λ - 3)` | diagonalization_generator.py, eigenvalue_generator.py, recurrence_generator.py |
| `CHAR_ROOTS` | 2 | `CHAR_ROOTS\|r = -2\|repeated` | recurrence_generator.py, second_order_ode_generator.py, undetermined_coeff_generator.py, variation_parameters_generator.py |
| `CHAR_SETUP` | 2 | `CHAR_SETUP\|p(λ) = det(λI - A)\|triangular determinant` | eigenvalue_generator.py |
| `CHECK` | 1, 2, 3, 4 | `CHECK\|multiply_back\|16×80+10=1290\|1290` | alternative_means_generator.py, annuity_generator.py, anova_generator.py, area_between_curves_generator.py, arithmetic_sequence_generator.py, assumption_check_generator.py, baby_step_giant_step_generator.py, ballot_reflection_generator.py, base_arithmetic_generator.py, bayes_multiple_hypotheses_generator.py, bayesian_update_generator.py, bch_generator.py, bitwise_ops_generator.py, boolean_algebra_generator.py, box_plot_generator.py, cantor_diagonal_generator.py, cantor_pairing_generator.py, cardinal_arithmetic_generator.py, casimir_generator.py, cauchy_riemann_generator.py, characteristic_vector_generator.py, chi_square_generator.py, cholesky_generator.py, classic_probability_puzzles_generator.py, clebsch_gordan_generator.py, clt_probability_generator.py, combinatory_logic_generator.py, commutator_generator.py, complement_probability_generator.py, completing_square_generator.py, conditional_expectation_generator.py, conditional_probability_generator.py, confidence_interval_generator.py, convolutional_code_viterbi_generator.py, coset_generator.py, countability_bijection_generator.py, covariance_algebra_generator.py, covariance_correlation_generator.py, cramers_rule_generator.py, cyclic_group_generator.py, cyk_parser_generator.py, dedekind_cut_generator.py, dfa_minimization_generator.py, dfa_simulation_generator.py, diagonalization_generator.py, diffie_hellman_generator.py, discrete_posterior_generator.py, discrete_uniform_bernoulli_generator.py, distribution_of_sum_generator.py, dot_plot_generator.py, ecdh_generator.py, ecdsa_generator.py, eigenvalue_generator.py, elliptic_curve_finite_field_generator.py, embedding_similarity_generator.py, empirical_cdf_generator.py, empirical_rule_generator.py, equilibrium_ice_generator.py, error_spotting_generator.py, estimator_bias_enum_generator.py, euler_circuit_generator.py, exact_ode_generator.py, expectation_of_function_generator.py, expected_value_classics_generator.py, expected_value_generator.py, experimental_probability_generator.py, extended_euclid_generator.py, factor_gcf_generator.py, factor_grouping_generator.py, factor_special_forms_generator.py, factor_trinomial_generator.py, feature_map_generator.py, fermi_estimation_generator.py, fill_in_step_generator.py, finite_sigma_algebra_generator.py, fisher_information_generator.py, five_number_summary_generator.py, formula_derivation_generator.py, foundations_critic_generator.py, fraction_line_plot_generator.py, function_inner_product_generator.py, fundamental_counting_principle_generator.py, game_theory_generator.py, gamma_matrix_generator.py, gauss_bonnet_generator.py, gaussian_curvature_generator.py, geometric_distribution_generator.py, geometric_mean_generator.py, geometric_probability_generator.py, geometric_sequence_generator.py, geometry_in_context_generator.py, godel_numbering_generator.py, gradient_generator.py, gram_schmidt_generator.py, graph_counting_generator.py, graph_interpret_generator.py, grouped_data_generator.py, growth_comparison_generator.py, hamming_code_generator.py, hereditarily_finite_set_generator.py, hermitian_check_generator.py, hessian_classify_generator.py, hilbert_axiom_derivation_generator.py, histogram_construct_generator.py, horner_evaluation_generator.py, hyperbolic_function_generator.py, hypergeometric_generator.py, hypothesis_test_generator.py, independence_check_generator.py, index_gymnastics_generator.py, induction_verify_generator.py, inference_setup_generator.py, information_gain_generator.py, integer_puzzle_word_generator.py, integers_as_pairs_generator.py, inverse_function_generator.py, inverse_normal_generator.py, kernel_perceptron_generator.py, kernel_validity_generator.py, kmeans_step_generator.py, knights_knaves_generator.py, knn_generator.py, ladder_operator_generator.py, lagrange_multiplier_generator.py, lambda_reduction_generator.py, law_of_total_probability_generator.py, least_squares_generator.py, legendre_construction_generator.py, lhopital_generator.py, lie_exponential_generator.py, likelihood_language_generator.py, likelihood_ratio_test_generator.py, limit_evaluation_generator.py, line_integral_generator.py, linear_fractional_generator.py, linear_model_word_generator.py, linear_transform_effect_generator.py, linearity_of_expectation_generator.py, lll_reduction_generator.py, log_equation_generator.py, logic_grid_puzzle_generator.py, logical_equivalence_laws_generator.py, long_division_generator.py, low_rank_approx_generator.py, lp_corner_generator.py, lu_decomposition_generator.py, lz_compression_generator.py, magnitude_comparison_generator.py, manual_square_root_generator.py, markov_chain_generator.py, markov_state_classification_generator.py, martingale_check_generator.py, matrix_exponential_generator.py, matrix_group_check_generator.py, matrix_inverse_generator.py, mean_adjustment_generator.py, mean_value_theorem_generator.py, measurement_uncertainty_generator.py, mental_strategy_generator.py, method_discrimination_generator.py, method_of_moments_generator.py, missing_information_generator.py, mixture_generator.py, mle_generator.py, mobius_transform_generator.py, modular_arithmetic_generator.py, modular_inverse_generator.py, money_life_generator.py, monte_carlo_arithmetic_generator.py, motion_word_generator.py, mse_decomposition_generator.py, multi_state_markov_generator.py, multi_step_word_generator.py, multinomial_probability_generator.py, naive_bayes_generator.py, named_distribution_generator.py, natural_deduction_generator.py, negative_binomial_generator.py, nfa_simulation_generator.py, nonparametric_test_generator.py, normal_approx_binomial_generator.py, normal_table_generator.py, odds_probability_generator.py, ode_system_generator.py, operation_properties_generator.py, optimization_in_context_generator.py, or_formula_generator.py, ordinal_arithmetic_generator.py, p_value_generator.py, partial_derivative_generator.py, partial_order_generator.py, partial_trace_generator.py, pauli_algebra_generator.py, pca_generator.py, pda_simulation_generator.py, peano_arithmetic_generator.py, percent_chain_generator.py, percent_word_problem_generator.py, percentile_generator.py, perceptron_generator.py, pgf_generator.py, plausibility_critic_generator.py, pmf_cdf_quantile_generator.py, poisson_process_generator.py, pollard_factorization_generator.py, polya_urn_generator.py, polynomial_inequality_generator.py, population_sample_generator.py, positive_definite_generator.py, power_series_generator.py, prenex_normal_form_generator.py, prime_factorization_generator.py, probability_axioms_finite_generator.py, probability_critic_generator.py, probability_inequality_generator.py, probability_measure_generator.py, projector_generator.py, proportion_word_problem_generator.py, qr_decomposition_generator.py, quadratic_factoring_generator.py, quadratic_square_root_generator.py, quadratic_word_generator.py, qualitative_reasoning_generator.py, quantifier_negation_generator.py, quaternion_generator.py, radical_variable_simplify_generator.py, random_walk_generator.py, rate_of_change_interpret_generator.py, ratio_table_generator.py, rationals_as_pairs_generator.py, recursive_explicit_generator.py, regex_to_automaton_generator.py, relation_closure_generator.py, representation_translation_generator.py, resolution_proof_generator.py, riemann_tensor_generator.py, rotational_dynamics_generator.py, rounding_effect_generator.py, routh_hurwitz_generator.py, rsa_generator.py, running_coupling_generator.py, rv_transform_generator.py, sample_space_list_generator.py, sampling_distribution_enum_generator.py, scatter_plot_describe_generator.py, semantic_tableau_generator.py, series_convergence_generator.py, set_algebra_laws_generator.py, shm_generator.py, signal_arithmetic_generator.py, significant_figures_generator.py, similar_triangles_generator.py, simple_probability_generator.py, simplex_generator.py, simpsons_paradox_generator.py, slope_inference_generator.py, special_solution_equation_generator.py, standard_deviation_generator.py, statics_generator.py, stem_and_leaf_generator.py, stereographic_generator.py, structure_constant_generator.py, structure_isomorphism_generator.py, sufficiency_factorization_generator.py, svd_generator.py, svm_margin_generator.py, syllogism_generator.py, systems_elimination_generator.py, systems_word_generator.py, t_interval_generator.py, tally_frequency_generator.py, taylor_series_generator.py, tip_bill_split_generator.py, tonelli_shanks_generator.py, totient_generator.py, transportation_generator.py, tree_diagram_probability_generator.py, turing_machine_trace_generator.py, two_sample_test_generator.py, two_step_equation_generator.py, two_way_table_generator.py, type_error_power_generator.py, type_theory_generator.py, uncertainty_generator.py, unit_rate_generator.py, venn_region_count_generator.py, weighted_mean_generator.py, work_rate_generator.py, young_tableaux_generator.py, z_score_generator.py, zf_axiom_identify_generator.py |
| `CHECK_POINT` | 3 | `CHECK_POINT\|x=0\|14·0 + 12 = 12\|14·0 + 10 = 10` | special_solution_equation_generator.py |
| `CHINCHILLA` | 2 | `CHINCHILLA\|20N\|700000000` | scaling_law_generator.py |
| `CHI_DF` | 2 | `CHI_DF\|df = (3 - 1)(3 - 1)\|4` | chi_square_generator.py |
| `CHI_FORMULA` | 1 | `CHI_FORMULA\|E = (row·column)/N; χ² = Σ (O - E)^2/E` | chi_square_generator.py |
| `CHI_SETUP` | 2 | `CHI_SETUP\|observed rows: 8, 6, 6 / 8, 9, 13 / 24, 15, 11\|independence; shape 3x3; df = 4; α = 0.05; critical = 9.488` | chi_square_generator.py |
| `CHI_TERM` | 3 | `CHI_TERM\|r1c1: 17 - 16 = 1\|1^2 = 1\|1/16 = 0.0625` | chi_square_generator.py |
| `CHOLESKY_ENTRY` | 2 | `CHOLESKY_ENTRY\|l11\|4` | cholesky_generator.py |
| `CHOL_SETUP` | 2 | `CHOL_SETUP\|A = [[16, -8, 4], [-8, 13, 10], [4, 10, 21]]\|A = L L^T` | cholesky_generator.py |
| `CHRISTOFFEL_FORMULA` | 1 | `CHRISTOFFEL_FORMULA\|Gamma^i_jk = 1/2 g^im(d_j g_mk + d_k g_mj - d_m g_jk)` | christoffel_generator.py |
| `CHRISTOFFEL_SETUP` | 3 | `CHRISTOFFEL_SETUP\|polar\|g_rr=1, g_thetatheta=r^2\|r=71` | christoffel_generator.py |
| `CHRISTOFFEL_VALUE` | 2 | `CHRISTOFFEL_VALUE\|Gamma^phi_thetatheta\|-4680/9409` | riemann_tensor_generator.py |
| `CHURCH_NUMERAL` | 2 | `CHURCH_NUMERAL\|2\|lambda t. (lambda h. (t (t h)))` | lambda_reduction_generator.py |
| `CIRCLE_ANGLE_SETUP` | 2 | `CIRCLE_ANGLE_SETUP\|inscribed angle 29°\|central angle on the same arc` | circle_angle_generator.py |
| `CIRCLE_CALCULATE` | 2 | `CIRCLE_CALCULATE\|C = 10π\|10π` | circle_generator.py |
| `CIRCLE_EQ` | 1 | `CIRCLE_EQ\|(x - 1)^2 + (y - 5)^2 = 64` | complex_locus_generator.py |
| `CIRCLE_FORMULA` | 1 | `CIRCLE_FORMULA\|C = 2πr` | circle_generator.py |
| `CIRCLE_SETUP` | 2 | `CIRCLE_SETUP\|5\|radius` | circle_equation_generator.py, circle_generator.py |
| `CIRCLE_SUBSTITUTE` | 1 | `CIRCLE_SUBSTITUTE\|C = 2 × π × 5` | circle_generator.py |
| `CIRCULATION_SUM` | 2 | `CIRCULATION_SUM\|2*10^2*pi\|200*pi` | vector_theorem_generator.py |
| `CI_FORMULA` | 1 | `CI_FORMULA\|x̄ ± E` | confidence_interval_generator.py, t_interval_generator.py |
| `CI_SETUP` | 2 | `CI_SETUP\|σ = 8, E = 1, z* = 1.28\|minimum sample size for the mean` | confidence_interval_generator.py, t_interval_generator.py |
| `CLASS` | 2 | `CLASS\|remainder 0\|{3, 6, 9}` | equivalence_relation_generator.py, markov_state_classification_generator.py |
| `CLASSIFY` | 2 | `CLASSIFY\|contingency\|T at 6 of 8 rows` | foundations_critic_generator.py, truth_table_generator.py |
| `CLASS_TYPE` | 3 | `CLASS_TYPE\|{1, 2, 3}\|an edge leaves\|transient` | markov_state_classification_generator.py |
| `CLAUSE` | 2 | `CLAUSE\|C1\|(P82135)` | resolution_proof_generator.py |
| `CLIFFORD_EXPECT` | 3 | `CLIFFORD_EXPECT\|2*eta=2\|I_entry=0\|0` | gamma_matrix_generator.py |
| `CLOCK_ANGLE` | 2 | `CLOCK_ANGLE\|minute hand\|270°` | spatial_description_generator.py |
| `CLOSURE_ADD` | 2 | `CLOSURE_ADD\|(11, 11)\|reflexive` | relation_closure_generator.py |
| `CLT_CENTER` | 2 | `CLT_CENTER\|E[x̄] = μ\|268` | clt_probability_generator.py |
| `CLT_CHECK` | 2 | `CLT_CHECK\|n = 169 ≥ 30\|approximately normal` | clt_probability_generator.py, inference_setup_generator.py |
| `CLUE_APPLY` | 3 | `CLUE_APPLY\|clue 1\|Quin does not have drum\|24 → 18 candidates` | logic_grid_puzzle_generator.py |
| `CLUSTER_MEMBERS` | 2 | `CLUSTER_MEMBERS\|C1\|P1,P2,P4` | kmeans_step_generator.py |
| `CMP` | 2, 3 | `CMP\|37\|43\|<` | assumption_check_generator.py, decision_under_uncertainty_generator.py, dedekind_cut_generator.py, experimental_probability_generator.py, fermi_estimation_generator.py, fraction_comparison_generator.py, graph_interpret_generator.py, growth_comparison_generator.py, integers_as_pairs_generator.py, likelihood_language_generator.py, linear_model_word_generator.py, logical_connective_eval_generator.py, magnitude_comparison_generator.py, measurement_uncertainty_generator.py, money_life_generator.py, pmf_cdf_quantile_generator.py, probability_measure_generator.py, qualitative_reasoning_generator.py, rate_of_change_interpret_generator.py, rationals_as_pairs_generator.py, risk_communication_generator.py, set_builder_roster_generator.py, simpsons_paradox_generator.py, square_cube_law_generator.py, unit_rate_generator.py |
| `CMP_DIGIT` | 4 | `CMP_DIGIT\|pos_0\|9\|1\|>` | number_comparison_generator.py |
| `CMP_NUM` | 3 | `CMP_NUM\|903.19\|102.54\|>` | number_comparison_generator.py |
| `CNF` | 1 | `CNF\|ω^2·5 + ω·2 + 3` | ordinal_arithmetic_generator.py |
| `CNF_FORM` | 1 | `CNF_FORM\|(X OR Y OR Z) AND (X OR Y OR NOT Z) AND (X OR NOT Y OR Z) AND (NOT X OR Y OR Z) AND (NOT X OR Y OR NOT Z)` | boolean_algebra_generator.py |
| `CODEWORD` | 1, 3 | `CODEWORD\|1110000` | hamming_code_generator.py, kraft_inequality_generator.py |
| `CODE_LENGTH` | 2 | `CODE_LENGTH\|A\|l=2` | huffman_coding_generator.py |
| `COEFF` | 2 | `COEFF\|a_1\|41760` | laurent_series_generator.py, series_solution_generator.py |
| `COEFFS` | 1, 2 | `COEFFS\|1, -5, 1, 5, 2` | horner_evaluation_generator.py, polynomial_zeros_generator.py, synthetic_division_generator.py |
| `COEFF_MATCH` | 2 | `COEFF_MATCH\|x^n\|(n+1)a_(n+1) = 4a_n` | series_solution_generator.py |
| `COEFF_PAIR` | 3 | `COEFF_PAIR\|i=0, j=3\|0+3=3\|56` | generating_function_generator.py |
| `COFACTOR` | 2 | `COFACTOR\|(1,1) sign +\|minor [[4, -4], [4, -2]]` | determinant_generator.py |
| `COLLIDER_SETUP` | 3 | `COLLIDER_SETUP\|events_fb\|L=7 fb^-1\|sigma=13 fb` | cross_section_generator.py |
| `COLLISION` | 1 | `COLLISION\|f(d) = f(q) = 14` | function_properties_generator.py |
| `COLLISION_SETUP` | 3 | `COLLISION_SETUP\|inelastic_2d\|m1=2, v1=(5,7)\|m2=19, v2=(10,-4)` | collision_generator.py |
| `COL_BASIS` | 2 | `COL_BASIS\|original columns 1, 2, 3\|[[10, -3, 19], [-3, 1, -6], [1, 0, 2]]` | subspace_basis_generator.py |
| `COMB` | 2 | `COMB\|C(5,1)\|5` | bec_channel_generator.py |
| `COMBO` | 2 | `COMBO\|x = -v1 - 5*v2\|[-1, -4]` | diagonalization_generator.py |
| `COMB_CONST` | 3 | `COMB_CONST\|7\|+6\|13` | derivative_product_quotient_generator.py, equation_from_two_points_generator.py, linear_complex_generator.py, rational_expr_add_sub_generator.py, simplify_expression_generator.py, special_solution_equation_generator.py |
| `COMB_FORMULA` | 1 | `COMB_FORMULA\|C(n, r) = P(n, r)/r!` | permutation_combination_generator.py |
| `COMB_RULE` | 2 | `COMB_RULE\|S x y z\|x z (y z)` | combinatory_logic_generator.py |
| `COMB_SETUP` | 2 | `COMB_SETUP\|C(18, 5)\|n!/(r!·(n-r)!)` | counting_classics_generator.py, permutation_combination_generator.py, stars_and_bars_generator.py |
| `COMB_X` | 1, 3 | `COMB_X\|3x\|+4x\|7x` | derivative_product_quotient_generator.py, integer_puzzle_word_generator.py, linear_complex_generator.py, rational_expr_add_sub_generator.py, simplify_expression_generator.py, special_solution_equation_generator.py, systems_word_generator.py |
| `COMMON_DEN` | 1 | `COMMON_DEN\|14` | formula_derivation_generator.py |
| `COMMON_DIFF` | 2 | `COMMON_DIFF\|-4 - (-6)\|2` | arithmetic_sequence_generator.py, recursive_explicit_generator.py |
| `COMMON_RATIO` | 2 | `COMMON_RATIO\|1694/2662\|7/11` | geometric_sequence_generator.py, recursive_explicit_generator.py |
| `COMMUTATOR` | 2 | `COMMUTATOR\|[A,B]\|[[0, -117i/2], [-117i/2, 0]]` | structure_constant_generator.py |
| `COMM_ENTRY` | 3 | `COMM_ENTRY\|(1,1)\|0 - 0\|0` | structure_constant_generator.py |
| `COMM_FORMULA` | 1 | `COMM_FORMULA\|[A,B]f=A(Bf)-B(Af)` | commutator_generator.py |
| `COMM_RESULT` | 2 | `COMM_RESULT\|[x,p]f\|10i*x^11` | commutator_generator.py |
| `COMM_SETUP` | 3 | `COMM_SETUP\|[x,p]f\|f=x^11\|p=-i*hbar*D, hbar=10` | commutator_generator.py |
| `COMPARE` | 2, 3 | `COMPARE\|6 = 6\|log_b(a) = k` | algorithm_trace_generator.py, equilibrium_ice_generator.py, fixed_point_generator.py, master_theorem_generator.py, scatter_plot_describe_generator.py, two_way_table_generator.py |
| `COMPASS_TURN` | 2 | `COMPASS_TURN\|NW counterclockwise 1 steps\|W` | spatial_description_generator.py |
| `COMPLEMENT` | 1, 2, 3 | `COMPLEMENT\|P(Aᶜ) = 1 − P(A)\|1 − 1/2\|1/2` | classic_probability_puzzles_generator.py, complement_probability_generator.py, derangement_generator.py, hypergeometric_generator.py, odds_probability_generator.py, probability_axioms_finite_generator.py, probability_critic_generator.py, reliability_system_generator.py |
| `COMPLETE_SQUARE` | 2 | `COMPLETE_SQUARE\|half of -4 = -2\|(-2)^2 = 4` | completing_square_generator.py, conic_standard_form_generator.py, polar_parametric_generator.py |
| `COMPOSE` | 3 | `COMPOSE\|b\|f(b) = 23\|g(23) = N` | function_properties_generator.py |
| `COMPOSE_PAIR` | 3 | `COMPOSE_PAIR\|(h, 6)\|(6, C)\|(h, C)` | relation_operations_generator.py |
| `COMPOSITE_FACTOR` | 2 | `COMPOSITE_FACTOR\|3\|59` | divisibility_classification_generator.py |
| `COMPOSITE_SETUP` | 2 | `COMPOSITE_SETUP\|add the scores, then divide by the count\|mean of 5 numbers` | composite_arithmetic_generator.py |
| `COMP_INEQ_PART` | 2 | `COMP_INEQ_PART\|Part 1\|x + 2 < 2 -> x < 0` | compound_inequality_generator.py |
| `COMP_INEQ_SETUP` | 1 | `COMP_INEQ_SETUP\|x + 2 < 2 or x + 2 > 14` | compound_inequality_generator.py |
| `CONCLUDE` | 1 | `CONCLUDE\|odd` | direct_proof_algebra_generator.py |
| `CONCLUSION_AT` | 2 | `CONCLUSION_AT\|p=T, q=F, r=T, s=F\|T` | argument_form_generator.py |
| `CONCLUSION_CHECK` | 1 | `CONCLUSION_CHECK\|not forced` | syllogism_generator.py |
| `COND_COL` | 3 | `COND_COL\|South given Option A\|1/4\|25%` | two_way_table_generator.py |
| `COND_COUNT` | 2 | `COND_COUNT\|sleep=good and exercise=no\|77` | conditional_probability_generator.py |
| `COND_ENTROPY` | 1 | `COND_ENTROPY\|H(Y given X)=H(X,Y)-H(X)` | mutual_information_generator.py |
| `COND_EXP` | 2, 3 | `COND_EXP\|E[X given Y=1]\|9/4` | conditional_expectation_generator.py |
| `COND_EXP_ATOM` | 3 | `COND_EXP_ATOM\|{1}\|sum 7 / 1\|7` | finite_sigma_algebra_generator.py |
| `COND_FORMULA` | 1 | `COND_FORMULA\|P(size=large given delivery=pickup) = count(both)/count(delivery=pickup)` | conditional_expectation_generator.py, conditional_probability_generator.py, joint_distribution_generator.py, two_way_table_probability_generator.py |
| `COND_PARTS` | 2 | `COND_PARTS\|n > 522\|n > 456` | conditional_forms_generator.py |
| `COND_PROB_ATOM` | 3 | `COND_PROB_ATOM\|{1}\|1 of 1\|1` | finite_sigma_algebra_generator.py |
| `COND_ROW` | 3 | `COND_ROW\|In person given Group 2\|1/4\|25%` | two_way_table_generator.py |
| `COND_SETUP` | 2, 3 | `COND_SETUP\|exercise=yes and sleep=good: 60; exercise=yes and sleep=poor: 51; exercise=no and sleep=good: 77; exercise=no and sleep=poor: 43\|P(sleep=good given exercise=no)` | conditional_probability_generator.py |
| `COND_TOTAL` | 2 | `COND_TOTAL\|exercise=no total\|77 + 43 = 120` | conditional_probability_generator.py |
| `COND_VAR` | 2 | `COND_VAR\|Var(X given Y=0)\|705575/36864` | conditional_expectation_generator.py |
| `CONGRUENCE_REDUCE` | 2 | `CONGRUENCE_REDUCE\|20x congruent to 3\|mod 9` | modular_inverse_generator.py |
| `CONGRUENCE_SOLUTIONS` | 3 | `CONGRUENCE_SOLUTIONS\|base 6\|step 9\|6` | modular_inverse_generator.py |
| `CONIC_SETUP` | 2 | `CONIC_SETUP\|y^2 = -12x\|vertex, focus, directrix` | conic_standard_form_generator.py, ellipse_features_generator.py, hyperbola_features_generator.py, parabola_features_generator.py |
| `CONJ` | 2 | `CONJ\|phi_1=0\|0` | braket_generator.py |
| `CONJUGATE` | 2 | `CONJUGATE\|5 + 4i\|5 - 4i` | complex_division_generator.py, quaternion_generator.py |
| `CONNECTIVE` | 2 | `CONNECTIVE\|p ∨ q\|T` | logical_connective_eval_generator.py |
| `CONSERVATION_SETUP` | 2 | `CONSERVATION_SETUP\|pi0 + e- + e+ + pi0 -> gamma + gamma\|check=Q,B,Le,Lmu` | conservation_law_generator.py |
| `CONSERVE_CHECK` | 3 | `CONSERVE_CHECK\|Q\|left=0,right=0\|conserved` | conservation_law_generator.py |
| `CONSTRAINT_SUBST` | 3 | `CONSTRAINT_SUBST\|x + y = 24\|x = 3*24/4\|18` | lagrange_multiplier_generator.py |
| `CONST_SOLVE` | 2 | `CONST_SOLVE\|C1 = -3\|C2 = -4` | recurrence_generator.py |
| `CONTOUR_SETUP` | 3 | `CONTOUR_SETUP\|abs(z)=5\|positive orientation\|f=-3/(z+6) + 6/(z+7) + 4/(z-8)` | contour_integral_generator.py |
| `CONTRADICTION` | 2 | `CONTRADICTION\|r−d is nonnegative and in S\|r−d < r` | induction_verify_generator.py |
| `CONT_CORR` | 2 | `CONT_CORR\|P(X ≥ 162)\|P(Y ≥ 161.5)` | normal_approx_binomial_generator.py |
| `CONT_DIST_SETUP` | 3 | `CONT_DIST_SETUP\|f(x)=k*x\|support=[0,15]\|interval=(5,8)` | continuous_distribution_generator.py |
| `CONVERGENT` | 2 | `CONVERGENT\|i=0\|4/1` | continued_fraction_generator.py |
| `CONVERGE_CHECK` | 2 | `CONVERGE_CHECK\|abs(r) = 7/11 < 1\|converges` | geometric_sequence_generator.py, series_convergence_generator.py |
| `CONV_ENCODE_STEP` | 3 | `CONV_ENCODE_STEP\|i=1\|prev=0,u=0\|00` | convolutional_code_viterbi_generator.py |
| `CONV_FACTOR` | 2 | `CONV_FACTOR\|1 hr\|60 min` | cross_section_generator.py, dimensional_analysis_generator.py, linear_transform_effect_generator.py, multi_step_unit_conversion_generator.py, rate_conversion_generator.py, square_cube_law_generator.py, unit_conversion_generator.py |
| `CONV_INIT` | 2 | `CONV_INIT\|h_-2=0,h_-1=1\|k_-2=1,k_-1=0` | continued_fraction_generator.py |
| `CONV_RECEIVED` | 2 | `CONV_RECEIVED\|011101\|flipped position 2` | convolutional_code_viterbi_generator.py |
| `CONV_RESULT` | 2 | `CONV_RESULT\|2520 min\|42 hr` | dimensional_analysis_generator.py, multi_step_unit_conversion_generator.py, rate_conversion_generator.py, temperature_conversion_generator.py, unit_conversion_generator.py |
| `CONV_SETUP` | 2, 3 | `CONV_SETUP\|x=[7,2,5,0,8]\|h=[0,3,4]` | convolution_generator.py, convolutional_code_viterbi_generator.py |
| `CONV_STEP` | 3 | `CONV_STEP\|i=0\|h=4\|k=1` | continued_fraction_generator.py |
| `CONV_SUM` | 2 | `CONV_SUM\|M=0\|121/1024` | convolution_generator.py, distribution_of_sum_generator.py |
| `CONV_WINDOW` | 2 | `CONV_WINDOW\|s=0\|1/32·13/16` | convolution_generator.py, distribution_of_sum_generator.py |
| `COORDS` | 2 | `COORDS\|c = P^-1 x\|[-1, -5]` | diagonalization_generator.py |
| `CORRECT_BIT` | 3 | `CORRECT_BIT\|position=1\|0->1\|corrected=1010101` | hamming_code_generator.py |
| `CORR_FORMULA` | 1 | `CORR_FORMULA\|r = Sxy/√(Sxx·Syy)` | covariance_correlation_generator.py, joint_distribution_generator.py, regression_generator.py |
| `CORR_PROPERTY` | 2 | `CORR_PROPERTY\|positive rescaling and shifts\|correlation unchanged` | covariance_correlation_generator.py |
| `COS` | 2 | `COS\|pi\|-1` | positional_encoding_generator.py |
| `COSET` | 2 | `COSET\|eH\|{e, r2s}` | coset_generator.py |
| `COSET_ELEM` | 2 | `COSET_ELEM\|eH\|e` | coset_generator.py |
| `COSET_SKIP` | 2 | `COSET_SKIP\|s\|already listed` | coset_generator.py |
| `COSET_START` | 2 | `COSET_START\|rep e\|eH` | coset_generator.py |
| `COSINE` | 2 | `COSINE\|A,A\|1` | embedding_similarity_generator.py, lr_schedule_generator.py |
| `COST` | 1 | `COST\|initial` | transportation_generator.py |
| `COUNT` | 2, 3 | `COUNT\|neither\|3` | attribute_sorting_generator.py, bayesian_update_generator.py, classic_probability_puzzles_generator.py, empirical_cdf_generator.py, equivalence_relation_generator.py, finite_sigma_algebra_generator.py, graph_interpret_generator.py, likelihood_language_generator.py, logical_connective_eval_generator.py, method_of_moments_generator.py, mle_generator.py, nonparametric_test_generator.py, one_to_one_correspondence_generator.py, percentile_generator.py, probability_addition_rule_generator.py, random_digit_simulation_generator.py, sampling_distribution_enum_generator.py, scatter_plot_describe_generator.py, set_builder_roster_generator.py, set_membership_subset_generator.py, set_operations_generator.py |
| `COUNTEREXAMPLE` | 2, 3 | `COUNTEREXAMPLE\|n = 565\|565 is divisible by 5 but not by 12` | argument_form_generator.py, conditional_forms_generator.py, counterexample_search_generator.py, truth_table_generator.py |
| `COUNTERMODEL` | 1 | `COUNTERMODEL\|editors=TFF, librarians=FFF, dancers=FTF` | syllogism_generator.py |
| `COUNT_DP` | 3 | `COUNT_DP\|2\|1\|3` | decimal_mult_generator.py |
| `COUNT_RULE` | 2 | `COUNT_RULE\|reflexive relations\|2^(card(A)^2−card(A))` | function_properties_generator.py, set_counting_generator.py |
| `COUNT_SETUP` | 1, 2 | `COUNT_SETUP\|arrangements of 7 cards\|7!` | counting_classics_generator.py, counting_to_probability_generator.py |
| `COUPON` | 1 | `COUPON\|680` | bond_pricing_generator.py |
| `COUPON_STAGE` | 2 | `COUPON_STAGE\|collected=0, unseen=8\|new probability=1` | expected_value_classics_generator.py |
| `COVER` | 3 | `COVER\|17\|31\|no c strictly between` | partial_order_generator.py |
| `COV_ENTRY` | 2 | `COV_ENTRY\|xx\|32` | pca_generator.py |
| `COV_FORMULA` | 1 | `COV_FORMULA\|Cov=E[XY]-E[X]E[Y]` | joint_distribution_generator.py |
| `COV_RULE` | 1, 2 | `COV_RULE\|Cov(X,X+Y)\|Var(X) + Cov(X,Y)` | covariance_algebra_generator.py |
| `CRC_CHECK` | 3 | `CRC_CHECK\|codeword=100000101\|remainder=0000\|valid` | crc_generator.py |
| `CRC_REMAINDER` | 1 | `CRC_REMAINDER\|0101` | crc_generator.py |
| `CRC_SETUP` | 3 | `CRC_SETUP\|data=10000\|poly=10011\|augmented=100000000` | crc_generator.py |
| `CRC_SKIP` | 2 | `CRC_SKIP\|i=1\|leading bit 0` | crc_generator.py |
| `CRC_XOR` | 3 | `CRC_XOR\|i=0\|10000 xor 10011\|00011` | crc_generator.py |
| `CREDIBLE_PICK` | 3 | `CREDIBLE_PICK\|0.3\|81/92\|81/92` | discrete_posterior_generator.py |
| `CRIT_EQS` | 2 | `CRIT_EQS\|f_x = 0\|-2*x + y + 11 = 0` | hessian_classify_generator.py |
| `CRIT_REGION` | 2 | `CRIT_REGION\|reject if x̄ > 116 + 2.33·4\|125.32` | type_error_power_generator.py |
| `CRIT_SOLVE` | 3 | `CRIT_SOLVE\|det\|(-2)*(-8) - 1^2\|15` | hessian_classify_generator.py |
| `CRLB` | 2 | `CRLB\|1/I_n(p)\|1/90` | fisher_information_generator.py |
| `CROSSOVER` | 3 | `CROSSOVER\|2\|$428.00\|$450.00` | growth_comparison_generator.py |
| `CROSS_ENTROPY` | 2 | `CROSS_ENTROPY\|target=1\|ln(2)` | perplexity_generator.py, softmax_gradient_generator.py |
| `CROSS_MULT` | 1 | `CROSS_MULT\|9·BC = 6·12` | similar_triangles_generator.py, triangle_solve_generator.py |
| `CROSS_RATIO` | 1 | `CROSS_RATIO\|7/4` | mobius_transform_generator.py |
| `CROSS_RATIO_SETUP` | 4 | `CROSS_RATIO_SETUP\|z1=-2\|z2=-7\|z3=3\|z4=0` | mobius_transform_generator.py |
| `CRT_CHECK` | 3 | `CRT_CHECK\|i=1\|4\|4` | crt_generator.py |
| `CRT_CONGRUENCE` | 3 | `CRT_CONGRUENCE\|i=1\|x=4\|mod 5` | crt_generator.py |
| `CRT_FACTOR` | 3 | `CRT_FACTOR\|i=1\|M_i=7\|mod 5` | crt_generator.py |
| `CRT_SETUP` | 1 | `CRT_SETUP\|2 congruences` | crt_generator.py |
| `CRT_TERM` | 2 | `CRT_TERM\|i=1\|84` | crt_generator.py |
| `CRT_TOTAL_MODULUS` | 2 | `CRT_TOTAL_MODULUS\|5, 7\|35` | crt_generator.py |
| `CR_SETUP` | 2 | `CR_SETUP\|u=-3x^2 + 3y^2 + 4x + 5y\|v=-6xy - 5x + 4y` | cauchy_riemann_generator.py |
| `CUM_INTERVAL` | 2 | `CUM_INTERVAL\|A\|[0,1/4)` | arithmetic_coding_generator.py |
| `CUM_ROW` | 2 | `CUM_ROW\|50-59\|20` | grouped_data_generator.py |
| `CURL_COMPONENT` | 3 | `CURL_COMPONENT\|Q_x - P_y\|6 + 6\|12` | div_curl_generator.py |
| `CURRENT_YIELD` | 1 | `CURRENT_YIELD\|0.08` | bond_pricing_generator.py |
| `CURVATURE_FORMULA` | 2 | `CURVATURE_FORMULA\|circle\|kappa = 1/R` | curve_geometry_generator.py |
| `CURVE_GEOM_SETUP` | 3 | `CURVE_GEOM_SETUP\|r(t) = <7*t + 4, 24*t - 1>\|0 <= t <= 5\|arc length` | curve_geometry_generator.py |
| `CURVE_SETUP` | 2 | `CURVE_SETUP\|f(x) = x^3 - 9x^2 + 24x - 8\|critical points and their nature` | curve_analysis_generator.py |
| `CUT_RULE` | 2 | `CUT_RULE\|L(√2)\|q < 0 or q² < 2` | dedekind_cut_generator.py |
| `CV_FORMULA` | 1 | `CV_FORMULA\|σ/μ × 100%` | standard_deviation_generator.py |
| `CW_START` | 2 | `CW_START\|leading 1\|1/1` | countability_bijection_generator.py |
| `CW_STEP` | 3 | `CW_STEP\|bit 0\|1/1\|1/2` | countability_bijection_generator.py |
| `CX_A` | 3 | `CX_A\|0\|-12i/13\|-12i/13` | braket_generator.py, spin_half_generator.py |
| `CX_M` | 3 | `CX_M\|0\|-5/13\|0` | braket_generator.py, spin_half_generator.py |
| `CX_SETUP` | 2 | `CX_SETUP\|(2 - 4i) + (5 - 4i)\|add` | complex_division_generator.py, complex_number_ops_generator.py |
| `CYCLE` | 1 | `CYCLE\|(1 5 2 4 3)` | permutation_group_generator.py |
| `CYCLE_LENGTHS` | 1 | `CYCLE_LENGTHS\|5` | permutation_group_generator.py |
| `CYCLE_REJECT` | 2 | `CYCLE_REJECT\|CE\|endpoints already connected` | mst_generator.py |
| `CYCLE_TRACE` | 2 | `CYCLE_TRACE\|start 1\|1->5->2->4->3->1` | permutation_group_generator.py |
| `CYCLIC_START` | 2 | `CYCLIC_START\|14\|identity 0` | cyclic_group_generator.py |
| `CYCLIC_SUBGROUP` | 2 | `CYCLIC_SUBGROUP\|{0, 14, 12, 10, 8, 6, 4, 2}\|8` | cyclic_group_generator.py |
| `CYK_CELL` | 2 | `CYK_CELL\|1,2\|{C,S}` | cyk_parser_generator.py |
| `CYK_COMBINE` | 3 | `CYK_COMBINE\|C V\|{S}\|cell 1,2` | cyk_parser_generator.py |
| `CYK_RULE` | 2 | `CYK_RULE\|C\|d or V C or V V` | cyk_parser_generator.py |
| `CYK_SETUP` | 2 | `CYK_SETUP\|string ddd\|length 3` | cyk_parser_generator.py |
| `CYK_SPAN` | 1 | `CYK_SPAN\|2` | cyk_parser_generator.py |
| `CYK_SPLIT` | 3 | `CYK_SPLIT\|cell 1,2\|1,1 x 2,2\|{C,V} x {C,V}` | cyk_parser_generator.py |
| `CYK_TERMINAL` | 3 | `CYK_TERMINAL\|cell 1,1\|d\|{C,V}` | cyk_parser_generator.py |
| `CYL_BOUNDS` | 2 | `CYL_BOUNDS\|z\|0..9` | triple_integral_generator.py |
| `CYL_CONVERT` | 2 | `CYL_CONVERT\|5*z dV\|5*z*r dz dr dtheta` | triple_integral_generator.py |
| `D` | 3 | `D\|129\|80\|1` | ac_circuit_generator.py, activation_generator.py, adam_step_generator.py, alternative_means_generator.py, angle_defect_generator.py, annuity_generator.py, anova_generator.py, antiderivative_generator.py, arithmetic_coding_generator.py, arithmetic_sequence_generator.py, assumption_check_generator.py, attention_generator.py, backprop_generator.py, ballot_reflection_generator.py, bayes_multiple_hypotheses_generator.py, bayesian_update_generator.py, bisection_generator.py, blackbody_generator.py, bond_pricing_generator.py, branching_ratio_generator.py, cantor_pairing_generator.py, casimir_force_generator.py, cholesky_generator.py, christoffel_generator.py, circle_angle_generator.py, circle_equation_generator.py, classic_probability_puzzles_generator.py, classifier_metrics_generator.py, clt_probability_generator.py, collision_generator.py, complex_number_ops_generator.py, composite_arithmetic_generator.py, conditional_expectation_generator.py, conditional_probability_generator.py, confidence_interval_generator.py, conic_standard_form_generator.py, continuous_distribution_generator.py, coset_generator.py, countability_bijection_generator.py, counting_classics_generator.py, covariance_algebra_generator.py, covariance_correlation_generator.py, cramers_rule_generator.py, cross_section_generator.py, crt_generator.py, curve_analysis_generator.py, de_moivre_generator.py, decimal_div_generator.py, dedekind_cut_generator.py, definite_integral_generator.py, dimensional_analysis_generator.py, discrete_posterior_generator.py, discrete_uniform_bernoulli_generator.py, distribution_of_sum_generator.py, doppler_generator.py, einstein_summation_generator.py, electrostatics_generator.py, embedding_similarity_generator.py, empirical_cdf_generator.py, empirical_rule_generator.py, energy_conservation_generator.py, entropy_change_generator.py, entropy_generator.py, equilibrium_ice_generator.py, error_spotting_generator.py, estimator_bias_enum_generator.py, exact_ode_generator.py, expectation_of_function_generator.py, expected_value_classics_generator.py, exponential_equation_generator.py, exponential_model_generator.py, fermi_estimation_generator.py, fill_in_step_generator.py, finite_difference_generator.py, finite_sigma_algebra_generator.py, fisher_information_generator.py, flops_memory_generator.py, formula_derivation_generator.py, fourier_series_generator.py, fraction_line_plot_generator.py, function_inner_product_generator.py, function_operations_generator.py, game_theory_generator.py, gas_law_generator.py, gas_stoichiometry_generator.py, gauss_bonnet_generator.py, gauss_law_generator.py, gaussian_curvature_generator.py, generating_function_generator.py, geometric_distribution_generator.py, geometric_mean_generator.py, geometric_sequence_generator.py, geometry_area_perimeter_generator.py, geometry_in_context_generator.py, gradient_descent_generator.py, gradient_step_generator.py, grouped_data_generator.py, growth_comparison_generator.py, hamiltonian_generator.py, hawking_generator.py, heat_engine_generator.py, histogram_construct_generator.py, huffman_coding_generator.py, hydrogen_atom_generator.py, hyperbolic_distance_generator.py, hyperbolic_function_generator.py, hypergeometric_generator.py, hypothesis_test_generator.py, index_and_growth_generator.py, inference_setup_generator.py, information_gain_generator.py, integer_puzzle_word_generator.py, integrating_factor_generator.py, interference_generator.py, interpolation_generator.py, invariant_mass_generator.py, inverse_normal_generator.py, jacobi_symbol_generator.py, joint_distribution_generator.py, kernel_ridge_generator.py, kinematics_generator.py, kl_divergence_generator.py, kmeans_step_generator.py, kraft_inequality_generator.py, ladder_operator_generator.py, lagrangian_generator.py, laplace_ivp_generator.py, laurent_series_generator.py, layer_norm_generator.py, lcm_generator.py, least_squares_generator.py, legendre_construction_generator.py, likelihood_ratio_test_generator.py, limit_evaluation_generator.py, linear_model_word_generator.py, linear_simple_generator.py, linear_transform_effect_generator.py, linearity_of_expectation_generator.py, log_conversion_generator.py, logistic_growth_generator.py, long_division_generator.py, lr_schedule_generator.py, magnetism_generator.py, magnitude_comparison_generator.py, manual_square_root_generator.py, markov_chain_generator.py, martingale_check_generator.py, matrix_inverse_generator.py, matrix_norm_generator.py, mean_adjustment_generator.py, mean_value_theorem_generator.py, measurement_uncertainty_generator.py, mental_strategy_generator.py, method_discrimination_generator.py, method_of_moments_generator.py, midpoint_generator.py, missing_information_generator.py, mixture_generator.py, mle_generator.py, modular_inverse_generator.py, money_life_generator.py, monte_carlo_arithmetic_generator.py, motion_word_generator.py, mse_decomposition_generator.py, multi_state_markov_generator.py, multi_step_unit_conversion_generator.py, multinomial_probability_generator.py, naive_bayes_generator.py, named_distribution_generator.py, natural_units_generator.py, negative_binomial_generator.py, nets_surface_area_generator.py, newton_raphson_generator.py, newtons_laws_generator.py, npv_irr_generator.py, ode_substitution_generator.py, optics_generator.py, optimization_generator.py, optimization_in_context_generator.py, or_formula_generator.py, orbital_mechanics_generator.py, order_of_operations_generator.py, order_statistics_generator.py, p_value_generator.py, parabola_features_generator.py, param_count_generator.py, parametric_calculus_generator.py, particle_in_box_generator.py, partition_function_generator.py, pca_generator.py, percent_chain_generator.py, percent_problem_generator.py, percentile_generator.py, permutation_combination_generator.py, perplexity_generator.py, pgf_generator.py, physics_formula_generator.py, planck_units_generator.py, plausibility_critic_generator.py, poisson_process_generator.py, polar_parametric_generator.py, polya_urn_generator.py, population_sample_generator.py, primality_test_generator.py, probability_critic_generator.py, probability_inequality_generator.py, probability_measure_generator.py, projectile_motion_generator.py, proportion_word_problem_generator.py, proportional_relationship_generator.py, quadratic_residue_generator.py, quadratic_word_generator.py, qualitative_reasoning_generator.py, quantization_generator.py, quantum_formula_generator.py, radical_rationalize_generator.py, random_walk_generator.py, rate_conversion_generator.py, rate_of_change_interpret_generator.py, ratio_table_generator.py, recurrence_generator.py, regression_generator.py, regular_polygon_area_generator.py, relativistic_energy_generator.py, repeating_decimal_generator.py, representation_translation_generator.py, riemann_sum_generator.py, riemann_tensor_generator.py, right_triangle_trig_generator.py, rotational_dynamics_generator.py, round_solids_generator.py, routh_hurwitz_generator.py, runge_kutta_generator.py, running_coupling_generator.py, rv_transform_generator.py, sampling_distribution_enum_generator.py, scaling_law_generator.py, scatter_plot_describe_generator.py, scenario_generator.py, schwarzschild_generator.py, second_order_ode_generator.py, segment_partition_generator.py, separable_pde_generator.py, series_convergence_generator.py, series_solution_generator.py, set_counting_generator.py, shm_generator.py, similar_triangles_generator.py, simplex_generator.py, sinusoid_features_generator.py, slope_inference_generator.py, slope_two_points_generator.py, softmax_gradient_generator.py, solution_chem_generator.py, spatial_description_generator.py, special_relativity_generator.py, special_right_triangle_generator.py, spherical_excess_generator.py, spherical_triangle_generator.py, spin_half_generator.py, square_cube_law_generator.py, standard_deviation_generator.py, standing_wave_generator.py, stars_and_bars_generator.py, statics_generator.py, stereographic_generator.py, stoichiometry_generator.py, study_design_generator.py, svm_margin_generator.py, systems_word_generator.py, t_interval_generator.py, taylor_series_generator.py, telescoping_generator.py, temperature_conversion_generator.py, tip_bill_split_generator.py, totient_generator.py, transient_circuit_generator.py, triangle_area_sas_generator.py, triangle_solve_generator.py, trig_identity_eval_generator.py, trig_six_functions_generator.py, two_sample_test_generator.py, two_way_table_generator.py, type_error_power_generator.py, u_substitution_generator.py, undetermined_coeff_generator.py, unit_conversion_generator.py, unit_rate_generator.py, variation_parameters_generator.py, vector_ops_generator.py, wavefunction_generator.py, weighted_mean_generator.py, work_rate_generator.py, young_tableaux_generator.py, z_score_generator.py |
| `DALEMBERT` | 1 | `DALEMBERT\|u=(f(x-ct)+f(x+ct))/2` | separable_pde_generator.py |
| `DATA_PRECISION` | 1 | `DATA_PRECISION\|n/sigma^2` | bayesian_update_generator.py |
| `DATE_ORDINAL` | 2 | `DATE_ORDINAL\|2027-05-03\|740104` | calendar_arithmetic_generator.py |
| `DB_FORMULA` | 1 | `DB_FORMULA\|G_dB=10*log10(P2/P1)` | signal_arithmetic_generator.py |
| `DECIDE` | 2 | `DECIDE\|A+B\|value 76` | decision_under_uncertainty_generator.py, optimization_in_context_generator.py |
| `DECISION` | 2 | `DECISION\|f(x)\|85` | kernel_perceptron_generator.py, svm_margin_generator.py |
| `DECODE` | 2 | `DECODE\|1101010101\|{a, c, g, i, p, v}` | characteristic_vector_generator.py |
| `DEC_ADD_COL` | 3 | `DEC_ADD_COL\|frac_0\|4+0+0\|->4 (carry 0)` | decimal_add_sub_generator.py |
| `DEC_ALIGN` | 2 | `DEC_ALIGN\|37.64\|74.50` | decimal_add_sub_generator.py |
| `DEC_CARRY_FINAL` | 1 | `DEC_CARRY_FINAL\|1` | decimal_add_sub_generator.py |
| `DEC_SHIFT` | 3 | `DEC_SHIFT\|15.9/0.4\|159/4\|1` | decimal_div_generator.py, percent_problem_generator.py |
| `DEC_SUB_COL` | 3 | `DEC_SUB_COL\|frac_0\|0-8 (borrow_in 0)\|->2 (borrow_out 1)` | decimal_add_sub_generator.py |
| `DEC_TO_FRAC` | 2 | `DEC_TO_FRAC\|1.33\|133/100` | fraction_decimal_percent_converter.py |
| `DEC_TO_PERCENT` | 2 | `DEC_TO_PERCENT\|0.8\|80%` | fraction_decimal_percent_converter.py, index_and_growth_generator.py, mixture_generator.py, percent_chain_generator.py, percent_problem_generator.py, risk_communication_generator.py, scenario_generator.py, simple_probability_generator.py, standard_deviation_generator.py, tip_bill_split_generator.py |
| `DEC_TYPE` | 2 | `DEC_TYPE\|83/106\|repeating` | repeating_decimal_generator.py |
| `DEC_VALUE` | 2 | `DEC_VALUE\|83/106\|0.7(8301886792452)` | repeating_decimal_generator.py |
| `DEDUCE` | 3 | `DEDUCE\|Quin\|item = compass\|only solution left` | logic_grid_puzzle_generator.py |
| `DEDUP` | 2 | `DEDUP\|A raw [4, 57, 13, 25, 79, 79]\|{4, 13, 25, 57, 79}` | set_membership_subset_generator.py |
| `DEFINE_VAR` | 2 | `DEFINE_VAR\|a\|tens digit` | integer_puzzle_word_generator.py, linear_model_word_generator.py, systems_word_generator.py |
| `DEGREE` | 2, 3 | `DEGREE\|A\|B, D\|2` | euler_circuit_generator.py, graph_counting_generator.py |
| `DEGREE_COMPARE` | 2 | `DEGREE_COMPARE\|deg num = 1 < deg den = 2\|y = 0` | limit_evaluation_generator.py, rational_function_features_generator.py, series_convergence_generator.py |
| `DEGREE_SEQUENCE` | 1 | `DEGREE_SEQUENCE\|2, 2, 2, 0` | graph_counting_generator.py |
| `DELTA_VALUE` | 2 | `DELTA_VALUE\|delta_22\|1` | index_gymnastics_generator.py |
| `DEMOIVRE_POWER` | 1 | `DEMOIVRE_POWER\|64 cis(0 deg)` | de_moivre_generator.py |
| `DEMOIVRE_SETUP` | 2, 4 | `DEMOIVRE_SETUP\|arbitrary_roots\|R=81\|theta=180 deg\|n=4` | de_moivre_generator.py |
| `DENSITY` | 2 | `DENSITY\|f_X(x)\|1/12` | rv_transform_generator.py |
| `DENSITY_MATRIX` | 1 | `DENSITY_MATRIX\|rho=[[16/19,0],[0,3/19]]` | density_matrix_generator.py |
| `DENSITY_SETUP` | 2, 3 | `DENSITY_SETUP\|state=Schmidt\|psi=(sqrt(18)ket00 + sqrt(13)ket11)/sqrt(31)` | density_matrix_generator.py, partial_trace_generator.py |
| `DEPTH` | 1, 2 | `DEPTH\|3` | wff_parsing_generator.py |
| `DEQUANT_VALUE` | 2 | `DEQUANT_VALUE\|1\|27/20` | quantization_generator.py |
| `DERANGE_PROB` | 2 | `DERANGE_PROB\|D_5/5!\|44/120` | derangement_generator.py |
| `DERANGE_ROW` | 2 | `DERANGE_ROW\|0\|1` | expected_value_classics_generator.py |
| `DERANGE_SETUP` | 2 | `DERANGE_SETUP\|n = 5\|no item fixed` | derangement_generator.py |
| `DERANGE_VALUE` | 2 | `DERANGE_VALUE\|D_2\|1` | derangement_generator.py |
| `DERIV` | 2, 3 | `DERIV\|d_r g_thetatheta = 2r\|at r=71\|142` | christoffel_generator.py, gaussian_curvature_generator.py, riemann_tensor_generator.py |
| `DERIVATIVE` | 1, 2 | `DERIVATIVE\|g'(x)\|-4/9` | fisher_information_generator.py, fixed_point_generator.py, mgf_generator.py, mle_generator.py |
| `DERIVE` | 2 | `DERIVE\|43 pairs\|each sums to 87` | formula_derivation_generator.py |
| `DERIVED` | 2 | `DERIVED\|C5\|□` | resolution_proof_generator.py |
| `DERIV_FORM` | 2 | `DERIV_FORM\|y'\|(C2 - 2(C1 + C2x))e^(-2x)` | second_order_ode_generator.py, undetermined_coeff_generator.py, variation_parameters_generator.py |
| `DERIV_RULE` | 2 | `DERIV_RULE\|power rule\|d/dx of c·x^n = c·n·x^(n-1)` | chain_rule_generator.py, derivative_power_rule_generator.py, derivative_product_quotient_generator.py, derivative_transcendental_generator.py, lhopital_generator.py, linear_approx_generator.py, log_diff_higher_order_generator.py, multivar_chain_rule_generator.py |
| `DERIV_SERIES` | 2 | `DERIV_SERIES\|y'\|sum (n+1)a_(n+1)x^n` | series_solution_generator.py |
| `DERIV_SETUP` | 2 | `DERIV_SETUP\|f(x) = 2x^5 + 3x^2 + 7x + 6\|f'(x)` | chain_rule_generator.py, derivative_power_rule_generator.py, derivative_product_quotient_generator.py, derivative_transcendental_generator.py, log_diff_higher_order_generator.py, tangent_line_generator.py |
| `DESIGN_CUE` | 2 | `DESIGN_CUE\|"gave half the group"\|experiment` | study_design_generator.py |
| `DESIGN_MATRIX` | 2 | `DESIGN_MATRIX\|X = [[1, -1], [1, 0], [1, 1]]\|y = [15, 11, 13]` | least_squares_generator.py |
| `DET` | 2 | `DET\|K\|-70` | kernel_ridge_generator.py, kernel_validity_generator.py |
| `DET2` | 2 | `DET2\|ad - bc\|-4` | ode_system_generator.py |
| `DET_FORMULA` | 1 | `DET_FORMULA\|det = a11·M11 - a12·M12 + a13·M13` | cramers_rule_generator.py, determinant_generator.py, matrix_inverse_generator.py |
| `DEV_ROW` | 3 | `DEV_ROW\|57\|-6\|36` | anova_generator.py, estimator_bias_enum_generator.py, mle_generator.py, slope_inference_generator.py, standard_deviation_generator.py, t_interval_generator.py |
| `DFA_ACCEPT` | 1 | `DFA_ACCEPT\|q2` | dfa_minimization_generator.py, dfa_simulation_generator.py |
| `DFA_INPUT` | 1 | `DFA_INPUT\|1101` | dfa_simulation_generator.py |
| `DFA_MIN_SETUP` | 3 | `DFA_MIN_SETUP\|states A, B, C\|alphabet 0, 1\|start A` | dfa_minimization_generator.py |
| `DFA_MIN_TRANSITION` | 3 | `DFA_MIN_TRANSITION\|A\|0\|A` | dfa_minimization_generator.py |
| `DFA_READ` | 2 | `DFA_READ\|pos 1\|1` | dfa_simulation_generator.py |
| `DFA_SETUP` | 3 | `DFA_SETUP\|states q0, q1, q2\|alphabet 0, 1\|start q0` | dfa_simulation_generator.py |
| `DFA_STATE` | 2 | `DFA_STATE\|start\|q0` | dfa_simulation_generator.py |
| `DFA_STEP` | 3 | `DFA_STEP\|q0\|1\|q1` | dfa_simulation_generator.py |
| `DFA_TRANSITION` | 3 | `DFA_TRANSITION\|q0\|0\|q0` | dfa_simulation_generator.py |
| `DFS_EDGE` | 2 | `DFS_EDGE\|E->C\|tree` | graph_traversal_generator.py |
| `DFT_BIN` | 1 | `DFT_BIN\|X0=x0+x1+x2+x3` | dft_generator.py |
| `DFT_SETUP` | 2 | `DFT_SETUP\|N=4\|x=[8,7,4,-3]` | dft_generator.py |
| `DH_PUBLIC` | 2 | `DH_PUBLIC\|Alice\|17` | diffie_hellman_generator.py |
| `DH_SECRET` | 2 | `DH_SECRET\|Alice\|21` | diffie_hellman_generator.py |
| `DH_SETUP` | 2 | `DH_SETUP\|p=29\|g=14` | diffie_hellman_generator.py |
| `DH_SHARED` | 2 | `DH_SHARED\|Alice\|1` | diffie_hellman_generator.py |
| `DIAG` | 2 | `DIAG\|row 1\|7` | cantor_diagonal_generator.py |
| `DIAGONAL` | 3 | `DIAGONAL\|w=149\|start=11175\|offset=68` | cantor_pairing_generator.py |
| `DIAG_FORM` | 3 | `DIAG_FORM\|P = [[1, 2], [3, 7]]\|D = [[-3, 0], [0, -2]]\|P^-1 = [[7, -2], [-3, 1]]` | diagonalization_generator.py, matrix_exponential_generator.py |
| `DIFF_ROW` | 2 | `DIFF_ROW\|Delta y\|[-2, -26, -50]` | finite_difference_generator.py |
| `DIFF_SETUP` | 3 | `DIFF_SETUP\|f(x,y) = x^2 + y^2 - 2*x + 2*y\|point (-3, -3)\|dx=1/4, dy=1/4` | multivar_chain_rule_generator.py |
| `DIFF_SUM` | 3 | `DIFF_SUM\|f_x*dx + f_y*dy\|(-8)*1/4 + (-4)*1/4\|-3` | multivar_chain_rule_generator.py |
| `DIGIT_MAP` | 2 | `DIGIT_MAP\|make\|0–2 (3 of 10 digits)` | random_digit_simulation_generator.py |
| `DIGIT_PICK` | 2, 3 | `DIGIT_PICK\|72\|reject\|> 40` | study_design_generator.py |
| `DIGIT_SCAN` | 3 | `DIGIT_SCAN\|81095\|makes 2\|no` | random_digit_simulation_generator.py |
| `DIJKSTRA_INIT` | 2 | `DIJKSTRA_INIT\|start B\|A=inf, B=0, C=inf, D=inf` | dijkstra_generator.py |
| `DIM` | 2 | `DIM\|2*2+1\|5` | casimir_generator.py |
| `DIRECTION` | 3 | `DIRECTION\|result after doubling\|multiplies by 8\|216 m³ → 1728 m³` | qualitative_reasoning_generator.py |
| `DIRECTRIX` | 1 | `DIRECTRIX\|x = 3` | parabola_features_generator.py |
| `DISC` | 2, 3 | `DISC\|7056\|4352\|2704` | complex_quadratic_generator.py, discriminant_generator.py, polynomial_zeros_generator.py, quadratic_generator.py |
| `DISCRIMINATE` | 3 | `DISCRIMINATE\|A\|additive\|fixed amount each round` | method_discrimination_generator.py |
| `DISC_CLASSIFY` | 2 | `DISC_CLASSIFY\|169 > 0\|two real solutions` | complex_quadratic_generator.py, discriminant_generator.py, polynomial_zeros_generator.py |
| `DIST` | 3 | `DIST\|2\|2x+3\|4x+6` | derivative_limit_def_generator.py, derivative_product_quotient_generator.py, equation_from_two_points_generator.py, function_composition_generator.py, parallel_perpendicular_line_generator.py, point_slope_generator.py, polar_parametric_generator.py, radical_multiply_generator.py, radical_rationalize_generator.py, rational_expr_add_sub_generator.py, recursive_explicit_generator.py, simplify_expression_generator.py, solid_revolution_generator.py, special_solution_equation_generator.py, tangent_line_generator.py |
| `DIST2` | 2, 3 | `DIST2\|P1\|C1\|10` | embedding_similarity_generator.py, kernel_evaluation_generator.py, kmeans_step_generator.py |
| `DIST_COMBINE` | 1 | `DIST_COMBINE\|24y - 65 = -17` | systems_substitution_generator.py |
| `DIST_ENTRY` | 3 | `DIST_ENTRY\|state 1\|sum incoming flow\|181/540` | multi_state_markov_generator.py |
| `DIST_FORMULA` | 1 | `DIST_FORMULA\|d = √((x2 - x1)^2 + (y2 - y1)^2)` | complex_locus_generator.py, distance_formula_generator.py, hypercube_counting_generator.py |
| `DIST_ROW` | 3 | `DIST_ROW\|15\|1/9\|1/9` | sampling_distribution_enum_generator.py |
| `DIST_RULE` | 1, 2 | `DIST_RULE\|F_M(k)=F_X(k)F_Y(k)` | distribution_of_sum_generator.py |
| `DIST_SETUP` | 2, 3 | `DIST_SETUP\|Bernoulli\|p = 2/29` | discrete_uniform_bernoulli_generator.py, named_distribution_generator.py, pmf_cdf_quantile_generator.py |
| `DIST_TABLE` | 2 | `DIST_TABLE\|visited B\|A=8, B=0, C=6, D=3` | dijkstra_generator.py |
| `DIST_TERM` | 2 | `DIST_TERM\|3x\|- 9x^3 + 9x^2 + 6x` | multiplying_polynomials_generator.py |
| `DIVIDE_EQ` | 2 | `DIVIDE_EQ\|divide by y^2\|y^(-2)dy/dx + 2y^(-1) = 4` | ode_substitution_generator.py |
| `DIVMOD` | 3, 4 | `DIVMOD\|2218\|16\|138\|r=10` | base_conversion_generator.py, induction_verify_generator.py, recursive_definition_unfold_generator.py |
| `DIV_CHECK` | 3 | `DIV_CHECK\|29\|2\|remainder 1` | conditional_forms_generator.py, counterexample_search_generator.py, divisibility_classification_generator.py, logical_connective_eval_generator.py, set_builder_roster_generator.py |
| `DIV_COEFF` | 1, 3 | `DIV_COEFF\|13\|7\|x=13/7` | integer_puzzle_word_generator.py, linear_complex_generator.py, systems_word_generator.py |
| `DIV_SETUP` | 2 | `DIV_SETUP\|159\|4` | decimal_div_generator.py, percent_problem_generator.py |
| `DIV_SUM` | 3 | `DIV_SUM\|P_x + Q_y\|6 - 1\|5` | div_curl_generator.py |
| `DIV_TERM` | 3 | `DIV_TERM\|16y^2\|2\|8y^2` | factor_gcf_generator.py, finite_field_generator.py, polynomial_long_division_generator.py |
| `DNF_FORM` | 1 | `DNF_FORM\|(NOT A AND NOT B AND NOT C) OR (NOT A AND B AND NOT C) OR (A AND NOT B AND NOT C) OR (A AND NOT B AND C) OR (A AND B AND NOT C)` | boolean_algebra_generator.py |
| `DOMAIN` | 1, 2 | `DOMAIN\|x = 23..32\|{23, 24, 25, 26, 27, 28, 29, 30, 31, 32}` | quantifier_finite_domain_generator.py, relation_operations_generator.py, set_builder_roster_generator.py |
| `DOMAIN_COND` | 2 | `DOMAIN_COND\|radicand ≥ 0\|x + 5 ≥ 0` | domain_range_generator.py |
| `DOMAIN_NOTE` | 2 | `DOMAIN_NOTE\|x ≠ 0\|denominator cannot be zero` | domain_range_generator.py, log_equation_generator.py, logistic_growth_generator.py, probability_addition_rule_generator.py, rational_equation_generator.py, unit_circle_generator.py |
| `DOMINANT` | 2 | `DOMINANT\|2^n\|n = 15 through 35` | qualitative_reasoning_generator.py |
| `DOPPLER_FORMULA` | 1 | `DOPPLER_FORMULA\|f_obs=f*sqrt((1+beta)/(1-beta))` | doppler_generator.py |
| `DOPPLER_SETUP` | 3 | `DOPPLER_SETUP\|relativistic_approach\|f=801\|beta=40/41` | doppler_generator.py |
| `DOT` | 2, 3 | `DOT\|(10, 0) · (1, 0)\|10*1 + 0*0\|10` | embedding_similarity_generator.py, feature_map_generator.py, fundamental_form_generator.py, gradient_generator.py, gram_schmidt_generator.py, kernel_evaluation_generator.py, line_integral_generator.py, lll_reduction_generator.py, qr_decomposition_generator.py |
| `DOT4` | 4 | `DOT4\|gamma0gamma0\|(2,3)\|0*0 + -1*0 + 0*-1 + 0*0\|0` | gamma_matrix_generator.py |
| `DOT_FORMULA` | 1 | `DOT_FORMULA\|cos θ = (u·v)/(‖u‖ · ‖v‖)` | dot_product_generator.py |
| `DOT_ROW` | 2 | `DOT_ROW\|5\|1` | dot_plot_generator.py |
| `DOUBLE_SETUP` | 2, 3 | `DOUBLE_SETUP\|integrand x^2 + y^2\|upper-half disk radius 3` | double_integral_generator.py |
| `DPLL_BACKTRACK` | 2 | `DPLL_BACKTRACK\|A\|True` | dpll_trace_generator.py |
| `DPLL_BRANCH` | 3 | `DPLL_BRANCH\|depth 0\|A\|True` | dpll_trace_generator.py |
| `DPLL_CONFLICT` | 1 | `DPLL_CONFLICT\|A=True, B=True` | dpll_trace_generator.py |
| `DPLL_SAT` | 1 | `DPLL_SAT\|A=True, B=True` | dpll_trace_generator.py |
| `DPLL_SETUP` | 3 | `DPLL_SETUP\|(A OR B) AND (A OR not B) AND (not A OR B) AND (not A OR not B)\|variables A, B\|True first` | dpll_trace_generator.py |
| `DPLL_SIMPLIFY` | 2 | `DPLL_SIMPLIFY\|A=True, B=True\|conflict` | dpll_trace_generator.py |
| `DPLL_STATE` | 3 | `DPLL_STATE\|depth 0\|none\|4 clauses left` | dpll_trace_generator.py |
| `DPLL_UNIT` | 2 | `DPLL_UNIT\|(B)\|B=True` | dpll_trace_generator.py |
| `DP_CELL` | 3 | `DP_CELL\|i=1,c=0\|base\|0` | dp_table_generator.py |
| `DP_COINS` | 1 | `DP_COINS\|1, 4, 6` | dp_table_generator.py |
| `DP_ITEMS` | 1 | `DP_ITEMS\|1:(w=5,v=3); 2:(w=2,v=4); 3:(w=3,v=5); 4:(w=3,v=8)` | dp_table_generator.py |
| `DP_ROW` | 2 | `DP_ROW\|i=0\|0, 0, 0, 0, 0, 0, 0, 0` | dp_table_generator.py |
| `DP_SETUP` | 2, 3 | `DP_SETUP\|0/1 knapsack\|capacity 7` | dp_table_generator.py |
| `DRT` | 2 | `DRT\|outward leg\|t = 130/35` | motion_word_generator.py |
| `D_POWER` | 2 | `D_POWER\|D^5\|[[-243, 0], [0, -32]]` | diagonalization_generator.py |
| `E` | 3 | `E\|8\|2\|64` | ac_circuit_generator.py, adam_step_generator.py, angle_defect_generator.py, annuity_generator.py, arc_sector_generator.py, backprop_generator.py, bayes_multiple_hypotheses_generator.py, bec_channel_generator.py, blackbody_generator.py, bond_pricing_generator.py, casimir_force_generator.py, casimir_generator.py, christoffel_generator.py, circle_equation_generator.py, clt_probability_generator.py, complex_division_generator.py, complex_locus_generator.py, conditional_expectation_generator.py, confidence_interval_generator.py, conic_standard_form_generator.py, continuous_distribution_generator.py, counting_to_probability_generator.py, covariance_algebra_generator.py, de_moivre_generator.py, dedekind_cut_generator.py, definite_integral_generator.py, density_matrix_generator.py, derivative_limit_def_generator.py, diagonalization_generator.py, discrete_posterior_generator.py, discrete_uniform_bernoulli_generator.py, distance_formula_generator.py, doppler_generator.py, electrostatics_generator.py, ellipse_features_generator.py, embedding_similarity_generator.py, energy_conservation_generator.py, euler_formula_generator.py, expectation_of_function_generator.py, exponential_equation_generator.py, exponential_model_generator.py, factor_special_forms_generator.py, feature_map_generator.py, finance_generator.py, fisher_information_generator.py, formula_derivation_generator.py, four_vector_generator.py, fractal_iteration_generator.py, function_composition_generator.py, function_evaluation_generator.py, function_operations_generator.py, function_table_generator.py, fundamental_form_generator.py, gauss_bonnet_generator.py, gauss_law_generator.py, gaussian_curvature_generator.py, geometric_mean_generator.py, geometric_sequence_generator.py, geometry_in_context_generator.py, gradient_descent_generator.py, gradient_step_generator.py, growth_comparison_generator.py, hamiltonian_generator.py, hawking_generator.py, hermitian_check_generator.py, huffman_coding_generator.py, hydrogen_atom_generator.py, hyperbola_features_generator.py, hyperbolic_function_generator.py, hypercube_counting_generator.py, index_and_growth_generator.py, invariant_mass_generator.py, kernel_evaluation_generator.py, kmeans_step_generator.py, knn_generator.py, kraft_inequality_generator.py, lagrangian_generator.py, laurent_series_generator.py, layer_norm_generator.py, likelihood_ratio_test_generator.py, limit_evaluation_generator.py, log_conversion_generator.py, log_equation_generator.py, log_properties_generator.py, low_rank_approx_generator.py, magnitude_comparison_generator.py, matrix_group_check_generator.py, matrix_norm_generator.py, mean_value_theorem_generator.py, method_discrimination_generator.py, method_of_moments_generator.py, metric_arc_length_generator.py, mgf_generator.py, minkowski_interval_generator.py, mobius_transform_generator.py, mse_decomposition_generator.py, natural_units_generator.py, npv_irr_generator.py, optimization_generator.py, optimization_in_context_generator.py, or_formula_generator.py, orbital_mechanics_generator.py, order_statistics_generator.py, particle_in_box_generator.py, pca_generator.py, pgf_generator.py, piecewise_evaluation_generator.py, planck_units_generator.py, polar_parametric_generator.py, portfolio_generator.py, probability_inequality_generator.py, projectile_motion_generator.py, pythag_hyp_generator.py, quadratic_word_generator.py, qualitative_reasoning_generator.py, radical_equation_generator.py, radical_multiply_generator.py, radical_rationalize_generator.py, rational_exponent_generator.py, recursive_explicit_generator.py, regression_generator.py, related_rates_generator.py, relativistic_energy_generator.py, remainder_factor_theorem_generator.py, riemann_tensor_generator.py, rotational_dynamics_generator.py, round_solids_generator.py, rv_transform_generator.py, sampling_distribution_enum_generator.py, scenario_generator.py, schwarzschild_generator.py, set_counting_generator.py, set_operations_generator.py, shm_generator.py, significant_figures_generator.py, spherical_excess_generator.py, spin_half_generator.py, standard_deviation_generator.py, stereographic_generator.py, sufficiency_factorization_generator.py, svm_margin_generator.py, t_interval_generator.py, tangent_line_generator.py, taylor_series_generator.py, triangle_solve_generator.py, trig_identity_eval_generator.py, trig_six_functions_generator.py, two_sample_test_generator.py, uncertainty_generator.py, vector_ops_generator.py, wavefunction_generator.py, z_transform_generator.py |
| `ECDF_ROW` | 2 | `ECDF_ROW\|7\|1/4` | empirical_cdf_generator.py |
| `ECDF_SETUP` | 2 | `ECDF_SETUP\|n = 4\|F̂(x) = count(X ≤ x)/n` | empirical_cdf_generator.py |
| `ECDH_SETUP` | 2 | `ECDH_SETUP\|E:y^2=x^3+2x+2 over F_17\|G=(5,1)` | ecdh_generator.py |
| `ECDSA_NONCE` | 2 | `ECDSA_NONCE\|kG=(10,6)\|r=10` | ecdsa_generator.py |
| `ECDSA_PUBLIC` | 1 | `ECDSA_PUBLIC\|Q=dG=(6,3)` | ecdsa_generator.py |
| `ECDSA_SETUP` | 4 | `ECDSA_SETUP\|E/F_17, G=(5,1), n=19\|d=2\|z=7\|k=3` | ecdsa_generator.py |
| `ECDSA_SIGN` | 2 | `ECDSA_SIGN\|s=k^-1(z+rd) mod n\|s=9` | ecdsa_generator.py |
| `ECDSA_VERIFY` | 2 | `ECDSA_VERIFY\|u1=5\|u2=18` | ecdsa_generator.py |
| `EC_ACCUM` | 2 | `EC_ACCUM\|1P\|(10,6)` | elliptic_curve_finite_field_generator.py |
| `EC_ADD` | 1 | `EC_ADD\|(10,6)` | ecdsa_generator.py |
| `EC_IDENTITY` | 2 | `EC_IDENTITY\|O + Q\|(10,6)` | elliptic_curve_finite_field_generator.py |
| `EC_INVERSE` | 3 | `EC_INVERSE\|(2,12)\|(2,7)\|O` | elliptic_curve_finite_field_generator.py |
| `EC_POINT_CHECK` | 3 | `EC_POINT_CHECK\|P\|y^2 mod p = 1\|x^3+ax+b mod p = 1` | elliptic_curve_finite_field_generator.py |
| `EC_PUBLIC` | 2 | `EC_PUBLIC\|A=(3,1)\|B=(3,1)` | ecdh_generator.py |
| `EC_SCALAR` | 2 | `EC_SCALAR\|a=4\|aG=(3,1)` | ecdh_generator.py, ecdsa_generator.py |
| `EC_SCALAR_SETUP` | 2 | `EC_SCALAR_SETUP\|k=4\|P=(10,6)` | elliptic_curve_finite_field_generator.py |
| `EC_SETUP` | 3 | `EC_SETUP\|p=17\|a=2\|b=2` | elliptic_curve_finite_field_generator.py |
| `EC_SHARED` | 2 | `EC_SHARED\|aB=(10,11)\|bA=(10,11)` | ecdh_generator.py |
| `EC_SLOPE` | 2 | `EC_SLOPE\|2P\|5` | elliptic_curve_finite_field_generator.py |
| `EC_SLOPE_FORMULA` | 2 | `EC_SLOPE_FORMULA\|2P\|(3x1^2+a)/(2y1)` | elliptic_curve_finite_field_generator.py |
| `EC_X3` | 2 | `EC_X3\|2P\|7` | elliptic_curve_finite_field_generator.py |
| `EC_Y3` | 2 | `EC_Y3\|2P\|11` | elliptic_curve_finite_field_generator.py |
| `EDGE_CHECK` | 3 | `EDGE_CHECK\|(2619, 2619)\|(m, m)\|absent` | structure_isomorphism_generator.py |
| `EDGE_CHOOSE` | 3 | `EDGE_CHOOSE\|CD\|weight 22\|add D` | mst_generator.py |
| `EDGE_CONSIDER` | 2 | `EDGE_CONSIDER\|CD\|weight 18` | mst_generator.py |
| `EDGE_COUNT` | 2 | `EDGE_COUNT\|m\|3` | euler_circuit_generator.py, graph_counting_generator.py |
| `EDGE_LIST` | 1 | `EDGE_LIST\|AB, AC, BD, CD` | euler_circuit_generator.py |
| `EDGE_WEIGHT` | 2 | `EDGE_WEIGHT\|AB\|8` | dijkstra_generator.py, mst_generator.py |
| `EIGENPAIR` | 2 | `EIGENPAIR\|lambda = -4\|[1, 1]` | ode_system_generator.py |
| `EIGENVALUE` | 1, 2 | `EIGENVALUE\|λ = -4\|p(-4) = 0` | diagonalization_generator.py, eigenvalue_generator.py, matrix_exponential_generator.py, separable_pde_generator.py, svd_generator.py |
| `EIGENVALUES` | 2 | `EIGENVALUES\|A^T A\|4,49` | low_rank_approx_generator.py, matrix_norm_generator.py, pca_generator.py |
| `EIGENVECTOR` | 2 | `EIGENVECTOR\|A + 4I times v = 0\|[1, 0]` | diagonalization_generator.py, eigenvalue_generator.py, matrix_exponential_generator.py, svd_generator.py |
| `EIGEN_CHECK` | 3 | `EIGEN_CHECK\|sigma_y psi\|-1*psi\|lambda=-1` | spin_half_generator.py |
| `EIGEN_MATRIX` | 2 | `EIGEN_MATRIX\|A + 4I\|[[0, -1], [0, 7]]` | eigenvalue_generator.py |
| `EINSTEIN_SETUP` | 2, 3 | `EINSTEIN_SETUP\|contract\|A_ij=[[-1, -4], [-4, -2]]\|B_jk=[[4, 3], [0, -3]]` | einstein_summation_generator.py |
| `ELEC_FORMULA` | 1 | `ELEC_FORMULA\|V=sum(q_i/r_i)` | electrostatics_generator.py |
| `ELEC_SETUP` | 2, 3 | `ELEC_SETUP\|potential_axis\|q1=3, r1=2\|q2=4, r2=10` | electrostatics_generator.py |
| `ELEMENT_ORDER` | 2 | `ELEMENT_ORDER\|rs\|2` | cayley_table_generator.py |
| `ELEMENT_SCAN` | 3 | `ELEMENT_SCAN\|4\|in A=yes\|in B=yes` | set_expression_generator.py, set_membership_subset_generator.py, set_operations_generator.py |
| `ELIMINATE` | 1, 3 | `ELIMINATE\|clue 1\|Quin: drum; Ravi: camera; Cleo: compass; Kira: pencil\|violates clue` | logic_grid_puzzle_generator.py, newtons_laws_generator.py |
| `ELIMINATE_LAMBDA` | 2 | `ELIMINATE_LAMBDA\|f_x = f_y\|3*y = x` | lagrange_multiplier_generator.py |
| `EL_EQUATION` | 1 | `EL_EQUATION\|mL^2*thetaddot+mgL*sin(theta)=0` | lagrangian_generator.py |
| `EL_SOLVE` | 2 | `EL_SOLVE\|thetaddot\|-(5/4)*sin(theta)` | lagrangian_generator.py |
| `EMBED_SETUP` | 1 | `EMBED_SETUP\|A=(-3,4), B=(5,12), C=(4,3)` | embedding_similarity_generator.py |
| `ENDPOINT_COUNT` | 2 | `ENDPOINT_COUNT\|2\|3003` | ballot_reflection_generator.py |
| `ENERGY_FORMULA` | 1 | `ENERGY_FORMULA\|vf^2=vi^2+2W/m` | energy_conservation_generator.py |
| `ENERGY_LEVEL` | 2 | `ENERGY_LEVEL\|E_15=hbar*omega*(n+1/2)\|372` | ladder_operator_generator.py |
| `ENERGY_SETUP` | 3 | `ENERGY_SETUP\|work_energy\|m=21\|vi=3, W=756` | energy_conservation_generator.py |
| `ENERGY_TERM` | 1 | `ENERGY_TERM\|T=1/2*m*L^2*thetadot^2` | lagrangian_generator.py |
| `ENGINE_FORMULA` | 1 | `ENGINE_FORMULA\|W=Qh-Qc` | heat_engine_generator.py |
| `ENGINE_SETUP` | 3 | `ENGINE_SETUP\|engine_efficiency\|Qh=31\|Qc=10` | heat_engine_generator.py |
| `ENQUEUE` | 3 | `ENQUEUE\|A\|from C\|A` | graph_traversal_generator.py |
| `ENTER` | 2 | `ENTER\|x\|most negative reduced cost -6` | simplex_generator.py |
| `ENTROPY_FORMULA` | 1 | `ENTROPY_FORMULA\|DeltaS_mix=-sum n_i ln(x_i)` | entropy_change_generator.py |
| `ENTROPY_SETUP` | 2, 3 | `ENTROPY_SETUP\|eigenvalues=[1/32,1/8,1/16,1/32,1/2,1/8,1/32,1/16,1/64,1/64]\|S=-sum lambda log2(lambda)` | entropy_change_generator.py, entropy_generator.py, huffman_coding_generator.py, information_gain_generator.py, mutual_information_generator.py, von_neumann_entropy_generator.py |
| `ENTROPY_SKIP` | 2 | `ENTROPY_SKIP\|H(X,Y)\|p=0` | mutual_information_generator.py |
| `ENTROPY_TERM` | 4 | `ENTROPY_TERM\|row 0\|p=3/4\|I=0.415\|249/800` | entropy_rate_markov_generator.py |
| `ENTROPY_VALUE` | 2 | `ENTROPY_VALUE\|parent\|0.543875` | information_gain_generator.py |
| `ENTROPY_ZERO` | 2 | `ENTROPY_ZERO\|texture_left\|count=0` | information_gain_generator.py |
| `EPSILON_VALUE` | 2 | `EPSILON_VALUE\|eps_121\|0` | index_gymnastics_generator.py |
| `EPS_CLOSURE` | 2 | `EPS_CLOSURE\|{r2}\|{r2}` | nfa_simulation_generator.py |
| `EQUATE_EXP` | 1 | `EQUATE_EXP\|3x = 2` | exponential_equation_generator.py |
| `EQUILIBRIA` | 2 | `EQUILIBRIA\|f(y) = 0\|y=-10, y=6` | stability_generator.py |
| `EQ_2PT_SETUP` | 2 | `EQ_2PT_SETUP\|(-10, -6)\|(-7, -4)` | equation_from_two_points_generator.py |
| `EQ_OP_BOTH` | 3, 4 | `EQ_OP_BOTH\|add\|9\|x\|25` | absolute_value_equation_generator.py, area_between_curves_generator.py, completing_square_generator.py, curve_analysis_generator.py, error_spotting_generator.py, exponential_equation_generator.py, fill_in_step_generator.py, implicit_diff_generator.py, inverse_function_generator.py, linear_fractional_generator.py, log_diff_higher_order_generator.py, log_equation_generator.py, mean_value_theorem_generator.py, one_step_equation_generator.py, optimization_generator.py, partial_fractions_generator.py, polar_parametric_generator.py, quadratic_factoring_generator.py, quadratic_square_root_generator.py, radical_equation_generator.py, rational_equation_generator.py, related_rates_generator.py, remainder_factor_theorem_generator.py, separable_ode_generator.py, special_solution_equation_generator.py, systems_elimination_generator.py, systems_substitution_generator.py, trig_equation_generator.py, two_step_equation_generator.py |
| `EQ_OP_NOTE` | 3 | `EQ_OP_NOTE\|subtract\|b\|from both sides` | equation_from_two_points_generator.py, literal_equation_generator.py, parallel_perpendicular_line_generator.py, point_slope_generator.py, standard_form_conversion_generator.py |
| `EQ_RESULT` | 2 | `EQ_RESULT\|x\|25` | completing_square_generator.py, error_spotting_generator.py, fill_in_step_generator.py, linear_fractional_generator.py, linear_simple_generator.py, one_step_equation_generator.py, quadratic_factoring_generator.py, quadratic_square_root_generator.py, radical_equation_generator.py, rational_equation_generator.py, special_solution_equation_generator.py, two_step_equation_generator.py |
| `EQ_SETUP` | 1, 2 | `EQ_SETUP\|x = 2*20` | area_between_curves_generator.py, completing_square_generator.py, complex_quadratic_generator.py, cramers_rule_generator.py, discriminant_generator.py, error_spotting_generator.py, exponential_equation_generator.py, fill_in_step_generator.py, linear_fractional_generator.py, literal_equation_generator.py, log_equation_generator.py, one_step_equation_generator.py, polynomial_zeros_generator.py, proportion_word_problem_generator.py, proportional_relationship_generator.py, quadratic_factoring_generator.py, quadratic_generator.py, quadratic_square_root_generator.py, radical_equation_generator.py, rational_equation_generator.py, remainder_factor_theorem_generator.py, special_solution_equation_generator.py, standard_form_conversion_generator.py, trig_equation_generator.py, two_step_equation_generator.py |
| `EQ_SIMPLIFY` | 1 | `EQ_SIMPLIFY\|3x = 21` | error_spotting_generator.py, fill_in_step_generator.py, linear_fractional_generator.py, two_step_equation_generator.py |
| `ERROR_TYPE` | 2 | `ERROR_TYPE\|failing to conclude μ ≠ 755 when μ ≠ 755\|Type II` | inference_setup_generator.py |
| `ESCAPE_CHECK` | 3 | `ESCAPE_CHECK\|n=1\|norm2=281/16\|escaped` | fractal_iteration_generator.py |
| `ESTIMATE` | 2 | `ESTIMATE\|round the base before applying the percent\|$100.00` | assumption_check_generator.py, fermi_estimation_generator.py, long_division_generator.py, magnitude_comparison_generator.py, missing_information_generator.py, multi_digit_multiplication_generator.py, rounding_effect_generator.py |
| `ESTIMATE_CHECK` | 3 | `ESTIMATE_CHECK\|$100.00\|$111.35\|$111.35 ≈ $100.00 ✓` | assumption_check_generator.py, fermi_estimation_generator.py, long_division_generator.py, magnitude_comparison_generator.py, missing_information_generator.py, multi_digit_multiplication_generator.py, rounding_effect_generator.py |
| `EUCLID_DIV` | 4 | `EUCLID_DIV\|354\|180\|1\|174` | continued_fraction_generator.py, extended_euclid_generator.py, modular_inverse_generator.py, rsa_generator.py |
| `EULER_BACKTRACK` | 3 | `EULER_BACKTRACK\|A\|route suffix A\|stack A-B-D-C` | euler_circuit_generator.py |
| `EULER_CRITERION` | 2 | `EULER_CRITERION\|14^5 mod 11\|1` | quadratic_residue_generator.py |
| `EULER_FORMULA` | 1 | `EULER_FORMULA\|V - E + F = 2` | euler_characteristic_generator.py, euler_formula_generator.py |
| `EULER_NOTE` | 2 | `EULER_NOTE\|0\|the torus has a hole: χ = 0, not 2` | euler_characteristic_generator.py |
| `EULER_ROUTE` | 2 | `EULER_ROUTE\|A-B-D-C-A\|uses 4 edges` | euler_circuit_generator.py |
| `EULER_SETUP` | 2, 3 | `EULER_SETUP\|convex polyhedron: V = 5, E = 8\|F` | euler_characteristic_generator.py, euler_formula_generator.py |
| `EULER_STACK` | 2 | `EULER_STACK\|initial\|A` | euler_circuit_generator.py |
| `EULER_START` | 2 | `EULER_START\|A\|alphabetically first vertex` | euler_circuit_generator.py |
| `EULER_TRAVERSE` | 3 | `EULER_TRAVERSE\|A->B\|AB\|stack A-B` | euler_circuit_generator.py |
| `EVAL` | 1, 2, 3 | `EVAL\|f(-5)\|20` | anova_generator.py, arc_length_generator.py, area_between_curves_generator.py, circle_equation_generator.py, complex_division_generator.py, composite_arithmetic_generator.py, conic_standard_form_generator.py, covariance_correlation_generator.py, cramers_rule_generator.py, definite_integral_generator.py, derivative_limit_def_generator.py, determinant_generator.py, dot_product_generator.py, ellipse_features_generator.py, euler_method_generator.py, exact_ode_generator.py, five_number_summary_generator.py, function_composition_generator.py, function_operations_generator.py, horner_evaluation_generator.py, hyperbola_features_generator.py, improper_integral_generator.py, lagrange_multiplier_generator.py, legendre_construction_generator.py, limit_evaluation_generator.py, line_integral_generator.py, linear_approx_generator.py, log_conversion_generator.py, log_properties_generator.py, matrix_inverse_generator.py, mean_value_theorem_generator.py, ode_substitution_generator.py, parabola_features_generator.py, parametric_calculus_generator.py, partial_fractions_generator.py, power_series_generator.py, recursive_explicit_generator.py, regular_polygon_area_generator.py, related_rates_generator.py, remainder_factor_theorem_generator.py, riemann_sum_generator.py, row_reduction_generator.py, runge_kutta_generator.py, solid_revolution_generator.py, standard_deviation_generator.py, tangent_line_generator.py, taylor_series_generator.py, triangle_solve_generator.py, trig_equation_generator.py, trig_identity_eval_generator.py, trig_six_functions_generator.py, vector_ops_generator.py |
| `EVAL_AT_ZERO` | 2 | `EVAL_AT_ZERO\|e^0=1\|e^(2*0)=1` | mgf_generator.py |
| `EVAL_PARTIAL` | 3 | `EVAL_PARTIAL\|f_x\|10*1 + 1\|11` | gradient_generator.py, multivar_chain_rule_generator.py |
| `EVAL_SUB` | 3 | `EVAL_SUB\|p=T, q=T\|formula: p ∨ p\|T` | set_identity_membership_table_generator.py, truth_table_generator.py |
| `EVENT` | 2, 3 | `EVENT\|A\|{6700, 6702, 6704, 6706, 6708, 6710, 6712, 6714, 6716, 6718, 6720, 6722, 6724}\|13` | complement_probability_generator.py, discrete_uniform_bernoulli_generator.py, finite_sigma_algebra_generator.py, fundamental_counting_principle_generator.py, independence_check_generator.py, probability_axioms_finite_generator.py, sample_space_list_generator.py, simple_probability_generator.py |
| `EV_FORMULA` | 1, 2 | `EV_FORMULA\|E[I] = P(I=1)\|1/13` | discrete_uniform_bernoulli_generator.py, expectation_of_function_generator.py, expected_value_generator.py |
| `EV_SETUP` | 2 | `EV_SETUP\|P(X=7) = 1/4; P(X=0) = 1/4; P(X=1) = 1/2\|Var(X)` | expected_value_generator.py |
| `EXACT_MATCH` | 2 | `EXACT_MATCH\|F_y = N\|4*x + g'(y) = 4*x + 4*y + 1` | exact_ode_generator.py |
| `EXPAND` | 1, 2 | `EXPAND\|ez\|4qb + 2q + 2b + 1` | complex_locus_generator.py, direct_proof_algebra_generator.py, mobius_transform_generator.py, zf_axiom_identify_generator.py |
| `EXPECTATION` | 3 | `EXPECTATION\|E[X]=23/49\|E[Y]=23/49\|E[XY]=759/4802` | joint_distribution_generator.py |
| `EXPECTED_COST` | 3 | `EXPECTED_COST\|buy now\|110\|110` | decision_under_uncertainty_generator.py |
| `EXPECTED_LOSS` | 2 | `EXPECTED_LOSS\|5% × 7300\|365` | decision_under_uncertainty_generator.py |
| `EXPECTED_PAYOFF` | 1 | `EXPECTED_PAYOFF\|row1 against q` | game_theory_generator.py |
| `EXP_APPLY` | 2 | `EXP_APPLY\|x(t) = e^(At)x(0)\|x(0) = [-6, 5]` | matrix_exponential_generator.py |
| `EXP_CELL` | 2, 3 | `EXP_CELL\|r1c1\|(20·40)/100\|8` | chi_square_generator.py |
| `EXP_DIAG` | 2 | `EXP_DIAG\|e^(Dt)\|[[e^(-6t), 0], [0, e^t]]` | matrix_exponential_generator.py |
| `EXP_ENTRY` | 3 | `EXP_ENTRY\|(1,1)\|e^t\|e^t` | matrix_exponential_generator.py |
| `EXP_EXPAND` | 1 | `EXP_EXPAND\|(-85) × (-85)` | exponent_generator.py |
| `EXP_FORM` | 1 | `EXP_FORM\|e^(At) = P*e^(Dt)*P^-1` | euler_formula_generator.py, matrix_exponential_generator.py |
| `EXP_PARTIAL` | 3 | `EXP_PARTIAL\|-85\|-85\|7225` | exponent_generator.py |
| `EXP_RULE_APPLY` | 3, 4 | `EXP_RULE_APPLY\|add\|14\|4\|18` | exponent_generator.py, exponent_mixed_rules_generator.py |
| `EXP_RULE_IDENTIFY` | 2 | `EXP_RULE_IDENTIFY\|product_rule\|x^a · x^b = x^(a+b)` | exponent_generator.py, exponent_mixed_rules_generator.py, rational_exponent_generator.py |
| `EXP_RULE_SETUP` | 1 | `EXP_RULE_SETUP\|(xb)^14 · (xb)^4` | exponent_generator.py, exponent_mixed_rules_generator.py, rational_exponent_generator.py |
| `EXP_RULE_SIMPLIFY` | 1 | `EXP_RULE_SIMPLIFY\|(xb)^18` | exponent_generator.py, exponent_mixed_rules_generator.py |
| `EXP_SETUP` | 2 | `EXP_SETUP\|-85\|2` | exponent_generator.py |
| `EXP_SUB` | 3 | `EXP_SUB\|t/tau\|6\|e^-6` | transient_circuit_generator.py |
| `EXP_VALUE` | 2 | `EXP_VALUE\|exp(-z)\|1` | activation_generator.py |
| `EXTRA_MATERIAL` | 3 | `EXTRA_MATERIAL\|10%\|26750\|29425` | spatial_packing_generator.py |
| `EXT_GCD_SETUP` | 2 | `EXT_GCD_SETUP\|354\|180` | extended_euclid_generator.py, modular_inverse_generator.py, rsa_generator.py |
| `F` | 2, 3 | `F\|28/6\|14/3` | complement_probability_generator.py, composite_arithmetic_generator.py, counting_to_probability_generator.py, derangement_generator.py, discrete_uniform_bernoulli_generator.py, fraction_decimal_percent_converter.py, fraction_op_generator.py, fundamental_counting_principle_generator.py, independence_check_generator.py, likelihood_language_generator.py, mixed_number_operation_generator.py, mobius_transform_generator.py, order_of_operations_generator.py, quaternion_generator.py, radical_rationalize_generator.py, random_digit_simulation_generator.py, rational_exponent_generator.py, rational_expr_add_sub_generator.py, repeating_decimal_generator.py, sample_space_list_generator.py, sampling_distribution_enum_generator.py, simple_probability_generator.py, slope_two_points_generator.py, two_way_table_probability_generator.py, venn_probability_generator.py |
| `FACT` | 2 | `FACT\|7\|5040` | counting_to_probability_generator.py, derangement_generator.py, expected_value_classics_generator.py, multinomial_probability_generator.py, named_distribution_generator.py, order_statistics_generator.py, poisson_process_generator.py, young_tableaux_generator.py |
| `FACTOR` | 1, 2 | `FACTOR\|2(2qb + q + b) + 1` | direct_proof_algebra_generator.py, polynomial_inequality_generator.py, second_order_ode_generator.py, transfer_function_generator.py, undetermined_coeff_generator.py, variation_parameters_generator.py |
| `FACTORIAL` | 2 | `FACTORIAL\|3\|6` | sufficiency_factorization_generator.py |
| `FACTOR_FORM` | 2 | `FACTOR_FORM\|72\|2^3 * 3^2` | totient_generator.py |
| `FACTOR_FOUND` | 2 | `FACTOR_FOUND\|2\|3` | totient_generator.py |
| `FACTOR_GROUP` | 3 | `FACTOR_GROUP\|4y^2 + 4y\|4y\|(y + 1)` | conic_standard_form_generator.py, curve_analysis_generator.py, derivative_limit_def_generator.py, factor_grouping_generator.py, factor_trinomial_generator.py |
| `FACTOR_PAIR_GOAL` | 2 | `FACTOR_PAIR_GOAL\|m·n = -27\|m + n = 6` | factor_trinomial_generator.py |
| `FACTOR_SETUP` | 1 | `FACTOR_SETUP\|72` | totient_generator.py |
| `FACT_CHECK` | 3 | `FACT_CHECK\|112\|1\|0` | factors_generator.py |
| `FACT_FORMULA` | 1 | `FACT_FORMULA\|8! = 1·2·3·4·5·6·7·8` | derangement_generator.py, permutation_combination_generator.py |
| `FACT_PAIR` | 2 | `FACT_PAIR\|1\|112` | factors_generator.py |
| `FACT_SETUP` | 2 | `FACT_SETUP\|8!\|expand the factorial` | permutation_combination_generator.py |
| `FACT_VALUE` | 2 | `FACT_VALUE\|11!\|39916800` | stars_and_bars_generator.py |
| `FAIR_PRICE` | 2 | `FAIR_PRICE\|0.4·120 + 0.6·40\|$72.00` | decision_under_uncertainty_generator.py |
| `FCP` | 3 | `FCP\|fonts\|6\|6` | classic_probability_puzzles_generator.py, counting_to_probability_generator.py, fundamental_counting_principle_generator.py |
| `FEATURE_MAP_SETUP` | 3 | `FEATURE_MAP_SETUP\|K(x,z)=(xz+2)^2\|phi(t)=(t^2,2t,2)\|x=3,z=13` | feature_map_generator.py |
| `FEATURE_VECTOR` | 2 | `FEATURE_VECTOR\|phi(x)\|(9,6,2)` | feature_map_generator.py |
| `FEEDBACK` | 1 | `FEEDBACK\|T=G/(1+G)` | transfer_function_generator.py |
| `FENCE_SIDES` | 2 | `FENCE_SIDES\|two widths + one length\|2 × 13 + L = 41` | geometry_in_context_generator.py |
| `FERMAT_SETUP` | 3 | `FERMAT_SETUP\|prime 29\|base 25\|exponent 201` | totient_generator.py |
| `FERMI_FACTOR` | 2 | `FERMI_FACTOR\|households\|1200` | fermi_estimation_generator.py |
| `FERMI_SETUP` | 2 | `FERMI_SETUP\|waste bags\|bags/year` | fermi_estimation_generator.py |
| `FIELD_SETUP` | 2 | `FIELD_SETUP\|GF(2)[x]\|addition is XOR` | finite_field_generator.py |
| `FIND_SLOPE` | 2 | `FIND_SLOPE\|Given slope (m1)\|-1/2` | parallel_perpendicular_line_generator.py |
| `FINITE_DIFF_SETUP` | 3 | `FINITE_DIFF_SETUP\|central_derivative\|x0=-4,h=2\|f-=140,f+=24` | finite_difference_generator.py |
| `FIN_FORMULA` | 1 | `FIN_FORMULA\|interest = balance*monthly rate; principal = payment - interest` | finance_generator.py |
| `FIN_SETUP` | 3 | `FIN_SETUP\|loan balance = 2700\|payment = 165, annual rate = 18%\|one-payment breakdown` | finance_generator.py |
| `FIRSTLAW_FORMULA` | 1 | `FIRSTLAW_FORMULA\|isothermal ideal gas: DeltaU=0` | first_law_generator.py |
| `FIRSTLAW_SETUP` | 3 | `FIRSTLAW_SETUP\|isothermal\|W=-15\|ideal gas` | first_law_generator.py |
| `FIRST_STEP` | 2 | `FIRST_STEP\|t_1=1+P11*t_1+P12*t_2\|t_2=1+P21*t_1+P22*t_2` | multi_state_markov_generator.py |
| `FISHER_INFO` | 1 | `FISHER_INFO\|I(p) = -E[second] = 1/p + 1/(1-p)` | fisher_information_generator.py |
| `FIT` | 3 | `FIT\|upright\|floor(80/25)·floor(45/10)·floor(95/20)\|48` | spatial_packing_generator.py |
| `FIXED_CHECK` | 3 | `FIXED_CHECK\|b\|f(b) = i\|not fixed` | function_properties_generator.py |
| `FIXED_EQ` | 1 | `FIXED_EQ\|z=(az+b)/(cz+d)` | mobius_transform_generator.py |
| `FIXED_POINT` | 1 | `FIXED_POINT\|-4` | mobius_transform_generator.py |
| `FIXED_POINT_SETUP` | 3 | `FIXED_POINT_SETUP\|g(x)=-4/9*x-1/2\|x0=3/2\|iterations=4` | fixed_point_generator.py |
| `FIXED_POINT_UPDATE` | 3 | `FIXED_POINT_UPDATE\|1\|x_0=3/2\|x_1=-7/6` | fixed_point_generator.py |
| `FLAG` | 2 | `FLAG\|2\|(p → p) ∨ (t ∧ q)` | assumption_check_generator.py, error_spotting_generator.py, foundations_critic_generator.py, probability_critic_generator.py |
| `FLIP` | 2 | `FLIP\|1\|7 → 1` | cantor_diagonal_generator.py |
| `FLOOR` | 2, 3 | `FLOOR\|3\|3` | named_distribution_generator.py, rounding_effect_generator.py |
| `FLOOR_DIV` | 3 | `FLOOR_DIV\|6\|2\|3` | algorithm_trace_generator.py |
| `FLOPS_SETUP` | 2 | `FLOPS_SETUP\|rule=2mnk\|m=128,d=256,h=256,o=32` | flops_memory_generator.py |
| `FLUX_SUM` | 2 | `FLUX_SUM\|(0 - 1 + 4)*112\|336` | vector_theorem_generator.py |
| `FOCUS` | 1 | `FOCUS\|(-3, 0)` | ellipse_features_generator.py, hyperbola_features_generator.py, parabola_features_generator.py |
| `FOIL_F` | 2 | `FOIL_F\|First: (-2) * (-7)\|14` | complex_division_generator.py, complex_number_ops_generator.py, multiplying_binomials_generator.py |
| `FOIL_I` | 2 | `FOIL_I\|Inner: (-8i) * (-7)\|56i` | complex_division_generator.py, complex_number_ops_generator.py, multiplying_binomials_generator.py |
| `FOIL_L` | 2 | `FOIL_L\|Last: (-8i) * (-3i)\|24i^2` | complex_division_generator.py, complex_number_ops_generator.py, multiplying_binomials_generator.py |
| `FOIL_O` | 2 | `FOIL_O\|Outer: (-2) * (-3i)\|6i` | complex_division_generator.py, complex_number_ops_generator.py, multiplying_binomials_generator.py |
| `FOIL_SETUP` | 1 | `FOIL_SETUP\|(2 + √6)(5 + √6)` | complex_division_generator.py, complex_number_ops_generator.py, multiplying_binomials_generator.py, radical_multiply_generator.py, trig_identity_verify_generator.py |
| `FOLD` | 2 | `FOLD\|count_c("i")\|0` | peano_arithmetic_generator.py, recursive_definition_unfold_generator.py |
| `FORCE_COMPONENT` | 1 | `FORCE_COMPONENT\|parallel=m*g*sin` | newtons_laws_generator.py |
| `FORCE_EQ` | 1 | `FORCE_EQ\|m*a=parallel-friction` | newtons_laws_generator.py |
| `FORM` | 2 | `FORM\|inverse\|If n ≤ 522, then n ≤ 456.` | conditional_forms_generator.py, zf_axiom_identify_generator.py |
| `FORMULA` | 1, 2 | `FORMULA\|sinh x = (e^x - e^(-x))/2` | collision_generator.py, gaussian_curvature_generator.py, hyperbolic_distance_generator.py, hyperbolic_function_generator.py, or_formula_generator.py, projectile_motion_generator.py, stereographic_generator.py, uncertainty_generator.py |
| `FORM_IDENTIFY` | 2 | `FORM_IDENTIFY\|difference_of_cubes\|a^3 - b^3 = (a - b)(a^2 + ab + b^2)` | completing_square_generator.py, conic_standard_form_generator.py, ellipse_features_generator.py, factor_special_forms_generator.py, hyperbola_features_generator.py, parabola_features_generator.py, radical_multiply_generator.py, radical_rationalize_generator.py, rational_equation_generator.py, rational_exponent_generator.py, rational_expr_add_sub_generator.py, rational_expr_mult_div_generator.py |
| `FOURIER_COEF` | 1 | `FOURIER_COEF\|b_11=6/11` | fourier_series_generator.py |
| `FOURIER_SETUP` | 3 | `FOURIER_SETUP\|sawtooth\|A=3\|n=11` | fourier_series_generator.py |
| `FOUR_VECTOR_SETUP` | 3 | `FOUR_VECTOR_SETUP\|signature=+---\|p=[1,2,2,0]\|q=[-6,-4,-3,0]` | four_vector_generator.py |
| `FPC` | 1 | `FPC\|Var(x̄) = σ²/n × (N-n)/(N-1)` | estimator_bias_enum_generator.py |
| `FRACTAL_SETUP` | 4 | `FRACTAL_SETUP\|julia\|z0=(3/2,-1)\|c=(0,-1)\|N=4` | fractal_iteration_generator.py |
| `FRAC_BUILD` | 2 | `FRAC_BUILD\|17/70\|17/70` | classic_probability_puzzles_generator.py, conditional_probability_generator.py, geometric_probability_generator.py, hypergeometric_generator.py, two_way_table_probability_generator.py |
| `FRAC_REDUCE` | 2 | `FRAC_REDUCE\|31/-14\|-31/14` | angle_measure_generator.py, arc_length_generator.py, arc_sector_generator.py, complex_division_generator.py, frequency_table_generator.py, function_operations_generator.py, hyperbola_features_generator.py, implicit_diff_generator.py, improper_integral_generator.py, probability_addition_rule_generator.py, related_rates_generator.py, right_triangle_trig_generator.py |
| `FRAC_TO_DEC` | 2 | `FRAC_TO_DEC\|54/50\|1.08` | fraction_decimal_percent_converter.py, simple_probability_generator.py |
| `FREQ_SETUP` | 2 | `FREQ_SETUP\|population standard deviation\|n=7` | frequency_table_generator.py, grouped_data_generator.py, standard_deviation_generator.py |
| `FULL_CHANGE` | 2 | `FULL_CHANGE\|(250 − 200)/200\|25%` | statistical_literacy_generator.py |
| `FUNC_OP` | 2 | `FUNC_OP\|(f · g)(-5)\|f(-5) · g(-5)` | function_composition_generator.py, function_operations_generator.py |
| `FUNC_SETUP` | 2 | `FUNC_SETUP\|x: -1, 2, 4, 5, 9; h(x): 12, -9, -6, 23, -13\|h(5)` | domain_range_generator.py, function_composition_generator.py, function_evaluation_generator.py, function_operations_generator.py, function_table_generator.py, inverse_function_generator.py, piecewise_evaluation_generator.py, rational_function_features_generator.py |
| `FUNDAMENTAL_FORM_SETUP` | 3 | `FUNDAMENTAL_FORM_SETUP\|sphere\|R=2\|theta in [0,pi], phi in [60,90]` | fundamental_form_generator.py |
| `F_FORMULA` | 1 | `F_FORMULA\|F = MSB/MSW` | anova_generator.py |
| `GAME_SETUP` | 2 | `GAME_SETUP\|payoffs=(11,2;8,17)\|row player maximizes, column player minimizes` | game_theory_generator.py |
| `GAMMA_SETUP` | 3 | `GAMMA_SETUP\|anticommutator_entry\|gamma0,gamma0\|entry=(2,3)` | gamma_matrix_generator.py |
| `GAS_FORMULA` | 1 | `GAS_FORMULA\|PV=nRT so n=PV/T` | gas_law_generator.py, gas_stoichiometry_generator.py |
| `GAS_SETUP` | 3 | `GAS_SETUP\|ideal_moles\|P=10, V=23\|T=12, R=1` | gas_law_generator.py |
| `GAS_STOICH_SETUP` | 3 | `GAS_STOICH_SETUP\|gas_to_mass\|2 H2 + O2 -> 2 H2O\|gas=H2, target=H2O` | gas_stoichiometry_generator.py |
| `GATE_MATRIX` | 2 | `GATE_MATRIX\|CNOT\|ket00bra00+ket01bra01+ket11bra10+ket10bra11` | quantum_gate_generator.py |
| `GAUSSIAN_CURVATURE_SETUP` | 2, 3 | `GAUSSIAN_CURVATURE_SETUP\|saddle\|z=(9x^2-18y^2)/2\|point=(0,0)` | gaussian_curvature_generator.py |
| `GAUSS_BONNET_SETUP` | 3 | `GAUSS_BONNET_SETUP\|sphere\|R=16\|chi=2` | gauss_bonnet_generator.py |
| `GAUSS_FORMULA` | 1 | `GAUSS_FORMULA\|2*E*A=sigma*A` | gauss_law_generator.py |
| `GAUSS_SETUP` | 3 | `GAUSS_SETUP\|sheet_charge\|sigma=76\|A=20` | gauss_law_generator.py |
| `GCD` | 2 | `GCD\|gcd(44,120)\|4` | derangement_generator.py, pollard_factorization_generator.py |
| `GCD_DIV` | 4 | `GCD_DIV\|5081\|8468\|0\|5081` | rationals_as_pairs_generator.py |
| `GCD_DONE` | 1 | `GCD_DONE\|1` | rationals_as_pairs_generator.py |
| `GCD_RESULT` | 1, 2 | `GCD_RESULT\|1` | lcm_generator.py, modular_inverse_generator.py, permutation_group_generator.py, rsa_generator.py, totient_generator.py |
| `GCD_START` | 2 | `GCD_START\|36\|38` | gcf_generator.py, lcm_generator.py, rationals_as_pairs_generator.py |
| `GCD_STEP` | 3 | `GCD_STEP\|36\|38\|36` | gcf_generator.py, lcm_generator.py |
| `GCF_COEFF` | 2 | `GCF_COEFF\|16, 14\|2` | factor_gcf_generator.py, quadratic_factoring_generator.py, rational_expr_simplify_generator.py |
| `GCF_RESULT` | 1 | `GCF_RESULT\|2` | factor_gcf_generator.py, quadratic_factoring_generator.py, rational_expr_simplify_generator.py |
| `GCF_VAR` | 2 | `GCF_VAR\|y^5, y^3, y^2\|y^2` | factor_gcf_generator.py, quadratic_factoring_generator.py, rational_expr_simplify_generator.py |
| `GD_SETUP` | 3 | `GD_SETUP\|f(x,y)=1/2*(2x^2+1y^2)\|start=(-10,2)\|eta=1/8` | gradient_descent_generator.py |
| `GD_UPDATE` | 3 | `GD_UPDATE\|w_old=(2,1)\|eta=1/7\|w_new=(12/7,-1/7)` | gradient_step_generator.py |
| `GELLMANN_IDENTITY` | 3 | `GELLMANN_IDENTITY\|Tr(lambda_7 lambda_3)\|2 delta_ab\|0` | pauli_algebra_generator.py |
| `GELLMANN_SETUP` | 3 | `GELLMANN_SETUP\|trace\|A=3lambda_7\|B=-lambda_3` | pauli_algebra_generator.py |
| `GENERAL` | 2 | `GENERAL\|a_n\|C1(4)^n + C2(2)^n` | recurrence_generator.py |
| `GENERALIZE` | 2 | `GENERALIZE\|n/2 pairs of (n + 1)\|S = n(n + 1)/2` | formula_derivation_generator.py |
| `GEOMETRIC_FORMULA` | 2 | `GEOMETRIC_FORMULA\|c_n = A*(-1)^n/d^(n+1)\|A=-5, d=-5` | laurent_series_generator.py |
| `GEOM_FORMULA` | 1 | `GEOM_FORMULA\|P(X≤k)=1-q^k` | geometric_distribution_generator.py |
| `GEOM_SETUP` | 2 | `GEOM_SETUP\|p=3/10, q=7/10\|P(X≤4)` | geometric_distribution_generator.py |
| `GEO_PROB_FORMULA` | 1 | `GEO_PROB_FORMULA\|probability = favorable length / total length` | geometric_probability_generator.py |
| `GEO_PROB_SETUP` | 2 | `GEO_PROB_SETUP\|number line from 0 to 24\|lands between 20 and 22` | geometric_probability_generator.py |
| `GEO_SETUP` | 2 | `GEO_SETUP\|right triangle, altitude to hypotenuse; leg = 109 with projection p = 1 on the hypotenuse\|the hypotenuse c` | geometric_mean_generator.py |
| `GF2_XOR` | 3 | `GF2_XOR\|quotient x\|0 xor 1\|1` | finite_field_generator.py |
| `GF_DIV_CHECK` | 3 | `GF_DIV_CHECK\|16 / 3\|not integer\|reject` | generating_function_generator.py |
| `GF_EXPAND` | 2 | `GF_EXPAND\|(1 + x)^3\|sum C(a,i)x^i` | generating_function_generator.py |
| `GF_SETUP` | 2 | `GF_SETUP\|[x^3]\|(1 + x)^3(1 + x)^8` | generating_function_generator.py |
| `GIANT_FACTOR` | 2 | `GIANT_FACTOR\|g^-m mod p\|5` | baby_step_giant_step_generator.py |
| `GIANT_STEP` | 2 | `GIANT_STEP\|i=0\|27` | baby_step_giant_step_generator.py |
| `GLB` | 1 | `GLB\|∅` | partial_order_generator.py |
| `GOAL` | 1 | `GOAL\|show k² is odd` | direct_proof_algebra_generator.py, point_slope_generator.py, standard_form_conversion_generator.py |
| `GODEL_DECODE` | 2 | `GODEL_DECODE\|3, 1, 3\|) p )` | godel_numbering_generator.py |
| `GODEL_TERM` | 2 | `GODEL_TERM\|2^1\|2` | godel_numbering_generator.py |
| `GRAD` | 2 | `GRAD\|1\|-1/2` | softmax_gradient_generator.py |
| `GRADIENT_FORMULA` | 1 | `GRADIENT_FORMULA\|grad=(2x,1y)` | gradient_descent_generator.py, matrix_calculus_generator.py |
| `GRAD_ENTRY` | 2 | `GRAD_ENTRY\|g1\|-4` | matrix_calculus_generator.py |
| `GRAD_RESULT` | 2 | `GRAD_RESULT\|grad g\|(1, 1)` | lagrange_multiplier_generator.py |
| `GRAD_SETUP` | 3 | `GRAD_SETUP\|f(x,y) = 5*x^2 + 3*y^2 + x + 4*y\|point (1, 1)\|gradient` | gradient_generator.py |
| `GRAPH_CHANGE` | 3 | `GRAPH_CHANGE\|9am\|10am\|-3` | graph_interpret_generator.py |
| `GRAPH_DATA` | 2 | `GRAPH_DATA\|bar_chart\|Baseball:2,Basketball:2,Football:7,Soccer:5,Swimming:5,Tennis:5` | graph_interpret_generator.py |
| `GRAPH_MAX` | 2 | `GRAPH_MAX\|Fish\|15` | graph_interpret_generator.py |
| `GRAPH_MAX_CHANGE` | 3 | `GRAPH_MAX_CHANGE\|12pm\|1pm\|-4` | graph_interpret_generator.py |
| `GRAPH_MIN` | 2 | `GRAPH_MIN\|2020\|12` | graph_interpret_generator.py |
| `GRAPH_READ` | 2 | `GRAPH_READ\|Art\|30` | graph_interpret_generator.py |
| `GRAPH_SETUP` | 2 | `GRAPH_SETUP\|vertices A, B, C, D\|edges AB, AD, BD` | dijkstra_generator.py, euler_circuit_generator.py, graph_counting_generator.py, graph_traversal_generator.py |
| `GRASSMANN_RESULT` | 3 | `GRASSMANN_RESULT\|constant=1\|theta=-1\|1 - theta` | grassmann_generator.py |
| `GRASSMANN_SETUP` | 3 | `GRASSMANN_SETUP\|integrate\|expr=-8 + 2theta\|int1=0,inttheta=1` | grassmann_generator.py |
| `GREATEST` | 1 | `GREATEST\|none` | partial_order_generator.py |
| `GREAT_CIRCLE_SETUP` | 3 | `GREAT_CIRCLE_SETUP\|R=4\|A=(0,-60)\|B=(60,-60)` | great_circle_generator.py |
| `GROUP` | 2 | `GROUP\|(4y^2 + 4y)\|(y + 1)` | factor_grouping_generator.py, factor_trinomial_generator.py |
| `GROUP_MULT` | 3 | `GROUP_MULT\|e\|e\|e` | coset_generator.py |
| `GROUP_SETUP` | 2, 3 | `GROUP_SETUP\|D3\|symmetries of a triangle` | cayley_table_generator.py, coset_generator.py, cyclic_group_generator.py |
| `GS_SETUP` | 2 | `GS_SETUP\|vectors [[1, 0, 1], [0, 0, 2], [1, 1, -3]]\|orthogonal basis, not normalized` | gram_schmidt_generator.py |
| `GS_SUBTRACT` | 2 | `GS_SUBTRACT\|remove projection on u1\|[-1, 0, 1]` | gram_schmidt_generator.py, qr_decomposition_generator.py |
| `GS_VECTOR` | 2 | `GS_VECTOR\|u1 = v1\|[1, 0, 1]` | gram_schmidt_generator.py |
| `G_ROW` | 3 | `G_ROW\|x=37\|g = 37\|37 × 1/50 = 37/50` | expectation_of_function_generator.py |
| `HA` | 1 | `HA\|y = 0` | rational_function_features_generator.py |
| `HAMILTON` | 2 | `HAMILTON\|i*i\|-1` | quaternion_generator.py |
| `HAMILTONIAN` | 1 | `HAMILTONIAN\|H=p_theta^2/(2mL^2)+mgL*(1-cos(theta))` | hamiltonian_generator.py |
| `HAMMING_PLACE` | 2 | `HAMMING_PLACE\|positions 1,2,3,4,5,6,7\|p1,p2,d1,p4,d2,d3,d4` | hamming_code_generator.py |
| `HAMMING_RECEIVED` | 1 | `HAMMING_RECEIVED\|r=0010101` | hamming_code_generator.py |
| `HAMMING_SETUP` | 2 | `HAMMING_SETUP\|data=1000\|even parity` | hamming_code_generator.py |
| `HAM_EQ` | 2 | `HAM_EQ\|thetadot=dH/dp_theta\|thetadot=p_theta/50` | hamiltonian_generator.py |
| `HAM_SETUP` | 3 | `HAM_SETUP\|pendulum\|m=2, L=5\|g=10, q=theta` | hamiltonian_generator.py |
| `HARMONIC_NUMBER` | 2 | `HARMONIC_NUMBER\|H_7\|363/140` | expected_value_classics_generator.py |
| `HARMONIC_SETUP` | 1 | `HARMONIC_SETUP\|u=3x^2 - 3y^2 + 3x + 2y` | cauchy_riemann_generator.py |
| `HAWKING_SETUP` | 3 | `HAWKING_SETUP\|entropy\|S_BH=k_B*c^3*A/(4*hbar*G)\|k_B=2,c=4,A=48,hbar=10,G=1` | hawking_generator.py |
| `HESSIAN_DET` | 3 | `HESSIAN_DET\|D = f_xx*f_yy - f_xy^2\|(-2)*(-8) - 1^2\|15` | hessian_classify_generator.py |
| `HESSIAN_SETUP` | 2 | `HESSIAN_SETUP\|f(x,y) = -x^2 - 4*y^2 + x*y + 11*x - 28*y\|find and classify the critical point` | hessian_classify_generator.py |
| `HESSIAN_TEST` | 3 | `HESSIAN_TEST\|D = 15\|f_xx = -2\|local maximum` | hessian_classify_generator.py |
| `HIDDEN_PRE` | 2 | `HIDDEN_PRE\|h1\|z=3` | backprop_generator.py |
| `HIT` | 3 | `HIT\|(1,0)\|1 ≤ 1\|in` | monte_carlo_arithmetic_generator.py |
| `HIT_EQ` | 2 | `HIT_EQ\|t0=1+p00*t0+p01*t1\|t1=1+p10*t0+p11*t1` | markov_chain_generator.py |
| `HMM_SETUP` | 2 | `HMM_SETUP\|states H,L\|observations ABB` | viterbi_generator.py |
| `HMM_START` | 1 | `HMM_START\|H=1/2, L=1/2` | viterbi_generator.py |
| `HOLE` | 1 | `HOLE\|x = 4` | rational_function_features_generator.py |
| `HOM_SOL` | 2 | `HOM_SOL\|y_h\|y_h = C1e^(-2x) + C2e^(3x)` | undetermined_coeff_generator.py, variation_parameters_generator.py |
| `HOOK` | 4 | `HOOK\|(1,1)\|right=4\|below=2\|hook=7` | young_tableaux_generator.py |
| `HORNER_SETUP` | 2 | `HORNER_SETUP\|2x^3 + x^2 - 2x - 1\|x = -1` | horner_evaluation_generator.py |
| `HT_SETUP` | 2 | `HT_SETUP\|H0: p = 0.5; Ha: p ≠ 0.5\|n = 400, 155 successes, critical value = 1.96` | hypothesis_test_generator.py, p_value_generator.py, two_sample_test_generator.py, type_error_power_generator.py |
| `HUFFMAN_FORMULA` | 1 | `HUFFMAN_FORMULA\|L=sum p_i*l_i` | huffman_coding_generator.py |
| `HUFFMAN_MERGE` | 2 | `HUFFMAN_MERGE\|A:1/4 + C:1/4\|AC:1/2` | huffman_coding_generator.py |
| `HUFFMAN_SETUP` | 1 | `HUFFMAN_SETUP\|A=1/4, B=1/2, C=1/4` | huffman_coding_generator.py |
| `HYDROGEN_FORMULA` | 1 | `HYDROGEN_FORMULA\|Delta_E=R_E*(1/n_low^2-1/n_high^2)` | hydrogen_atom_generator.py |
| `HYDROGEN_SETUP` | 3 | `HYDROGEN_SETUP\|transition_energy\|n_low=5, n_high=7\|R_E=4 eV` | hydrogen_atom_generator.py |
| `HYPERBOLIC_DISTANCE_SETUP` | 3 | `HYPERBOLIC_DISTANCE_SETUP\|disk\|P=(0,0)\|Q=(17/33,0)` | hyperbolic_distance_generator.py |
| `HYPERBOLIC_SETUP` | 2 | `HYPERBOLIC_SETUP\|e^x=17/10\|e^(-x)=10/17` | hyperbolic_function_generator.py |
| `HYPERCUBE_FORMULA` | 1 | `HYPERCUBE_FORMULA\|k-faces of the n-cube: C(n,k) · 2^(n-k)` | hypercube_counting_generator.py |
| `HYPERCUBE_SETUP` | 2 | `HYPERCUBE_SETUP\|5-cube\|number of vertices (k = 0)` | hypercube_counting_generator.py |
| `HYPERGEO_FORMULA` | 1 | `HYPERGEO_FORMULA\|P(counts) = product of type combinations/C(N,n)` | hypergeometric_generator.py |
| `HYPERGEO_SETUP` | 2 | `HYPERGEO_SETUP\|N = 8, n = 3\|1 black, 1 silver, 1 gold` | hypergeometric_generator.py |
| `HYPERGEO_TERM` | 2 | `HYPERGEO_TERM\|X = 1\|4/7` | hypergeometric_generator.py |
| `HYP_STATE` | 3 | `HYP_STATE\|H0: μ = 392\|Ha: μ > 392\|right-tailed` | inference_setup_generator.py |
| `I` | 2 | `I\|5/3\|3/5` | fraction_op_generator.py, mixed_number_operation_generator.py, rational_expr_mult_div_generator.py |
| `ICE_ROW` | 2 | `ICE_ROW\|equilibrium\|[A]=3, [B]=4.5` | equilibrium_ice_generator.py |
| `IDENTIFY` | 2 | `IDENTIFY\|order matters\|use P(n, r)` | permutation_combination_generator.py |
| `IDENTITY` | 2 | `IDENTITY\|Vandermonde\|Σ C(3,i)C(8,6-i) = C(11,6)` | counting_classics_generator.py, function_inner_product_generator.py, index_gymnastics_generator.py |
| `IDENTITY_SETUP` | 2 | `IDENTITY_SETUP\|verify: sin^2 β = (1 - cos β)(1 + cos β)\|transform the right side` | trig_identity_verify_generator.py |
| `IDENT_MATCH` | 1 | `IDENT_MATCH\|sin^2 β = sin^2 β` | trig_identity_verify_generator.py |
| `IDENT_SUB` | 1, 2 | `IDENT_SUB\|1 - cos^2 β = sin^2 β` | parametric_calculus_generator.py, trig_identity_verify_generator.py |
| `IE_FORMULA` | 1, 2 | `IE_FORMULA\|count(R or C) = count(R) + count(C) − count(R and C)` | expected_value_classics_generator.py, inclusion_exclusion_generator.py, probability_measure_generator.py, two_way_table_probability_generator.py, venn_probability_generator.py |
| `IE_SETUP` | 2 | `IE_SETUP\|n(A)=21, n(B)=32, n(C)=15\|n(AB)=3, n(AC)=3, n(BC)=8, n(ABC)=2` | inclusion_exclusion_generator.py |
| `IFACTOR` | 2 | `IFACTOR\|mu = e^(∫ 2 dx)\|e^(2x)` | integrating_factor_generator.py, ode_substitution_generator.py |
| `IG_SETUP` | 3 | `IG_SETUP\|parent pos=14, neg=2\|total=16\|splits=texture,region` | information_gain_generator.py |
| `IMAGE` | 2 | `IMAGE\|b\|11` | function_properties_generator.py, mobius_transform_generator.py |
| `IMPLICIT_DIFF` | 2 | `IMPLICIT_DIFF\|d/dx of x^3\|3x^2` | implicit_diff_generator.py, log_diff_higher_order_generator.py, related_rates_generator.py |
| `IMPLICIT_SETUP` | 2 | `IMPLICIT_SETUP\|x^3 + y^3 = 133\|dy/dx` | implicit_diff_generator.py |
| `IMPROPER_TO_MIX` | 2 | `IMPROPER_TO_MIX\|143/12\|11 11/12` | composite_arithmetic_generator.py, mixed_number_operation_generator.py, order_of_operations_generator.py |
| `INDEGREE` | 2 | `INDEGREE\|A\|0` | graph_traversal_generator.py |
| `INDEGREE_UPDATE` | 2 | `INDEGREE_UPDATE\|B\|0` | graph_traversal_generator.py |
| `INDEP_CHECK` | 3 | `INDEP_CHECK\|P(A ∩ B) = 0\|product = 9/400\|no` | independence_check_generator.py, joint_distribution_generator.py |
| `INDEP_FORMULA` | 1 | `INDEP_FORMULA\|independent iff P(A ∩ B) = P(A)·P(B)` | independence_check_generator.py, joint_distribution_generator.py |
| `INDEX` | 3 | `INDEX\|G size 6\|H size 2\|3` | coset_generator.py |
| `INDEX_METRIC` | 3 | `INDEX_METRIC\|lower\|Minkowski\|g_ii=[-1,1,1,1]` | index_raising_generator.py |
| `INDEX_NUMBER` | 2 | `INDEX_NUMBER\|400/100\|4` | index_and_growth_generator.py |
| `INDEX_SETUP` | 3 | `INDEX_SETUP\|c=3\|j=2, k=1\|l=2, m=3` | index_gymnastics_generator.py |
| `INDICATOR` | 2 | `INDICATOR\|I_v = 1 if value v appears\|P(I_v = 1) = 1 − (7/8)^2` | linearity_of_expectation_generator.py |
| `INDUCT_ASSUME` | 1, 2 | `INDUCT_ASSUME\|n = 4a + 5b\|a,b nonnegative` | induction_verify_generator.py |
| `INDUCT_BASE` | 2 | `INDUCT_BASE\|n=12\|12 = 4·3 + 5·0` | induction_verify_generator.py |
| `INDUCT_STEP` | 1, 2 | `INDUCT_STEP\|n → n+4\|n+4 = 4(a+1) + 5b` | induction_verify_generator.py |
| `INEQ_BOUND` | 2 | `INEQ_BOUND\|P(union A_i)\|≤ 6/7` | probability_inequality_generator.py |
| `INEQ_FLIP` | 1 | `INEQ_FLIP\|Multiplying by negative number reverses inequality` | domain_range_generator.py, linear_fractional_generator.py, one_step_inequality_generator.py, two_step_inequality_generator.py |
| `INEQ_FORMULA` | 2 | `INEQ_FORMULA\|Boole union bound\|P(union A_i)≤ΣP(A_i)` | probability_inequality_generator.py |
| `INEQ_OP_ALL` | 3 | `INEQ_OP_ALL\|add\|4\|-2 ≤ 5x ≤ 10` | absolute_value_inequality_generator.py, compound_inequality_generator.py |
| `INEQ_OP_BOTH` | 4 | `INEQ_OP_BOTH\|multiply\|5\|x\|-40` | domain_range_generator.py, linear_fractional_generator.py, one_step_inequality_generator.py, two_step_inequality_generator.py |
| `INEQ_RESULT` | 3 | `INEQ_RESULT\|x\|≤\|-40` | domain_range_generator.py, linear_fractional_generator.py, one_step_inequality_generator.py, two_step_inequality_generator.py |
| `INEQ_SETUP` | 1 | `INEQ_SETUP\|x/5 ≤ -8` | linear_fractional_generator.py, one_step_inequality_generator.py, polynomial_inequality_generator.py, two_step_inequality_generator.py |
| `INEQ_SIMPLIFY` | 1 | `INEQ_SIMPLIFY\|x + 6 ≥ -1` | domain_range_generator.py, linear_fractional_generator.py, two_step_inequality_generator.py |
| `INEX_TERM` | 3 | `INEX_TERM\|0\|1×2^3\|8` | function_properties_generator.py |
| `INFO_GAIN` | 2 | `INFO_GAIN\|texture\|0.13825` | information_gain_generator.py |
| `INFO_SETUP` | 2 | `INFO_SETUP\|p=1/8\|I=-log2(p)` | entropy_generator.py |
| `INFO_TABLE` | 1 | `INFO_TABLE\|1/8=3, 1/4=2, 3/4=0.415, 7/8=0.193, 1=0` | information_gain_generator.py |
| `INFO_VALUE` | 2 | `INFO_VALUE\|p=7/8\|I=0.193` | information_gain_generator.py |
| `INITIAL` | 2 | `INITIAL\|D_0 = 1\|D_1 = 0` | derangement_generator.py |
| `INITIAL_COEFF` | 2 | `INITIAL_COEFF\|a_0\|10440` | series_solution_generator.py |
| `INITIAL_EQ` | 2 | `INITIAL_EQ\|C1 + C2\|-7` | recurrence_generator.py |
| `INITIAL_SYSTEM` | 2 | `INITIAL_SYSTEM\|C1[1, 1] + C2[2, 1]\|[-9, -6]` | ode_system_generator.py |
| `INNER_ANTIDERIV` | 2 | `INNER_ANTIDERIV\|dr\|r^4/4` | double_integral_generator.py, triple_integral_generator.py |
| `INNER_EVAL` | 2, 3 | `INNER_EVAL\|r=0..3\|3^4/4\|81/4` | double_integral_generator.py, triple_integral_generator.py |
| `INNER_PRODUCT` | 2 | `INNER_PRODUCT\|inner(phi,psi)\|-2` | braket_generator.py |
| `INNER_PRODUCT_SETUP` | 3 | `INNER_PRODUCT_SETUP\|interval=[0,2pi]\|f=sin(45x)\|g=sin(26x)` | function_inner_product_generator.py |
| `INSERT_KEY` | 3 | `INSERT_KEY\|pass 1\|24\|index 1` | algorithm_trace_generator.py |
| `INSERT_PLACE` | 2 | `INSERT_PLACE\|index 1\|13, 24, 20, 11, 8, 10` | algorithm_trace_generator.py |
| `INTEGRAL` | 1, 2 | `INTEGRAL\|integral cos(19x) on [0,2pi]\|0` | fourier_series_generator.py, function_inner_product_generator.py, legendre_construction_generator.py |
| `INTEGRAL_SETUP` | 1 | `INTEGRAL_SETUP\|L = integral from 0 to 3pi/4 of 10 dtheta` | metric_arc_length_generator.py |
| `INTEGRATE` | 2 | `INTEGRATE\|v_y = u_x\|v=6xy - 2x + 3y + phi(x)` | cauchy_riemann_generator.py |
| `INTEGRATION_BY_PARTS` | 2 | `INTEGRATION_BY_PARTS\|u=x\|dv=sin(nx)dx` | fourier_series_generator.py |
| `INTEG_RULE` | 2 | `INTEG_RULE\|power rule\|∫ x^n dx = x^(n+1)/(n+1) + C` | antiderivative_generator.py, definite_integral_generator.py, ode_substitution_generator.py, partial_fractions_generator.py, separable_ode_generator.py, solid_revolution_generator.py, u_substitution_generator.py |
| `INTEG_SETUP` | 2 | `INTEG_SETUP\|∫ (16x^3 + 2x) dx\|antiderivative` | antiderivative_generator.py, arc_length_generator.py, definite_integral_generator.py, improper_integral_generator.py, integration_by_parts_generator.py, parametric_calculus_generator.py, partial_fractions_generator.py, u_substitution_generator.py |
| `INTERCEPT_FORMULA` | 1 | `INTERCEPT_FORMULA\|a = ȳ - b·x̄` | regression_generator.py |
| `INTERFERENCE_FORMULA` | 1 | `INTERFERENCE_FORMULA\|d*sin(theta)=m*lambda` | interference_generator.py |
| `INTERFERENCE_SETUP` | 3 | `INTERFERENCE_SETUP\|diffraction_grating\|m=3, lambda=20\|d=88` | interference_generator.py |
| `INTERPRET` | 2 | `INTERPRET\|15\|fixed booking charge` | linear_model_word_generator.py, rate_of_change_interpret_generator.py, representation_translation_generator.py |
| `INTERP_SETUP` | 3 | `INTERP_SETUP\|newton\|points=(-4,-28), (1,-8), (5,-28)\|x=-2` | interpolation_generator.py |
| `INTERVAL` | 2 | `INTERVAL\|length\|[11.5, 12.5]` | measurement_uncertainty_generator.py |
| `INTERVAL_CLASS` | 2 | `INTERVAL_CLASS\|s2=-5\|spacelike` | minkowski_interval_generator.py |
| `INT_ABS` | 2 | `INT_ABS\|7\|7` | integer_operations_generator.py |
| `INT_ALIGN` | 2 | `INT_ALIGN\|30414\|85701` | multi_digit_addition_generator.py, multi_digit_subtraction_generator.py |
| `INT_APPLY_SIGN` | 3 | `INT_APPLY_SIGN\|6\|positive\|6` | integer_operations_generator.py |
| `INT_OP` | 4 | `INT_OP\|-\|7\|1\|6` | integer_operations_generator.py |
| `INT_REWRITE` | 2 | `INT_REWRITE\|-12 - 9\|-12 + (-9)` | integer_operations_generator.py |
| `INT_SIGN_RULE` | 2 | `INT_SIGN_RULE\|different_signs\|Different signs: subtract absolute values, take sign of larger absolute value` | integer_operations_generator.py |
| `INVARIANT` | 3 | `INVARIANT\|sizes\|3\|4` | structure_isomorphism_generator.py |
| `INVERSE_LAPLACE` | 2 | `INVERSE_LAPLACE\|-4/(s + 3)\|-4e^(-3t)` | laplace_ivp_generator.py |
| `INVERSE_MAP` | 2 | `INVERSE_MAP\|x=(u+v)/2\|y=(u-v)/2` | rv_transform_generator.py |
| `INVERSE_METRIC` | 2 | `INVERSE_METRIC\|g^rr=1\|g^thetatheta=1/r^2` | christoffel_generator.py, riemann_tensor_generator.py |
| `INVERSE_PAIR` | 2 | `INVERSE_PAIR\|(b, 24)\|(24, b)` | function_properties_generator.py, relation_operations_generator.py |
| `INV_FORMULA` | 1 | `INV_FORMULA\|A⁻¹ = (1/det)·[[d, -b], [-c, a]]` | matrix_inverse_generator.py |
| `INV_TRANSFORM` | 2, 3 | `INV_TRANSFORM\|F(x)=x^2/4\|x=2*sqrt(u)` | monte_carlo_arithmetic_generator.py |
| `IRR_SETUP` | 2 | `IRR_SETUP\|c0=-1600,c1=2400\|r0=1/5,iterations=2` | npv_irr_generator.py |
| `IRR_VALUE` | 2 | `IRR_VALUE\|f1\|400` | npv_irr_generator.py |
| `ITERATE` | 2 | `ITERATE\|n=1\|z=(5/4,-4)` | fractal_iteration_generator.py, gradient_descent_generator.py |
| `IVT_SETUP` | 2 | `IVT_SETUP\|f(x) = x^3 + 2x - 8 on [2, 3]\|does the IVT guarantee a root?` | mean_value_theorem_generator.py |
| `I_CYCLE` | 2 | `I_CYCLE\|i^1\|i` | complex_number_ops_generator.py |
| `I_SQUARE` | 2 | `I_SQUARE\|24i^2\|-24` | complex_division_generator.py, complex_log_generator.py, complex_number_ops_generator.py |
| `JACOBIAN` | 2 | `JACOBIAN\|dA\|r dr dtheta` | double_integral_generator.py |
| `JACOBI_END` | 2 | `JACOBI_END\|gcd(6,99)>1\|0` | jacobi_symbol_generator.py |
| `JACOBI_RECIPROCITY` | 3 | `JACOBI_RECIPROCITY\|a mod 4 = 3\|n mod 4 = 3\|flip sign` | jacobi_symbol_generator.py |
| `JACOBI_SETUP` | 3 | `JACOBI_SETUP\|a=6\|n=99\|n odd` | jacobi_symbol_generator.py |
| `JACOBI_SWAP` | 3 | `JACOBI_SWAP\|a=99\|n=3\|sign 1` | jacobi_symbol_generator.py |
| `JACOBI_TWO_RULE` | 3 | `JACOBI_TWO_RULE\|n mod 8 = 3\|flip sign\|sign -1` | jacobi_symbol_generator.py |
| `JAC_DET` | 3 | `JAC_DET\|x_u*y_v - x_v*y_u\|(-2)*(-1) - (-3)*(-2)\|-4` | jacobian_generator.py |
| `JAC_MATRIX` | 2 | `JAC_MATRIX\|[[x_u, x_v], [y_u, y_v]]\|[[-2, -3], [-2, -1]]` | jacobian_generator.py, rv_transform_generator.py |
| `JAC_SETUP` | 3 | `JAC_SETUP\|x = -2*u - 3*v\|y = -2*u - v\|d(x,y)/d(u,v)` | jacobian_generator.py |
| `JOINT_REL` | 3 | `JOINT_REL\|South and Option B\|3/50\|6%` | two_way_table_generator.py |
| `JOINT_ROW` | 2 | `JOINT_ROW\|x=0, y=0\|7/256` | conditional_expectation_generator.py, covariance_algebra_generator.py |
| `JOINT_SETUP` | 3 | `JOINT_SETUP\|X,Y in {0,1}\|p00=1053/4802, p01=1495/4802\|p10=1495/4802, p11=759/4802` | joint_distribution_generator.py |
| `KERNEL_BASE` | 3 | `KERNEL_BASE\|A,A\|dot+c=2+1\|3` | feature_map_generator.py, kernel_evaluation_generator.py |
| `KERNEL_EXPONENT` | 2 | `KERNEL_EXPONENT\|A,A\|0` | kernel_evaluation_generator.py |
| `KERNEL_SETUP` | 3 | `KERNEL_SETUP\|type=rbf\|points=A=(3,3), B=(-1,0), C=(-3,1)\|gamma=1/2` | kernel_evaluation_generator.py |
| `KERNEL_VALIDITY` | 1 | `KERNEL_VALIDITY\|psd=false` | kernel_validity_generator.py |
| `KERNEL_VALUE` | 2 | `KERNEL_VALUE\|A,A\|1` | feature_map_generator.py, kernel_evaluation_generator.py, kernel_perceptron_generator.py, kernel_ridge_generator.py |
| `KIN_FORMULA` | 1 | `KIN_FORMULA\|t = d/v` | invariant_mass_generator.py, kinematics_generator.py |
| `KIN_SETUP` | 3, 4 | `KIN_SETUP\|d = 341 feet\|v = 31 ft/s\|time` | invariant_mass_generator.py, kinematics_generator.py |
| `KL_FORMULA` | 1 | `KL_FORMULA\|D=sum source_i*log2(source_i/target_i)` | kl_divergence_generator.py |
| `KL_SETUP` | 3 | `KL_SETUP\|P=[255/65534,1/2,16256/32767]\|Q=[16320/32767,1/2,127/65534]\|direction=Q to P` | kl_divergence_generator.py |
| `KMAP_GROUP` | 2 | `KMAP_GROUP\|1010, 1011, 1110, 1111\|Q AND S` | boolean_algebra_generator.py |
| `KMAP_ROW` | 2 | `KMAP_ROW\|QR=00\|1, 0, 0, 1` | boolean_algebra_generator.py |
| `KMAP_SETUP` | 2 | `KMAP_SETUP\|rows QR=00,QR=01,QR=11,QR=10\|columns ST=00,ST=01,ST=11,ST=10` | boolean_algebra_generator.py |
| `KMAP_SIMPLIFY` | 1 | `KMAP_SIMPLIFY\|(Q AND S) OR (NOT R AND NOT T) OR (Q AND R AND T) OR (R AND S AND T)` | boolean_algebra_generator.py |
| `KMEANS_SETUP` | 2 | `KMEANS_SETUP\|points=P1=(1,-1), P2=(-5,4), P3=(5,5), P4=(-5,2)\|centroids=C1=(-2,-2), C2=(5,-4)` | kmeans_step_generator.py |
| `KNAPSACK_OPTION` | 4 | `KNAPSACK_OPTION\|A\|11\|17\|feasible` | optimization_in_context_generator.py |
| `KNN_DISTANCE` | 3 | `KNN_DISTANCE\|P1\|label=B\|d2=130` | knn_generator.py |
| `KNN_NEIGHBORS` | 1 | `KNN_NEIGHBORS\|P2:16:A,P5:20:A,P3:89:B` | knn_generator.py |
| `KNN_SETUP` | 3 | `KNN_SETUP\|q=(4,-5)\|k=3\|training=P1=(-5,2,B), P2=(0,-5,A), P3=(-4,0,B), P4=(3,5,B), P5=(0,-3,A)` | knn_generator.py |
| `KNN_SORT` | 1 | `KNN_SORT\|P2:16:A,P5:20:A,P3:89:B,P4:101:B,P1:130:B` | knn_generator.py |
| `KP_EXAMPLE` | 3 | `KP_EXAMPLE\|1\|x=4,y=-1\|alpha=(0,0,0)` | kernel_perceptron_generator.py |
| `KP_SETUP` | 3 | `KP_SETUP\|kernel=linear\|data=[(4,-1), (-1,-1), (-3,-1)]\|alpha0=(0,0,0)` | kernel_perceptron_generator.py |
| `KP_TERM` | 2 | `KP_TERM\|j=1\|0` | kernel_perceptron_generator.py |
| `KRAFT_CHECK` | 2, 3 | `KRAFT_CHECK\|sum=1\|complete` | huffman_coding_generator.py, kraft_inequality_generator.py |
| `KRAFT_CLASSIFY` | 2 | `KRAFT_CLASSIFY\|slack=13/32\|incomplete` | kraft_inequality_generator.py |
| `KRAFT_FORMULA` | 1 | `KRAFT_FORMULA\|sum 2^-l_i` | huffman_coding_generator.py, kraft_inequality_generator.py |
| `KRAFT_SETUP` | 2 | `KRAFT_SETUP\|A=5, B=2, C=2, D=4\|binary prefix code` | kraft_inequality_generator.py |
| `KRAFT_TERM` | 3 | `KRAFT_TERM\|A\|l=5\|1/32` | kraft_inequality_generator.py |
| `KRR_SETUP` | 3 | `KRR_SETUP\|kernel=linear\|data=[(1,4), (5,-4)]\|lambda=1,x*=-3` | kernel_ridge_generator.py |
| `KS_ROW` | 3 | `KS_ROW\|x = 1, before\|abs(0 − 0.1)\|0.1` | empirical_cdf_generator.py |
| `KV_CACHE` | 2 | `KV_CACHE\|values\|2097152` | flops_memory_generator.py |
| `K_EXPR` | 1, 2 | `K_EXPR\|K = [B]/[A]` | equilibrium_ice_generator.py |
| `L` | 2, 3 | `L\|2\|7\|14` | alternative_means_generator.py, complement_probability_generator.py, experimental_probability_generator.py, fraction_comparison_generator.py, fraction_op_generator.py, linear_fractional_generator.py, mixed_number_operation_generator.py, rational_expr_add_sub_generator.py |
| `LABEL` | 2 | `LABEL\|M, C, R\|35, 138, 23` | population_sample_generator.py, study_design_generator.py |
| `LABEL_COUNT` | 2 | `LABEL_COUNT\|A\|2` | knn_generator.py |
| `LADDER_APPLY` | 2 | `LADDER_APPLY\|adag ket14\|sqrt(15) ket15` | ladder_operator_generator.py |
| `LADDER_COMM` | 2 | `LADDER_COMM\|[a,adag] ketn\|ket28` | ladder_operator_generator.py |
| `LADDER_RULE` | 2 | `LADDER_RULE\|J_- = J1_- + J2_-\|lower from highest weights` | clebsch_gordan_generator.py, ladder_operator_generator.py |
| `LADDER_SETUP` | 3 | `LADDER_SETUP\|single_step_energy\|state=ket14\|hbar=12, omega=2` | ladder_operator_generator.py |
| `LAGRANGE_EQ` | 2 | `LAGRANGE_EQ\|f_x = lambda\|3*x^2*y` | lagrange_multiplier_generator.py |
| `LAGRANGE_FACTOR` | 3 | `LAGRANGE_FACTOR\|L_0\|j=1\|-3` | interpolation_generator.py |
| `LAGRANGE_SETUP` | 3 | `LAGRANGE_SETUP\|f(x,y) = x^3*y\|constraint x + y = 24\|maximize` | lagrange_multiplier_generator.py |
| `LAGRANGIAN` | 1, 2 | `LAGRANGIAN\|L=T-V` | lagrangian_generator.py |
| `LAG_SETUP` | 3 | `LAG_SETUP\|pendulum\|m=9, L=8\|g=10, q=theta` | lagrangian_generator.py |
| `LAMBDA_SETUP` | 2 | `LAMBDA_SETUP\|(((lambda g. (lambda g. (g e))) (lambda q. q)) r)\|leftmost-outermost` | lambda_reduction_generator.py |
| `LAPLACE` | 2 | `LAPLACE\|L[y' + 3y]\|(sY + 8) + 3Y` | laplace_ivp_generator.py, transfer_function_generator.py |
| `LAPLACE_TABLE` | 1 | `LAPLACE_TABLE\|L{y'} = sY - y(0); L{e^(kt)} = 1/(s-k); L^-1{1/(s-k)} = e^(kt)` | laplace_ivp_generator.py |
| `LATTICE_PAIR` | 3 | `LATTICE_PAIR\|(4, 4)\|lub 4\|glb 4` | partial_order_generator.py |
| `LAURENT_SETUP` | 3 | `LAURENT_SETUP\|center a=4\|w=(z-4)\|f=-5/(z-9)` | laurent_series_generator.py |
| `LAURENT_TERM` | 1 | `LAURENT_TERM\|2(z+4)^-2` | residue_generator.py |
| `LAW` | 3 | `LAW\|idempotent\|s ∨ s\|s` | logical_equivalence_laws_generator.py, set_algebra_laws_generator.py |
| `LAYERNORM_SETUP` | 3 | `LAYERNORM_SETUP\|x=(-9,11)\|gamma=(1,1)\|beta=(-3,4)` | layer_norm_generator.py |
| `LB` | 2 | `LB\|{∅, {d, k}}\|{∅}` | partial_order_generator.py |
| `LCG_SETUP` | 2 | `LCG_SETUP\|a=1, c=5, m=12\|x_0=10` | monte_carlo_arithmetic_generator.py |
| `LCG_STEP` | 3 | `LCG_STEP\|1\|(1*10+5) mod 12\|3` | monte_carlo_arithmetic_generator.py |
| `LCM_FROM_GCD` | 3 | `LCM_FROM_GCD\|137*53\|1\|7261` | lcm_generator.py |
| `LCM_STEP` | 3 | `LCM_STEP\|1\|2\|2` | permutation_group_generator.py, pollard_factorization_generator.py |
| `LEADING_MINOR` | 2 | `LEADING_MINOR\|Delta1\|25` | positive_definite_generator.py |
| `LEAF_KEY` | 2 | `LEAF_KEY\|4 ∣ 2\|42` | stem_and_leaf_generator.py |
| `LEAST` | 1 | `LEAST\|none` | induction_verify_generator.py, partial_order_generator.py |
| `LEGENDRE_RESULT` | 3 | `LEGENDRE_RESULT\|1\|1\|quadratic residue` | quadratic_residue_generator.py |
| `LEGENDRE_SETUP` | 2 | `LEGENDRE_SETUP\|a=14\|p=11` | legendre_construction_generator.py, quadratic_residue_generator.py |
| `LEVEL` | 2 | `LEVEL\|h\|65729` | type_theory_generator.py |
| `LIE_EXP_FORM` | 2 | `LIE_EXP_FORM\|e^(theta J)\|cos(theta)I + sin(theta)J` | lie_exponential_generator.py |
| `LIE_EXP_SETUP` | 4 | `LIE_EXP_SETUP\|SO3\|axis=x\|theta=840 deg\|K=[[0, 0, 0], [0, 0, -1], [0, 1, 0]]` | lie_exponential_generator.py |
| `LIKELIHOOD` | 2, 3 | `LIKELIHOOD\|1\|certain` | bayes_multiple_hypotheses_generator.py, likelihood_language_generator.py |
| `LIKELIHOOD_FACTOR` | 2 | `LIKELIHOOD_FACTOR\|g(T,λ) = λ^n e^(-λT)\|h(x) = 1` | sufficiency_factorization_generator.py |
| `LIKELIHOOD_RATIO` | 2 | `LIKELIHOOD_RATIO\|L(p;x)/L(p;y)\|1` | sufficiency_factorization_generator.py |
| `LIMIT` | 3 | `LIMIT\|(3n + 12)/(n + 12)\|3\|leading coefficients` | qualitative_reasoning_generator.py |
| `LIMITING_REAGENT` | 2 | `LIMITING_REAGENT\|O2\|CO2=26 mol` | stoichiometry_generator.py |
| `LIMIT_CHECK` | 2 | `LIMIT_CHECK\|CO2 from CO=27 mol\|CO2 from O2=26 mol` | stoichiometry_generator.py |
| `LIMIT_SETUP` | 1, 2 | `LIMIT_SETUP\|lim x→5 of (x^2 - 11x + 30)/(x - 5)\|0/0: factor and cancel` | derivative_limit_def_generator.py, improper_integral_generator.py, lhopital_generator.py, limit_evaluation_generator.py, power_series_generator.py, series_convergence_generator.py |
| `LINEARITY` | 1, 2 | `LINEARITY\|E[X] = Σ E[I_v]\|8 × 15/64` | expected_value_classics_generator.py, linearity_of_expectation_generator.py |
| `LINEAR_EFFECT` | 3 | `LINEAR_EFFECT\|mean\|k·value + c\|3·18` | linear_transform_effect_generator.py |
| `LINEAR_SYSTEM` | 2 | `LINEAR_SYSTEM\|a=4/5, b=-1/5\|c=-1/13, d=11/13` | markov_chain_generator.py, multi_state_markov_generator.py |
| `LINE_EQ` | 1 | `LINE_EQ\|-12x - 10y + 9 = 0` | complex_locus_generator.py |
| `LINE_INTEGRAL` | 3 | `LINE_INTEGRAL\|int_0^1 dot dt\|-3/2 - 6\|-15/2` | line_integral_generator.py |
| `LINE_RELATION_SETUP` | 3 | `LINE_RELATION_SETUP\|perpendicular\|y = -1/2x + 5\|(7, 7)` | parallel_perpendicular_line_generator.py |
| `LINE_SETUP` | 2 | `LINE_SETUP\|F(x,y) = <10*x - y + 3, 4*y - x + 5>\|from (2, 3) to (3, -4)` | line_integral_generator.py |
| `LIST_MAX` | 2 | `LIST_MAX\|7/46, 1/3, 3/8\|3/8` | dedekind_cut_generator.py |
| `LLL_DONE` | 1 | `LLL_DONE\|[(-14,-4),(2,15)]` | lll_reduction_generator.py |
| `LLL_SETUP` | 1 | `LLL_SETUP\|[(-14,-4),(-12,11)]` | lll_reduction_generator.py |
| `LOCUS_SETUP` | 3 | `LOCUS_SETUP\|z=x+iy\|center=(1,5)\|radius=8` | complex_locus_generator.py |
| `LOG2` | 2 | `LOG2\|1/32\|-5` | entropy_generator.py, huffman_coding_generator.py, mutual_information_generator.py, von_neumann_entropy_generator.py |
| `LOG2_RATIO` | 3 | `LOG2_RATIO\|i=0\|ratio=128\|log=7` | kl_divergence_generator.py |
| `LOG_BOTH_SIDES` | 1 | `LOG_BOTH_SIDES\|log_7(7^x) = log_7(53)` | exponential_equation_generator.py, log_diff_higher_order_generator.py, separable_ode_generator.py |
| `LOG_EVAL` | 2 | `LOG_EVAL\|25/8\|ln(25/8)` | hyperbolic_distance_generator.py |
| `LOG_EXACT` | 2 | `LOG_EXACT\|log_10(1000000)\|6` | master_theorem_generator.py |
| `LOG_FORM` | 1 | `LOG_FORM\|log_b(x) = y ⟺ b^y = x` | log_conversion_generator.py, log_equation_generator.py |
| `LOG_FORMULA` | 1 | `LOG_FORMULA\|log z = ln r + i(arg + 2pi*k)` | complex_log_generator.py |
| `LOG_IDENT` | 2 | `LOG_IDENT\|ln(e) = 1\|1` | exponential_equation_generator.py, log_conversion_generator.py |
| `LOG_LIKELIHOOD` | 1 | `LOG_LIKELIHOOD\|ell(lambda)=36*log(lambda)-8*lambda+C` | fisher_information_generator.py, mle_generator.py, sufficiency_factorization_generator.py |
| `LOG_ONE_TO_ONE` | 1 | `LOG_ONE_TO_ONE\|2x + 1 = x + 7` | log_equation_generator.py |
| `LOG_POWER` | 2 | `LOG_POWER\|3log_2(x)\|log_2(x^3)` | derivative_transcendental_generator.py, log_diff_higher_order_generator.py, log_properties_generator.py, ph_calculation_generator.py |
| `LOG_PRODUCT` | 1, 2 | `LOG_PRODUCT\|log_2(x^3) + log_2(y^2)\|log_2(x^3y^2)` | log_equation_generator.py, log_properties_generator.py, ph_calculation_generator.py |
| `LOG_QUOTIENT` | 2 | `LOG_QUOTIENT\|log_3(3x/y^3)\|log_3(3x) - log_3(y^3)` | log_properties_generator.py |
| `LOG_SETUP` | 1, 2 | `LOG_SETUP\|3log_2(x) + 2log_2(y)\|condense` | complex_log_generator.py, log_properties_generator.py |
| `LOG_SOFTMAX` | 2 | `LOG_SOFTMAX\|1\|ln(1/2)` | softmax_gradient_generator.py |
| `LOG_SUPPLIED` | 2 | `LOG_SUPPLIED\|log10(1/10)\|-1` | signal_arithmetic_generator.py |
| `LOG_TERM` | 3 | `LOG_TERM\|16\|ln(2)\|16*ln(2)` | entropy_change_generator.py |
| `LOG_TICKS` | 2 | `LOG_TICKS\|4\|÷10000` | index_and_growth_generator.py |
| `LOOKUP_SUPPLIED` | 2 | `LOOKUP_SUPPLIED\|z*\|1.96` | anova_generator.py, confidence_interval_generator.py, hypothesis_test_generator.py, inverse_normal_generator.py, likelihood_ratio_test_generator.py, named_distribution_generator.py, poisson_process_generator.py, slope_inference_generator.py, t_interval_generator.py, two_sample_test_generator.py |
| `LORA_COUNT` | 2 | `LORA_COUNT\|r*(d_in+d_out)\|46400` | param_count_generator.py |
| `LOWRANK_SETUP` | 2 | `LOWRANK_SETUP\|A=[[19,0], [0,8]]\|rank=1` | low_rank_approx_generator.py |
| `LP_CORNER_SETUP` | 3 | `LP_CORNER_SETUP\|max z=x+3y\|0<=x<=24, 0<=y<=21\|x+y<=30` | lp_corner_generator.py |
| `LR_FORMULA` | 1 | `LR_FORMULA\|Wilks df = unrestricted parameters - null parameters` | likelihood_ratio_test_generator.py |
| `LR_PHASE` | 1 | `LR_PHASE\|warmup` | lr_schedule_generator.py |
| `LR_SETUP` | 3 | `LR_SETUP\|base=1/1000\|min=1/10000\|warmup=50,total=850,t=47` | lr_schedule_generator.py |
| `LR_VALUE` | 1 | `LR_VALUE\|47/50000` | lr_schedule_generator.py |
| `LS_LINE` | 2 | `LS_LINE\|a = 13, b = -1\|ŷ = 13 - x` | least_squares_generator.py |
| `LS_SETUP` | 2 | `LS_SETUP\|points [(-1, 15), (0, 11), (1, 13)]\|model y = a + bx` | least_squares_generator.py |
| `LUB` | 1 | `LUB\|{d, k}` | partial_order_generator.py |
| `LUHN_DIGIT` | 3 | `LUHN_DIGIT\|digit 5\|keep\|5 -> 5` | modular_arithmetic_generator.py |
| `LU_ENTRY` | 3 | `LU_ENTRY\|u11\|a11 = -3\|-3` | lu_decomposition_generator.py |
| `LU_RESULT` | 2 | `LU_RESULT\|L\|[[1, 0, 0], [0, 1, 0], [0, -2, 1]]` | lu_decomposition_generator.py |
| `LU_SETUP` | 2 | `LU_SETUP\|A = [[-3, 5, -5], [0, 2, 0], [0, -4, 4]]\|unit lower L` | lu_decomposition_generator.py |
| `LZ77_EMIT` | 1 | `LZ77_EMIT\|(0,0,h)` | lz_compression_generator.py |
| `LZ77_EXPAND` | 4 | `LZ77_EXPAND\|(0,0,a)\|no copy\|then add a\|out = a` | lz_compression_generator.py |
| `LZ77_MATCH` | 4 | `LZ77_MATCH\|pos 0\|literal\|offset 0, len 0\|next h` | lz_compression_generator.py |
| `LZ77_SEARCH` | 3 | `LZ77_SEARCH\|pos 1\|start 0\|len 0` | lz_compression_generator.py |
| `LZ78_APPEND` | 2 | `LZ78_APPEND\|empty + o\|out = o` | lz_compression_generator.py |
| `LZ78_DICT` | 2 | `LZ78_DICT\|0\|empty` | lz_compression_generator.py |
| `LZ78_EMIT` | 1 | `LZ78_EMIT\|(0,b)` | lz_compression_generator.py |
| `LZ78_LOOKUP` | 2 | `LZ78_LOOKUP\|index 0\|phrase empty` | lz_compression_generator.py |
| `LZ78_MATCH` | 4 | `LZ78_MATCH\|pos 0\|phrase empty\|index 0\|next b` | lz_compression_generator.py |
| `LZ_SETUP` | 2 | `LZ_SETUP\|LZ78 decode\|(0,o), (0,g), (2,g), (1,g), (3,$)` | lz_compression_generator.py |
| `M` | 2, 3 | `M\|1\|80\|80` | ac_circuit_generator.py, activation_generator.py, adam_step_generator.py, alternative_means_generator.py, angle_defect_generator.py, angle_measure_generator.py, annuity_generator.py, arc_length_generator.py, arc_sector_generator.py, arithmetic_coding_generator.py, arithmetic_sequence_generator.py, assumption_check_generator.py, attention_generator.py, backprop_generator.py, bayes_multiple_hypotheses_generator.py, bec_channel_generator.py, binomial_probability_generator.py, bisection_generator.py, black_scholes_generator.py, blackbody_generator.py, bond_pricing_generator.py, calorimetry_generator.py, cantor_pairing_generator.py, cardinal_arithmetic_generator.py, casimir_force_generator.py, casimir_generator.py, cayley_table_generator.py, chain_rule_generator.py, channel_capacity_generator.py, chi_square_generator.py, christoffel_generator.py, circle_angle_generator.py, classic_probability_puzzles_generator.py, classifier_metrics_generator.py, clt_probability_generator.py, collision_generator.py, commutator_generator.py, complement_probability_generator.py, complex_locus_generator.py, complex_log_generator.py, composite_arithmetic_generator.py, conditional_expectation_generator.py, conditional_probability_generator.py, confidence_interval_generator.py, conic_standard_form_generator.py, continued_fraction_generator.py, continuous_distribution_generator.py, contour_integral_generator.py, convolution_generator.py, coset_generator.py, countability_bijection_generator.py, counterexample_search_generator.py, counting_classics_generator.py, counting_to_probability_generator.py, covariance_algebra_generator.py, covariance_correlation_generator.py, cramers_rule_generator.py, cross_section_generator.py, crt_generator.py, curve_analysis_generator.py, cyclic_group_generator.py, de_moivre_generator.py, decimal_div_generator.py, definite_integral_generator.py, density_matrix_generator.py, derangement_generator.py, derivative_limit_def_generator.py, derivative_power_rule_generator.py, derivative_transcendental_generator.py, determinant_generator.py, dimensional_analysis_generator.py, discrete_posterior_generator.py, discrete_uniform_bernoulli_generator.py, distribution_of_sum_generator.py, doppler_generator.py, dot_plot_generator.py, dot_product_generator.py, einstein_summation_generator.py, electrostatics_generator.py, elliptic_curve_finite_field_generator.py, embedding_similarity_generator.py, empirical_rule_generator.py, energy_conservation_generator.py, entropy_change_generator.py, entropy_generator.py, entropy_rate_markov_generator.py, equilibrium_ice_generator.py, equivalence_relation_generator.py, error_spotting_generator.py, estimator_bias_enum_generator.py, euler_method_generator.py, evaluate_expression_generator.py, expectation_of_function_generator.py, expected_value_classics_generator.py, expected_value_generator.py, experimental_probability_generator.py, exponential_model_generator.py, extended_euclid_generator.py, factor_special_forms_generator.py, feature_map_generator.py, fermi_estimation_generator.py, fill_in_step_generator.py, finance_generator.py, finite_difference_generator.py, finite_field_generator.py, finite_sigma_algebra_generator.py, first_law_generator.py, fisher_information_generator.py, five_number_summary_generator.py, fixed_point_generator.py, flops_memory_generator.py, formula_derivation_generator.py, four_vector_generator.py, fourier_series_generator.py, fractal_iteration_generator.py, fraction_line_plot_generator.py, fraction_op_generator.py, function_composition_generator.py, function_evaluation_generator.py, function_operations_generator.py, function_properties_generator.py, function_table_generator.py, fundamental_form_generator.py, game_theory_generator.py, gas_law_generator.py, gas_stoichiometry_generator.py, gauss_bonnet_generator.py, gauss_law_generator.py, gaussian_curvature_generator.py, generating_function_generator.py, geometric_distribution_generator.py, geometric_mean_generator.py, geometric_sequence_generator.py, geometry_area_perimeter_generator.py, geometry_in_context_generator.py, godel_numbering_generator.py, gradient_descent_generator.py, gradient_step_generator.py, graph_counting_generator.py, graph_interpret_generator.py, grassmann_generator.py, great_circle_generator.py, grouped_data_generator.py, growth_comparison_generator.py, hamiltonian_generator.py, hawking_generator.py, hermitian_check_generator.py, horner_evaluation_generator.py, huffman_coding_generator.py, hydrogen_atom_generator.py, hypercube_counting_generator.py, hypergeometric_generator.py, hypothesis_test_generator.py, independence_check_generator.py, index_gymnastics_generator.py, index_raising_generator.py, inference_setup_generator.py, information_gain_generator.py, integer_puzzle_word_generator.py, integers_as_pairs_generator.py, interference_generator.py, interpolation_generator.py, invariant_mass_generator.py, inverse_normal_generator.py, joint_distribution_generator.py, kernel_evaluation_generator.py, kernel_perceptron_generator.py, kernel_ridge_generator.py, kernel_validity_generator.py, kinematics_generator.py, kl_divergence_generator.py, ladder_operator_generator.py, lagrangian_generator.py, laplace_ivp_generator.py, laurent_series_generator.py, law_of_total_probability_generator.py, layer_norm_generator.py, lcm_generator.py, legendre_construction_generator.py, lhopital_generator.py, likelihood_ratio_test_generator.py, limit_evaluation_generator.py, linear_approx_generator.py, linear_model_word_generator.py, linear_transform_effect_generator.py, linearity_of_expectation_generator.py, log_conversion_generator.py, log_diff_higher_order_generator.py, logistic_growth_generator.py, long_division_generator.py, lp_corner_generator.py, lr_schedule_generator.py, magnetism_generator.py, magnitude_comparison_generator.py, markov_chain_generator.py, martingale_check_generator.py, matrix_calculus_generator.py, matrix_group_check_generator.py, matrix_inverse_generator.py, matrix_ops_generator.py, mean_adjustment_generator.py, mean_value_theorem_generator.py, measurement_uncertainty_generator.py, mental_strategy_generator.py, method_discrimination_generator.py, method_of_moments_generator.py, metric_arc_length_generator.py, mgf_generator.py, midpoint_generator.py, missing_information_generator.py, mixed_number_operation_generator.py, mixture_generator.py, mle_generator.py, mobius_transform_generator.py, mod_exp_generator.py, modular_inverse_generator.py, money_life_generator.py, monte_carlo_arithmetic_generator.py, motion_word_generator.py, mse_decomposition_generator.py, multi_state_markov_generator.py, multi_step_unit_conversion_generator.py, multi_step_word_generator.py, multinomial_probability_generator.py, mutual_information_generator.py, naive_bayes_generator.py, named_distribution_generator.py, natural_units_generator.py, negative_binomial_generator.py, nets_surface_area_generator.py, newton_raphson_generator.py, newtons_laws_generator.py, nonparametric_test_generator.py, normal_approx_binomial_generator.py, normal_table_generator.py, npv_irr_generator.py, ode_system_generator.py, operation_properties_generator.py, optics_generator.py, optimization_generator.py, optimization_in_context_generator.py, or_formula_generator.py, orbital_mechanics_generator.py, order_of_operations_generator.py, order_statistics_generator.py, ordinal_arithmetic_generator.py, p_value_generator.py, param_count_generator.py, parametric_calculus_generator.py, particle_in_box_generator.py, partition_function_generator.py, pca_generator.py, percent_chain_generator.py, percent_problem_generator.py, percent_word_problem_generator.py, percentile_generator.py, perceptron_generator.py, permutation_combination_generator.py, pgf_generator.py, physics_formula_generator.py, piecewise_evaluation_generator.py, planck_units_generator.py, plausibility_critic_generator.py, poisson_process_generator.py, polar_parametric_generator.py, polya_urn_generator.py, polynomial_zeros_generator.py, population_sample_generator.py, portfolio_generator.py, positive_definite_generator.py, primality_test_generator.py, probability_critic_generator.py, probability_inequality_generator.py, projectile_motion_generator.py, proportion_word_problem_generator.py, proportional_relationship_generator.py, quadratic_residue_generator.py, quadratic_word_generator.py, qualitative_reasoning_generator.py, quantization_generator.py, quantum_formula_generator.py, quark_composition_generator.py, quaternion_generator.py, radical_multiply_generator.py, radical_rationalize_generator.py, random_walk_generator.py, rate_conversion_generator.py, rate_of_change_interpret_generator.py, ratio_table_generator.py, rational_equation_generator.py, rational_exponent_generator.py, rationals_as_pairs_generator.py, recurrence_generator.py, recursive_definition_unfold_generator.py, recursive_explicit_generator.py, reed_solomon_generator.py, regression_generator.py, regular_polygon_area_generator.py, related_rates_generator.py, relativistic_energy_generator.py, reliability_system_generator.py, remainder_factor_theorem_generator.py, representation_translation_generator.py, riemann_sum_generator.py, riemann_tensor_generator.py, right_triangle_trig_generator.py, rotational_dynamics_generator.py, round_solids_generator.py, rounding_effect_generator.py, routh_hurwitz_generator.py, row_reduction_generator.py, rsa_generator.py, runge_kutta_generator.py, running_coupling_generator.py, rv_transform_generator.py, sampling_distribution_enum_generator.py, scaling_law_generator.py, scatter_plot_describe_generator.py, scenario_generator.py, schwarzschild_generator.py, second_order_ode_generator.py, segment_partition_generator.py, separable_pde_generator.py, series_solution_generator.py, set_builder_roster_generator.py, set_counting_generator.py, set_operations_generator.py, shm_generator.py, signal_arithmetic_generator.py, significant_figures_generator.py, similar_triangles_generator.py, simplex_generator.py, slope_inference_generator.py, solid_revolution_generator.py, solution_chem_generator.py, spatial_description_generator.py, spatial_packing_generator.py, special_relativity_generator.py, special_right_triangle_generator.py, spherical_excess_generator.py, spherical_triangle_generator.py, square_cube_law_generator.py, standing_wave_generator.py, stars_and_bars_generator.py, statics_generator.py, stereographic_generator.py, stoichiometry_generator.py, study_design_generator.py, sufficiency_factorization_generator.py, svm_margin_generator.py, synthetic_division_generator.py, systems_word_generator.py, t_interval_generator.py, tangent_line_generator.py, taxicab_geometry_generator.py, taylor_series_generator.py, temperature_conversion_generator.py, tensor_product_generator.py, tip_bill_split_generator.py, totient_generator.py, transfer_function_generator.py, transformation_generator.py, transient_circuit_generator.py, transportation_generator.py, triangle_area_sas_generator.py, triangle_solve_generator.py, trig_identity_eval_generator.py, two_sample_test_generator.py, two_way_table_generator.py, type_error_power_generator.py, uncertainty_generator.py, undetermined_coeff_generator.py, unit_circle_generator.py, unit_conversion_generator.py, vector_ops_generator.py, volume_rect_prism_generator.py, von_neumann_entropy_generator.py, wavefunction_generator.py, weighted_mean_generator.py, work_rate_generator.py, young_tableaux_generator.py, z_score_generator.py, z_transform_generator.py |
| `MAG_FORMULA` | 1 | `MAG_FORMULA\|magnitude = √(x^2 + y^2)` | magnetism_generator.py, vector_ops_generator.py |
| `MAG_SETUP` | 3 | `MAG_SETUP\|loop_center\|I=41, R=16\|mu0=1` | magnetism_generator.py |
| `MAIN_CONNECTIVE` | 1 | `MAIN_CONNECTIVE\|∨` | wff_parsing_generator.py |
| `MAP` | 2 | `MAP\|b\|f(b) = i` | function_properties_generator.py |
| `MAP_ESTIMATE` | 2 | `MAP_ESTIMATE\|(alpha'-1)/(alpha'+beta'-2)\|1/4` | bayesian_update_generator.py |
| `MARGIN` | 2 | `MARGIN\|2/norm(w)\|2/13` | svm_margin_generator.py |
| `MARGINAL` | 1, 3 | `MARGINAL\|P(Y=1)\|3/32 + 1/32\|1/8` | conditional_expectation_generator.py, joint_distribution_generator.py, mutual_information_generator.py |
| `MARGIN_COL` | 3 | `MARGIN_COL\|Option A\|2 + 1 + 1\|4` | two_way_table_generator.py |
| `MARGIN_ROW` | 3 | `MARGIN_ROW\|Day\|10 + ? + 5\|16` | two_way_table_generator.py |
| `MARKOV_GRAPH` | 2 | `MARKOV_GRAPH\|states 1 through 5\|1→2, 2→2, 2→3, 3→1, 3→5, 4→5, 5→4, 5→5` | markov_state_classification_generator.py |
| `MARKOV_SETUP` | 2, 3 | `MARKOV_SETUP\|two_state\|P00=1/9, P01=8/9\|P10=1/2, P11=1/2` | entropy_rate_markov_generator.py, markov_chain_generator.py, multi_state_markov_generator.py |
| `MARTINGALE_SETUP` | 2 | `MARTINGALE_SETUP\|M_k=Y_1Y_2...Y_k\|E[Y]=1/2(1/2)+1/2(3/2)=1` | martingale_check_generator.py |
| `MARTINGALE_STEP` | 3 | `MARTINGALE_STEP\|E[M_9 given M_8=9/256]\|weighted two-point next product\|9/256` | martingale_check_generator.py |
| `MASTER_CASE` | 2 | `MASTER_CASE\|case 2\|Θ(n^6 log n)` | master_theorem_generator.py |
| `MATCH_REP` | 2 | `MATCH_REP\|A\|y = 2x + 33` | representation_translation_generator.py |
| `MATMUL_FLOPS` | 2 | `MATMUL_FLOPS\|XW1\|16777216` | flops_memory_generator.py |
| `MATRIX_ADD` | 2 | `MATRIX_ADD\|P0+P1\|[[1,0],[0,1]]` | bch_generator.py, casimir_generator.py, projector_generator.py |
| `MATRIX_ENTRY` | 1 | `MATRIX_ENTRY\|P2_01=P00*P01 + P01*P11` | markov_chain_generator.py |
| `MATRIX_ENTRY_SUM` | 3 | `MATRIX_ENTRY_SUM\|(2,3)\|0 + 0\|0` | gamma_matrix_generator.py |
| `MATRIX_EXP` | 3 | `MATRIX_EXP\|e^A\|I + A\|[[1, 0, 0], [0, 1, -1], [0, 0, 1]]` | bch_generator.py |
| `MATRIX_GROUP_SETUP` | 2 | `MATRIX_GROUP_SETUP\|SU2\|M=[[-323/325,-36/325],[-36/325,323/325]]` | matrix_group_check_generator.py |
| `MATRIX_MULT` | 2, 3 | `MATRIX_MULT\|row1 dot col1\|2295225/2108370889*2295225/2108370889+69526380/2108370889*69526380/2108370889\|2295225/2108370889` | projector_generator.py |
| `MATRIX_POWER` | 2 | `MATRIX_POWER\|K^2\|[[0, 0, 0], [0, -1, 0], [0, 0, -1]]` | lie_exponential_generator.py |
| `MATRIX_PRODUCT` | 2 | `MATRIX_PRODUCT\|AB\|[[0, -117i/4], [-117i/4, 0]]` | bch_generator.py, casimir_generator.py, gamma_matrix_generator.py, pauli_algebra_generator.py, structure_constant_generator.py |
| `MATRIX_ROW` | 2 | `MATRIX_ROW\|d\|0 0 0 0 0` | graph_counting_generator.py, relation_operations_generator.py |
| `MATRIX_SCALE` | 2 | `MATRIX_SCALE\|1/2 ladder sum\|[[4232/81, 0, 0, 0, 0], [0, 10580/81, 0, 0, 0], [0, 0, 4232/27, 0, 0], [0, 0, 0, 10580/81, 0], [0, 0, 0, 0, 4232/81]]` | bch_generator.py, casimir_generator.py |
| `MATRIX_SETUP` | 2 | `MATRIX_SETUP\|hermitian\|A=[[-17,7],[7,-17]]` | hermitian_check_generator.py |
| `MATRIX_SUB` | 2 | `MATRIX_SUB\|AB - BA\|[[0, 0, 0], [1, 0, 0], [0, 0, 0]]` | bch_generator.py |
| `MATRIX_SUM` | 1 | `MATRIX_SUM\|B=A+A^T` | matrix_calculus_generator.py |
| `MATRIX_VALUE` | 2 | `MATRIX_VALUE\|A\|[[0, 9i/2], [-9i/2, 0]]` | pauli_algebra_generator.py, structure_constant_generator.py |
| `MAT_ENTRY` | 2, 3 | `MAT_ENTRY\|(1,1)\|4` | lie_exponential_generator.py, matrix_calculus_generator.py, matrix_ops_generator.py |
| `MAT_SETUP` | 2 | `MAT_SETUP\|A = [[3, -1], [3, 2]], B = [[1, 1], [1, 5]]\|A + B` | determinant_generator.py, diagonalization_generator.py, eigenvalue_generator.py, matrix_exponential_generator.py, matrix_inverse_generator.py, matrix_ops_generator.py, row_reduction_generator.py, subspace_basis_generator.py, svd_generator.py |
| `MAX` | 2, 3 | `MAX\|8, 1\|8` | dp_table_generator.py, inference_setup_generator.py, matrix_norm_generator.py, mle_generator.py, taxicab_geometry_generator.py |
| `MAXIMAL` | 1 | `MAXIMAL\|{23, 51, 60}` | partial_order_generator.py |
| `MAXTERM` | 2 | `MAXTERM\|000\|X OR Y OR Z` | boolean_algebra_generator.py |
| `MAX_ABS` | 2 | `MAX_ABS\|point (1, 72)\|10` | scatter_plot_describe_generator.py |
| `MC_SETUP` | 3 | `MC_SETUP\|expression=a^T x\|a=(-4,2)\|x=(5,6)` | matrix_calculus_generator.py |
| `MEAN` | 1 | `MEAN\|1` | layer_norm_generator.py |
| `MEAN_DIV` | 3 | `MEAN_DIV\|78\|6\|13` | anova_generator.py, composite_arithmetic_generator.py, covariance_correlation_generator.py, dot_plot_generator.py, estimator_bias_enum_generator.py, five_number_summary_generator.py, regression_generator.py, scatter_plot_describe_generator.py, simple_stats_generator.py, slope_inference_generator.py, standard_deviation_generator.py, stem_and_leaf_generator.py |
| `MEASURE` | 3 | `MEASURE\|B − A\|∅\|0` | probability_measure_generator.py |
| `MEASURE_BASIS` | 3 | `MEASURE_BASIS\|z\|ket+z=ket0\|ket-z=ket1` | spin_half_generator.py |
| `MEASURE_CHECK` | 2 | `MEASURE_CHECK\|A splits an atom\|no` | finite_sigma_algebra_generator.py |
| `MEASURE_FAVORABLE` | 2 | `MEASURE_FAVORABLE\|interval length\|22 - 20 = 2` | geometric_probability_generator.py |
| `MEASURE_PROB` | 3 | `MEASURE_PROB\|computational basis\|P(11)=1\|all other outcomes 0` | quantum_gate_generator.py |
| `MEASURE_TOTAL` | 2 | `MEASURE_TOTAL\|total length\|24` | geometric_probability_generator.py |
| `MEDIAN_PAIR` | 2 | `MEDIAN_PAIR\|9\|17` | dot_plot_generator.py, five_number_summary_generator.py, mean_adjustment_generator.py, simple_stats_generator.py, stem_and_leaf_generator.py |
| `MEDIAN_PICK` | 1, 2 | `MEDIAN_PICK\|10` | dot_plot_generator.py, five_number_summary_generator.py, mean_adjustment_generator.py, simple_stats_generator.py, stem_and_leaf_generator.py |
| `MEMBER` | 1 | `MEMBER\|53/32 ∈ L(2)` | dedekind_cut_generator.py |
| `MEMBERSHIP_BAD` | 2 | `MEMBERSHIP_BAD\|need 21543\|got 21542` | type_theory_generator.py |
| `MEMBERSHIP_OK` | 1 | `MEMBERSHIP_OK\|type(j) = type(h) + 1` | type_theory_generator.py |
| `MEMBER_ROW` | 1, 3 | `MEMBER_ROW\|x∈G, x∈J, x∈K` | foundations_critic_generator.py, set_identity_membership_table_generator.py |
| `MEMORY_SETUP` | 3 | `MEMORY_SETUP\|kv_cache\|L=4,h=16,d_k=128\|seq=128,precision_bytes=4` | flops_memory_generator.py |
| `MEMORY_UNIT` | 2 | `MEMORY_UNIT\|MiB\|8` | flops_memory_generator.py |
| `MERGE_BEGIN` | 3 | `MERGE_BEGIN\|merge 1\|lo=1,mid=2,hi=3\|left 32; right 6` | algorithm_trace_generator.py |
| `MERGE_COMPARE` | 3 | `MERGE_COMPARE\|32\|6\|take right` | algorithm_trace_generator.py |
| `MERGE_DONE` | 3 | `MERGE_DONE\|merge 1\|range 1-2\|array 40, 6, 32, 20, 24, 21, 19` | algorithm_trace_generator.py |
| `MERGE_TAKE` | 2 | `MERGE_TAKE\|6\|merged 6` | algorithm_trace_generator.py |
| `METRIC` | 2 | `METRIC\|taxicab circle\|all points with abs(x) + abs(y) = 11` | taxicab_geometry_generator.py |
| `METRICS_SETUP` | 1 | `METRICS_SETUP\|TP=26, FP=16, FN=18, TN=42` | classifier_metrics_generator.py |
| `METRIC_ARC_SETUP` | 3 | `METRIC_ARC_SETUP\|polar metric\|ds^2=dr^2+r^2 dtheta^2\|r=10, theta:0->3pi/4` | metric_arc_length_generator.py |
| `METRIC_FORMULA` | 1 | `METRIC_FORMULA\|precision=TP/(TP+FP)` | classifier_metrics_generator.py |
| `METRIC_RESTRICT` | 2 | `METRIC_RESTRICT\|dr=0\|ds^2=r^2 dtheta^2` | metric_arc_length_generator.py |
| `MGF_SETUP` | 3 | `MGF_SETUP\|P(X=0)=45/47\|P(X=1)=1/47\|P(X=2)=1/47` | mgf_generator.py |
| `MGF_TERM` | 3 | `MGF_TERM\|x=0\|p0*e^(0t)\|45/47` | mgf_generator.py |
| `MIDDLE_EVAL` | 3 | `MIDDLE_EVAL\|r=0..5\|5^2/2\|25/2` | triple_integral_generator.py |
| `MIDLINE` | 1 | `MIDLINE\|y = -5` | sinusoid_features_generator.py |
| `MIDPOINT` | 2 | `MIDPOINT\|iter 1\|3` | algorithm_trace_generator.py |
| `MID_FORMULA` | 1 | `MID_FORMULA\|M = ((x1 + x2)/2, (y1 + y2)/2)` | circle_equation_generator.py, midpoint_generator.py |
| `MID_ROW` | 3 | `MID_ROW\|80-99\|89.5\|179` | grouped_data_generator.py |
| `MIN` | 2 | `MIN\|35,8\|8` | matrix_norm_generator.py, two_sample_test_generator.py |
| `MIN3` | 4 | `MIN3\|2\|2\|1\|1` | dp_table_generator.py |
| `MINIMAL` | 1 | `MINIMAL\|{7, 14, 42}` | partial_order_generator.py |
| `MINIMAX` | 2 | `MINIMAX\|A\|60 > 0` | decision_under_uncertainty_generator.py |
| `MINKOWSKI_FORMULA` | 1 | `MINKOWSKI_FORMULA\|eta_total=eta1+eta2` | minkowski_interval_generator.py |
| `MINKOWSKI_SETUP` | 3 | `MINKOWSKI_SETUP\|rapidity_addition\|eta1=-1/2\|eta2=3/2` | minkowski_interval_generator.py |
| `MINTERM` | 2 | `MINTERM\|000\|NOT A AND NOT B AND NOT C` | boolean_algebra_generator.py |
| `MIN_INITIAL` | 3 | `MIN_INITIAL\|nonaccept A\|accept B, C\|{A}, {B,C}` | dfa_minimization_generator.py |
| `MIN_REFINE` | 2 | `MIN_REFINE\|round 1\|{A}, {B,C}` | dfa_minimization_generator.py |
| `MIN_SIGNATURE` | 3 | `MIN_SIGNATURE\|round 1\|A\|0->B0,1->B1` | dfa_minimization_generator.py |
| `MIN_STABLE` | 1 | `MIN_STABLE\|{A}, {B,C}` | dfa_minimization_generator.py |
| `MIN_TRANSITION` | 3 | `MIN_TRANSITION\|{A}\|0\|{A}` | dfa_minimization_generator.py |
| `MISSED` | 1 | `MISSED\|24` | function_properties_generator.py |
| `MISSING` | 2 | `MISSING\|the speed of train B\|35t + bt = 175` | missing_information_generator.py |
| `MIX_FORMULA` | 2 | `MIX_FORMULA\|q=(d-b)/(a-b-c+d)\|p=(d-c)/(a-b-c+d)` | game_theory_generator.py |
| `MIX_IMPROPER` | 2 | `MIX_IMPROPER\|5 2/3\|17/3` | composite_arithmetic_generator.py, mixed_number_operation_generator.py, order_of_operations_generator.py |
| `MI_FORMULA` | 1 | `MI_FORMULA\|I=H(X)+H(Y)-H(X,Y)` | mutual_information_generator.py |
| `MI_SETUP` | 2 | `MI_SETUP\|rows=[[0,0,1/4,0];[0,1/2,0,0];[1/8,0,0,1/8]]\|task=H(X,Y)` | mutual_information_generator.py |
| `MLE_SETUP` | 2, 3 | `MLE_SETUP\|poisson\|parameter=lambda\|data=[4,2,7,8,2,7,1,5]` | mle_generator.py |
| `MOBIUS_SETUP` | 2 | `MOBIUS_SETUP\|T(z)=(-12)/(z + 7)\|fixed points` | mobius_transform_generator.py |
| `MODE` | 2 | `MODE\|2\|8` | frequency_table_generator.py, grouped_data_generator.py, simple_stats_generator.py |
| `MODEL` | 1 | `MODEL\|A = P(1 - r)^t` | exponential_model_generator.py |
| `MODEL_APPLY` | 1 | `MODEL_APPLY\|A = 23100 · (1 - 0.22)^2` | exponential_model_generator.py |
| `MODEL_EQ` | 2 | `MODEL_EQ\|x = 60*(1+20/100)\|changed value` | assumption_check_generator.py, decision_under_uncertainty_generator.py, fermi_estimation_generator.py, formula_derivation_generator.py, geometry_in_context_generator.py, growth_comparison_generator.py, index_and_growth_generator.py, integer_puzzle_word_generator.py, linear_model_word_generator.py, magnitude_comparison_generator.py, measurement_uncertainty_generator.py, mental_strategy_generator.py, method_discrimination_generator.py, missing_information_generator.py, mixture_generator.py, money_life_generator.py, motion_word_generator.py, multi_step_word_generator.py, optimization_in_context_generator.py, percent_chain_generator.py, percent_word_problem_generator.py, plausibility_critic_generator.py, proportion_word_problem_generator.py, quadratic_word_generator.py, qualitative_reasoning_generator.py, rate_of_change_interpret_generator.py, representation_translation_generator.py, risk_communication_generator.py, rounding_effect_generator.py, scenario_generator.py, significant_figures_generator.py, simpsons_paradox_generator.py, spatial_description_generator.py, spatial_packing_generator.py, square_cube_law_generator.py, statistical_literacy_generator.py, systems_word_generator.py, unit_rate_generator.py, work_rate_generator.py |
| `MODEL_OUTPUT` | 1 | `MODEL_OUTPUT\|7/2` | activation_generator.py |
| `MODEXP_MULTIPLY` | 2 | `MODEXP_MULTIPLY\|bit 1=1\|7` | mod_exp_generator.py, quadratic_residue_generator.py |
| `MODEXP_SETUP` | 3 | `MODEXP_SETUP\|base 54\|exponent 84\|modulus 47` | mod_exp_generator.py |
| `MODEXP_SQUARE` | 2 | `MODEXP_SQUARE\|bit 1=1\|1` | mod_exp_generator.py, quadratic_residue_generator.py |
| `MODEXP_STATE` | 2 | `MODEXP_STATE\|after bit 1\|7` | mod_exp_generator.py, quadratic_residue_generator.py |
| `MODE_COUNT` | 2 | `MODE_COUNT\|3\|1` | simple_stats_generator.py |
| `MODE_RULE` | 1 | `MODE_RULE\|mode=floor(lambda); integer lambda also has lambda-1` | named_distribution_generator.py |
| `MOD_INVERSE` | 2 | `MOD_INVERSE\|20 mod 9\|5` | crt_generator.py, ecdsa_generator.py, elliptic_curve_finite_field_generator.py, modular_inverse_generator.py, rsa_generator.py |
| `MOD_NORMALIZE` | 3 | `MOD_NORMALIZE\|-4\|mod 9\|5` | modular_inverse_generator.py, rsa_generator.py |
| `MOD_POWER` | 3 | `MOD_POWER\|67^16\|mod 72\|49` | diffie_hellman_generator.py, pollard_factorization_generator.py, primality_test_generator.py, rsa_generator.py, tonelli_shanks_generator.py, totient_generator.py |
| `MOD_REDUCE` | 3 | `MOD_REDUCE\|55\|mod 10\|5` | calendar_arithmetic_generator.py, cayley_table_generator.py, coset_generator.py, crt_generator.py, cyclic_group_generator.py, de_moivre_generator.py, elliptic_curve_finite_field_generator.py, finite_field_generator.py, jacobi_symbol_generator.py, lie_exponential_generator.py, mod_exp_generator.py, modular_arithmetic_generator.py, modular_inverse_generator.py, primality_test_generator.py, quadratic_residue_generator.py, reed_solomon_generator.py, rsa_generator.py, totient_generator.py |
| `MOD_SETUP` | 2, 3, 4 | `MOD_SETUP\|Luhn modulus 10\|prefix 5534926863` | modular_arithmetic_generator.py, modular_inverse_generator.py |
| `MOD_SOLVE` | 2 | `MOD_SOLVE\|d ≡ -5 mod 10\|5` | modular_arithmetic_generator.py |
| `MOD_TERM` | 2 | `MOD_TERM\|10 * 3\|30` | modular_arithmetic_generator.py |
| `MOE` | 2 | `MOE\|1/√100\|10%` | statistical_literacy_generator.py |
| `MOE_FORMULA` | 1 | `MOE_FORMULA\|E = z*·σ/√n` | confidence_interval_generator.py, t_interval_generator.py |
| `MOLAR_MASS` | 2 | `MOLAR_MASS\|CO\|28 g/mol` | gas_stoichiometry_generator.py, stoichiometry_generator.py |
| `MOLAR_VOLUME` | 2 | `MOLAR_VOLUME\|1 mol gas\|24 L` | stoichiometry_generator.py |
| `MOMENT` | 2 | `MOMENT\|m1\|1/2` | adam_step_generator.py |
| `MOMENTUM` | 1 | `MOMENTUM\|x components` | collision_generator.py |
| `MOMENT_FORMULA` | 2 | `MOMENT_FORMULA\|E[X_A]=np_A; Var(X_A)=np_A(1-p_A)\|Cov(X_A,X_B)=-np_Ap_B` | multinomial_probability_generator.py |
| `MOMENT_TERM` | 3 | `MOMENT_TERM\|E[X]\|x=0, y=0\|0` | covariance_algebra_generator.py |
| `MOMENT_X` | 3 | `MOMENT_X\|M_x = 1/2 int y^2 dx\|3^2*13^3/6\|6591/2` | centroid_generator.py |
| `MOMENT_Y` | 3 | `MOMENT_Y\|M_y = int x*y dx\|3*13^3/3\|2197` | centroid_generator.py |
| `MOM_EQUATION` | 2 | `MOM_EQUATION\|E[X]=lambda\|xbar=lambda` | method_of_moments_generator.py |
| `MOM_SETUP` | 3 | `MOM_SETUP\|poisson\|parameter=lambda\|data=[9,3,8,0,7,2,4,1,9]` | method_of_moments_generator.py |
| `MONO_ADD_EXP` | 2 | `MONO_ADD_EXP\|x^1 * x^9 = x^(1+9)\|x^10` | monomial_mult_div_generator.py |
| `MONO_DIV_COEFF` | 2 | `MONO_DIV_COEFF\|-12 / 3\|-4` | monomial_mult_div_generator.py |
| `MONO_MULT_COEFF` | 2 | `MONO_MULT_COEFF\|2 * 1\|2` | monomial_mult_div_generator.py |
| `MONO_SETUP` | 1 | `MONO_SETUP\|(2x)(x^9)` | monomial_mult_div_generator.py |
| `MONO_SUB_EXP` | 2 | `MONO_SUB_EXP\|x^4 / x^3 = x^(4-3)\|x^1 = x` | monomial_mult_div_generator.py |
| `MONTY_SETUP` | 2 | `MONTY_SETUP\|doors=3, opened=1, pick=1\|host never opens the prize door` | classic_probability_puzzles_generator.py |
| `MOOD` | 2 | `MOOD\|OAA\|figure 4` | syllogism_generator.py |
| `MOVE_TERM` | 1, 2, 3 | `MOVE_TERM\|-4x\|left\|3x-6+4x = +7` | area_between_curves_generator.py, completing_square_generator.py, conic_standard_form_generator.py, integer_puzzle_word_generator.py, linear_complex_generator.py, polar_parametric_generator.py, quadratic_factoring_generator.py, quadratic_square_root_generator.py, radical_equation_generator.py, special_solution_equation_generator.py, standard_form_conversion_generator.py |
| `MP` | 2 | `MP\|lines 1,2\|(d → ¬k) → (((n ∨ g) → ¬g) → ((d ∨ e) → ((n ∨ g) → ¬g)))` | hilbert_axiom_derivation_generator.py |
| `MR_DECOMPOSE` | 2 | `MR_DECOMPOSE\|98\|2^1 * 49` | primality_test_generator.py |
| `MR_SETUP` | 2 | `MR_SETUP\|n=99\|witnesses 4, 13` | primality_test_generator.py |
| `MR_SQUARE` | 2 | `MR_SQUARE\|r=1\|28` | primality_test_generator.py |
| `MR_WITNESS` | 1 | `MR_WITNESS\|4` | primality_test_generator.py |
| `MR_WITNESS_RESULT` | 2 | `MR_WITNESS_RESULT\|4\|composite` | primality_test_generator.py |
| `MSE_DECOMP` | 1 | `MSE_DECOMP\|MSE(T1) = Var(T1) + bias(T1)²` | mse_decomposition_generator.py |
| `MSE_FORMULA` | 2 | `MSE_FORMULA\|L=(1/n) sum r_i^2\|grad=(2/n) sum r_i*[1,x_i]` | gradient_step_generator.py |
| `MSE_GRADIENT` | 2 | `MSE_GRADIENT\|g0=2\|g1=8` | gradient_step_generator.py |
| `MSE_ROW` | 4 | `MSE_ROW\|T1\|bias = -4\|Var = 1.28\|MSE = 17.28` | mse_decomposition_generator.py |
| `MSE_SAMPLE` | 3 | `MSE_SAMPLE\|i=1\|pred=2\|r=-2` | gradient_step_generator.py |
| `MSE_SETUP` | 3 | `MSE_SETUP\|model y_hat=w0+w1*x\|samples=[(0,4), (2,0)]\|w=(2,1), eta=1/7` | gradient_step_generator.py |
| `MST_ADD` | 2 | `MST_ADD\|CD\|total 22` | mst_generator.py |
| `MST_SET` | 1 | `MST_SET\|CD` | mst_generator.py |
| `MST_SETUP` | 2 | `MST_SETUP\|weighted undirected graph\|vertices A, B, C, D` | mst_generator.py |
| `MU` | 2 | `MU\|31/53\|round=1` | lll_reduction_generator.py |
| `MULTIPLY_IF` | 2 | `MULTIPLY_IF\|e^(2x)y' + 2e^(2x)y\|8e^(2x)` | integrating_factor_generator.py, ode_substitution_generator.py |
| `MULTIVALUED_LOG` | 2 | `MULTIVALUED_LOG\|ln(288) + i*(-169pi/180 + 2pi*k)\|k in Z` | complex_log_generator.py |
| `MULTI_FORMULA` | 2 | `MULTI_FORMULA\|n!/(a!b!c!...)\|11! / repeats` | multinomial_probability_generator.py, stars_and_bars_generator.py |
| `MULTI_SETUP` | 2 | `MULTI_SETUP\|1 F, 5 I's, 5 O's\|total 11` | multinomial_probability_generator.py, stars_and_bars_generator.py |
| `MUL_PARTIAL` | 3 | `MUL_PARTIAL\|5\|85843\|429215` | decimal_mult_generator.py, multi_digit_multiplication_generator.py |
| `MUL_SETUP` | 2 | `MUL_SETUP\|85843\|8795` | decimal_mult_generator.py, multi_digit_multiplication_generator.py |
| `MUL_TERM` | 3 | `MUL_TERM\|10\|-8.5x\|-85x` | linear_fractional_generator.py, polynomial_long_division_generator.py, rational_equation_generator.py |
| `MVT_SETUP` | 2 | `MVT_SETUP\|f(x) = x^2 - 5x + 6 on [-3, -1]\|find the c guaranteed by the MVT` | mean_value_theorem_generator.py |
| `MV_CHAIN_SETUP` | 3 | `MV_CHAIN_SETUP\|z = f(x,y) = 4*x^2 + 5*y^2 + 4*x*y + 2*x + 2*y\|x = 4*t - 1, y = -2*t\|t = 1` | multivar_chain_rule_generator.py |
| `NATURAL_SETUP` | 3 | `NATURAL_SETUP\|cross section\|hbar=1,c=1\|E=3/2 eV` | natural_units_generator.py |
| `NB_FEATURE_COUNT` | 3 | `NB_FEATURE_COUNT\|Spam\|money=1\|count=18` | naive_bayes_generator.py |
| `NB_LIKELIHOOD` | 3 | `NB_LIKELIHOOD\|Spam\|money=1\|19/21` | naive_bayes_generator.py |
| `NB_PRIOR` | 2 | `NB_PRIOR\|Spam\|19/35` | naive_bayes_generator.py |
| `NB_SCORE` | 2 | `NB_SCORE\|Spam\|start=19/35` | naive_bayes_generator.py |
| `NB_SETUP` | 3 | `NB_SETUP\|query=money=1, link=1, long=0\|alpha=1\|classes=Spam,Ham` | naive_bayes_generator.py |
| `NCR` | 2 | `NCR\|C(3, 1)\|3` | ballot_reflection_generator.py, binomial_probability_generator.py, classic_probability_puzzles_generator.py, derangement_generator.py, distribution_of_sum_generator.py, expected_value_classics_generator.py, generating_function_generator.py, hypercube_counting_generator.py, hypergeometric_generator.py, likelihood_ratio_test_generator.py, linearity_of_expectation_generator.py, method_discrimination_generator.py, multinomial_probability_generator.py, negative_binomial_generator.py, nonparametric_test_generator.py, pgf_generator.py, polya_urn_generator.py, random_walk_generator.py |
| `NEAREST` | 2 | `NEAREST\|queen\|(2,4)` | embedding_similarity_generator.py |
| `NEED` | 2 | `NEED\|line 3 gives the scale factor 2\|line 5 answers 10` | fill_in_step_generator.py |
| `NEGATE` | 2 | `NEGATE\|944\|-944` | countability_bijection_generator.py |
| `NEGBIN_FORMULA` | 1 | `NEGBIN_FORMULA\|P(N≤n)=Σ from m=r to n of P(N=m)` | negative_binomial_generator.py |
| `NEGBIN_SETUP` | 2 | `NEGBIN_SETUP\|r=2, p=4/5, n=4\|P(N≤4)` | negative_binomial_generator.py |
| `NEG_CONNECTIVE` | 2 | `NEG_CONNECTIVE\|¬(Prime(n) → Odd(n))\|Prime(n) ∧ ¬Odd(n)` | prenex_normal_form_generator.py, quantifier_negation_generator.py |
| `NEG_LOG` | 2 | `NEG_LOG\|p=1/16\|ln(16)` | perplexity_generator.py |
| `NEG_QUANT` | 2 | `NEG_QUANT\|¬∀n\|∃n ¬` | prenex_normal_form_generator.py, quantifier_negation_generator.py |
| `NEST` | 2 | `NEST\|{a}\|{{{∅, {∅, {∅}}, {{∅}}}, {∅, {∅}, {{∅}}, {{{∅}}}}, {∅, {∅, {∅}}, {{{∅}}}}}}` | hereditarily_finite_set_generator.py |
| `NET_SETUP` | 2 | `NET_SETUP\|2 rectangles 5 by 7; 2 rectangles 5 by 3; 2 rectangles 7 by 3\|total surface area` | nets_surface_area_generator.py, spatial_description_generator.py |
| `NEWTON_DD` | 2 | `NEWTON_DD\|f[x0,x1]\|4` | interpolation_generator.py |
| `NEWTON_SETUP` | 2, 3 | `NEWTON_SETUP\|f(x)=x^2-34\|f'(x)=2x\|x0=6,iterations=2` | newton_raphson_generator.py, newtons_laws_generator.py |
| `NEWTON_STEP` | 2 | `NEWTON_STEP\|1\|11/25` | npv_irr_generator.py |
| `NEWTON_UPDATE` | 3 | `NEWTON_UPDATE\|1\|x_0=6\|x_1=35/6` | newton_raphson_generator.py |
| `NEW_SLOPE` | 2 | `NEW_SLOPE\|New slope (m2) = 2\|Perpendicular lines have negative reciprocal slopes` | parallel_perpendicular_line_generator.py |
| `NEW_STRING` | 1 | `NEW_STRING\|11211111` | cantor_diagonal_generator.py |
| `NFA_ACCEPT` | 1 | `NFA_ACCEPT\|r5` | nfa_simulation_generator.py |
| `NFA_ACTIVE` | 2 | `NFA_ACTIVE\|start\|{r2}` | nfa_simulation_generator.py |
| `NFA_EPSILON` | 2 | `NFA_EPSILON\|r0\|{r1}` | nfa_simulation_generator.py |
| `NFA_INPUT` | 1 | `NFA_INPUT\|acbcc` | nfa_simulation_generator.py |
| `NFA_MOVE` | 4 | `NFA_MOVE\|{r2}\|a\|r2->{r2}\|{r2}` | nfa_simulation_generator.py |
| `NFA_READ` | 2 | `NFA_READ\|pos 1\|a` | nfa_simulation_generator.py |
| `NFA_SETUP` | 3 | `NFA_SETUP\|states r2, r3, r5\|alphabet a, b, c\|start r2` | nfa_simulation_generator.py |
| `NFA_TRANSITION` | 3 | `NFA_TRANSITION\|r2\|a\|{r2}` | nfa_simulation_generator.py |
| `NILPOTENT` | 3 | `NILPOTENT\|n>=2\|theta^2=0\|0` | grassmann_generator.py |
| `NLL` | 2 | `NLL\|200 tokens\|200*ln(16)` | perplexity_generator.py |
| `NNT` | 2 | `NNT\|1/0.04\|25 people` | risk_communication_generator.py |
| `NORM2` | 2 | `NORM2\|b1\|212` | lll_reduction_generator.py |
| `NORMALIZE` | 2 | `NORMALIZE\|1\|1` | clebsch_gordan_generator.py, layer_norm_generator.py |
| `NORMALIZE_SIGN` | 2 | `NORMALIZE_SIGN\|(-1,4)\|(1,-4)` | lll_reduction_generator.py |
| `NORMAL_EQ` | 2 | `NORMAL_EQ\|X^T X\|[[3, 0], [0, 2]]` | least_squares_generator.py |
| `NORMAL_SLOPE` | 2 | `NORMAL_SLOPE\|-1/(-3)\|1/3` | tangent_line_generator.py |
| `NORMAL_SYMMETRY` | 2 | `NORMAL_SYMMETRY\|N_neg_d1=0.3\|N_neg_d2=0.35` | black_scholes_generator.py |
| `NORM_CHECK` | 2 | `NORM_CHECK\|P(+z)+P(-z)\|1` | spin_half_generator.py |
| `NORM_SETUP` | 2 | `NORM_SETUP\|X ~ N(110, 10)\|z-score of x = 84` | empirical_rule_generator.py, inverse_normal_generator.py, matrix_norm_generator.py, normal_table_generator.py, z_score_generator.py |
| `NORM_SQUARED` | 2 | `NORM_SQUARED\|q\|1` | quaternion_generator.py |
| `NO_COLLISION` | 1 | `NO_COLLISION\|all outputs distinct` | function_properties_generator.py |
| `NO_MISSED` | 1 | `NO_MISSED\|all codomain values hit` | function_properties_generator.py |
| `NO_REDEX` | 2 | `NO_REDEX\|(r e)\|no beta redex remains` | lambda_reduction_generator.py |
| `NO_WITNESS` | 2, 3 | `NO_WITNESS\|x=4\|tried y in {4, 5, 20, 23, 30, 40}` | peano_arithmetic_generator.py, quantifier_finite_domain_generator.py |
| `NPR` | 2 | `NPR\|P(6,2)\|30` | method_discrimination_generator.py |
| `NPV_SETUP` | 2 | `NPV_SETUP\|c0=-700,c1=800,c2=1000,c3=300\|rate=5%` | npv_irr_generator.py |
| `NPV_TERM` | 2 | `NPV_TERM\|t=0\|-700` | npv_irr_generator.py |
| `NULL_REL` | 2 | `NULL_REL\|x1 = 0\|x1 = 0` | subspace_basis_generator.py |
| `NULL_VECTOR` | 2 | `NULL_VECTOR\|x4=1\|[0, -1, 4, 1]` | subspace_basis_generator.py |
| `NUMBER_OPERATOR` | 2 | `NUMBER_OPERATOR\|N ket1\|ket1` | ladder_operator_generator.py |
| `NW_ALLOC` | 1, 3 | `NW_ALLOC\|cell x11\|min(20,13)\|13` | transportation_generator.py |
| `NYQUIST` | 1 | `NYQUIST\|required rate = 2*f_max` | signal_arithmetic_generator.py |
| `OBJECTIVE` | 1 | `OBJECTIVE\|at (0,0)` | lp_corner_generator.py |
| `OCCURS_CHECK` | 3 | `OCCURS_CHECK\|X\|f(X)\|fail` | unification_generator.py |
| `ODDS` | 2 | `ODDS\|against\|38:37` | bayes_multiple_hypotheses_generator.py, odds_probability_generator.py |
| `ODDS_FORMULA` | 1 | `ODDS_FORMULA\|odds against A = P(Aᶜ) : P(A)` | odds_probability_generator.py |
| `ODDS_REDUCE` | 2 | `ODDS_REDUCE\|332:462\|166:231` | odds_probability_generator.py |
| `ODD_VERTICES` | 2 | `ODD_VERTICES\|none\|0` | euler_circuit_generator.py |
| `ODE_SETUP` | 2, 3 | `ODE_SETUP\|dy/dx = y^2, y(0) = 20\|solve` | euler_method_generator.py, exact_ode_generator.py, integrating_factor_generator.py, laplace_ivp_generator.py, logistic_growth_generator.py, ode_substitution_generator.py, ode_system_generator.py, runge_kutta_generator.py, second_order_ode_generator.py, separable_ode_generator.py, series_solution_generator.py, stability_generator.py, undetermined_coeff_generator.py, variation_parameters_generator.py |
| `OPTICS_FORMULA` | 1 | `OPTICS_FORMULA\|1/f=1/d_o+1/d_i` | optics_generator.py |
| `OPTICS_SETUP` | 3 | `OPTICS_SETUP\|mirror_magnification\|f=12, d_o=58\|h_o=2` | optics_generator.py |
| `OPTION` | 2 | `OPTION\|A\|$740.00` | optimization_in_context_generator.py, representation_translation_generator.py |
| `OPT_SETUP` | 2 | `OPT_SETUP\|square sheet 6 by 6; cut corners x and fold\|maximize volume` | optimization_generator.py |
| `ORBIT_FORMULA` | 1 | `ORBIT_FORMULA\|a_c=v^2/r` | orbital_mechanics_generator.py |
| `ORBIT_SETUP` | 3 | `ORBIT_SETUP\|centripetal_force\|m=6\|r=40, v=16` | orbital_mechanics_generator.py |
| `ORDER_MAG` | 3 | `ORDER_MAG\|$57800000.00\|10^7 dollars\|5.78 × 10^7` | magnitude_comparison_generator.py |
| `ORDER_PAIR` | 2 | `ORDER_PAIR\|17 ≤ 31\|reachable in H` | partial_order_generator.py |
| `ORDER_PDF` | 1 | `ORDER_PDF\|f_{1:4}(x)=4*(1-x)^3` | order_statistics_generator.py |
| `ORDER_SETUP` | 3 | `ORDER_SETUP\|n=4\|k=1\|q=9/14` | order_statistics_generator.py |
| `ORDER_START` | 2 | `ORDER_START\|rs\|identity e` | cayley_table_generator.py |
| `ORDER_STEP` | 2 | `ORDER_STEP\|k=1\|rs` | cayley_table_generator.py |
| `ORD_CMP` | 2 | `ORD_CMP\|coefficients at exponent 3\|3 > 2` | ordinal_arithmetic_generator.py |
| `ORD_RULE` | 2, 3 | `ORD_RULE\|absorption\|left terms below exponent 3 disappear` | ordinal_arithmetic_generator.py |
| `ORIENT` | 2 | `ORIENT\|on their side\|54` | spatial_packing_generator.py |
| `ORTHOGONALITY` | 2 | `ORTHOGONALITY\|lower multiplet\|orthogonal to higher J` | clebsch_gordan_generator.py |
| `OR_SETUP` | 3 | `OR_SETUP\|EOQ\|D=180\|S=30, H=3` | or_formula_generator.py |
| `OST_EQUATION` | 2 | `OST_EQUATION\|E[M_tau]=M_0\|x(2187/128)+(1−x)=27/8` | martingale_check_generator.py |
| `OUTCOME_CHECK` | 3 | `OUTCOME_CHECK\|H65\|heads and an odd spinner label\|yes` | sample_space_list_generator.py |
| `OUTER_ANTIDERIV` | 2 | `OUTER_ANTIDERIV\|dx\|12*x^2` | double_integral_generator.py |
| `OUTER_EVAL` | 3 | `OUTER_EVAL\|x=1..4\|12*(4^2 - 1^2)\|180` | double_integral_generator.py |
| `OUTER_PRODUCT` | 1 | `OUTER_PRODUCT\|rho=18/31ket00bra00 + sqrt(234)/31(ket00bra11+ket11bra00) + 13/31ket11bra11` | partial_trace_generator.py |
| `OUTPUT` | 1 | `OUTPUT\|y_hat=-1` | backprop_generator.py |
| `OVERTIME` | 3 | `OVERTIME\|15\|$36.00\|$540.00` | money_life_generator.py |
| `PAIR` | 2 | `PAIR\|apple\|beaver` | one_to_one_correspondence_generator.py |
| `PAIRING` | 2 | `PAIRING\|(188, 187)\|(m + n)(m + n + 1)/2 + n` | cantor_pairing_generator.py |
| `PAIR_DIFF` | 3 | `PAIR_DIFF\|85\|90\|-5` | t_interval_generator.py |
| `PAIR_RULE` | 1, 2 | `PAIR_RULE\|(a, b) · (c, d)\|(ac + bd, ad + bc)` | integers_as_pairs_generator.py, rationals_as_pairs_generator.py |
| `PARALLEL_RELATION` | 1 | `PARALLEL_RELATION\|(4x + 21) + (2x + 51) = 180` | angle_relationships_generator.py |
| `PARALLEL_SETUP` | 2 | `PARALLEL_SETUP\|co_interior\|Co-interior angles are supplementary (sum to 180°)` | angle_relationships_generator.py |
| `PARALLEL_SOLVE` | 2 | `PARALLEL_SOLVE\|6x + 72 = 180\|x = 18` | angle_relationships_generator.py |
| `PARAMETER` | 2 | `PARAMETER\|the mean exam score of all students\|μ` | inference_setup_generator.py |
| `PARAMS` | 3 | `PARAMS\|W1=[[1,0], [1,2]]\|b1=(2,0)\|v=(-1,-2), c=2` | backprop_generator.py |
| `PARAM_PART` | 2 | `PARAM_PART\|full_matrix\|215040` | param_count_generator.py |
| `PARAM_PATH` | 3 | `PARAM_PATH\|r(t)\|(-t - 2, 1)\|0 <= t <= 1` | line_integral_generator.py |
| `PARAM_SETUP` | 2, 3 | `PARAM_SETUP\|x = t + 16, y = -9t - 15\|eliminate t` | param_count_generator.py, parametric_calculus_generator.py, polar_parametric_generator.py |
| `PARITY` | 1, 2 | `PARITY\|transpositions 4\|even` | fourier_series_generator.py, permutation_group_generator.py |
| `PARITY_CALC` | 2 | `PARITY_CALC\|p1=d1 xor d2 xor d4\|1 xor 0 xor 0=1` | hamming_code_generator.py |
| `PARSE` | 2, 3 | `PARSE\|p\|atom` | wff_parsing_generator.py |
| `PARTFRAC_SETUP` | 1 | `PARTFRAC_SETUP\|(-4x - 14)/(x + 4)^2 = A/(x + 4) + B/(x + 4)^2` | partial_fractions_generator.py, telescoping_generator.py |
| `PARTIAL` | 2 | `PARTIAL\|u_x\|6x + 3` | cauchy_riemann_generator.py, fundamental_form_generator.py, hamiltonian_generator.py, lagrangian_generator.py |
| `PARTIAL_FRAC` | 2 | `PARTIAL_FRAC\|Y(s)\|-4/(s + 3) - 4/(s - 2)` | laplace_ivp_generator.py |
| `PARTIAL_RESULT` | 2 | `PARTIAL_RESULT\|f_y\|8*x*y^3 + 21*x*y^2` | div_curl_generator.py, exact_ode_generator.py, gradient_generator.py, hessian_classify_generator.py, jacobian_generator.py, lagrange_multiplier_generator.py, line_integral_generator.py, multivar_chain_rule_generator.py, partial_derivative_generator.py, vector_theorem_generator.py |
| `PARTIAL_RULE` | 3 | `PARTIAL_RULE\|7*x*y^3\|d/dy\|21*x*y^2` | partial_derivative_generator.py |
| `PARTIAL_SETUP` | 2 | `PARTIAL_SETUP\|f(x,y) = 2*x*y^4 + 7*x*y^3\|f_y` | partial_derivative_generator.py |
| `PARTIAL_TRACE` | 2 | `PARTIAL_TRACE\|ket00bra00\|ket0bra0` | partial_trace_generator.py |
| `PARTICLE_TABLE` | 1 | `PARTICLE_TABLE\|pi0(Q=0,B=0,Le=0,Lmu=0); e-(Q=-1,B=0,Le=1,Lmu=0); e+(Q=1,B=0,Le=-1,Lmu=0); gamma(Q=0,B=0,Le=0,Lmu=0)` | conservation_law_generator.py |
| `PARTICULAR` | 2 | `PARTICULAR\|y_p\|2` | undetermined_coeff_generator.py, variation_parameters_generator.py |
| `PARTICULAR_CHECK` | 2 | `PARTICULAR_CHECK\|K = -5\|5K - 6K - 10 = K` | recurrence_generator.py |
| `PARTICULAR_TRY` | 2 | `PARTICULAR_TRY\|a_n = K\|constant forcing` | recurrence_generator.py |
| `PARTITION` | 1 | `PARTITION\|{{3, 6, 9}, {4, 7, 10}, {5, 8}}` | equivalence_relation_generator.py |
| `PARTITION_FORMULA` | 1 | `PARTITION_FORMULA\|Z=g0+g1*b` | partition_function_generator.py |
| `PARTITION_SETUP` | 3 | `PARTITION_SETUP\|degenerate_two_level\|g0=4, g1=3\|epsilon=14, b=1/10` | partition_function_generator.py |
| `PARTS_CHOOSE` | 2 | `PARTS_CHOOSE\|u = -224x, dv = e^x dx\|du = -224 dx, v = e^x` | integration_by_parts_generator.py |
| `PARTS_FORMULA` | 1 | `PARTS_FORMULA\|∫ u dv = uv - ∫ v du` | integration_by_parts_generator.py |
| `PASCAL_ROW` | 2 | `PASCAL_ROW\|0\|1` | pascal_triangle_generator.py |
| `PASCAL_SETUP` | 1 | `PASCAL_SETUP\|12C8` | pascal_triangle_generator.py |
| `PATH` | 2 | `PATH\|32→20→40\|add (32, 40)` | relation_closure_generator.py |
| `PATH_DERIV` | 2 | `PATH_DERIV\|r'(t)\|(-1, 0)` | curve_geometry_generator.py, line_integral_generator.py |
| `PATH_EDGE` | 2 | `PATH_EDGE\|1→1\|4/7` | multi_state_markov_generator.py |
| `PATTERN` | 2 | `PATTERN\|exponential\|constant ratio` | representation_translation_generator.py |
| `PAULI_IDENTITY` | 3 | `PAULI_IDENTITY\|{sigma_x,sigma_z}\|2 delta_ij I\|0` | pauli_algebra_generator.py |
| `PAULI_MATRIX` | 2 | `PAULI_MATRIX\|sigma_y\|[[0,-i],[i,0]]` | spin_half_generator.py |
| `PAULI_SETUP` | 3 | `PAULI_SETUP\|anticommutator\|A=-4sigma_x\|B=2sigma_z` | pauli_algebra_generator.py |
| `PCA_SETUP` | 2 | `PCA_SETUP\|points=[(6,-2), (-10,-2), (-2,3), (-2,-7)]\|population covariance` | pca_generator.py |
| `PCT_CHANGE` | 2 | `PCT_CHANGE\|(29 − 25)/25\|16%` | index_and_growth_generator.py, risk_communication_generator.py |
| `PCT_ERROR` | 2 | `PCT_ERROR\|abs(66.5 − 70)/70\|5%` | measurement_uncertainty_generator.py |
| `PCT_LESS` | 2 | `PCT_LESS\|(64 − 32)/64\|50%` | statistical_literacy_generator.py |
| `PCT_MORE` | 2 | `PCT_MORE\|32 × 2\|64` | statistical_literacy_generator.py |
| `PCT_RANK` | 3 | `PCT_RANK\|20\|50\|40%` | percentile_generator.py |
| `PCT_STEP` | 3 | `PCT_STEP\|1\|120*(1+20/100)\|144` | percent_chain_generator.py |
| `PC_VECTOR` | 2 | `PC_VECTOR\|e1\|(1,0)` | pca_generator.py |
| `PDA_POP` | 2 | `PDA_POP\|(\|stack=$(` | pda_simulation_generator.py |
| `PDA_PUSH` | 2 | `PDA_PUSH\|(\|stack=$(` | pda_simulation_generator.py |
| `PDA_READ` | 1 | `PDA_READ\|(` | pda_simulation_generator.py |
| `PDA_REJECT` | 1 | `PDA_REJECT\|too many b symbols` | pda_simulation_generator.py |
| `PDA_SETUP` | 2 | `PDA_SETUP\|balanced_parentheses\|stack=$` | pda_simulation_generator.py |
| `PDA_STATE` | 3 | `PDA_STATE\|pos 1\|q\|stack=$` | pda_simulation_generator.py |
| `PDE_SETUP` | 2 | `PDE_SETUP\|u_tt = 4u_xx\|u(x,0)=x^2, u_t(x,0)=0` | separable_pde_generator.py |
| `PDF_FORMULA` | 1 | `PDF_FORMULA\|f_Y(y)=1/(24*sqrt(y))` | rv_transform_generator.py |
| `PD_SETUP` | 2 | `PD_SETUP\|A=[[25,-10], [-10,20]]\|Sylvester criterion` | positive_definite_generator.py |
| `PEANO_BASE` | 2 | `PEANO_BASE\|S0 + 0\|S0` | peano_arithmetic_generator.py |
| `PEANO_EQ` | 2 | `PEANO_EQ\|SSSSS0^S0\|SSSSS0^0 · SSSSS0` | peano_arithmetic_generator.py |
| `PERCENTILE_PICK` | 2 | `PERCENTILE_PICK\|position 2\|32.5` | nonparametric_test_generator.py |
| `PERCENT_CALC_PART` | 3 | `PERCENT_CALC_PART\|1.555\|1225\|1904.875` | percent_problem_generator.py |
| `PERCENT_TO_DEC` | 2 | `PERCENT_TO_DEC\|51%\|0.51` | annuity_generator.py, bond_pricing_generator.py, composite_arithmetic_generator.py, exponential_model_generator.py, fill_in_step_generator.py, finance_generator.py, fraction_decimal_percent_converter.py, mixture_generator.py, npv_irr_generator.py, percent_chain_generator.py, percent_problem_generator.py, percent_word_problem_generator.py, piecewise_evaluation_generator.py, plausibility_critic_generator.py, portfolio_generator.py, qualitative_reasoning_generator.py, tip_bill_split_generator.py, weighted_mean_generator.py |
| `PERCEPTRON_RULE` | 2 | `PERCEPTRON_RULE\|score=w0+w1*x1+w2*x2\|if y*score <= 0 update` | perceptron_generator.py |
| `PERCEPTRON_SAMPLE` | 3 | `PERCEPTRON_SAMPLE\|i=1\|x=(-2,0)\|y=1` | perceptron_generator.py |
| `PERCEPTRON_SCORE` | 2 | `PERCEPTRON_SCORE\|i=1\|score=-6` | perceptron_generator.py |
| `PERCEPTRON_SETUP` | 3 | `PERCEPTRON_SETUP\|eta=2\|w=(-2,2,2)\|samples=[(-2,0,1), (-1,1,1), (3,1,-1)]` | perceptron_generator.py |
| `PERCEPTRON_UPDATE` | 2, 3 | `PERCEPTRON_UPDATE\|i=1\|w=(0,-2,2)` | perceptron_generator.py |
| `PERIM` | 1 | `PERIM\|40` | geometry_area_perimeter_generator.py, polygon_perimeter_generator.py |
| `PERIOD` | 1 | `PERIOD\|180°` | sinusoid_features_generator.py |
| `PERM_COMPOSE` | 3 | `PERM_COMPOSE\|i=1\|tau(i)=3\|sigma(tau(i))=5` | permutation_group_generator.py |
| `PERM_FORMULA` | 1 | `PERM_FORMULA\|P(n, r) = n·(n-1)···(n-r+1), 4 factors` | permutation_combination_generator.py |
| `PERM_RESULT` | 1 | `PERM_RESULT\|[5, 4, 1, 3, 2]` | permutation_group_generator.py |
| `PERM_ROW` | 2 | `PERM_ROW\|{5, 18, 21} vs {25, 30, 37}\|44/3 − 92/3 = -16` | nonparametric_test_generator.py |
| `PERM_SETUP` | 2, 3 | `PERM_SETUP\|P(14, 4)\|n!/(n-r)!` | permutation_combination_generator.py, permutation_group_generator.py |
| `PERPLEXITY` | 2 | `PERPLEXITY\|exp(CE)\|16` | perplexity_generator.py |
| `PERPLEXITY_SETUP` | 2 | `PERPLEXITY_SETUP\|tokens=200\|p=1/16` | perplexity_generator.py |
| `PER_1000` | 2 | `PER_1000\|37 × 1000/50000\|0.74 per 1000` | risk_communication_generator.py |
| `PE_ENTRY` | 2 | `PE_ENTRY\|0\|0` | positional_encoding_generator.py |
| `PE_SETUP` | 3 | `PE_SETUP\|position=21\|d=2\|theta=pi` | positional_encoding_generator.py |
| `PF_PRIME` | 1 | `PF_PRIME\|431` | godel_numbering_generator.py, prime_factorization_generator.py, repeating_decimal_generator.py |
| `PF_STEP` | 3 | `PF_STEP\|1293\|3\|431` | godel_numbering_generator.py, prime_factorization_generator.py, repeating_decimal_generator.py |
| `PGF_DERIV` | 1, 2 | `PGF_DERIV\|G'(s)\|(3/2)s^3 + (3/16)s^2 + (5/8)s + 1/16` | pgf_generator.py |
| `PGF_SETUP` | 1 | `PGF_SETUP\|G(s) = Σ P(X=k)·s^k` | pgf_generator.py |
| `PGF_TERM` | 2 | `PGF_TERM\|k=4\|(3/8)s^4` | pgf_generator.py |
| `PHASE_SHIFT` | 1 | `PHASE_SHIFT\|30° right` | sinusoid_features_generator.py |
| `PHI_STEP` | 2 | `PHI_STEP\|p=2\|36` | totient_generator.py |
| `PHYS_FORMULA` | 1 | `PHYS_FORMULA\|F = W/d` | physics_formula_generator.py |
| `PHYS_SETUP` | 3 | `PHYS_SETUP\|W = 570 joules\|d = 19 meters\|force` | physics_formula_generator.py |
| `PH_FORMULA` | 1 | `PH_FORMULA\|pH=-log10([H+])` | ph_calculation_generator.py |
| `PH_SETUP` | 2, 3 | `PH_SETUP\|hydronium_with_log\|[H+]=4*10^-5\|log10(4)=0.6` | ph_calculation_generator.py |
| `PI2_NUM` | 3 | `PI2_NUM\|-57/163840\|π^2\|-57π^2/163840` | casimir_force_generator.py |
| `PICTO_COUNT` | 2 | `PICTO_COUNT\|Fish\|3` | graph_interpret_generator.py |
| `PICTO_KEY` | 2 | `PICTO_KEY\|●\|5` | graph_interpret_generator.py |
| `PIVOT` | 3 | `PIVOT\|row=s1\|column=x\|pivot=1` | simplex_generator.py |
| `PIVOT_COLS` | 2 | `PIVOT_COLS\|columns 1, 2, 3\|rank = 3` | subspace_basis_generator.py |
| `PI_COEFF` | 2 | `PI_COEFF\|16π/9\|16/9` | arc_sector_generator.py |
| `PI_DEN` | 3 | `PI_DEN\|27/160\|π\|27/(160π)` | gauss_law_generator.py, hawking_generator.py, magnetism_generator.py |
| `PI_FORM` | 2 | `PI_FORM\|1/3/pi\|1/(3π)` | expected_value_classics_generator.py |
| `PI_MULT` | 3 | `PI_MULT\|2/3\|π\|2π/3` | shm_generator.py |
| `PLACE_DP` | 3 | `PLACE_DP\|1010786\|3\|1010.786` | decimal_mult_generator.py |
| `PLACE_DP_Q` | 3 | `PLACE_DP_Q\|3975\|2\|39.75` | decimal_div_generator.py, percent_problem_generator.py |
| `PLACE_VALUE` | 2 | `PLACE_VALUE\|5 * 16^0\|5` | base_conversion_generator.py |
| `PLANCK_SETUP` | 4 | `PLANCK_SETUP\|time\|hbar=81\|G=64\|c=4` | planck_units_generator.py |
| `PLAUSIBLE` | 2 | `PLAUSIBLE\|yes\|plausible` | fermi_estimation_generator.py, magnitude_comparison_generator.py, plausibility_critic_generator.py |
| `PLOT_READ` | 2, 3 | `PLOT_READ\|row 22\|●●\|2` | box_plot_generator.py, dot_plot_generator.py, fraction_line_plot_generator.py, stem_and_leaf_generator.py |
| `PLUS_MINUS` | 2 | `PLUS_MINUS\|x = ±√5113\|x = √5113 or x = -√5113` | completing_square_generator.py, quadratic_square_root_generator.py, rational_equation_generator.py |
| `PMF_ROW` | 2 | `PMF_ROW\|0\|87/256` | probability_inequality_generator.py |
| `POINT_FROM_LAMBDA` | 3 | `POINT_FROM_LAMBDA\|x\|12*2/2\|12` | lagrange_multiplier_generator.py |
| `POINT_SET` | 2 | `POINT_SET\|n=10\|(1,0), (3/4,1/4), (1/2,9/10), (4/5,4/5), (0,0), (9/10,1/2), (4/5,4/5), (2/3,1/3), (3/4,1/4), (9/10,1/2)` | monte_carlo_arithmetic_generator.py |
| `POINT_SLOPE_SETUP` | 1 | `POINT_SLOPE_SETUP\|y + 6 = 2/3(x + 10)` | equation_from_two_points_generator.py, parallel_perpendicular_line_generator.py, point_slope_generator.py |
| `POLAR_AREA_FORMULA` | 1 | `POLAR_AREA_FORMULA\|A = (1/2) ∫ r^2 dθ` | parametric_calculus_generator.py |
| `POLAR_BOUNDS` | 2 | `POLAR_BOUNDS\|r\|0..3` | double_integral_generator.py |
| `POLAR_CONVERT` | 2 | `POLAR_CONVERT\|x^2 + y^2\|r^2` | double_integral_generator.py |
| `POLAR_EVAL` | 3 | `POLAR_EVAL\|theta range * radial integral\|pi * 81/4\|81/4*pi` | double_integral_generator.py |
| `POLAR_FORM` | 1 | `POLAR_FORM\|11 cis(180 deg)` | euler_formula_generator.py |
| `POLAR_FORMULA` | 1 | `POLAR_FORMULA\|x = r cos θ, y = r sin θ` | polar_parametric_generator.py |
| `POLAR_SETUP` | 2, 3 | `POLAR_SETUP\|(r, θ) = (60, -25785°)\|rectangular coordinates` | parametric_calculus_generator.py, polar_parametric_generator.py |
| `POLES` | 1 | `POLES\|s=-6, -12` | transfer_function_generator.py |
| `POLE_ORDER` | 1 | `POLE_ORDER\|2` | residue_generator.py |
| `POLE_TEST` | 3 | `POLE_TEST\|pole -6\|abs(-6) < 5\|outside` | contour_integral_generator.py |
| `POLISH` | 1 | `POLISH\|ACKrppArKqr` | wff_parsing_generator.py |
| `POLLARD_FACTOR` | 2 | `POLLARD_FACTOR\|17\|29` | pollard_factorization_generator.py |
| `POLLARD_PM1_SETUP` | 3 | `POLLARD_PM1_SETUP\|n=589\|base=5\|B=7` | pollard_factorization_generator.py |
| `POLLARD_RHO_SETUP` | 3 | `POLLARD_RHO_SETUP\|n=493\|c=5\|x0=2` | pollard_factorization_generator.py |
| `POLYA_COUNT_FORMULA` | 1 | `POLYA_COUNT_FORMULA\|C(n,k)(r)_(k,c)(b)_(n-k,c)/(r+b)_(n,c)` | polya_urn_generator.py |
| `POLYA_SETUP` | 2 | `POLYA_SETUP\|r=5, b=3, c=1\|P(sequence B, B)` | polya_urn_generator.py |
| `POLYA_STEP` | 3 | `POLYA_STEP\|draw 1: B\|3/8\|5R 4B` | polya_urn_generator.py |
| `POLYDIV_SETUP` | 2 | `POLYDIV_SETUP\|9x^3 - 30x^2 + 34x - 6\|3x - 5` | finite_field_generator.py, polynomial_long_division_generator.py |
| `POLY_ACCUM` | 2 | `POLY_ACCUM\|x^0\|8` | finite_field_generator.py |
| `POLY_ADD_START` | 1 | `POLY_ADD_START\|max degree 3` | finite_field_generator.py |
| `POLY_COEFF` | 3 | `POLY_COEFF\|sum\|x^0\|1` | finite_field_generator.py |
| `POLY_COMBINE` | 1 | `POLY_COMBINE\|x^2 + 8x + 13` | multiplying_binomials_generator.py, polynomial_add_sub_generator.py |
| `POLY_DIST_NEG` | 1 | `POLY_DIST_NEG\|Distribute negative sign to second polynomial` | polynomial_add_sub_generator.py |
| `POLY_DIV_SETUP` | 1 | `POLY_DIV_SETUP\|(-9x^6 - 45x^5 - 45x^5 + 9x^4) / (-9x^2)` | polynomial_div_monomial_generator.py |
| `POLY_DIV_SPLIT` | 1 | `POLY_DIV_SPLIT\|(-9x^6) / (-9x^2) + (-45x^5) / (-9x^2) + (-45x^5) / (-9x^2) + (9x^4) / (-9x^2)` | polynomial_div_monomial_generator.py |
| `POLY_FORMULA` | 1 | `POLY_FORMULA\|A = (1/2)·a·P` | regular_polygon_area_generator.py |
| `POLY_GROUP_LIKE` | 1 | `POLY_GROUP_LIKE\|(x^2) + (8x) + (6 +7)` | multiplying_polynomials_generator.py, polynomial_add_sub_generator.py |
| `POLY_INPUT` | 2 | `POLY_INPUT\|f(x)\|4x^2 + 4x + 2` | finite_field_generator.py |
| `POLY_MUL` | 2 | `POLY_MUL\|((1/4)s^2 + (1/4)s + 1/2)((1/4)s^3 + (1/8)s^2 + (7/16)s + 3/16)\|(1/16)s^5 + (3/32)s^4 + (17/64)s^3 + (7/32)s^2 + (17/64)s + 3/32` | pgf_generator.py |
| `POLY_MULT_SETUP` | 1 | `POLY_MULT_SETUP\|(3x + 1)(-3x^2 + 3x + 2)` | multiplying_polynomials_generator.py |
| `POLY_MUL_START` | 2 | `POLY_MUL_START\|degree 2\|degree 3` | finite_field_generator.py |
| `POLY_REMAINDER` | 1 | `POLY_REMAINDER\|x` | finite_field_generator.py |
| `POLY_SCALE` | 3 | `POLY_SCALE\|x^3 - 3x/5\|5/2\|(5x^3 - 3x)/2` | legendre_construction_generator.py |
| `POLY_SETUP` | 1, 2 | `POLY_SETUP\|(x^2 + 6) + (8x + 7)` | factor_gcf_generator.py, factor_grouping_generator.py, factor_special_forms_generator.py, factor_trinomial_generator.py, polynomial_add_sub_generator.py, rational_expr_add_sub_generator.py, rational_expr_mult_div_generator.py, rational_expr_simplify_generator.py, regular_polygon_area_generator.py |
| `POLY_SUB` | 2, 3 | `POLY_SUB\|(9x^3 - 30x^2) - (9x^3 - 15x^2)\|-15x^2` | legendre_construction_generator.py, polynomial_long_division_generator.py |
| `POOLED_RATE` | 2 | `POOLED_RATE\|A\|42/100 = 42%` | simpsons_paradox_generator.py, statistical_literacy_generator.py |
| `PORT_FORMULA` | 2 | `PORT_FORMULA\|E=wA*rA+wB*rB\|Var=wA^2*varA+wB^2*varB+2*wA*wB*cov` | portfolio_generator.py |
| `PORT_RESULT` | 2 | `PORT_RESULT\|expected_return=29/300\|variance=4/225` | portfolio_generator.py |
| `PORT_SETUP` | 3 | `PORT_SETUP\|wA=1/3,wB=2/3\|rA=15%,rB=7%\|varA=0.04,varB=0.04,cov=-0.01` | portfolio_generator.py |
| `POSTERIOR` | 3 | `POSTERIOR\|U1\|(1/20)/(17/36)\|9/85` | bayes_multiple_hypotheses_generator.py, probability_critic_generator.py |
| `POSTERIOR_PARAM` | 1 | `POSTERIOR_PARAM\|alpha' = alpha + successes` | bayesian_update_generator.py |
| `POSTERIOR_PREDICTIVE` | 2, 3 | `POSTERIOR_PREDICTIVE\|Normal\|mean=-13/25\|variance=56/25` | bayesian_update_generator.py |
| `POSTERIOR_ROW` | 2 | `POSTERIOR_ROW\|0.2\|32768/79469` | discrete_posterior_generator.py |
| `POST_PRECISION` | 1 | `POST_PRECISION\|prior precision + data precision` | bayesian_update_generator.py |
| `POTENTIAL_BUILD` | 3 | `POTENTIAL_BUILD\|integrate P dx\|5*x^2 - x*y + 3*x + g(y)\|g'(y) remains` | exact_ode_generator.py, line_integral_generator.py |
| `POTENTIAL_RESULT` | 2 | `POTENTIAL_RESULT\|phi(x,y)\|5*x^2 + 2*y^2 - x*y + 3*x + 5*y` | exact_ode_generator.py, line_integral_generator.py |
| `POW` | 2 | `POW\|12^5\|248832` | ballot_reflection_generator.py, binomial_probability_generator.py, classic_probability_puzzles_generator.py, distribution_of_sum_generator.py, expected_value_classics_generator.py, geometric_distribution_generator.py, linearity_of_expectation_generator.py, martingale_check_generator.py, monte_carlo_arithmetic_generator.py, multinomial_probability_generator.py, named_distribution_generator.py, negative_binomial_generator.py, nonparametric_test_generator.py, poisson_process_generator.py, random_walk_generator.py, recurrence_generator.py |
| `POWER_ENTRY` | 3 | `POWER_ENTRY\|(1,1)\|(-243)*7 + (-64)*(-3)\|-1509` | diagonalization_generator.py |
| `POWER_FORM` | 1 | `POWER_FORM\|A^5 = P*D^5*P^-1` | diagonalization_generator.py |
| `POWER_FORMULA` | 1 | `POWER_FORMULA\|β = P(x̄ ≤ 125.32 given μ = 119.52)` | type_error_power_generator.py |
| `POWER_INTEGRAL` | 2 | `POWER_INTEGRAL\|int_0^a x dx\|a^2/2` | continuous_distribution_generator.py, wavefunction_generator.py |
| `POWER_REDUCE` | 2 | `POWER_REDUCE\|67^64\|67^16 mod 72` | totient_generator.py |
| `POWER_RULE` | 2 | `POWER_RULE\|2x^5\|10x^4` | chain_rule_generator.py, commutator_generator.py, curve_analysis_generator.py, derivative_power_rule_generator.py, derivative_product_quotient_generator.py, derivative_transcendental_generator.py, lhopital_generator.py, linear_approx_generator.py, log_diff_higher_order_generator.py, mean_value_theorem_generator.py, optimization_generator.py, tangent_line_generator.py |
| `POWER_SETUP` | 2 | `POWER_SETUP\|(e^(i*68 deg))^(9i)\|principal logarithm` | complex_log_generator.py |
| `POWER_SET_RESULT` | 1 | `POWER_SET_RESULT\|{∅, {k}, {m}, {p}, {t}, {k, m}, {k, p}, {k, t}, {m, p}, {m, t}, {p, t}, {k, m, p}, {k, m, t}, {k, p, t}, {m, p, t}, {k, m, p, t}}` | set_operations_generator.py |
| `POWER_SHIFT` | 3 | `POWER_SHIFT\|k=0\|0-3\|-3` | laurent_series_generator.py |
| `PP_CHANGE` | 2 | `PP_CHANGE\|29 − 25\|4 points` | index_and_growth_generator.py, risk_communication_generator.py |
| `PP_SETUP` | 2 | `PP_SETUP\|rate 5 per hour, t=12 minutes\|P(T_2≤t)=P(N(t)≥2)` | poisson_process_generator.py |
| `PP_VS_PCT` | 2 | `PP_VS_PCT\|1.2 points\|+200%` | risk_communication_generator.py |
| `PREDICATES` | 1 | `PREDICATES\|M(x): x is a dancer; W(x): x is patient` | english_to_logic_generator.py |
| `PREDICT` | 2 | `PREDICT\|x*\|16/9` | kernel_ridge_generator.py |
| `PREIMAGE` | 2 | `PREIMAGE\|20\|{g}` | function_properties_generator.py |
| `PREMISE` | 2 | `PREMISE\|1\|b` | natural_deduction_generator.py |
| `PREMISES_ALL_T` | 2 | `PREMISES_ALL_T\|p=T, q=T, r=T, s=T\|no` | argument_form_generator.py |
| `PRIME` | 1 | `PRIME\|157` | divisibility_classification_generator.py |
| `PRIM_CANDIDATES` | 2 | `PRIM_CANDIDATES\|visited C\|CD=22, BC=23, AC=24` | mst_generator.py |
| `PRIM_START` | 1 | `PRIM_START\|C` | mst_generator.py |
| `PRINCIPAL_LOG` | 1 | `PRINCIPAL_LOG\|ln(288) - i*169pi/180` | complex_log_generator.py |
| `PRINCIPAL_MINOR` | 2 | `PRINCIPAL_MINOR\|K11\|3` | kernel_validity_generator.py |
| `PRIOR_PRECISION` | 1 | `PRIOR_PRECISION\|1/tau^2` | bayesian_update_generator.py |
| `PROBABILITY` | 2 | `PROBABILITY\|P(+z)\|6400/7921` | spin_half_generator.py |
| `PROB_CONDITIONAL` | 2 | `PROB_CONDITIONAL\|P(black card given first was black card)\|25/51` | compound_probability_generator.py |
| `PROB_DEPENDENT` | 1 | `PROB_DEPENDENT\|Drawing without replacement means dependent events` | compound_probability_generator.py |
| `PROB_DESCRIBE` | 1 | `PROB_DESCRIBE\|Draw with replacement: yellow, then orange, then silver` | compound_probability_generator.py |
| `PROB_IDENTIFY` | 2 | `PROB_IDENTIFY\|P(draw 1 is yellow)\|1/4` | compound_probability_generator.py |
| `PROB_INDEPENDENT` | 1 | `PROB_INDEPENDENT\|Replacement restores the same distribution, so the draws are independent` | compound_probability_generator.py |
| `PROB_MULTIPLY` | 3 | `PROB_MULTIPLY\|1/4\|1/8\|1/32` | compound_probability_generator.py |
| `PROB_SETUP` | 2 | `PROB_SETUP\|13\|25` | complement_probability_generator.py, counting_to_probability_generator.py, discrete_uniform_bernoulli_generator.py, fundamental_counting_principle_generator.py, independence_check_generator.py, likelihood_language_generator.py, odds_probability_generator.py, random_digit_simulation_generator.py, sample_space_list_generator.py, simple_probability_generator.py, venn_probability_generator.py |
| `PROB_SIMPLIFY` | 2 | `PROB_SIMPLIFY\|650/2652\|25/102` | compound_probability_generator.py |
| `PROB_WEIGHT` | 2 | `PROB_WEIGHT\|0^2\|0` | clebsch_gordan_generator.py |
| `PRODUCT` | 2 | `PRODUCT\|Delta x^2 * Delta p^2\|15625pi^2/12 - 1/2` | uncertainty_generator.py |
| `PROJECT` | 2 | `PROJECT\|P1\|8` | pca_generator.py |
| `PROJECTILE_SETUP` | 3 | `PROJECTILE_SETUP\|vx=16\|vy=21\|g=10` | projectile_motion_generator.py |
| `PROJECTION` | 2 | `PROJECTION\|X*beta\|[14, 13, 12]` | least_squares_generator.py, legendre_construction_generator.py |
| `PROJECTOR_SETUP` | 2 | `PROJECTOR_SETUP\|v=(1515/45917, 45892/45917)\|P=vv^T=[[2295225/2108370889,69526380/2108370889],[69526380/2108370889,2106075664/2108370889]]` | projector_generator.py |
| `PROJ_COEFF` | 3 | `PROJ_COEFF\|v2 on u1\|2/2\|1` | gram_schmidt_generator.py |
| `PROJ_VECTOR` | 2 | `PROJ_VECTOR\|u1\|[1, 0, 1]` | gram_schmidt_generator.py |
| `PROPAGATE` | 2, 3 | `PROPAGATE\|min × min, max × max\|[132.25, 146.25]` | measurement_uncertainty_generator.py |
| `PROPERTY_MATCH` | 3 | `PROPERTY_MATCH\|transitive property of equality\|if a = b and b = c, then a = c\|z = b; b = 7966` | operation_properties_generator.py |
| `PROPERTY_RESULT` | 2 | `PROPERTY_RESULT\|reflexive\|no` | relation_check_generator.py |
| `PROP_SETUP` | 1 | `PROP_SETUP\|1/2 = 20/x` | proportion_word_problem_generator.py, proportional_relationship_generator.py, similar_triangles_generator.py, triangle_solve_generator.py |
| `PSD_SETUP` | 2 | `PSD_SETUP\|K=[[3,10], [10,10]]\|criterion=all principal minors >= 0` | kernel_validity_generator.py |
| `PULL` | 2 | `PULL\|∃v\|from left past ∧` | prenex_normal_form_generator.py |
| `PURITY` | 1 | `PURITY\|Tr(rho^2)=265/361` | density_matrix_generator.py |
| `PUZZLE_REL` | 2 | `PUZZLE_REL\|consecutive\|x, x+1, x+2` | integer_puzzle_word_generator.py |
| `PVALUE_RULE` | 2 | `PVALUE_RULE\|right tail\|p = 1 − Φ(z)` | p_value_generator.py |
| `PYTHAG_CALCULATE` | 2 | `PYTHAG_CALCULATE\|h² = 900 - 324 = 576\|576` | pythag_leg_generator.py |
| `PYTHAG_CONTEXT` | 3 | `PYTHAG_CONTEXT\|ladder\|ladder=30ft, given=18ft\|diagram=ULJ` | pythag_leg_generator.py |
| `PYTHAG_FORMULA` | 1 | `PYTHAG_FORMULA\|a² + b² = c²` | pythag_hyp_generator.py, pythag_leg_generator.py |
| `PYTHAG_MODEL` | 3 | `PYTHAG_MODEL\|ground=18\|wall=?\|ladder=30` | pythag_leg_generator.py |
| `PYTHAG_ROOT` | 2 | `PYTHAG_ROOT\|13225\|115` | pythag_leg_generator.py |
| `PYTHAG_SETUP` | 2, 3 | `PYTHAG_SETUP\|legs=120,442\|hypotenuse YL=?` | pythag_hyp_generator.py, pythag_leg_generator.py |
| `PYTHAG_SOLVE` | 2 | `PYTHAG_SOLVE\|b² = 1755625 - 1742400\|13225` | pythag_leg_generator.py |
| `PYTHAG_SQUARE` | 2 | `PYTHAG_SQUARE\|1320\|1742400` | pythag_leg_generator.py |
| `PYTHAG_SUBSTITUTE` | 1 | `PYTHAG_SUBSTITUTE\|1320² + b² = 1325²` | pythag_leg_generator.py |
| `Q1` | 4 | `Q1\|84\|52\|8\|17` | complex_quadratic_generator.py, polynomial_zeros_generator.py, quadratic_generator.py |
| `Q2` | 4 | `Q2\|84\|52\|8\|4` | complex_quadratic_generator.py, polynomial_zeros_generator.py, quadratic_generator.py |
| `QN_ADD` | 4 | `QN_ADD\|Q\|left\|0 + pi0(0)\|0` | conservation_law_generator.py |
| `QR_ENTRY` | 2 | `QR_ENTRY\|q1\|[1, 0, 0]` | qr_decomposition_generator.py |
| `QR_SETUP` | 2 | `QR_SETUP\|A = [[3, 5, -4], [0, 6, 1], [0, 0, 6]]\|Gram-Schmidt columns` | qr_decomposition_generator.py |
| `QUADRANT` | 2 | `QUADRANT\|304°\|quadrant IV` | angle_measure_generator.py, polar_parametric_generator.py, unit_circle_generator.py |
| `QUADRANT_ROW` | 3 | `QUADRANT_ROW\|(62, 105)\|−,−\|agree` | scatter_plot_describe_generator.py |
| `QUADRATIC` | 3 | `QUADRATIC\|1\|7\|12` | mobius_transform_generator.py |
| `QUANTILE` | 3 | `QUANTILE\|1/4\|first x with F(x) ≥ q\|12` | pmf_cdf_quantile_generator.py |
| `QUANTUM_FORMULA` | 1 | `QUANTUM_FORMULA\|Delta_lambda=h/(m*c)*(1-cos(theta))` | quantum_formula_generator.py |
| `QUANTUM_SETUP` | 2, 3 | `QUANTUM_SETUP\|gate=CNOT\|input=e^(i369π/187)·ket10` | quantum_formula_generator.py, quantum_gate_generator.py |
| `QUANT_CASE` | 1, 2 | `QUANT_CASE\|x=4` | quantifier_finite_domain_generator.py |
| `QUANT_CHOICE` | 1 | `QUANT_CHOICE\|no → ∀ with negated property` | english_to_logic_generator.py |
| `QUANT_RESULT` | 2, 3 | `QUANT_RESULT\|∀x ∃y\|false` | quantifier_finite_domain_generator.py |
| `QUANT_SETUP` | 3 | `QUANT_SETUP\|x=(34/25,-141/100,-1/5)\|scale=1/20\|zero_point=2` | quantization_generator.py |
| `QUANT_VALUE` | 2 | `QUANT_VALUE\|1\|29` | quantization_generator.py |
| `QUARK_CHARGE` | 2 | `QUARK_CHARGE\|s\|-1/3` | quark_composition_generator.py |
| `QUARK_SETUP` | 3 | `QUARK_SETUP\|baryon,count=688\|s s c\|u=2/3,d=-1/3,s=-1/3,c=2/3,b=-1/3; anti=-charge` | quark_composition_generator.py |
| `QUARTILE` | 3 | `QUARTILE\|Q1\|5,12,12,12,17\|12` | five_number_summary_generator.py |
| `QUAT_COMPONENT` | 3 | `QUAT_COMPONENT\|q*v\|real\|-1` | quaternion_generator.py |
| `QUAT_INVERSE` | 2 | `QUAT_INVERSE\|q\|(0,0,0,1)` | quaternion_generator.py |
| `QUAT_MUL_START` | 3 | `QUAT_MUL_START\|q*v\|q\|v` | quaternion_generator.py |
| `QUAT_RESULT` | 2 | `QUAT_RESULT\|q*v\|(-1,-2,-3,0)` | quaternion_generator.py |
| `QUAT_SETUP` | 2 | `QUAT_SETUP\|q=(0,0,0,-1)\|v=(0,3,-2,-1)` | quaternion_generator.py |
| `QUEUE_STATE` | 2 | `QUEUE_STATE\|initial\|C` | graph_traversal_generator.py |
| `QUOTIENT` | 1 | `QUOTIENT\|x` | finite_field_generator.py |
| `Q_EXPR` | 1 | `Q_EXPR\|Q = [B]/[A]` | equilibrium_ice_generator.py |
| `R` | 1 | `R\|27` | complex_number_ops_generator.py, finite_field_generator.py, long_division_generator.py, polynomial_long_division_generator.py, polynomial_zeros_generator.py, synthetic_division_generator.py |
| `RANGE` | 1 | `RANGE\|{3, 14, 19, 23}` | relation_operations_generator.py |
| `RANK` | 2 | `RANK\|∅\|0` | hereditarily_finite_set_generator.py |
| `RANK_POS` | 2 | `RANK_POS\|6\|value 18` | percentile_generator.py |
| `RANK_ROW` | 3 | `RANK_ROW\|8\|1\|B` | nonparametric_test_generator.py |
| `RAPIDITY_SUM` | 2 | `RAPIDITY_SUM\|collinear boosts\|1` | minkowski_interval_generator.py |
| `RATE` | 2, 3 | `RATE\|together\|1/5 job per hour` | work_rate_generator.py |
| `RATE_FORMULA` | 1 | `RATE_FORMULA\|P(T_2≤t)=1-e^(-lambda*t)(1+lambda*t)` | poisson_process_generator.py |
| `RATE_MONTHLY` | 2 | `RATE_MONTHLY\|18% / 12\|0.015` | finance_generator.py |
| `RATE_SETUP` | 2 | `RATE_SETUP\|91 ft ladder; the base slides away at 2 ft/min; base is 84 ft from the wall\|dy/dt` | related_rates_generator.py |
| `RATE_SUM` | 2 | `RATE_SUM\|1/15 + 1/10\|1/6` | work_rate_generator.py |
| `RATE_SUPPLIED` | 2 | `RATE_SUPPLIED\|1 USD\|0.9 EUR` | money_life_generator.py |
| `RATIO` | 2, 3 | `RATIO\|3*y = x\|y = x/3` | lagrange_multiplier_generator.py, simplex_generator.py |
| `RATIONALIZE` | 1 | `RATIONALIZE\|√137/√137` | dot_product_generator.py, limit_evaluation_generator.py, radical_rationalize_generator.py, special_right_triangle_generator.py |
| `RATIO_BASE` | 3 | `RATIO_BASE\|35:49\|7\|5:7` | error_spotting_generator.py, fill_in_step_generator.py, ratio_table_generator.py |
| `RATIO_CHECK` | 3 | `RATIO_CHECK\|A\|12, 12, 12\|constant` | method_discrimination_generator.py |
| `RATIO_PART` | 3 | `RATIO_PART\|Ana\|6\|$240.00` | money_life_generator.py |
| `RATIO_TABLE` | 2 | `RATIO_TABLE\|Water (oz): 35, ?, 50, 60\|Concentrate (oz): 49, 56, 70, 84` | error_spotting_generator.py, fill_in_step_generator.py, ratio_table_generator.py |
| `RAW_FORMULA` | 1 | `RAW_FORMULA\|x = μ + z·σ` | inverse_normal_generator.py, normal_table_generator.py, z_score_generator.py |
| `REACH_PASS` | 2 | `REACH_PASS\|k=0\|R1=(1,1,0,0,0); R2=(0,1,1,0,0); R3=(1,0,1,0,1); R4=(0,0,0,1,1); R5=(0,0,0,1,1)` | markov_state_classification_generator.py |
| `REAL_RATE` | 2 | `REAL_RATE\|100·(100 + 56)/(100 + 0) − 100\|56%` | index_and_growth_generator.py |
| `REARRANGE_EQ` | 1 | `REARRANGE_EQ\|whole = 5678 / 0.085` | percent_problem_generator.py |
| `RECIPROCAL` | 2 | `RECIPROCAL\|csc θ = 1/sin θ\|-17/15` | trig_six_functions_generator.py |
| `RECIP_ROW` | 2 | `RECIP_ROW\|36\|1/36` | alternative_means_generator.py |
| `RECOVER_DATA` | 2 | `RECOVER_DATA\|positions 3,5,6,7\|1101` | hamming_code_generator.py |
| `RECT_FORM` | 1 | `RECT_FORM\|4sqrt2 - 4sqrt2i` | de_moivre_generator.py, euler_formula_generator.py |
| `RECUR` | 3 | `RECUR\|5P_5 = 9x P_4 - 4P_3\|P_4 = (35x^4 - 30x^2 + 3)/8\|P_3 = (5x^3 - 3x)/2` | legendre_construction_generator.py |
| `RECURRENCE` | 2 | `RECURRENCE\|a_(n+1)\|4a_n/(n+1)` | derangement_generator.py, series_solution_generator.py |
| `REC_SETUP` | 1, 2 | `REC_SETUP\|a_n = 6 a_(n-1) - 8 a_(n-2)\|a_0 = -7, a_1 = -20` | master_theorem_generator.py, recurrence_generator.py |
| `REDUCE` | 2, 3 | `REDUCE\|(2506, 6986)\|(0, 4480)` | integers_as_pairs_generator.py, rationals_as_pairs_generator.py |
| `REDUCED_DENSITY` | 1 | `REDUCED_DENSITY\|rho_A=[[18/31,0],[0,13/31]]` | partial_trace_generator.py |
| `REFLECT` | 2 | `REFLECT\|paths ever below 0\|reflect at first visit to -1` | ballot_reflection_generator.py |
| `REFLEXIVE_CHECK` | 2 | `REFLEXIVE_CHECK\|(12, 12)\|present` | equivalence_relation_generator.py, relation_check_generator.py |
| `REGEX_ACCEPT` | 1 | `REGEX_ACCEPT\|q77255_3, q77255_4` | regex_to_automaton_generator.py |
| `REGEX_SETUP` | 3 | `REGEX_SETUP\|(a or b)*(ab or ba)\|alphabet a,b\|canonical progress DFA` | regex_to_automaton_generator.py |
| `REGEX_STATE` | 2 | `REGEX_STATE\|q77255_0\|start` | regex_to_automaton_generator.py |
| `REGEX_TRANSITION` | 3 | `REGEX_TRANSITION\|q77255_0\|a\|q77255_1` | regex_to_automaton_generator.py |
| `REGION` | 2 | `REGION\|all three\|∅` | attribute_sorting_generator.py, venn_region_count_generator.py |
| `REGION_EQ` | 2 | `REGION_EQ\|A ∩ B\|13` | venn_region_count_generator.py |
| `REGION_MEASURE` | 3 | `REGION_MEASURE\|disk area\|10^2*pi\|100*pi` | vector_theorem_generator.py |
| `REGION_REWRITE` | 2 | `REGION_REWRITE\|0 <= y <= 15\|y/5 <= x <= 3` | double_integral_generator.py |
| `REGRESS_MEAN` | 2 | `REGRESS_MEAN\|77 + 0.7·(5 − 77)\|26.6` | statistical_literacy_generator.py |
| `REG_ROW` | 3 | `REG_ROW\|x-x̄=-2\|y-ȳ=0\|product=0` | covariance_correlation_generator.py, regression_generator.py |
| `REG_SETUP` | 2 | `REG_SETUP\|line ŷ = 38.8 - 0.6x\|predict ŷ at x = 10` | regression_generator.py, slope_inference_generator.py |
| `REJECT` | 1, 2 | `REJECT\|x = 23` | cantor_pairing_generator.py, conditional_forms_generator.py, counterexample_search_generator.py, factor_trinomial_generator.py, knights_knaves_generator.py, log_conversion_generator.py, log_equation_generator.py, optimization_generator.py, polynomial_inequality_generator.py, quadratic_word_generator.py, radical_equation_generator.py, rational_equation_generator.py, rational_root_generator.py, set_builder_roster_generator.py, structure_isomorphism_generator.py |
| `RELAX` | 3 | `RELAX\|B->A\|update inf to 8\|via weight 8` | dijkstra_generator.py |
| `RELIABILITY` | 3 | `RELIABILITY\|parallel block\|1 − 1/10 × 1/6\|59/60` | reliability_system_generator.py |
| `RELU` | 3 | `RELU\|z=3\|h=3\|deriv=1` | backprop_generator.py |
| `REL_ENERGY_FORMULA` | 1 | `REL_ENERGY_FORMULA\|w=(u+v)/(1+u*v), c=1` | relativistic_energy_generator.py |
| `REL_ENERGY_SETUP` | 3 | `REL_ENERGY_SETUP\|velocity_addition\|u=-2/5\|v=0` | relativistic_energy_generator.py |
| `REL_FORMULA` | 1 | `REL_FORMULA\|t=gamma*tau` | special_relativity_generator.py |
| `REL_FREQ` | 3 | `REL_FREQ\|theoretical A\|3/6\|1/2` | experimental_probability_generator.py |
| `REL_PAIR` | 2 | `REL_PAIR\|(1, 1)\|same block` | equivalence_relation_generator.py |
| `REL_SETUP` | 2, 3 | `REL_SETUP\|A = {12, 18, 22, 31, 32, 40, 46, 49}\|R = {(12, 12), (12, 18), (12, 31), (18, 12), (18, 18), (18, 31), (22, 22), (22, 32), (22, 40), (22, 46), (22, 49), (31, 12), (31, 18), (31, 31), (32, 22), (32, 32), (32, 40), (32, 46), (32, 49), (40, 22), (40, 32), (40, 40), (40, 46), (40, 49), (46, 22), (46, 32), (46, 40), (46, 46), (46, 49), (49, 22), (49, 32), (49, 40), (49, 46), (49, 49)}` | equivalence_relation_generator.py, relation_check_generator.py, relation_closure_generator.py, relation_operations_generator.py, special_relativity_generator.py |
| `RENAME` | 2 | `RENAME\|∀v\|∀v1` | prenex_normal_form_generator.py |
| `RENORMALIZE` | 3 | `RENORMALIZE\|a\|(3/199)/(94/199)\|3/94` | probability_measure_generator.py |
| `REPEAT` | 2 | `REPEAT\|state 3\|first seen at index 0` | monte_carlo_arithmetic_generator.py |
| `REPEAT_DETECT` | 2 | `REPEAT_DETECT\|remainder 88 repeats\|repetend 8301886792452` | repeating_decimal_generator.py |
| `REPRESENT` | 2 | `REPRESENT\|odd e\|e = 2q + 1` | direct_proof_algebra_generator.py |
| `REP_DIM` | 2 | `REP_DIM\|6bar\|6` | young_tableaux_generator.py |
| `RESIDUAL` | 2 | `RESIDUAL\|y - X*beta\|[1, -2, 1]` | least_squares_generator.py |
| `RESIDUE` | 1, 3 | `RESIDUE\|1` | contour_integral_generator.py, residue_generator.py |
| `RESIDUE_SETUP` | 2 | `RESIDUE_SETUP\|a=-4\|f=(2 + (z+4) - 3(z+4)^2 - 2(z+4)^3)/(z+4)^2` | residue_generator.py |
| `RESIDUE_SUM` | 1 | `RESIDUE_SUM\|0` | contour_integral_generator.py |
| `RESID_ROW` | 3 | `RESID_ROW\|(7, 94)\|ŷ=94\|residual=0` | scatter_plot_describe_generator.py |
| `RESID_SETUP` | 2 | `RESID_SETUP\|point (4, 73), line ŷ = 71.8 - 0.6x\|residual = observed − predicted` | regression_generator.py |
| `RESOLVE` | 3 | `RESOLVE\|C1\|C2\|P82135` | resolution_proof_generator.py |
| `RESTRICT_CHECK` | 3 | `RESTRICT_CHECK\|(i, 7)\|i in D=no\|skip` | relation_operations_generator.py |
| `RES_EMPTY` | 1 | `RES_EMPTY\|C5` | resolution_proof_generator.py |
| `RES_SETUP` | 1 | `RES_SETUP\|C1=(P82135), C2=(¬P82135), C3=(¬P15409 ∨ ¬P19542), C4=(¬P15409 ∨ ¬P82135)` | resolution_proof_generator.py |
| `RES_SKIP` | 3 | `RES_SKIP\|C1\|C2\|(P26874 ∨ P81702)` | resolution_proof_generator.py |
| `REVENUE` | 1 | `REVENUE\|R = p(80 − 4p)` | optimization_in_context_generator.py, quadratic_word_generator.py |
| `REVERSAL` | 1 | `REVERSAL\|A wins each group, B wins overall` | simpsons_paradox_generator.py |
| `REVERSE` | 2 | `REVERSE\|A,A,8\|8AA` | base_arithmetic_generator.py, base_conversion_generator.py, bitwise_ops_generator.py |
| `REVERSE_PCT` | 2 | `REVERSE_PCT\|x*(1+5/100) = 147\|140` | percent_chain_generator.py |
| `REWRITE` | 1, 2 | `REWRITE\|b = 7966` | antiderivative_generator.py, arc_length_generator.py, area_between_curves_generator.py, assumption_check_generator.py, cardinal_arithmetic_generator.py, chain_rule_generator.py, circle_equation_generator.py, clt_probability_generator.py, combinatory_logic_generator.py, completing_square_generator.py, complex_division_generator.py, complex_log_generator.py, complex_number_ops_generator.py, complex_quadratic_generator.py, confidence_interval_generator.py, conic_standard_form_generator.py, cramers_rule_generator.py, curve_analysis_generator.py, definite_integral_generator.py, derivative_limit_def_generator.py, derivative_power_rule_generator.py, derivative_product_quotient_generator.py, derivative_transcendental_generator.py, domain_range_generator.py, dot_product_generator.py, english_to_logic_generator.py, euler_formula_generator.py, evaluate_expression_generator.py, exponent_generator.py, exponent_mixed_rules_generator.py, exponential_equation_generator.py, factor_gcf_generator.py, factor_grouping_generator.py, factor_special_forms_generator.py, factor_trinomial_generator.py, formula_derivation_generator.py, frequency_table_generator.py, function_composition_generator.py, function_operations_generator.py, horner_evaluation_generator.py, implicit_diff_generator.py, improper_integral_generator.py, induction_verify_generator.py, inference_setup_generator.py, integrating_factor_generator.py, integration_by_parts_generator.py, inverse_function_generator.py, inverse_normal_generator.py, lambda_reduction_generator.py, laurent_series_generator.py, lhopital_generator.py, limit_evaluation_generator.py, linear_approx_generator.py, linear_complex_generator.py, linear_fractional_generator.py, literal_equation_generator.py, log_conversion_generator.py, log_diff_higher_order_generator.py, log_equation_generator.py, log_properties_generator.py, logical_equivalence_laws_generator.py, logistic_growth_generator.py, master_theorem_generator.py, matrix_inverse_generator.py, method_of_moments_generator.py, mgf_generator.py, midpoint_generator.py, mle_generator.py, normal_approx_binomial_generator.py, normal_table_generator.py, ode_substitution_generator.py, operation_properties_generator.py, optimization_generator.py, optimization_in_context_generator.py, order_of_operations_generator.py, ordinal_arithmetic_generator.py, p_value_generator.py, parametric_calculus_generator.py, partial_fractions_generator.py, permutation_combination_generator.py, polar_parametric_generator.py, polynomial_zeros_generator.py, power_series_generator.py, prenex_normal_form_generator.py, quadratic_factoring_generator.py, quadratic_word_generator.py, qualitative_reasoning_generator.py, quantifier_negation_generator.py, radical_add_sub_generator.py, radical_equation_generator.py, radical_multiply_generator.py, radical_rationalize_generator.py, radical_variable_simplify_generator.py, rational_equation_generator.py, rational_exponent_generator.py, rational_expr_add_sub_generator.py, rational_expr_mult_div_generator.py, rational_expr_simplify_generator.py, rational_function_features_generator.py, recursive_explicit_generator.py, regression_generator.py, related_rates_generator.py, right_triangle_trig_generator.py, row_reduction_generator.py, separable_ode_generator.py, separable_pde_generator.py, series_convergence_generator.py, series_solution_generator.py, set_algebra_laws_generator.py, set_expression_generator.py, set_operations_generator.py, simplify_expression_generator.py, sinusoid_features_generator.py, slope_inference_generator.py, solid_revolution_generator.py, special_right_triangle_generator.py, special_solution_equation_generator.py, spin_half_generator.py, standard_form_conversion_generator.py, stars_and_bars_generator.py, synthetic_division_generator.py, systems_word_generator.py, t_interval_generator.py, tangent_line_generator.py, taxicab_geometry_generator.py, taylor_series_generator.py, trig_equation_generator.py, trig_identity_eval_generator.py, trig_identity_verify_generator.py, trig_six_functions_generator.py, type_error_power_generator.py, u_substitution_generator.py, vector_ops_generator.py, z_transform_generator.py |
| `RG_SETUP` | 3 | `RG_SETUP\|one_loop\|alpha0=1/13\|beta=1,L=1` | running_coupling_generator.py |
| `RHO_ITER` | 4 | `RHO_ITER\|1\|x=9, y=86\|abs(r)=77\|gcd=1` | pollard_factorization_generator.py |
| `RICCI_ENTRY` | 2 | `RICCI_ENTRY\|R_phiphi\|1` | riemann_tensor_generator.py |
| `RIDGE_ENTRY` | 2 | `RIDGE_ENTRY\|K\|[[1,5], [5,25]]` | kernel_ridge_generator.py |
| `RIEMANN_ENTRY` | 2 | `RIEMANN_ENTRY\|R^phi_theta phi theta\|5184/9409` | riemann_tensor_generator.py |
| `RIEMANN_SETUP` | 2, 3 | `RIEMANN_SETUP\|f(x) = 4x + 3 on [-2, 6], n = 4\|midpoint Riemann sum` | riemann_sum_generator.py, riemann_tensor_generator.py |
| `RISING_FACTOR` | 2, 3 | `RISING_FACTOR\|red\|empty product\|1` | polya_urn_generator.py |
| `RISK` | 3 | `RISK\|relative\|(18 − 6)/6\|+200%` | risk_communication_generator.py |
| `RK_COMBINE` | 2 | `RK_COMBINE\|k1+2k2+2k3+k4\|-1415/64` | runge_kutta_generator.py |
| `RK_STAGE` | 3 | `RK_STAGE\|k1\|t=-3/2\|y=5` | runge_kutta_generator.py |
| `RODRIGUES_FORM` | 2 | `RODRIGUES_FORM\|e^(theta K)\|I + sin(theta)K + (1-cos(theta))K^2` | lie_exponential_generator.py |
| `ROOT` | 1, 2, 3 | `ROOT\|25\|2\|5` | ac_circuit_generator.py, adam_step_generator.py, alternative_means_generator.py, cholesky_generator.py, clt_probability_generator.py, completing_square_generator.py, confidence_interval_generator.py, countability_bijection_generator.py, covariance_algebra_generator.py, de_moivre_generator.py, doppler_generator.py, embedding_similarity_generator.py, energy_conservation_generator.py, estimator_bias_enum_generator.py, expectation_of_function_generator.py, factor_special_forms_generator.py, formula_derivation_generator.py, four_vector_generator.py, fundamental_form_generator.py, geometry_in_context_generator.py, hypothesis_test_generator.py, invariant_mass_generator.py, joint_distribution_generator.py, ladder_operator_generator.py, layer_norm_generator.py, low_rank_approx_generator.py, matrix_norm_generator.py, method_discrimination_generator.py, method_of_moments_generator.py, metric_arc_length_generator.py, monte_carlo_arithmetic_generator.py, normal_approx_binomial_generator.py, or_formula_generator.py, orbital_mechanics_generator.py, p_value_generator.py, planck_units_generator.py, pythag_hyp_generator.py, qr_decomposition_generator.py, quadratic_generator.py, quadratic_square_root_generator.py, radical_add_sub_generator.py, radical_multiply_generator.py, radical_rationalize_generator.py, radical_variable_simplify_generator.py, rational_equation_generator.py, rational_exponent_generator.py, regression_generator.py, relativistic_energy_generator.py, round_solids_generator.py, rv_transform_generator.py, schwarzschild_generator.py, shm_generator.py, slope_inference_generator.py, svd_generator.py, svm_margin_generator.py, t_interval_generator.py, two_sample_test_generator.py, type_error_power_generator.py |
| `ROOT_ANGLE` | 2 | `ROOT_ANGLE\|k=0\|45 deg` | de_moivre_generator.py |
| `ROOT_EXTRACT` | 2 | `ROOT_EXTRACT\|16` | exponent_generator.py |
| `ROOT_IDENTIFY` | 3 | `ROOT_IDENTIFY\|4096\|perfect_cube\|16` | exponent_generator.py |
| `ROOT_SETUP` | 1 | `ROOT_SETUP\|∛4096` | exponent_generator.py, radical_add_sub_generator.py, radical_multiply_generator.py, radical_rationalize_generator.py, radical_variable_simplify_generator.py |
| `ROOT_SIMPLIFY` | 1, 2 | `ROOT_SIMPLIFY\|3√19` | complex_quadratic_generator.py, distance_formula_generator.py, dot_product_generator.py, euler_formula_generator.py, exponent_generator.py, geometric_mean_generator.py, hypercube_counting_generator.py, polar_parametric_generator.py, vector_ops_generator.py |
| `ROSTER` | 2 | `ROSTER\|S\|{25}` | set_builder_roster_generator.py |
| `ROTATED_VECTOR` | 1 | `ROTATED_VECTOR\|(-3,2,-1)` | quaternion_generator.py |
| `ROT_FORMULA` | 1 | `ROT_FORMULA\|I1*omega1=I2*omega2` | rotational_dynamics_generator.py |
| `ROT_SETUP` | 3 | `ROT_SETUP\|angular_momentum\|I1=14, omega1=14\|I2=6` | rotational_dynamics_generator.py |
| `ROUND` | 2, 3 | `ROUND\|0.1952\|4 decimal places\|0.1952` | named_distribution_generator.py, poisson_process_generator.py, quantization_generator.py, rounding_effect_generator.py, significant_figures_generator.py |
| `ROUNDTRIP_ERROR` | 2 | `ROUNDTRIP_ERROR\|sum_abs\|1/50` | quantization_generator.py |
| `ROUND_CHECK` | 3 | `ROUND_CHECK\|9\|4\|<5` | place_value_rounding_generator.py |
| `ROUND_RESULT` | 2 | `ROUND_RESULT\|27.94\|27.9` | place_value_rounding_generator.py |
| `ROUND_SF` | 3 | `ROUND_SF\|439/14\|2\|31` | significant_figures_generator.py |
| `ROUTH_ROW` | 2 | `ROUTH_ROW\|s^3\|1, 33` | routh_hurwitz_generator.py |
| `ROUTH_SETUP` | 1 | `ROUTH_SETUP\|p(s)=s^3+1s^2+33s+71` | routh_hurwitz_generator.py |
| `ROW` | 2 | `ROW\|b=F, j=T, r=T\|F` | foundations_critic_generator.py |
| `ROW_ENTROPY` | 2 | `ROW_ENTROPY\|H0\|649/800` | entropy_rate_markov_generator.py |
| `ROW_OP` | 1, 2 | `ROW_OP\|R2 → R2 - R1\|[0, 1, -4]` | row_reduction_generator.py, simplex_generator.py, subspace_basis_generator.py |
| `RREF_RESULT` | 2 | `RREF_RESULT\|RREF(A)\|[[1, 0, 0, 0], [0, 1, 0, 1], [0, 0, 1, -4]]` | subspace_basis_generator.py |
| `RSA_DECRYPT` | 2 | `RSA_DECRYPT\|46\|6` | rsa_generator.py |
| `RSA_ENCRYPT` | 2 | `RSA_ENCRYPT\|6\|46` | rsa_generator.py |
| `RSA_PRIVATE_KEY` | 1 | `RSA_PRIVATE_KEY\|d=27` | rsa_generator.py |
| `RSA_PUBLIC_KEY` | 2 | `RSA_PUBLIC_KEY\|n=85\|e=19` | rsa_generator.py |
| `RSA_SETUP` | 3 | `RSA_SETUP\|p=5\|q=17\|message=6` | rsa_generator.py |
| `RSQ_FORMULA` | 1 | `RSQ_FORMULA\|r^2 = Sxy^2/(Sxx·Syy)` | regression_generator.py |
| `RS_CORRECT` | 2 | `RS_CORRECT\|position=3\|[28,17,26,10]` | reed_solomon_generator.py |
| `RS_EVAL` | 2 | `RS_EVAL\|x=4\|9` | reed_solomon_generator.py |
| `RS_LINE` | 3 | `RS_LINE\|m0=13\|m1=3\|agree=3` | reed_solomon_generator.py |
| `RS_PAIR` | 2 | `RS_PAIR\|x=5,22\|y=28,17` | reed_solomon_generator.py |
| `RS_RECEIVED` | 1 | `RS_RECEIVED\|[28,17,15,10]` | reed_solomon_generator.py |
| `RS_SETUP` | 3 | `RS_SETUP\|F_31\|RS(4,2)\|points 5,22,25,30; one error allowed` | reed_solomon_generator.py |
| `RUIN_FORMULA` | 1, 2 | `RUIN_FORMULA\|(1-r^i)/(1-r^N)\|r=q/p` | random_walk_generator.py |
| `RUIN_PROB` | 2 | `RUIN_PROB\|1 − 0.5625\|0.4375` | decision_under_uncertainty_generator.py |
| `RUIN_SETUP` | 2 | `RUIN_SETUP\|biased, i=2, N=5\|p=2/3, q=1/3` | random_walk_generator.py |
| `RULE` | 2 | `RULE\|conservative df\|df = min(n1 − 1, n2 − 1)` | alternative_means_generator.py, box_plot_generator.py, discrete_posterior_generator.py, empirical_cdf_generator.py, grouped_data_generator.py, histogram_construct_generator.py, inference_setup_generator.py, linear_transform_effect_generator.py, nonparametric_test_generator.py, percentile_generator.py, scatter_plot_describe_generator.py, study_design_generator.py, two_sample_test_generator.py, two_way_table_generator.py |
| `RULE_68_95` | 2 | `RULE_68_95\|within 2σ\|95%` | empirical_rule_generator.py |
| `RULE_OF_70` | 2 | `RULE_OF_70\|5%\|14` | growth_comparison_generator.py |
| `RUNNING_TOTAL` | 3 | `RUNNING_TOTAL\|0\|8\|8` | function_properties_generator.py |
| `RV_LEVEL` | 2 | `RV_LEVEL\|X=-3\|{1, 2}` | finite_sigma_algebra_generator.py |
| `RW_MOMENTS` | 2 | `RW_MOMENTS\|E[S_n]=n(p-q)\|Var(S_n)=4npq` | random_walk_generator.py |
| `RW_PATHS` | 3 | `RW_PATHS\|u-d=-6, u+d=8\|solve\|u=1, d=7` | random_walk_generator.py |
| `RW_SETUP` | 2 | `RW_SETUP\|p=1/2, n=8\|P(S_8=-6)` | random_walk_generator.py |
| `S` | 3 | `S\|129\|80\|49` | ac_circuit_generator.py, activation_generator.py, adam_step_generator.py, angle_defect_generator.py, angle_measure_generator.py, annuity_generator.py, arc_length_generator.py, area_between_curves_generator.py, arithmetic_coding_generator.py, arithmetic_sequence_generator.py, backprop_generator.py, ballot_reflection_generator.py, bayesian_update_generator.py, bec_channel_generator.py, binomial_probability_generator.py, bisection_generator.py, black_scholes_generator.py, box_plot_generator.py, calendar_arithmetic_generator.py, calorimetry_generator.py, cantor_pairing_generator.py, casimir_force_generator.py, casimir_generator.py, channel_capacity_generator.py, cholesky_generator.py, circle_angle_generator.py, circle_equation_generator.py, classic_probability_puzzles_generator.py, clt_probability_generator.py, collision_generator.py, commutator_generator.py, complement_probability_generator.py, complex_locus_generator.py, complex_log_generator.py, complex_number_ops_generator.py, complex_quadratic_generator.py, composite_arithmetic_generator.py, conditional_expectation_generator.py, confidence_interval_generator.py, continued_fraction_generator.py, continuous_distribution_generator.py, countability_bijection_generator.py, counting_classics_generator.py, covariance_algebra_generator.py, cramers_rule_generator.py, decimal_div_generator.py, definite_integral_generator.py, density_matrix_generator.py, derangement_generator.py, determinant_generator.py, dft_generator.py, discrete_posterior_generator.py, discrete_uniform_bernoulli_generator.py, distance_formula_generator.py, distribution_of_sum_generator.py, doppler_generator.py, dot_plot_generator.py, ellipse_features_generator.py, elliptic_curve_finite_field_generator.py, embedding_similarity_generator.py, empirical_rule_generator.py, entropy_generator.py, equilibrium_ice_generator.py, estimator_bias_enum_generator.py, euler_characteristic_generator.py, euler_circuit_generator.py, euler_method_generator.py, expectation_of_function_generator.py, expected_value_generator.py, exponential_model_generator.py, extended_euclid_generator.py, finance_generator.py, finite_difference_generator.py, first_law_generator.py, fisher_information_generator.py, five_number_summary_generator.py, formula_derivation_generator.py, four_vector_generator.py, fourier_series_generator.py, fractal_iteration_generator.py, fraction_line_plot_generator.py, fraction_op_generator.py, function_inner_product_generator.py, function_operations_generator.py, fundamental_counting_principle_generator.py, fundamental_form_generator.py, game_theory_generator.py, gaussian_curvature_generator.py, generating_function_generator.py, geometric_distribution_generator.py, geometric_sequence_generator.py, geometry_in_context_generator.py, gradient_descent_generator.py, gradient_step_generator.py, graph_interpret_generator.py, graph_traversal_generator.py, grouped_data_generator.py, growth_comparison_generator.py, hamiltonian_generator.py, heat_engine_generator.py, hermitian_check_generator.py, hydrogen_atom_generator.py, hyperbola_features_generator.py, hyperbolic_distance_generator.py, hyperbolic_function_generator.py, hypercube_counting_generator.py, hypergeometric_generator.py, hypothesis_test_generator.py, inclusion_exclusion_generator.py, index_gymnastics_generator.py, inference_setup_generator.py, information_gain_generator.py, integer_puzzle_word_generator.py, integrating_factor_generator.py, interpolation_generator.py, invariant_mass_generator.py, inverse_normal_generator.py, joint_distribution_generator.py, kernel_evaluation_generator.py, kernel_ridge_generator.py, kernel_validity_generator.py, kinematics_generator.py, kmeans_step_generator.py, knn_generator.py, kraft_inequality_generator.py, ladder_operator_generator.py, lagrangian_generator.py, layer_norm_generator.py, legendre_construction_generator.py, likelihood_ratio_test_generator.py, linear_model_word_generator.py, linear_simple_generator.py, linear_transform_effect_generator.py, linearity_of_expectation_generator.py, logistic_growth_generator.py, long_division_generator.py, low_rank_approx_generator.py, lp_corner_generator.py, lr_schedule_generator.py, manual_square_root_generator.py, markov_chain_generator.py, martingale_check_generator.py, matrix_group_check_generator.py, matrix_inverse_generator.py, matrix_ops_generator.py, mean_adjustment_generator.py, mean_value_theorem_generator.py, measurement_uncertainty_generator.py, mental_strategy_generator.py, method_of_moments_generator.py, metric_arc_length_generator.py, mgf_generator.py, midpoint_generator.py, minkowski_interval_generator.py, missing_information_generator.py, mixed_number_operation_generator.py, mle_generator.py, mobius_transform_generator.py, modular_inverse_generator.py, money_life_generator.py, motion_word_generator.py, mse_decomposition_generator.py, multi_state_markov_generator.py, multi_step_word_generator.py, multinomial_probability_generator.py, mutual_information_generator.py, naive_bayes_generator.py, named_distribution_generator.py, negative_binomial_generator.py, newton_raphson_generator.py, newtons_laws_generator.py, normal_approx_binomial_generator.py, normal_table_generator.py, npv_irr_generator.py, ode_substitution_generator.py, ode_system_generator.py, optics_generator.py, optimization_generator.py, optimization_in_context_generator.py, or_formula_generator.py, order_of_operations_generator.py, order_statistics_generator.py, p_value_generator.py, parabola_features_generator.py, parametric_calculus_generator.py, particle_in_box_generator.py, pca_generator.py, percent_chain_generator.py, percent_problem_generator.py, percent_word_problem_generator.py, percentile_generator.py, permutation_group_generator.py, pgf_generator.py, ph_calculation_generator.py, piecewise_evaluation_generator.py, plausibility_critic_generator.py, pmf_cdf_quantile_generator.py, poisson_process_generator.py, polar_parametric_generator.py, pollard_factorization_generator.py, positive_definite_generator.py, probability_addition_rule_generator.py, probability_axioms_finite_generator.py, probability_critic_generator.py, probability_inequality_generator.py, probability_measure_generator.py, quadratic_residue_generator.py, quadratic_word_generator.py, quantization_generator.py, quantum_formula_generator.py, quaternion_generator.py, radical_add_sub_generator.py, radical_rationalize_generator.py, random_walk_generator.py, rate_of_change_interpret_generator.py, rational_expr_add_sub_generator.py, recurrence_generator.py, regression_generator.py, related_rates_generator.py, reliability_system_generator.py, riemann_sum_generator.py, riemann_tensor_generator.py, rotational_dynamics_generator.py, rounding_effect_generator.py, routh_hurwitz_generator.py, row_reduction_generator.py, rsa_generator.py, runge_kutta_generator.py, rv_transform_generator.py, sampling_distribution_enum_generator.py, scatter_plot_describe_generator.py, scenario_generator.py, schwarzschild_generator.py, second_order_ode_generator.py, segment_partition_generator.py, separable_pde_generator.py, series_convergence_generator.py, set_counting_generator.py, shm_generator.py, signal_arithmetic_generator.py, slope_inference_generator.py, slope_two_points_generator.py, softmax_gradient_generator.py, solid_revolution_generator.py, spatial_description_generator.py, spatial_packing_generator.py, special_relativity_generator.py, spherical_excess_generator.py, spin_half_generator.py, standard_deviation_generator.py, standing_wave_generator.py, stars_and_bars_generator.py, statics_generator.py, stem_and_leaf_generator.py, stereographic_generator.py, sufficiency_factorization_generator.py, systems_word_generator.py, t_interval_generator.py, tally_frequency_generator.py, taxicab_geometry_generator.py, taylor_series_generator.py, telescoping_generator.py, temperature_conversion_generator.py, tip_bill_split_generator.py, totient_generator.py, transformation_generator.py, transportation_generator.py, triangle_solve_generator.py, trig_identity_eval_generator.py, trig_six_functions_generator.py, two_sample_test_generator.py, two_way_table_generator.py, two_way_table_probability_generator.py, type_error_power_generator.py, undetermined_coeff_generator.py, unit_circle_generator.py, vector_ops_generator.py, venn_probability_generator.py, venn_region_count_generator.py, weighted_mean_generator.py, work_rate_generator.py, z_score_generator.py |
| `SAMPLE_ENUM` | 2, 4 | `SAMPLE_ENUM\|{15, 15}\|x̄=15` | estimator_bias_enum_generator.py, mse_decomposition_generator.py, sampling_distribution_enum_generator.py |
| `SAMPLE_MOMENT` | 2 | `SAMPLE_MOMENT\|xbar\|43/9` | method_of_moments_generator.py |
| `SAMPLE_SIZE_FORMULA` | 1 | `SAMPLE_SIZE_FORMULA\|n = (z*·σ/E)^2` | confidence_interval_generator.py |
| `SAMPLE_SPACE` | 1, 2, 3 | `SAMPLE_SPACE\|coin × spinner\|H65, H91, H98, T65, T91, T98\|6` | classic_probability_puzzles_generator.py, sample_space_list_generator.py |
| `SAMPLE_VALUE` | 2 | `SAMPLE_VALUE\|1\|3` | monte_carlo_arithmetic_generator.py |
| `SAMP_DIST_SETUP` | 2 | `SAMP_DIST_SETUP\|μ = 268, σ = 65, n = 169\|sampling distribution of x̄` | clt_probability_generator.py |
| `SA_BASES` | 2 | `SA_BASES\|2π(19)² = 2π × 361\|722π` | volume_3d_generator.py |
| `SA_FACES` | 3 | `SA_FACES\|top/bottom\|9 × 8\|72` | volume_3d_generator.py |
| `SA_FORMULA` | 1 | `SA_FORMULA\|SA = 2(lw + lh + wh)` | round_solids_generator.py, volume_3d_generator.py |
| `SA_LATERAL` | 2 | `SA_LATERAL\|2π × 19 × 9\|342π` | volume_3d_generator.py |
| `SA_SETUP` | 2 | `SA_SETUP\|rectangular_prism\|l=9, w=8, h=12` | volume_3d_generator.py |
| `SA_TOTAL` | 2 | `SA_TOTAL\|SA = 2(72 + 108 + 96)\|552` | round_solids_generator.py, volume_3d_generator.py |
| `SB_FORMULA` | 1 | `SB_FORMULA\|C(n-1, k-1)` | stars_and_bars_generator.py |
| `SB_SETUP` | 2 | `SB_SETUP\|x1+...+x3 = 27\|xi >= 1` | stars_and_bars_generator.py |
| `SCALE_DIV` | 3 | `SCALE_DIV\|5580\|124\|45` | scaling_generator.py |
| `SCALE_EXACT` | 2 | `SCALE_EXACT\|8*cos\|4sqrt2` | de_moivre_generator.py, euler_formula_generator.py |
| `SCALE_IDENTIFY` | 2 | `SCALE_IDENTIFY\|4.5 centimeters\|actual_dimension` | scaling_generator.py |
| `SCALE_LAW` | 2 | `SCALE_LAW\|area\|k² = 10000` | square_cube_law_generator.py |
| `SCALE_MODE` | 3 | `SCALE_MODE\|λ = -8\|(-64)\|-64` | diagonalization_generator.py |
| `SCALE_MULT` | 3 | `SCALE_MULT\|4.5\|14\|63` | scaling_generator.py |
| `SCALE_SETUP` | 3 | `SCALE_SETUP\|1 centimeter\|14 meters\|14` | scaling_generator.py |
| `SCALE_SHIFT` | 2 | `SCALE_SHIFT\|1\|-4` | layer_norm_generator.py |
| `SCALING_COMPUTE` | 2 | `SCALING_COMPUTE\|6ND\|14070000000000000000` | scaling_law_generator.py |
| `SCALING_SETUP` | 3 | `SCALING_SETUP\|N=35000000\|D=67000000000\|F=64000000000000000` | scaling_law_generator.py |
| `SCAN` | 2 | `SCAN\|(\|parenthesis depth 1` | wff_parsing_generator.py |
| `SCHWARZSCHILD_SETUP` | 3, 4 | `SCHWARZSCHILD_SETUP\|time_dilation\|r_s=96\|r=150` | schwarzschild_generator.py |
| `SCI_IDENTIFY` | 2 | `SCI_IDENTIFY\|1.09\|11` | exponent_generator.py |
| `SCI_MOVE_DECIMAL` | 2 | `SCI_MOVE_DECIMAL\|left\|11` | exponent_generator.py |
| `SCI_OPERATION` | 4 | `SCI_OPERATION\|multiply_coefficients\|1.6\|8.7\|13.92` | exponent_generator.py |
| `SCI_SETUP` | 1 | `SCI_SETUP\|109000000000` | exponent_generator.py |
| `SCORE_EQ` | 1 | `SCORE_EQ\|36/lambda=8` | mle_generator.py |
| `SEARCH_BOUNDS` | 3 | `SEARCH_BOUNDS\|iter 1\|lo=0\|hi=6` | algorithm_trace_generator.py |
| `SEARCH_STATE` | 2 | `SEARCH_STATE\|lo=4\|hi=6` | algorithm_trace_generator.py |
| `SECOND_DERIV_TEST` | 2 | `SECOND_DERIV_TEST\|f''(2) = -6 < 0\|local maximum at x = 2` | curve_analysis_generator.py, optimization_generator.py |
| `SECOND_PARTIAL` | 2 | `SECOND_PARTIAL\|f_xx\|-2` | hessian_classify_generator.py |
| `SECTION_FORMULA` | 1 | `SECTION_FORMULA\|P = (x1 + m/(m+n)·(x2 - x1), y1 + m/(m+n)·(y2 - y1))` | segment_partition_generator.py |
| `SECTION_SETUP` | 2 | `SECTION_SETUP\|A(-3, -2), B(21, 4); ratio 3:3 from A\|point P` | segment_partition_generator.py |
| `SECTOR_FORMULA` | 1 | `SECTOR_FORMULA\|A = (θ/360)·πr^2` | arc_sector_generator.py |
| `SELECT_MIN` | 2 | `SELECT_MIN\|B\|0` | dijkstra_generator.py |
| `SEPARATE` | 1, 2 | `SEPARATE\|y^(-2) dy = dx` | ode_substitution_generator.py, separable_ode_generator.py, separable_pde_generator.py |
| `SEPARATOR` | 3 | `SEPARATOR\|16/11\|in L(3/2)\|not in L(√2)` | dedekind_cut_generator.py |
| `SEQUENCE_FORMULA` | 2 | `SEQUENCE_FORMULA\|multiply probabilities in the stated order\|equal symbols may be grouped as powers` | multinomial_probability_generator.py |
| `SEQ_APPLY` | 1 | `SEQ_APPLY\|24 = -6 + (n - 1)·2` | arithmetic_sequence_generator.py, geometric_sequence_generator.py, recursive_explicit_generator.py |
| `SEQ_FORMULA` | 1 | `SEQ_FORMULA\|a_n = a_1 + (n - 1)d` | arithmetic_sequence_generator.py, geometric_sequence_generator.py, recursive_explicit_generator.py |
| `SEQ_SETUP` | 2 | `SEQ_SETUP\|-6, -4, -2, 0, ...\|which term equals 24` | arithmetic_sequence_generator.py, geometric_sequence_generator.py, recursive_explicit_generator.py |
| `SERIES` | 1 | `SERIES\|G=G1*G2` | transfer_function_generator.py |
| `SERIES_ASSUME` | 2 | `SERIES_ASSUME\|y\|sum a_n x^n` | series_solution_generator.py |
| `SERIES_GROUP` | 2 | `SERIES_GROUP\|even powers\|cos(theta)I` | lie_exponential_generator.py |
| `SERIES_PAIR` | 2 | `SERIES_PAIR\|1 + 86\|87` | formula_derivation_generator.py |
| `SERIES_SETUP` | 2 | `SERIES_SETUP\|Σ (-1)^(n+1)·1/n^5, n ≥ 1\|absolutely convergent, conditionally convergent, or divergent?` | legendre_construction_generator.py, power_series_generator.py, series_convergence_generator.py |
| `SERIES_TERM` | 3 | `SERIES_TERM\|n=0\|1\|1` | grassmann_generator.py |
| `SETUP` | 1, 2 | `SETUP\|assume u is the greatest integer; consider u + 1` | direct_proof_algebra_generator.py, induction_verify_generator.py, weighted_mean_generator.py |
| `SETUP_PERCENT_EQ` | 1 | `SETUP_PERCENT_EQ\|percent_dec = 1904 / 3400` | percent_problem_generator.py |
| `SET_SETUP` | 2, 3, 4 | `SET_SETUP\|A = {k}\|B = {d}\|A ∪ B` | set_expression_generator.py, set_operations_generator.py |
| `SET_SIDE` | 2 | `SET_SIDE\|left\|∅` | counterexample_search_generator.py |
| `SE_FORMULA` | 1 | `SE_FORMULA\|SE(x̄) = σ/√n` | clt_probability_generator.py, slope_inference_generator.py, t_interval_generator.py |
| `SHAPE` | 1 | `SHAPE\|universal restriction → implication` | english_to_logic_generator.py |
| `SHIFT` | 1, 2 | `SHIFT\|yi = xi - 1\|y1+...+y3 = 24` | algorithm_trace_generator.py, recurrence_generator.py, stars_and_bars_generator.py, z_transform_generator.py |
| `SHM_FORMULA` | 1 | `SHM_FORMULA\|omega^2=k/m` | shm_generator.py |
| `SHM_SETUP` | 3 | `SHM_SETUP\|mass_spring_energy\|m=7, k=63\|A=10, x=8` | shm_generator.py |
| `SHORTEST` | 2 | `SHORTEST\|(1,-4)\|norm^2=17` | lll_reduction_generator.py |
| `SHRINK_FACTOR` | 2 | `SHRINK_FACTOR\|20%/10%\|2` | statistical_literacy_generator.py |
| `SIDE` | 2 | `SIDE\|left\|∈` | set_identity_membership_table_generator.py |
| `SIGFIG` | 3 | `SIGFIG\|1.4896\|5\|the power of ten does not change the digit count` | significant_figures_generator.py |
| `SIGFIG_ROUND` | 3 | `SIGFIG_ROUND\|240000\|2 significant figures\|2.4 × 10^5` | fermi_estimation_generator.py |
| `SIGMA_EXPAND` | 1 | `SIGMA_EXPAND\|(-8) + (-4) + 0` | sigma_notation_generator.py |
| `SIGMA_GEN` | 2 | `SIGMA_GEN\|generators\|{1}; {2, 3}; {4, 5}` | finite_sigma_algebra_generator.py |
| `SIGMA_SETUP` | 2 | `SIGMA_SETUP\|Σ_(k=-3)^(-1) (4k + 4)\|expand and evaluate` | sigma_notation_generator.py |
| `SIGMA_TERM` | 3 | `SIGMA_TERM\|k=-3\|4(-3) + 4\|-8` | sigma_notation_generator.py |
| `SIGN` | 2, 3 | `SIGN\|left\|-24\|negative` | bisection_generator.py, covariance_correlation_generator.py, qualitative_reasoning_generator.py |
| `SIGNAL_SETUP` | 2, 3 | `SIGNAL_SETUP\|sampling\|f_max=1655 Hz\|f_s=4687 Hz` | signal_arithmetic_generator.py |
| `SIGN_CHART` | 2 | `SIGN_CHART\|critical values\|-7, 8` | polynomial_inequality_generator.py |
| `SIGN_ROW` | 3 | `SIGN_ROW\|pair 1\|+7\|+` | nonparametric_test_generator.py |
| `SIGN_RULE` | 2 | `SIGN_RULE\|arctan of a negative\|negative angle` | trig_equation_generator.py, trig_identity_eval_generator.py, trig_six_functions_generator.py, unit_circle_generator.py |
| `SIGN_TEST` | 4 | `SIGN_TEST\|(-inf, -10)\|y = -11\|f(y) = -17 (negative)\|down` | stability_generator.py |
| `SIMILAR_APPLY` | 3 | `SIMILAR_APPLY\|6\|4\|24` | scaling_generator.py |
| `SIMILAR_SCALE` | 3 | `SIMILAR_SCALE\|45\|9\|5` | scaling_generator.py |
| `SIMILAR_SETUP` | 3 | `SIMILAR_SETUP\|square\|9\|45` | scaling_generator.py |
| `SIMPLEX_SETUP` | 3 | `SIMPLEX_SETUP\|max z=6x+y\|x<=4\|y<=15` | simplex_generator.py |
| `SIM_SETUP` | 2 | `SIM_SETUP\|△ABC ~ △DEF; DE = 9, AB = 6, EF = 12\|find BC` | similar_triangles_generator.py |
| `SIN` | 2 | `SIN\|pi\|0` | positional_encoding_generator.py |
| `SINGULAR_VALUE` | 2 | `SINGULAR_VALUE\|sigma1\|19` | low_rank_approx_generator.py |
| `SINUSOID_SETUP` | 2 | `SINUSOID_SETUP\|y = -3sin(2(x - 30°)) - 5\|amplitude, period, phase shift, midline` | sinusoid_features_generator.py |
| `SIZE_REDUCE` | 2 | `SIZE_REDUCE\|b2=(-12, 11)\|b2-1b1=(2, 15)` | lll_reduction_generator.py |
| `SLOPE_CALC` | 2 | *(not observed in sampling)* | equation_from_two_points_generator.py |
| `SLOPE_FORMULA` | 1 | `SLOPE_FORMULA\|m = (y2 - y1) / (x2 - x1)` | equation_from_two_points_generator.py, regression_generator.py, slope_two_points_generator.py |
| `SLOPE_INT_IDENTIFY` | 2 | `SLOPE_INT_IDENTIFY\|Slope (m)\|0` | slope_intercept_form_generator.py |
| `SLOPE_INT_MATCH` | 2 | `SLOPE_INT_MATCH\|Compare to Slope-Intercept Form\|y = mx + b` | slope_intercept_form_generator.py |
| `SLOPE_INT_SETUP` | 1 | `SLOPE_INT_SETUP\|y = -9` | slope_intercept_form_generator.py |
| `SLOPE_RESULT` | 1 | `SLOPE_RESULT\|2/3` | equation_from_two_points_generator.py |
| `SLOPE_SETUP` | 2 | `SLOPE_SETUP\|(0, 0)\|(0, 5)` | slope_two_points_generator.py |
| `SLOPE_SUBST` | 1 | `SLOPE_SUBST\|m = (5 - 0) / (0 - 0)` | equation_from_two_points_generator.py, slope_two_points_generator.py |
| `SLOPE_UNDEFINED` | 1 | `SLOPE_UNDEFINED\|Division by zero` | slope_two_points_generator.py |
| `SOFTMAX_EXP` | 2 | `SOFTMAX_EXP\|1,1\|1` | attention_generator.py, softmax_gradient_generator.py |
| `SOFTMAX_PROB` | 2 | `SOFTMAX_PROB\|1\|1/2` | softmax_gradient_generator.py |
| `SOFTMAX_SETUP` | 3 | `SOFTMAX_SETUP\|z=(1*ln(9),1*ln(7),1*ln(2))\|T=1\|target=1` | softmax_gradient_generator.py |
| `SOFTMAX_WEIGHT` | 2 | `SOFTMAX_WEIGHT\|1,1\|1/3` | attention_generator.py |
| `SOLID_MATCH` | 2 | `SOLID_MATCH\|1 square and 4 identical triangles\|square pyramid` | spatial_description_generator.py |
| `SOLUTIONS` | 2 | `SOLUTIONS\|cos x = 0\|90°, 270°, 450°, 630°, 810°, 990°, 1170°, 1350°, 1530°, 1710°, 1890°, 2070°, 2250°, 2430°, 2610°, 2790°` | trig_equation_generator.py |
| `SOLUTION_FORMULA` | 1 | `SOLUTION_FORMULA\|M_final=(Ma*Va+Mb*Vb)/(Va+Vb)` | solution_chem_generator.py |
| `SOLUTION_SETUP` | 3 | `SOLUTION_SETUP\|mixing_molarity\|Ma=3, Va=24\|Mb=8, Vb=105` | solution_chem_generator.py |
| `SOLVE_CONST` | 2 | `SOLVE_CONST\|C1 = 1\|C2 = 3` | ode_system_generator.py, second_order_ode_generator.py, undetermined_coeff_generator.py |
| `SOLVE_U` | 2 | `SOLVE_U\|e^(-2x)u = 2e^(-2x) + C\|u = 2 + Ce^(2x)` | ode_substitution_generator.py |
| `SOLVE_Y` | 2 | `SOLVE_Y\|e^(2x)y = 4e^(2x) + C\|y = 4 + Ce^(-2x)` | integrating_factor_generator.py, laplace_ivp_generator.py, ode_substitution_generator.py |
| `SOL_ENTRY` | 3 | `SOL_ENTRY\|x1(t)\|(e^t)*(-6) + (0)*5\|-6*e^t` | matrix_exponential_generator.py |
| `SOL_FORM` | 1, 2 | `SOL_FORM\|y = (C1 + C2x)e^(-2x)` | ode_system_generator.py, second_order_ode_generator.py, undetermined_coeff_generator.py, variation_parameters_generator.py |
| `SORT` | 1, 2 | `SORT\|11,12,7,18,10,20\|7,10,11,12,18,20` | alternative_means_generator.py, dot_plot_generator.py, empirical_cdf_generator.py, five_number_summary_generator.py, graph_interpret_generator.py, histogram_construct_generator.py, linear_transform_effect_generator.py, mean_adjustment_generator.py, method_discrimination_generator.py, nonparametric_test_generator.py, percentile_generator.py, simple_stats_generator.py, stem_and_leaf_generator.py |
| `SORT_EDGES` | 1 | `SORT_EDGES\|CD=18, BC=19, AB=21, BD=22` | mst_generator.py |
| `SPECIAL_SOLUTION` | 2 | `SPECIAL_SOLUTION\|12 = 10\|contradiction: no value of x works` | radical_equation_generator.py, special_solution_equation_generator.py |
| `SPEED` | 2, 3 | `SPEED\|sqrt(a^2 + b^2)\|sqrt(7^2 + 24^2)\|25` | curve_geometry_generator.py |
| `SPHERICAL_BOUNDS` | 2 | `SPHERICAL_BOUNDS\|rho\|0..7` | triple_integral_generator.py |
| `SPHERICAL_CONVERT` | 2 | `SPHERICAL_CONVERT\|1 dV\|rho^2*sin(phi) drho dphi dtheta` | triple_integral_generator.py |
| `SPHERICAL_COSINES` | 1 | `SPHERICAL_COSINES\|cos(c)=sin(lat1)sin(lat2)+cos(lat1)cos(lat2)cos(dlon)` | great_circle_generator.py |
| `SPHERICAL_COSINE_LAW` | 1 | `SPHERICAL_COSINE_LAW\|cos(a)=cos(b)cos(c)+sin(b)sin(c)cos(A)` | spherical_triangle_generator.py |
| `SPHERICAL_EXCESS_SETUP` | 2 | `SPHERICAL_EXCESS_SETUP\|R=15\|angles=135,45,45` | spherical_excess_generator.py |
| `SPHERICAL_SINE_LAW` | 1 | `SPHERICAL_SINE_LAW\|sin(A)/sin(a)=sin(B)/sin(b)` | spherical_triangle_generator.py |
| `SPHERICAL_TRIANGLE_SETUP` | 2 | `SPHERICAL_TRIANGLE_SETUP\|b=90 deg, c=90 deg, A=90 deg\|find cos(a)` | spherical_triangle_generator.py |
| `SPIN_COMPONENT` | 2 | `SPIN_COMPONENT\|row=1\|-12i/13` | spin_half_generator.py |
| `SPIN_SETUP` | 3 | `SPIN_SETUP\|measurement_probability\|axis=z\|psi=[-80/89,39/89]` | spin_half_generator.py |
| `SPLIT_MIDDLE` | 2 | `SPLIT_MIDDLE\|5y = 4y + y\|4y^2 + 4y + y + 1` | factor_trinomial_generator.py |
| `SPLIT_SETUP` | 3 | `SPLIT_SETUP\|texture\|left pos=8, neg=0\|right pos=6, neg=2` | information_gain_generator.py |
| `SQRT_BOTH_SIDES` | 2 | `SQRT_BOTH_SIDES\|x^2 = 5113\|x = ±√5113` | completing_square_generator.py, quadratic_square_root_generator.py, rational_equation_generator.py |
| `SQRT_DIGIT` | 2 | `SQRT_DIGIT\|2\|root = 2` | manual_square_root_generator.py |
| `SQRT_NEG` | 2 | `SQRT_NEG\|√(-5184)\|72i` | complex_quadratic_generator.py, polynomial_zeros_generator.py |
| `SQRT_SETUP` | 2 | `SQRT_SETUP\|N = 45369\|groups 04, 53, 69` | manual_square_root_generator.py |
| `SQRT_TRIAL` | 3 | `SQRT_TRIAL\|x = 2\|(0 + 2)*2 = 4\|fits` | manual_square_root_generator.py |
| `SQUARE_BOTH_SIDES` | 2 | `SQUARE_BOTH_SIDES\|√(2x - 2) = x - 1\|2x - 2 = (x - 1)^2` | radical_equation_generator.py |
| `SQUARE_FACTOR` | 3 | `SQUARE_FACTOR\|280\|4 × 70\|4` | radical_add_sub_generator.py, radical_multiply_generator.py, radical_rationalize_generator.py, radical_variable_simplify_generator.py |
| `SQUARE_TEST` | 3 | `SQUARE_TEST\|169\|13^2 = 169\|perfect square` | discriminant_generator.py |
| `SS_BETWEEN` | 2 | `SS_BETWEEN\|4·((68 − 80)^2 + (72 − 80)^2 + (88 − 80)^2 + (92 − 80)^2)\|1664` | anova_generator.py |
| `SS_WITHIN` | 2 | `SS_WITHIN\|20 + 4 + 4 + 20\|48` | anova_generator.py |
| `STABILITY` | 3 | `STABILITY\|y=-10\|left down, right up\|unstable` | stability_generator.py |
| `STANDING_BOUNDARY` | 1 | `STANDING_BOUNDARY\|closed-open pipe uses h=2k-1` | standing_wave_generator.py |
| `STANDING_FORMULA` | 1 | `STANDING_FORMULA\|lambda=4L/h, f=v/lambda` | standing_wave_generator.py |
| `STANDING_SETUP` | 3 | `STANDING_SETUP\|closed_pipe\|k=3\|L=9, v=100` | standing_wave_generator.py |
| `STATEMENT_EVAL` | 3 | `STATEMENT_EVAL\|Theo says at least one of Theo and Quin is a knight\|T\|consistent` | knights_knaves_generator.py |
| `STATICS_FORMULA` | 1 | `STATICS_FORMULA\|sum_tau_left=0 => RB*L=W*x` | statics_generator.py |
| `STATICS_SETUP` | 3 | `STATICS_SETUP\|supported_beam\|W=173, L=18\|x=4` | statics_generator.py |
| `STATIONARY` | 2 | `STATIONARY\|pi0=2/3\|pi1=1/3` | entropy_rate_markov_generator.py |
| `STAT_ABS_DEV` | 2 | `STAT_ABS_DEV\|8\|8` | statistics_generator.py |
| `STAT_AVERAGE` | 2 | `STAT_AVERAGE\|(48 + 50) / 2\|49` | statistics_generator.py |
| `STAT_COUNT` | 1 | `STAT_COUNT\|5` | grouped_data_generator.py, statistics_generator.py |
| `STAT_DEVIATION` | 3 | `STAT_DEVIATION\|44\|36\|8` | statistics_generator.py |
| `STAT_DIVIDE` | 2 | `STAT_DIVIDE\|305 / 5\|61` | statistics_generator.py |
| `STAT_FREQUENCY` | 2 | `STAT_FREQUENCY\|31\|1` | statistics_generator.py |
| `STAT_MAD` | 3 | `STAT_MAD\|40\|5\|8` | statistics_generator.py |
| `STAT_MAX` | 1 | `STAT_MAX\|95` | statistics_generator.py |
| `STAT_MEAN` | 2 | `STAT_MEAN\|180 / 5\|36` | statistics_generator.py |
| `STAT_MIDDLE` | 2 | `STAT_MIDDLE\|position 5\|49` | statistics_generator.py |
| `STAT_MIN` | 1 | `STAT_MIN\|33` | statistics_generator.py |
| `STAT_MODE` | 2 | `STAT_MODE\|No mode\|All values appear with same frequency` | statistics_generator.py |
| `STAT_ORDER` | 1 | `STAT_ORDER\|17, 28, 30, 48, 49, 57, 57, 59, 95` | statistics_generator.py |
| `STAT_RANGE` | 2 | `STAT_RANGE\|95 - 33\|62` | statistics_generator.py |
| `STAT_SETUP` | 1, 2 | `STAT_SETUP\|71, 48, 79, 62, 45` | alternative_means_generator.py, box_plot_generator.py, covariance_correlation_generator.py, dot_plot_generator.py, fraction_line_plot_generator.py, histogram_construct_generator.py, linear_transform_effect_generator.py, mean_adjustment_generator.py, percentile_generator.py, population_sample_generator.py, sampling_distribution_enum_generator.py, scatter_plot_describe_generator.py, standard_deviation_generator.py, statistics_generator.py, stem_and_leaf_generator.py, tally_frequency_generator.py, two_way_table_generator.py, weighted_mean_generator.py |
| `STAT_SUM` | 2 | `STAT_SUM\|71 + 48 + 79 + 62 + 45\|305` | statistics_generator.py |
| `STD` | 1 | `STD\|10` | layer_norm_generator.py |
| `STEADY_EQUATION` | 2 | `STEADY_EQUATION\|pi0*pi01=pi1*pi10\|pi0+pi1=1` | markov_chain_generator.py, multi_state_markov_generator.py |
| `STEM_ROW` | 3 | `STEM_ROW\|4\|2 3 4\|42,43,44` | stem_and_leaf_generator.py |
| `STEPPING_STONE` | 2 | `STEPPING_STONE\|enter x21\|+x21 -x22 +x12 -x11` | transportation_generator.py |
| `STEREO_SETUP` | 3, 4 | `STEREO_SETUP\|sphere_to_plane\|X=36/101\|Y=16/101\|Z=93/101` | stereographic_generator.py |
| `STIRLING_CELL` | 3 | `STIRLING_CELL\|S(1,1)\|1×0+1\|1` | set_counting_generator.py |
| `STMT_EVAL` | 3 | `STMT_EVAL\|p\|29 is prime\|T` | logical_connective_eval_generator.py |
| `STOICH_RATIO` | 2 | `STOICH_RATIO\|CO->CO2\|2/2=1` | gas_stoichiometry_generator.py, stoichiometry_generator.py |
| `STOICH_SETUP` | 2, 3 | `STOICH_SETUP\|balance_equation\|Al + O2 -> Al2O3` | stoichiometry_generator.py |
| `STP_TERM` | 2 | `STP_TERM\|k=1\|1` | expected_value_classics_generator.py |
| `STRATEGY` | 2 | `STRATEGY\|distributive split\|67 = 60 + 7` | mental_strategy_generator.py |
| `STRUCTURE_CONSTANT` | 3 | `STRUCTURE_CONSTANT\|epsilon_yzx\|1\|-117iJx` | structure_constant_generator.py |
| `STRUCTURE_SETUP` | 3 | `STRUCTURE_SETUP\|A=-9Jy\|B=13Jz\|epsilon_yzx=1` | structure_constant_generator.py |
| `SU3_SETUP` | 2 | `SU3_SETUP\|left=3bar\|right=3bar` | young_tableaux_generator.py |
| `SUBEXPR` | 2 | `SUBEXPR\|A ∪ B\|{c, d, f}` | probability_measure_generator.py, set_expression_generator.py, set_operations_generator.py |
| `SUBGROUP` | 2 | `SUBGROUP\|H={e, r2s}\|size 2` | coset_generator.py |
| `SUBGROUP_ELEM` | 2 | `SUBGROUP_ELEM\|k=1\|14` | coset_generator.py, cyclic_group_generator.py |
| `SUBGROUP_RATE` | 3 | `SUBGROUP_RATE\|in-state\|A\|21/30 = 70%` | simpsons_paradox_generator.py |
| `SUBGROUP_START` | 2 | `SUBGROUP_START\|H=<16>\|identity 0` | coset_generator.py |
| `SUBPROOF_CLOSE` | 3 | `SUBPROOF_CLOSE\|→I\|lines 2–3\|d → (p ∧ d)` | natural_deduction_generator.py |
| `SUBPROOF_OPEN` | 2 | `SUBPROOF_OPEN\|assume\|d` | natural_deduction_generator.py |
| `SUBSET_CHECK` | 3 | `SUBSET_CHECK\|24\|in B?\|yes` | set_membership_subset_generator.py |
| `SUBSET_SIZE` | 2 | `SUBSET_SIZE\|0\|∅` | set_operations_generator.py |
| `SUBST` | 2, 3 | `SUBST\|s\|1\|19/8` | arc_length_generator.py, chain_rule_generator.py, curve_analysis_generator.py, derivative_limit_def_generator.py, evaluate_expression_generator.py, function_composition_generator.py, function_evaluation_generator.py, function_operations_generator.py, function_table_generator.py, implicit_diff_generator.py, integer_puzzle_word_generator.py, integrating_factor_generator.py, legendre_construction_generator.py, lhopital_generator.py, limit_evaluation_generator.py, line_integral_generator.py, linear_approx_generator.py, log_diff_higher_order_generator.py, logistic_growth_generator.py, mean_value_theorem_generator.py, ode_substitution_generator.py, optimization_generator.py, parametric_calculus_generator.py, partial_fractions_generator.py, pgf_generator.py, piecewise_evaluation_generator.py, polar_parametric_generator.py, power_series_generator.py, recursive_explicit_generator.py, related_rates_generator.py, remainder_factor_theorem_generator.py, second_order_ode_generator.py, separable_ode_generator.py, systems_word_generator.py, tangent_line_generator.py, taylor_series_generator.py, trig_equation_generator.py, u_substitution_generator.py, undetermined_coeff_generator.py |
| `SUBSTITUTE` | 2, 3 | `SUBSTITUTE\|L3\|p := ¬k; q := n → j\|(¬¬k → ¬(n → j)) → ((n → j) → ¬k)` | hilbert_axiom_derivation_generator.py, lambda_reduction_generator.py |
| `SUBSTITUTION` | 2 | `SUBSTITUTION\|u = y^(-1)\|u' = -y^(-2) dy/dx` | ode_substitution_generator.py |
| `SUB_COL` | 3 | `SUB_COL\|col_1\|8-8-borrow0\|->0 (borrow_out 0)` | multi_digit_subtraction_generator.py |
| `SUFFICIENT` | 2 | `SUFFICIENT\|T(x) = T(y) = Σx_i\|3` | sufficiency_factorization_generator.py |
| `SUM` | 2, 3 | `SUM\|9 + 49 + 17\|75` | anova_generator.py, bayesian_update_generator.py, covariance_correlation_generator.py, discrete_posterior_generator.py, estimator_bias_enum_generator.py, experimental_probability_generator.py, likelihood_language_generator.py, likelihood_ratio_test_generator.py, method_of_moments_generator.py, mle_generator.py, mse_decomposition_generator.py, random_digit_simulation_generator.py, regression_generator.py, reliability_system_generator.py, scatter_plot_describe_generator.py, slope_inference_generator.py, standard_deviation_generator.py, study_design_generator.py, sufficiency_factorization_generator.py, t_interval_generator.py |
| `SUM_ORDER` | 2 | `SUM_ORDER\|Σ i^4\|n^5` | master_theorem_generator.py |
| `SUPPLIER_ALLOCATE` | 3 | `SUPPLIER_ALLOCATE\|supplier A\|0\|capacity 61` | optimization_in_context_generator.py |
| `SUPPORT` | 2 | `SUPPORT\|0<=x<=12\|0<=y<=144` | rv_transform_generator.py |
| `SUPPORT_TERM` | 2 | `SUPPORT_TERM\|1\|(-12,0)` | svm_margin_generator.py |
| `SURVIVE_PROB` | 2 | `SURVIVE_PROB\|(1 − 0.25)^2\|0.5625` | decision_under_uncertainty_generator.py |
| `SVM_SETUP` | 3 | `SVM_SETUP\|x1=(-12,0),y1=1,alpha1=1\|x2=(0,5),y2=-1,alpha2=1\|b=5,x=(-5,-4)` | svm_margin_generator.py |
| `SWAP` | 2 | `SWAP\|norm b2=17\|norm b1=260` | lll_reduction_generator.py |
| `SWAP_VARS` | 1 | `SWAP_VARS\|x = y^3 - 5` | inverse_function_generator.py |
| `SYMBOL_CODE` | 2 | `SYMBOL_CODE\|¬\|7` | godel_numbering_generator.py |
| `SYMMETRIC_CHECK` | 3 | `SYMMETRIC_CHECK\|(12, 12)\|reverse (12, 12)\|present` | equivalence_relation_generator.py, relation_check_generator.py |
| `SYMMETRY` | 2 | `SYMMETRY\|odd function\|a0=0, a_n=0` | fourier_series_generator.py |
| `SYNDIV_SETUP` | 2 | `SYNDIV_SETUP\|x^4 - 5x^3 + x^2 + 5x + 2\|r = 1` | polynomial_zeros_generator.py, synthetic_division_generator.py |
| `SYNDROME_CALC` | 2 | `SYNDROME_CALC\|s1=b1 xor b3 xor b5 xor b7\|0 xor 1 xor 1 xor 1=1` | hamming_code_generator.py |
| `SYNDROME_VALUE` | 2 | `SYNDROME_VALUE\|s1=1, s2=0, s4=0\|position=1` | hamming_code_generator.py |
| `SYN_DROP` | 1 | `SYN_DROP\|1` | horner_evaluation_generator.py, polynomial_zeros_generator.py, synthetic_division_generator.py |
| `SYN_ROW` | 1 | `SYN_ROW\|1, -4, -3, 2, 4` | polynomial_zeros_generator.py, synthetic_division_generator.py |
| `SYSTEMATIC_PICK` | 2 | `SYSTEMATIC_PICK\|1\|3` | study_design_generator.py |
| `SYS_ADD` | 1 | `SYS_ADD\|Add equations: -4x = -16` | systems_elimination_generator.py |
| `SYS_EQ_NEW` | 1 | `SYS_EQ_NEW\|New equation with y only` | systems_substitution_generator.py |
| `SYS_ISOLATE` | 2 | `SYS_ISOLATE\|Isolate x in Eq 1\|x = -3y + 19` | systems_substitution_generator.py |
| `SYS_MULT` | 1 | `SYS_MULT\|Eq2 * -1` | systems_elimination_generator.py |
| `SYS_REWRITE` | 2 | `SYS_REWRITE\|-4x + 5y = 46\|3x - 5y = -37` | systems_elimination_generator.py |
| `SYS_SETUP` | 2 | `SYS_SETUP\|x = -4y + 13\|-5x + 4y = -17` | systems_elimination_generator.py, systems_substitution_generator.py |
| `SYS_SUBST` | 1 | `SYS_SUBST\|Substitute (-4y + 13) for x in Eq 2` | systems_substitution_generator.py |
| `SYS_SUBST_BACK` | 1 | `SYS_SUBST_BACK\|Substitute y=2 into Eq 1` | systems_elimination_generator.py, systems_substitution_generator.py |
| `TABLEAU` | 2, 3 | `TABLEAU\|initial\|s1: x + s1 = 4\|s2: y + s2 = 15` | simplex_generator.py |
| `TABLEAU_ROOT` | 1 | `TABLEAU_ROOT\|(g ∧ (¬f ∨ ¬f)) ∨ (g ∨ t)` | semantic_tableau_generator.py |
| `TABLEAU_RULE` | 3 | `TABLEAU_RULE\|3bar x 3bar\|two antiboxes split into symmetric plus antisymmetric\|6bar + 3` | young_tableaux_generator.py |
| `TABLE_CELL` | 2 | `TABLE_CELL\|route=bus, shift=day\|7` | independence_check_generator.py, two_way_table_generator.py, two_way_table_probability_generator.py |
| `TABLE_COMPARE` | 1, 2 | `TABLE_COMPARE\|match` | foundations_critic_generator.py, set_identity_membership_table_generator.py |
| `TABLE_DIFF` | 2 | `TABLE_DIFF\|1\|+17` | representation_translation_generator.py |
| `TABLE_ENTRY` | 2 | `TABLE_ENTRY\|g(0)\|2` | euler_method_generator.py, function_table_generator.py, taylor_series_generator.py |
| `TABLE_LOOKUP` | 2 | `TABLE_LOOKUP\|F(43)\|7/8` | clt_probability_generator.py, de_moivre_generator.py, dot_product_generator.py, euler_formula_generator.py, function_evaluation_generator.py, lie_exponential_generator.py, normal_approx_binomial_generator.py, normal_table_generator.py, p_value_generator.py, pascal_triangle_generator.py, pmf_cdf_quantile_generator.py, polar_parametric_generator.py, right_triangle_trig_generator.py, triangle_solve_generator.py, trig_equation_generator.py, trig_identity_eval_generator.py, type_error_power_generator.py, unit_circle_generator.py |
| `TABLE_RATIO` | 2 | `TABLE_RATIO\|1\|4` | representation_translation_generator.py |
| `TABLE_READ` | 3 | `TABLE_READ\|traveller A\|start 0 km\|speed 70 km/h` | motion_word_generator.py |
| `TABLE_ROW` | 2, 3 | `TABLE_ROW\|order A\|8 markers, 3 folders\|$148.00` | growth_comparison_generator.py, rate_of_change_interpret_generator.py, representation_translation_generator.py, systems_word_generator.py |
| `TABLE_TOTAL` | 2 | `TABLE_TOTAL\|grand\|7 + 26 + 35 + 57 = 125` | two_way_table_generator.py, two_way_table_probability_generator.py |
| `TAIL_ROW` | 2 | `TAIL_ROW\|3\|1/4` | likelihood_ratio_test_generator.py |
| `TALLY` | 2 | `TALLY\|H\|14` | experimental_probability_generator.py |
| `TALLY_ROW` | 3 | `TALLY_ROW\|History\|////\ /\|6` | tally_frequency_generator.py |
| `TANGENT_PLANE` | 2 | `TANGENT_PLANE\|z = z0 + fx(x-a) + fy(y-b)\|z = 36 - 9*(x - 0) + 18*(y - 3)` | gradient_generator.py |
| `TARGET_STATE` | 2 | `TARGET_STATE\|J=1\|M=-1` | clebsch_gordan_generator.py |
| `TAYLOR_FORMULA` | 1 | `TAYLOR_FORMULA\|P_n(x) = Σ f^(k)(a)/k!·(x - a)^k` | taylor_series_generator.py |
| `TAYLOR_SETUP` | 2 | `TAYLOR_SETUP\|f(x) = 1/x, center a = 1\|Taylor polynomial of degree 3` | taylor_series_generator.py |
| `TELESCOPE_CANCEL` | 2 | `TELESCOPE_CANCEL\|survive first and last\|1/63 - 1/166` | telescoping_generator.py |
| `TELE_SETUP` | 1 | `TELE_SETUP\|Σ k=63..165 (1/k - 1/(k+1))` | telescoping_generator.py |
| `TEMP_SCALE` | 2 | `TEMP_SCALE\|z1/T\|ln(9)` | softmax_gradient_generator.py |
| `TENSOR_ENTRY` | 2 | `TENSOR_ENTRY\|C_11\|-4` | einstein_summation_generator.py, index_raising_generator.py |
| `TENSOR_RULE` | 1 | `TENSOR_RULE\|diag(a,b) tensor diag(c,d)=diag(ac,ad,bc,bd)` | tensor_product_generator.py |
| `TENSOR_SETUP` | 3 | `TENSOR_SETUP\|A=diag(-2,-3)\|B=diag(0,3)\|u=[-2,-2], v=[4,2]` | tensor_product_generator.py |
| `TENSOR_STATE` | 2 | `TENSOR_STATE\|u tensor v\|[-8,-4,-8,-4]` | tensor_product_generator.py |
| `TERM` | 2, 3 | `TERM\|3 makes\|10 × (3/10)^3 × (7/10)^2\|1323/10000` | binomial_probability_generator.py, negative_binomial_generator.py, random_digit_simulation_generator.py |
| `TERMS` | 1 | `TERMS\|x[0..3]=[28,-112,448,-1792]` | z_transform_generator.py |
| `TEST_CHOOSE` | 2 | `TEST_CHOOSE\|alternating series test\|signs alternate` | power_series_generator.py, series_convergence_generator.py |
| `TEST_STAT_FORMULA` | 1 | `TEST_STAT_FORMULA\|z = (p̂ - p0)/√(p0(1-p0)/n)` | hypothesis_test_generator.py, p_value_generator.py, slope_inference_generator.py, t_interval_generator.py, two_sample_test_generator.py |
| `TF_SETUP` | 3 | `TF_SETUP\|ode\|y''+18y'+72y=3x'+3x\|zero initial conditions` | transfer_function_generator.py |
| `THEOREM` | 1, 2 | `THEOREM\|quadratic formula\|t = (-b ± √(b^2 - 4ac))/(2a)` | angle_defect_generator.py, circle_angle_generator.py, gauss_bonnet_generator.py, geometric_mean_generator.py, logistic_growth_generator.py, mean_value_theorem_generator.py, parametric_calculus_generator.py, polar_parametric_generator.py, quadratic_generator.py, rational_root_generator.py, remainder_factor_theorem_generator.py, series_convergence_generator.py, special_right_triangle_generator.py, spherical_excess_generator.py, taylor_series_generator.py, triangle_solve_generator.py, trig_identity_eval_generator.py, trig_six_functions_generator.py |
| `THEOREM_REWRITE` | 2 | `THEOREM_REWRITE\|circulation\|surface integral of curl F dot n` | vector_theorem_generator.py |
| `THEOREM_SETUP` | 3 | `THEOREM_SETUP\|Stokes\|F=<-2*y, 0, 0>\|disk radius 10 in z=0` | vector_theorem_generator.py |
| `THETA` | 2 | `THETA\|min(9,13)\|9` | transportation_generator.py |
| `THROUGHPUT` | 2 | `THROUGHPUT\|tokens_per_second\|6400000000/21` | scaling_law_generator.py |
| `TIME_COMPONENT` | 2 | `TIME_COMPONENT\|k=1\|2` | braket_generator.py |
| `TIME_DERIV` | 2 | `TIME_DERIV\|d/dt(m*L^2*thetadot)\|m*L^2*thetaddot` | lagrangian_generator.py |
| `TIME_EVOLVE` | 2 | `TIME_EVOLVE\|U psi\|[2,-1+2i]` | braket_generator.py |
| `TM_CONFIG` | 4 | `TM_CONFIG\|step 0\|state=q0\|head=0\|tape=1111` | turing_machine_trace_generator.py |
| `TM_HALT` | 2 | `TM_HALT\|step 5\|halted` | turing_machine_trace_generator.py |
| `TM_MOVE` | 3 | `TM_MOVE\|0\|R\|1` | turing_machine_trace_generator.py |
| `TM_READ` | 2 | `TM_READ\|head=0\|1` | turing_machine_trace_generator.py |
| `TM_RULE` | 2 | `TM_RULE\|q0,1\|q0,1,R` | turing_machine_trace_generator.py |
| `TM_SETUP` | 3 | `TM_SETUP\|unary_increment\|input=1111\|limit=7` | turing_machine_trace_generator.py |
| `TM_WRITE` | 2 | `TM_WRITE\|head=0\|1` | turing_machine_trace_generator.py |
| `TOPO_AVAILABLE` | 1 | `TOPO_AVAILABLE\|A` | graph_traversal_generator.py |
| `TOPO_PICK` | 2 | `TOPO_PICK\|available {11, 22}\|pick 11` | partial_order_generator.py |
| `TOPO_READY` | 1 | `TOPO_READY\|B` | graph_traversal_generator.py |
| `TOPO_SELECT` | 2 | `TOPO_SELECT\|A\|A` | graph_traversal_generator.py |
| `TOTAL_PROB_FORMULA` | 1 | `TOTAL_PROB_FORMULA\|P(B) = Σ P(cause)·P(B given cause)` | law_of_total_probability_generator.py |
| `TOTAL_PROB_TERM` | 3 | `TOTAL_PROB_TERM\|topaz\|23/54 × 1/2\|23/108` | law_of_total_probability_generator.py |
| `TOTAL_VARIANCE` | 2 | `TOTAL_VARIANCE\|Var(S) = E[N]Var(B) + Var(N)(E[B])²\|3511/6400` | conditional_expectation_generator.py |
| `TOTIENT_RESULT` | 2 | `TOTIENT_RESULT\|phi(72)\|24` | totient_generator.py |
| `TOWER` | 1, 2 | `TOWER\|E[S] = E[N]E[B]` | conditional_expectation_generator.py |
| `TRACE` | 2 | `TRACE\|6 - 9\|-3` | ode_system_generator.py |
| `TRACE_ADD` | 4 | `TRACE_ADD\|gamma1gamma1\|(1,1)\|0 + -1\|-1` | gamma_matrix_generator.py |
| `TRACE_ENTRY` | 2 | `TRACE_ENTRY\|(1,1)\|3` | einstein_summation_generator.py, pauli_algebra_generator.py |
| `TRACE_EXPECT` | 1, 3 | `TRACE_EXPECT\|Tr(rho A)=p0*a+p1*b` | density_matrix_generator.py, gamma_matrix_generator.py |
| `TRACE_SUM` | 2 | `TRACE_SUM\|3 + 3\|6` | pauli_algebra_generator.py |
| `TRANSFER` | 1 | `TRANSFER\|H(s)=(3s+3)/(s^2+18s+72)` | transfer_function_generator.py |
| `TRANSFORM_APPLY` | 2 | `TRANSFORM_APPLY\|((-3), -(6))\|(-3, -6)` | transformation_generator.py |
| `TRANSFORM_RULE` | 1 | `TRANSFORM_RULE\|(x, y) → (x, -y)` | transformation_generator.py |
| `TRANSFORM_SETUP` | 2, 3 | `TRANSFORM_SETUP\|P(-3, 6)\|reflection over the x-axis` | rv_transform_generator.py, transformation_generator.py |
| `TRANSIENT_FORMULA` | 1 | `TRANSIENT_FORMULA\|tau=L/R` | transient_circuit_generator.py |
| `TRANSIENT_SETUP` | 3 | `TRANSIENT_SETUP\|rl_rise\|R=6, L=36\|V=12, t=36` | transient_circuit_generator.py |
| `TRANSITIVE_CHECK` | 2, 3 | `TRANSITIVE_CHECK\|(12, 12) and (12, 12)\|need (12, 12)\|present` | equivalence_relation_generator.py, hereditarily_finite_set_generator.py, relation_check_generator.py |
| `TRANSLATE` | 2 | `TRANSLATE\|Every gardener is vigilant\|∀z (H(z) → Y(z))` | quantifier_negation_generator.py, representation_translation_generator.py |
| `TRANSPORT_SETUP` | 3 | `TRANSPORT_SETUP\|supply=(20,9)\|demand=(13,16)\|costs=(12,3;1,4)` | transportation_generator.py |
| `TREE_BRANCH` | 3 | `TREE_BRANCH\|AB\|33/35 × 1/17\|33/595` | probability_critic_generator.py, tree_diagram_probability_generator.py |
| `TRIANGULATE` | 2 | `TRIANGULATE\|4-gon\|2` | formula_derivation_generator.py |
| `TRIG_RATIO` | 2 | `TRIG_RATIO\|cos\|adjacent/hypotenuse` | right_triangle_trig_generator.py |
| `TRIG_SETUP` | 2 | `TRIG_SETUP\|right triangle, angle 66°, hypotenuse = 200; given cos 66° ≈ 0.4\|the adjacent side` | right_triangle_trig_generator.py, trig_identity_eval_generator.py, trig_six_functions_generator.py, unit_circle_generator.py |
| `TRIG_VALUE` | 2, 3 | `TRIG_VALUE\|sin(lat1)=0\|sin(lat2)=sqrt(3)/2\|cos(dlon)=1` | christoffel_generator.py, great_circle_generator.py, spherical_triangle_generator.py |
| `TRIM` | 2 | `TRIM\|low 11,13; high 47,51\|6 kept` | alternative_means_generator.py |
| `TRIPLE_EVAL` | 3 | `TRIPLE_EVAL\|z_part * r_part * angle\|5*81/2*25/2*2*pi\|10125/2*pi` | triple_integral_generator.py |
| `TRIPLE_SETUP` | 3 | `TRIPLE_SETUP\|integrand 5*z\|cylinder radius 5, height 9\|cylindrical` | triple_integral_generator.py |
| `TRI_ANGLE_SETUP` | 3 | `TRI_ANGLE_SETUP\|4x + 8\|2x + 14\|3x - 4` | angle_relationships_generator.py |
| `TRI_ANGLE_SOLVE` | 2 | `TRI_ANGLE_SOLVE\|9x + 18 = 180\|x = 18` | angle_relationships_generator.py |
| `TRI_ANGLE_SUM` | 1 | `TRI_ANGLE_SUM\|(4x + 8) + (2x + 14) + (3x - 4) = 180` | angle_relationships_generator.py |
| `TRI_AREA_FORMULA` | 1 | `TRI_AREA_FORMULA\|Area = (1/2)·a·b·sin C` | triangle_area_sas_generator.py |
| `TRI_SETUP` | 2 | `TRI_SETUP\|30-60-90 triangle, hypotenuse = 110\|both legs` | special_right_triangle_generator.py, triangle_area_sas_generator.py, triangle_solve_generator.py |
| `TRUE_RANGE` | 2 | `TRUE_RANGE\|5.99 to nearest 0.01 kg\|[5.985, 5.995)` | rounding_effect_generator.py |
| `TRUE_RATIO` | 2 | `TRUE_RATIO\|102 : 99\|34/33` | statistical_literacy_generator.py |
| `TRUNCATE` | 2 | `TRUNCATE\|rank=1\|discard=8` | low_rank_approx_generator.py |
| `TRUTH_ROW` | 1, 2 | `TRUTH_ROW\|row 1\|p=T, q=T` | argument_form_generator.py, boolean_algebra_generator.py, truth_table_generator.py |
| `TRY` | 1, 2, 3 | `TRY\|x = 23\|22 < x ≤ 32 and x is perfect square\|false` | cantor_pairing_generator.py, conditional_forms_generator.py, counterexample_search_generator.py, factor_trinomial_generator.py, growth_comparison_generator.py, log_conversion_generator.py, log_equation_generator.py, optimization_in_context_generator.py, polynomial_inequality_generator.py, quadratic_word_generator.py, radical_equation_generator.py, rational_equation_generator.py, rational_root_generator.py, set_builder_roster_generator.py, spatial_packing_generator.py, structure_isomorphism_generator.py |
| `TS_FACTOR` | 3 | `TS_FACTOR\|p-1=40\|q=5\|s=3` | tonelli_shanks_generator.py |
| `TS_INIT` | 4 | `TS_INIT\|m=3\|c=38\|t=40\|r=23` | tonelli_shanks_generator.py |
| `TS_LOOP` | 2 | `TS_LOOP\|i=1\|b=9` | tonelli_shanks_generator.py |
| `TS_NONRESIDUE` | 1 | `TS_NONRESIDUE\|3` | tonelli_shanks_generator.py |
| `TS_SETUP` | 2 | `TS_SETUP\|a=4\|p=41` | tonelli_shanks_generator.py |
| `TT_COLUMN` | 2 | `TT_COLUMN\|formula\|TTTT` | truth_table_generator.py |
| `TT_SETUP` | 2 | `TT_SETUP\|variables p, q\|4` | truth_table_generator.py |
| `TWIDDLE` | 1, 3 | `TWIDDLE\|W4=-i\|W4^2=-1\|W4^3=i` | dft_generator.py |
| `TWOS_SETUP` | 2 | `TWOS_SETUP\|8-bit two's complement\|offset = 2^8 = 256` | base_conversion_generator.py |
| `TYPE_ABS` | 2 | `TYPE_ABS\|lambda c\|a → b` | type_theory_generator.py |
| `TYPE_APP` | 3 | `TYPE_APP\|(a d)\|unify\|M` | type_theory_generator.py |
| `TYPE_ASSIGN` | 2 | `TYPE_ASSIGN\|a\|A → M` | type_theory_generator.py |
| `UB` | 2 | `UB\|{∅, {d, k}}\|{{d, k}, {d, k, l}}` | partial_order_generator.py |
| `UC_GUESS` | 2 | `UC_GUESS\|constant forcing\|y_p = A` | undetermined_coeff_generator.py |
| `UC_POINT` | 2 | `UC_POINT\|90°\|(0, 1)` | unit_circle_generator.py |
| `UNCERTAINTY_SETUP` | 3 | `UNCERTAINTY_SETUP\|particle in a box\|L=1, hbar=1\|n=125` | uncertainty_generator.py |
| `UNFOLD` | 2 | `UNFOLD\|count_c("cicbcbi")\|[c=c] + count_c("icbcbi")` | recursive_definition_unfold_generator.py |
| `UNIFY_BIND` | 3 | `UNIFY_BIND\|X\|b\|{X=b}` | unification_generator.py |
| `UNIFY_DECOMPOSE` | 2 | `UNIFY_DECOMPOSE\|f\|2 arguments` | unification_generator.py |
| `UNIFY_FAIL` | 1 | `UNIFY_FAIL\|occurs-check X in f(X)` | unification_generator.py |
| `UNIFY_PAIR` | 2 | `UNIFY_PAIR\|X\|f(X)` | unification_generator.py |
| `UNIFY_SETUP` | 3 | `UNIFY_SETUP\|X\|f(X)\|occurs-check` | unification_generator.py |
| `UNIF_FORMULA` | 1 | `UNIF_FORMULA\|E[X] = (a + b)/2; Var(X) = (n² − 1)/12` | discrete_uniform_bernoulli_generator.py |
| `UNIF_SETUP` | 2 | `UNIF_SETUP\|X uniform on integers 67 through 84\|n = 18` | discrete_uniform_bernoulli_generator.py |
| `UNION_ELEMENT` | 2 | `UNION_ELEMENT\|{∅, {∅, {∅}, {∅, {∅}}, {{∅}}}, {∅, {{∅}}, {{{∅}}}}, {{{{∅}}}}}\|contributes {∅, {∅, {∅}, {∅, {∅}}, {{∅}}}, {∅, {{∅}}, {{{∅}}}}, {{{{∅}}}}}` | hereditarily_finite_set_generator.py |
| `UNIT_ANALYSIS` | 3 | `UNIT_ANALYSIS\|kilometers\|hours\|kilometers per hour` | rate_of_change_interpret_generator.py |
| `UNIT_ATTACH` | 3 | `UNIT_ATTACH\|11\|seconds\|11 seconds` | cross_section_generator.py, kinematics_generator.py, physics_formula_generator.py |
| `UNIT_CONVERT` | 2 | `UNIT_CONVERT\|4 minutes\|240 seconds` | physics_formula_generator.py |
| `UNIT_NORMAL` | 2 | `UNIT_NORMAL\|T'(0)/norm T'(0)\|<-1, 0>` | curve_geometry_generator.py |
| `UNIT_PRICE` | 3 | `UNIT_PRICE\|A\|4.4/22\|$0.20` | money_life_generator.py, unit_rate_generator.py |
| `UNIT_RATE_DIV` | 3 | `UNIT_RATE_DIV\|42 hours\|14\|3 hours per mile` | unit_rate_generator.py |
| `UNIT_RATE_PICK` | 2 | `UNIT_RATE_PICK\|1\|6` | unit_rate_generator.py |
| `UNIT_RATE_SETUP` | 3 | `UNIT_RATE_SETUP\|14\|miles\|42 hours` | unit_rate_generator.py |
| `UNIT_RATE_TABLE` | 2 | `UNIT_RATE_TABLE\|1,3,5\|6,18,30` | unit_rate_generator.py |
| `UNIT_RULE` | 3 | `UNIT_RULE\|hbar=1\|L=1/E\|eV^-1` | natural_units_generator.py |
| `UNIT_TANGENT` | 2 | `UNIT_TANGENT\|r'(0)/speed\|<0, 1>` | curve_geometry_generator.py |
| `UNLIKE_RADICALS` | 2 | `UNLIKE_RADICALS\|√2 ≠ √5\|unlike radicands — cannot combine` | radical_add_sub_generator.py |
| `UNPAIR` | 2 | `UNPAIR\|11243\|(81, 68)` | cantor_pairing_generator.py |
| `UNPAIRED` | 2 | `UNPAIRED\|neither\|∅` | one_to_one_correspondence_generator.py |
| `UNROLL` | 2 | `UNROLL\|-5, -15, -45, -135\|geometric, r = 3` | recursive_explicit_generator.py |
| `UPDATE` | 2 | `UPDATE\|W1_11\|1/3` | backprop_generator.py, kernel_perceptron_generator.py |
| `U_VECTOR` | 2 | `U_VECTOR\|u1 = A*v1/σ1\|[1/√2, 1/√2]` | svd_generator.py |
| `VA` | 1 | `VA\|x = -4` | rational_function_features_generator.py |
| `VALIDITY` | 2 | `VALIDITY\|valid\|constructive dilemma` | argument_form_generator.py |
| `VALUE_FORMULA` | 1 | `VALUE_FORMULA\|v=(ad-bc)/(a-b-c+d)` | game_theory_generator.py |
| `VARIANCE` | 1, 2 | `VARIANCE\|Delta x^2\|1/12 - 1/(31250pi^2)` | layer_norm_generator.py, uncertainty_generator.py |
| `VAR_FORMULA` | 1 | `VAR_FORMULA\|Var(X) = p(1 − p)` | discrete_uniform_bernoulli_generator.py, expectation_of_function_generator.py, expected_value_generator.py |
| `VAR_ROW` | 3 | `VAR_ROW\|7 - 2.25 = 4.75\|(4.75)^2 = 22.5625\|1/4·22.5625 = 5.640625` | expected_value_generator.py, sampling_distribution_enum_generator.py |
| `VECTOR_NORM` | 2 | `VECTOR_NORM\|A\|5` | embedding_similarity_generator.py |
| `VECTOR_SETUP` | 2 | `VECTOR_SETUP\|F(x,y) = <6*x - 6*y, 6*x - y>\|divergence and scalar curl` | div_curl_generator.py |
| `VEC_ENTRY` | 3 | `VEC_ENTRY\|(1)\|(-64)\|-64` | diagonalization_generator.py |
| `VEC_SETUP` | 2 | `VEC_SETUP\|v = ⟨3, 0⟩\|magnitude` | dot_product_generator.py, vector_ops_generator.py |
| `VENN_MARK` | 2 | `VENN_MARK\|dancers ∩ ¬librarians\|x1` | syllogism_generator.py |
| `VENN_REGION` | 2 | `VENN_REGION\|A ∩ B ∩ C\|13` | venn_probability_generator.py |
| `VENN_SHADE` | 2 | `VENN_SHADE\|librarians − editors\|empty` | syllogism_generator.py |
| `VERIFY` | 2 | `VERIFY\|1\|ok` | error_spotting_generator.py, foundations_critic_generator.py, probability_critic_generator.py |
| `VERTEX` | 1 | `VERTEX\|(0, 0)` | ellipse_features_generator.py, hyperbola_features_generator.py, lp_corner_generator.py, parabola_features_generator.py |
| `VERTEX_SOLVE` | 2 | `VERTEX_SOLVE\|x=0\|y=0` | lp_corner_generator.py |
| `VISIT` | 2 | `VISIT\|E\|E` | graph_traversal_generator.py |
| `VISUAL_RATIO` | 2 | `VISUAL_RATIO\|16 : 13\|16/13` | statistical_literacy_generator.py |
| `VITERBI_BACKTRACE` | 2 | `VITERBI_BACKTRACE\|H->L->L\|9/256` | viterbi_generator.py |
| `VITERBI_CAND` | 3 | `VITERBI_CAND\|t=2,state=H\|from H\|9/128` | convolutional_code_viterbi_generator.py, viterbi_generator.py |
| `VITERBI_INIT` | 3 | `VITERBI_INIT\|H\|obs=A\|3/8` | viterbi_generator.py |
| `VITERBI_PICK` | 2, 3 | `VITERBI_PICK\|t=2,state=H\|from H\|9/128` | convolutional_code_viterbi_generator.py, viterbi_generator.py |
| `VOLUME` | 1 | `VOLUME\|192` | volume_rect_prism_generator.py |
| `VOLUME_SETUP` | 2 | `VOLUME_SETUP\|region under y = 34x on [0, 31], rotated about the x-axis\|disk method` | solid_revolution_generator.py |
| `VOL_BASE_AREA` | 2 | `VOL_BASE_AREA\|Base Area = (1/2) × 5 × 7\|17.5` | round_solids_generator.py, volume_3d_generator.py |
| `VOL_CALCULATE` | 2 | `VOL_CALCULATE\|V = 17.5 × 11\|192.5` | round_solids_generator.py, volume_3d_generator.py |
| `VOL_FORMULA` | 1 | `VOL_FORMULA\|V = Base Area × length` | round_solids_generator.py, solid_revolution_generator.py, volume_3d_generator.py |
| `VOL_SETUP` | 2 | `VOL_SETUP\|triangular_prism\|b=5, h_tri=7, length=11` | volume_3d_generator.py |
| `VOP_FORM` | 2 | `VOP_FORM\|u1' = -y2*g/W\|-360/3 * e^(8x)` | variation_parameters_generator.py |
| `WALK_ENTRY` | 2 | `WALK_ENTRY\|A^2[3,2]\|1` | graph_counting_generator.py |
| `WALK_GOAL` | 2 | `WALK_GOAL\|length 2\|3 to 2` | graph_counting_generator.py, multi_state_markov_generator.py |
| `WALK_TERM` | 3 | `WALK_TERM\|via 1\|A[3,1]*A[1,2]\|1` | graph_counting_generator.py, multi_state_markov_generator.py |
| `WARSHALL_K` | 2 | `WARSHALL_K\|k=18\|0 0 1 0; 0 0 1 1; 0 0 0 1; 1 0 1 0` | relation_closure_generator.py |
| `WASTE` | 3 | `WASTE\|20%\|336 → 403.2\|404` | geometry_in_context_generator.py |
| `WAVE_FORMULA` | 1 | `WAVE_FORMULA\|1=N^2*integral_0^L (x/L)^(2k) dx` | wavefunction_generator.py |
| `WAVE_SETUP` | 3 | `WAVE_SETUP\|power_interval\|psi=N*(x/L)^3\|0<=x<=42` | wavefunction_generator.py |
| `WEEKDAY_SCAN` | 2, 3 | `WEEKDAY_SCAN\|extra day 1\|Tuesday\|hit 0` | calendar_arithmetic_generator.py |
| `WEIGHT` | 2 | `WEIGHT\|green\|35/44` | complement_probability_generator.py, expectation_of_function_generator.py, pmf_cdf_quantile_generator.py, probability_axioms_finite_generator.py, probability_measure_generator.py, simpsons_paradox_generator.py |
| `WEIGHT_ROW` | 3 | `WEIGHT_ROW\|57\|1\|57` | standard_deviation_generator.py, weighted_mean_generator.py |
| `WEIGHT_VECTOR` | 2 | `WEIGHT_VECTOR\|w\|(-12,-5)` | svm_margin_generator.py |
| `WIDTH_FORMULA` | 1 | `WIDTH_FORMULA\|width = 2E, E = z*·σ/√n` | confidence_interval_generator.py |
| `WIDTH_SETUP` | 3 | `WIDTH_SETUP\|combined\|Gamma_a=6, Gamma_b=10, Gamma_c=11,hbar=2\|target=BR_b,tau` | branching_ratio_generator.py |
| `WINDOW_CHANGE` | 2 | `WINDOW_CHANGE\|(600 − 300)/300\|100%` | statistical_literacy_generator.py |
| `WITNESS` | 2, 3 | `WITNESS\|n=2\|Prime(2)=T\|Odd(2)=F` | induction_verify_generator.py, peano_arithmetic_generator.py, quantifier_finite_domain_generator.py, quantifier_negation_generator.py |
| `WORK_DIFF` | 3 | `WORK_DIFF\|phi(end) - phi(start)\|78 - 53\|25` | line_integral_generator.py |
| `WORST_CASE` | 2 | `WORST_CASE\|A\|60` | decision_under_uncertainty_generator.py |
| `WRONSKIAN` | 2 | `WRONSKIAN\|y1*y2' - y1'*y2\|3e^(-5x)` | variation_parameters_generator.py |
| `XOR` | 3 | `XOR\|control=1\|target=0\|1` | quantum_gate_generator.py |
| `YOUNG_SETUP` | 3 | `YOUNG_SETUP\|partition=[5,3,3]\|n=11\|group=S_11` | young_tableaux_generator.py |
| `Z` | 1 | `Z\|16 R10` | abacus_addition_generator.py, absolute_value_equation_generator.py, absolute_value_inequality_generator.py, ac_circuit_generator.py, activation_generator.py, adam_step_generator.py, algorithm_trace_generator.py, alternative_means_generator.py, angle_defect_generator.py, angle_measure_generator.py, angle_relationships_generator.py, annuity_generator.py, anova_generator.py, antiderivative_generator.py, arc_length_generator.py, arc_sector_generator.py, area_between_curves_generator.py, argument_form_generator.py, arithmetic_coding_generator.py, arithmetic_sequence_generator.py, assumption_check_generator.py, attention_generator.py, attribute_sorting_generator.py, baby_step_giant_step_generator.py, backprop_generator.py, ballot_reflection_generator.py, base_arithmetic_generator.py, base_conversion_generator.py, bayes_multiple_hypotheses_generator.py, bayesian_update_generator.py, bch_generator.py, bec_channel_generator.py, binomial_probability_generator.py, bisection_generator.py, bitwise_ops_generator.py, black_scholes_generator.py, blackbody_generator.py, bond_pricing_generator.py, boolean_algebra_generator.py, box_plot_generator.py, braket_generator.py, branching_ratio_generator.py, calendar_arithmetic_generator.py, calorimetry_generator.py, cantor_diagonal_generator.py, cantor_pairing_generator.py, cardinal_arithmetic_generator.py, casimir_force_generator.py, casimir_generator.py, cauchy_riemann_generator.py, cayley_table_generator.py, centroid_generator.py, chain_rule_generator.py, channel_capacity_generator.py, characteristic_vector_generator.py, chi_square_generator.py, cholesky_generator.py, christoffel_generator.py, circle_angle_generator.py, circle_equation_generator.py, circle_generator.py, classic_probability_puzzles_generator.py, classifier_metrics_generator.py, clebsch_gordan_generator.py, clt_probability_generator.py, collision_generator.py, combinatory_logic_generator.py, commutator_generator.py, complement_probability_generator.py, completing_square_generator.py, complex_division_generator.py, complex_locus_generator.py, complex_log_generator.py, complex_number_ops_generator.py, complex_quadratic_generator.py, composite_arithmetic_generator.py, compound_inequality_generator.py, compound_probability_generator.py, conditional_expectation_generator.py, conditional_forms_generator.py, conditional_probability_generator.py, confidence_interval_generator.py, conic_standard_form_generator.py, conservation_law_generator.py, continued_fraction_generator.py, continuous_distribution_generator.py, contour_integral_generator.py, convolution_generator.py, convolutional_code_viterbi_generator.py, coset_generator.py, countability_bijection_generator.py, counterexample_search_generator.py, counting_classics_generator.py, counting_to_probability_generator.py, covariance_algebra_generator.py, covariance_correlation_generator.py, cramers_rule_generator.py, crc_generator.py, cross_section_generator.py, crt_generator.py, curve_analysis_generator.py, curve_geometry_generator.py, cyclic_group_generator.py, cyk_parser_generator.py, de_moivre_generator.py, decimal_add_sub_generator.py, decimal_div_generator.py, decimal_mult_generator.py, decision_under_uncertainty_generator.py, dedekind_cut_generator.py, definite_integral_generator.py, density_matrix_generator.py, derangement_generator.py, derivative_limit_def_generator.py, derivative_power_rule_generator.py, derivative_product_quotient_generator.py, derivative_transcendental_generator.py, determinant_generator.py, dfa_minimization_generator.py, dfa_simulation_generator.py, dft_generator.py, diagonalization_generator.py, diffie_hellman_generator.py, dijkstra_generator.py, dimensional_analysis_generator.py, direct_proof_algebra_generator.py, discrete_posterior_generator.py, discrete_uniform_bernoulli_generator.py, discriminant_generator.py, distance_formula_generator.py, distribution_of_sum_generator.py, div_curl_generator.py, divisibility_classification_generator.py, domain_range_generator.py, doppler_generator.py, dot_plot_generator.py, dot_product_generator.py, double_integral_generator.py, dp_table_generator.py, dpll_trace_generator.py, ecdh_generator.py, ecdsa_generator.py, eigenvalue_generator.py, einstein_summation_generator.py, electrostatics_generator.py, ellipse_features_generator.py, elliptic_curve_finite_field_generator.py, embedding_similarity_generator.py, empirical_cdf_generator.py, empirical_rule_generator.py, energy_conservation_generator.py, english_to_logic_generator.py, entropy_change_generator.py, entropy_generator.py, entropy_rate_markov_generator.py, equation_from_two_points_generator.py, equilibrium_ice_generator.py, equivalence_relation_generator.py, error_spotting_generator.py, estimator_bias_enum_generator.py, euler_characteristic_generator.py, euler_circuit_generator.py, euler_formula_generator.py, euler_method_generator.py, evaluate_expression_generator.py, exact_ode_generator.py, expectation_of_function_generator.py, expected_value_classics_generator.py, expected_value_generator.py, experimental_probability_generator.py, exponent_generator.py, exponent_mixed_rules_generator.py, exponential_equation_generator.py, exponential_model_generator.py, extended_euclid_generator.py, factor_gcf_generator.py, factor_grouping_generator.py, factor_special_forms_generator.py, factor_trinomial_generator.py, factors_generator.py, feature_map_generator.py, fermi_estimation_generator.py, fill_in_step_generator.py, finance_generator.py, finite_difference_generator.py, finite_field_generator.py, finite_sigma_algebra_generator.py, first_law_generator.py, fisher_information_generator.py, five_number_summary_generator.py, fixed_point_generator.py, flops_memory_generator.py, formula_derivation_generator.py, foundations_critic_generator.py, four_vector_generator.py, fourier_series_generator.py, fractal_iteration_generator.py, fraction_comparison_generator.py, fraction_decimal_percent_converter.py, fraction_line_plot_generator.py, fraction_op_generator.py, frequency_table_generator.py, function_composition_generator.py, function_evaluation_generator.py, function_inner_product_generator.py, function_operations_generator.py, function_properties_generator.py, function_table_generator.py, fundamental_counting_principle_generator.py, fundamental_form_generator.py, game_theory_generator.py, gamma_matrix_generator.py, gas_law_generator.py, gas_stoichiometry_generator.py, gauss_bonnet_generator.py, gauss_law_generator.py, gaussian_curvature_generator.py, gcf_generator.py, generating_function_generator.py, geometric_distribution_generator.py, geometric_mean_generator.py, geometric_probability_generator.py, geometric_sequence_generator.py, geometry_area_perimeter_generator.py, geometry_in_context_generator.py, godel_numbering_generator.py, gradient_descent_generator.py, gradient_generator.py, gradient_step_generator.py, gram_schmidt_generator.py, graph_counting_generator.py, graph_interpret_generator.py, graph_traversal_generator.py, grassmann_generator.py, great_circle_generator.py, grouped_data_generator.py, growth_comparison_generator.py, hamiltonian_generator.py, hamming_code_generator.py, hawking_generator.py, heat_engine_generator.py, hereditarily_finite_set_generator.py, hermitian_check_generator.py, hessian_classify_generator.py, hilbert_axiom_derivation_generator.py, histogram_construct_generator.py, horner_evaluation_generator.py, huffman_coding_generator.py, hydrogen_atom_generator.py, hyperbola_features_generator.py, hyperbolic_distance_generator.py, hyperbolic_function_generator.py, hypercube_counting_generator.py, hypergeometric_generator.py, hypothesis_test_generator.py, implicit_diff_generator.py, improper_integral_generator.py, inclusion_exclusion_generator.py, independence_check_generator.py, index_and_growth_generator.py, index_gymnastics_generator.py, index_raising_generator.py, induction_verify_generator.py, inference_setup_generator.py, information_gain_generator.py, integer_operations_generator.py, integer_puzzle_word_generator.py, integers_as_pairs_generator.py, integrating_factor_generator.py, integration_by_parts_generator.py, interference_generator.py, interpolation_generator.py, invariant_mass_generator.py, inverse_function_generator.py, inverse_normal_generator.py, jacobi_symbol_generator.py, jacobian_generator.py, joint_distribution_generator.py, kernel_evaluation_generator.py, kernel_perceptron_generator.py, kernel_ridge_generator.py, kernel_validity_generator.py, kinematics_generator.py, kl_divergence_generator.py, kmeans_step_generator.py, knights_knaves_generator.py, knn_generator.py, kraft_inequality_generator.py, ladder_operator_generator.py, lagrange_multiplier_generator.py, lagrangian_generator.py, lambda_reduction_generator.py, laplace_ivp_generator.py, laurent_series_generator.py, law_of_total_probability_generator.py, layer_norm_generator.py, lcm_generator.py, least_squares_generator.py, legendre_construction_generator.py, lhopital_generator.py, lie_exponential_generator.py, likelihood_language_generator.py, likelihood_ratio_test_generator.py, limit_evaluation_generator.py, line_integral_generator.py, linear_approx_generator.py, linear_complex_generator.py, linear_fractional_generator.py, linear_model_word_generator.py, linear_simple_generator.py, linear_transform_effect_generator.py, linearity_of_expectation_generator.py, literal_equation_generator.py, lll_reduction_generator.py, log_conversion_generator.py, log_diff_higher_order_generator.py, log_equation_generator.py, log_properties_generator.py, logic_grid_puzzle_generator.py, logical_connective_eval_generator.py, logical_equivalence_laws_generator.py, logistic_growth_generator.py, long_division_generator.py, low_rank_approx_generator.py, lp_corner_generator.py, lr_schedule_generator.py, lu_decomposition_generator.py, lz_compression_generator.py, magnetism_generator.py, magnitude_comparison_generator.py, manual_square_root_generator.py, markov_chain_generator.py, markov_state_classification_generator.py, martingale_check_generator.py, master_theorem_generator.py, matrix_calculus_generator.py, matrix_exponential_generator.py, matrix_group_check_generator.py, matrix_inverse_generator.py, matrix_norm_generator.py, matrix_ops_generator.py, mean_adjustment_generator.py, mean_value_theorem_generator.py, measurement_uncertainty_generator.py, mental_strategy_generator.py, method_discrimination_generator.py, method_of_moments_generator.py, metric_arc_length_generator.py, mgf_generator.py, midpoint_generator.py, minkowski_interval_generator.py, missing_information_generator.py, mixed_number_operation_generator.py, mixture_generator.py, mle_generator.py, mobius_transform_generator.py, mod_exp_generator.py, modular_arithmetic_generator.py, modular_inverse_generator.py, money_life_generator.py, monomial_mult_div_generator.py, monte_carlo_arithmetic_generator.py, motion_word_generator.py, mse_decomposition_generator.py, mst_generator.py, multi_digit_addition_generator.py, multi_digit_multiplication_generator.py, multi_digit_subtraction_generator.py, multi_state_markov_generator.py, multi_step_unit_conversion_generator.py, multi_step_word_generator.py, multinomial_probability_generator.py, multiplying_binomials_generator.py, multiplying_polynomials_generator.py, multivar_chain_rule_generator.py, mutual_information_generator.py, naive_bayes_generator.py, named_distribution_generator.py, natural_deduction_generator.py, natural_units_generator.py, negative_binomial_generator.py, nets_surface_area_generator.py, newton_raphson_generator.py, newtons_laws_generator.py, nfa_simulation_generator.py, nonparametric_test_generator.py, normal_approx_binomial_generator.py, normal_table_generator.py, npv_irr_generator.py, number_comparison_generator.py, odds_probability_generator.py, ode_substitution_generator.py, ode_system_generator.py, one_step_equation_generator.py, one_step_inequality_generator.py, one_to_one_correspondence_generator.py, operation_properties_generator.py, optics_generator.py, optimization_generator.py, optimization_in_context_generator.py, or_formula_generator.py, orbital_mechanics_generator.py, order_of_operations_generator.py, order_statistics_generator.py, ordinal_arithmetic_generator.py, p_value_generator.py, parabola_features_generator.py, parallel_perpendicular_line_generator.py, param_count_generator.py, parametric_calculus_generator.py, partial_derivative_generator.py, partial_fractions_generator.py, partial_order_generator.py, partial_trace_generator.py, particle_in_box_generator.py, partition_function_generator.py, pascal_triangle_generator.py, pauli_algebra_generator.py, pca_generator.py, pda_simulation_generator.py, peano_arithmetic_generator.py, percent_chain_generator.py, percent_problem_generator.py, percent_word_problem_generator.py, percentile_generator.py, perceptron_generator.py, permutation_combination_generator.py, permutation_group_generator.py, perplexity_generator.py, pgf_generator.py, ph_calculation_generator.py, physics_formula_generator.py, piecewise_evaluation_generator.py, place_value_rounding_generator.py, planck_units_generator.py, plausibility_critic_generator.py, pmf_cdf_quantile_generator.py, point_slope_generator.py, poisson_process_generator.py, polar_parametric_generator.py, pollard_factorization_generator.py, polya_urn_generator.py, polygon_perimeter_generator.py, polynomial_add_sub_generator.py, polynomial_div_monomial_generator.py, polynomial_inequality_generator.py, polynomial_long_division_generator.py, polynomial_zeros_generator.py, population_sample_generator.py, portfolio_generator.py, positional_encoding_generator.py, positive_definite_generator.py, power_series_generator.py, prenex_normal_form_generator.py, primality_test_generator.py, prime_factorization_generator.py, probability_addition_rule_generator.py, probability_axioms_finite_generator.py, probability_critic_generator.py, probability_inequality_generator.py, probability_measure_generator.py, projectile_motion_generator.py, projector_generator.py, proportion_word_problem_generator.py, proportional_relationship_generator.py, pythag_hyp_generator.py, pythag_leg_generator.py, qr_decomposition_generator.py, quadratic_factoring_generator.py, quadratic_generator.py, quadratic_residue_generator.py, quadratic_square_root_generator.py, quadratic_word_generator.py, qualitative_reasoning_generator.py, quantifier_finite_domain_generator.py, quantifier_negation_generator.py, quantization_generator.py, quantum_formula_generator.py, quantum_gate_generator.py, quark_composition_generator.py, quaternion_generator.py, radical_add_sub_generator.py, radical_equation_generator.py, radical_multiply_generator.py, radical_rationalize_generator.py, radical_variable_simplify_generator.py, random_digit_simulation_generator.py, random_walk_generator.py, rate_conversion_generator.py, rate_of_change_interpret_generator.py, ratio_table_generator.py, rational_equation_generator.py, rational_exponent_generator.py, rational_expr_add_sub_generator.py, rational_expr_mult_div_generator.py, rational_expr_simplify_generator.py, rational_function_features_generator.py, rational_root_generator.py, rationals_as_pairs_generator.py, recurrence_generator.py, recursive_definition_unfold_generator.py, recursive_explicit_generator.py, reed_solomon_generator.py, regex_to_automaton_generator.py, regression_generator.py, regular_polygon_area_generator.py, related_rates_generator.py, relation_check_generator.py, relation_closure_generator.py, relation_operations_generator.py, relativistic_energy_generator.py, reliability_system_generator.py, remainder_factor_theorem_generator.py, repeating_decimal_generator.py, representation_translation_generator.py, residue_generator.py, resolution_proof_generator.py, riemann_sum_generator.py, riemann_tensor_generator.py, right_triangle_trig_generator.py, risk_communication_generator.py, rotational_dynamics_generator.py, round_solids_generator.py, rounding_effect_generator.py, routh_hurwitz_generator.py, row_reduction_generator.py, rsa_generator.py, runge_kutta_generator.py, running_coupling_generator.py, rv_transform_generator.py, sample_space_list_generator.py, sampling_distribution_enum_generator.py, scaling_generator.py, scaling_law_generator.py, scatter_plot_describe_generator.py, scenario_generator.py, schwarzschild_generator.py, second_order_ode_generator.py, segment_partition_generator.py, semantic_tableau_generator.py, separable_ode_generator.py, separable_pde_generator.py, series_convergence_generator.py, series_solution_generator.py, set_algebra_laws_generator.py, set_builder_roster_generator.py, set_counting_generator.py, set_expression_generator.py, set_identity_membership_table_generator.py, set_membership_subset_generator.py, set_operations_generator.py, shm_generator.py, sigma_notation_generator.py, signal_arithmetic_generator.py, significant_figures_generator.py, similar_triangles_generator.py, simple_probability_generator.py, simple_stats_generator.py, simplex_generator.py, simplify_expression_generator.py, simpsons_paradox_generator.py, sinusoid_features_generator.py, slope_inference_generator.py, slope_intercept_form_generator.py, slope_two_points_generator.py, softmax_gradient_generator.py, solid_revolution_generator.py, solution_chem_generator.py, spatial_description_generator.py, spatial_packing_generator.py, special_relativity_generator.py, special_right_triangle_generator.py, special_solution_equation_generator.py, spherical_excess_generator.py, spherical_triangle_generator.py, spin_half_generator.py, square_cube_law_generator.py, stability_generator.py, standard_deviation_generator.py, standard_form_conversion_generator.py, standing_wave_generator.py, stars_and_bars_generator.py, statics_generator.py, statistical_literacy_generator.py, statistics_generator.py, stem_and_leaf_generator.py, stereographic_generator.py, stoichiometry_generator.py, structure_constant_generator.py, structure_isomorphism_generator.py, study_design_generator.py, subspace_basis_generator.py, sufficiency_factorization_generator.py, svd_generator.py, svm_margin_generator.py, syllogism_generator.py, synthetic_division_generator.py, systems_elimination_generator.py, systems_substitution_generator.py, systems_word_generator.py, t_interval_generator.py, tally_frequency_generator.py, tangent_line_generator.py, taxicab_geometry_generator.py, taylor_series_generator.py, telescoping_generator.py, temperature_conversion_generator.py, tensor_product_generator.py, tip_bill_split_generator.py, tonelli_shanks_generator.py, totient_generator.py, transfer_function_generator.py, transformation_generator.py, transient_circuit_generator.py, transportation_generator.py, tree_diagram_probability_generator.py, triangle_area_sas_generator.py, triangle_solve_generator.py, trig_equation_generator.py, trig_identity_eval_generator.py, trig_identity_verify_generator.py, trig_six_functions_generator.py, triple_integral_generator.py, truth_table_generator.py, turing_machine_trace_generator.py, two_sample_test_generator.py, two_step_equation_generator.py, two_step_inequality_generator.py, two_way_table_generator.py, two_way_table_probability_generator.py, type_error_power_generator.py, type_theory_generator.py, u_substitution_generator.py, uncertainty_generator.py, undetermined_coeff_generator.py, unification_generator.py, unit_circle_generator.py, unit_conversion_generator.py, unit_rate_generator.py, variation_parameters_generator.py, vector_ops_generator.py, vector_theorem_generator.py, venn_probability_generator.py, venn_region_count_generator.py, viterbi_generator.py, volume_3d_generator.py, volume_rect_prism_generator.py, von_neumann_entropy_generator.py, wavefunction_generator.py, weighted_mean_generator.py, wff_parsing_generator.py, work_rate_generator.py, young_tableaux_generator.py, z_score_generator.py, z_transform_generator.py, zf_axiom_identify_generator.py |
| `ZERO` | 1 | `ZERO\|s=-1` | transfer_function_generator.py |
| `ZERO_PRODUCT` | 1, 2 | `ZERO_PRODUCT\|(x - 8) = 0\|x = 8` | area_between_curves_generator.py, assumption_check_generator.py, curve_analysis_generator.py, domain_range_generator.py, log_equation_generator.py, optimization_generator.py, polynomial_inequality_generator.py, polynomial_zeros_generator.py, quadratic_factoring_generator.py, quadratic_word_generator.py, qualitative_reasoning_generator.py, radical_equation_generator.py, trig_equation_generator.py |
| `ZPROD_ROW` | 3 | `ZPROD_ROW\|1\|0\|0` | covariance_correlation_generator.py |
| `ZSCORE` | 2 | `ZSCORE\|(161.5 − 150)/5\|2.30` | clt_probability_generator.py, empirical_rule_generator.py, normal_approx_binomial_generator.py, normal_table_generator.py, type_error_power_generator.py, z_score_generator.py |
| `ZSCORE_FORMULA` | 1 | `ZSCORE_FORMULA\|z = (x - μ)/σ` | z_score_generator.py |
| `ZT_PAIR` | 1 | `ZT_PAIR\|Z{r^n u[n]}=1/(1-r z^-1)` | z_transform_generator.py |
| `ZT_SETUP` | 2, 3 | `ZT_SETUP\|geometric\|x[n]=28*(-4)^n u[n]` | z_transform_generator.py |
