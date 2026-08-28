# Op-Code Legend

**Generated file — do not hand-edit.** Regenerate with `python tools/gen_opcode_legend.py` (verify freshness with `--check`).

The scratchpad vocabulary belongs to the model and evolves organically: generators may introduce new op-codes freely, and this legend is *descriptive*, not prescriptive. Steps are pipe-delimited strings (`CODE|field|field|...`, at most 4 payload fields) built with `helpers.step()`; the final step of every problem is `Z|<final_answer>`.

1822 distinct op-codes observed.

| Code | Payload fields | Example | Used by |
|---|---|---|---|
| `A` | 2, 3 | `A\|46\|46\|92` | ac_circuit_generator.py, activation_generator.py, adam_step_generator.py, algorithm_trace_generator.py, angle_defect_generator.py, angle_measure_generator.py, annuity_generator.py, arithmetic_coding_generator.py, arithmetic_sequence_generator.py, attention_generator.py, backprop_generator.py, base_conversion_generator.py, bayes_multiple_hypotheses_generator.py, bayesian_update_generator.py, binomial_probability_generator.py, bisection_generator.py, bond_pricing_generator.py, branching_ratio_generator.py, calendar_arithmetic_generator.py, calorimetry_generator.py, cantor_pairing_generator.py, cardinal_arithmetic_generator.py, casimir_generator.py, cayley_table_generator.py, channel_capacity_generator.py, chi_square_generator.py, circle_equation_generator.py, classifier_metrics_generator.py, collision_generator.py, commutator_generator.py, complement_probability_generator.py, complex_division_generator.py, complex_locus_generator.py, complex_number_ops_generator.py, composite_arithmetic_generator.py, conditional_expectation_generator.py, conditional_probability_generator.py, confidence_interval_generator.py, conic_standard_form_generator.py, continued_fraction_generator.py, contour_integral_generator.py, convolution_generator.py, coset_generator.py, countability_bijection_generator.py, counterexample_search_generator.py, counting_classics_generator.py, covariance_algebra_generator.py, crt_generator.py, curve_analysis_generator.py, cyclic_group_generator.py, de_moivre_generator.py, dedekind_cut_generator.py, definite_integral_generator.py, density_matrix_generator.py, derangement_generator.py, derivative_limit_def_generator.py, determinant_generator.py, dft_generator.py, dijkstra_generator.py, discrete_uniform_bernoulli_generator.py, distance_formula_generator.py, distribution_of_sum_generator.py, doppler_generator.py, dot_product_generator.py, dp_table_generator.py, einstein_summation_generator.py, electrostatics_generator.py, ellipse_features_generator.py, embedding_similarity_generator.py, energy_conservation_generator.py, entropy_change_generator.py, entropy_generator.py, entropy_rate_markov_generator.py, equivalence_relation_generator.py, euler_characteristic_generator.py, euler_formula_generator.py, euler_method_generator.py, evaluate_expression_generator.py, expectation_of_function_generator.py, expected_value_generator.py, exponential_model_generator.py, extended_euclid_generator.py, feature_map_generator.py, fill_in_step_generator.py, finance_generator.py, finite_field_generator.py, five_number_summary_generator.py, fixed_point_generator.py, flops_memory_generator.py, four_vector_generator.py, fractal_iteration_generator.py, fraction_op_generator.py, frequency_table_generator.py, function_composition_generator.py, function_evaluation_generator.py, function_inner_product_generator.py, function_operations_generator.py, function_table_generator.py, game_theory_generator.py, gaussian_curvature_generator.py, generating_function_generator.py, geometric_mean_generator.py, geometry_area_perimeter_generator.py, gradient_descent_generator.py, gradient_step_generator.py, graph_counting_generator.py, graph_interpret_generator.py, grassmann_generator.py, great_circle_generator.py, hamiltonian_generator.py, heat_engine_generator.py, hermitian_check_generator.py, horner_evaluation_generator.py, huffman_coding_generator.py, hyperbola_features_generator.py, hyperbolic_distance_generator.py, hyperbolic_function_generator.py, hypercube_counting_generator.py, hypergeometric_generator.py, inclusion_exclusion_generator.py, index_gymnastics_generator.py, information_gain_generator.py, integers_as_pairs_generator.py, integrating_factor_generator.py, interpolation_generator.py, invariant_mass_generator.py, joint_distribution_generator.py, kernel_evaluation_generator.py, kernel_perceptron_generator.py, kernel_ridge_generator.py, kl_divergence_generator.py, kmeans_step_generator.py, knn_generator.py, kraft_inequality_generator.py, ladder_operator_generator.py, lagrangian_generator.py, laplace_ivp_generator.py, law_of_total_probability_generator.py, layer_norm_generator.py, legendre_construction_generator.py, lhopital_generator.py, limit_evaluation_generator.py, linear_approx_generator.py, linearity_of_expectation_generator.py, low_rank_approx_generator.py, lp_corner_generator.py, lr_schedule_generator.py, manual_square_root_generator.py, markov_chain_generator.py, matrix_calculus_generator.py, matrix_group_check_generator.py, matrix_norm_generator.py, matrix_ops_generator.py, mean_value_theorem_generator.py, mgf_generator.py, midpoint_generator.py, minkowski_interval_generator.py, mixed_number_operation_generator.py, mobius_transform_generator.py, modular_arithmetic_generator.py, mst_generator.py, mutual_information_generator.py, naive_bayes_generator.py, named_distribution_generator.py, nets_surface_area_generator.py, newtons_laws_generator.py, normal_table_generator.py, npv_irr_generator.py, odds_probability_generator.py, operation_properties_generator.py, or_formula_generator.py, order_of_operations_generator.py, order_statistics_generator.py, ordinal_arithmetic_generator.py, parabola_features_generator.py, param_count_generator.py, partition_function_generator.py, pascal_triangle_generator.py, pca_generator.py, percent_word_problem_generator.py, perceptron_generator.py, permutation_group_generator.py, piecewise_evaluation_generator.py, pmf_cdf_quantile_generator.py, polar_parametric_generator.py, polygon_perimeter_generator.py, polynomial_zeros_generator.py, portfolio_generator.py, probability_addition_rule_generator.py, probability_axioms_finite_generator.py, probability_measure_generator.py, pythag_hyp_generator.py, quantization_generator.py, quark_composition_generator.py, quaternion_generator.py, radical_add_sub_generator.py, radical_multiply_generator.py, rational_expr_add_sub_generator.py, rationals_as_pairs_generator.py, recurrence_generator.py, recursive_definition_unfold_generator.py, recursive_explicit_generator.py, reed_solomon_generator.py, regression_generator.py, relativistic_energy_generator.py, reliability_system_generator.py, remainder_factor_theorem_generator.py, riemann_sum_generator.py, riemann_tensor_generator.py, rotational_dynamics_generator.py, round_solids_generator.py, runge_kutta_generator.py, running_coupling_generator.py, rv_transform_generator.py, segment_partition_generator.py, separable_pde_generator.py, set_counting_generator.py, shm_generator.py, sigma_notation_generator.py, simple_stats_generator.py, simplex_generator.py, softmax_gradient_generator.py, solution_chem_generator.py, spherical_excess_generator.py, spherical_triangle_generator.py, spin_half_generator.py, standard_deviation_generator.py, stars_and_bars_generator.py, statics_generator.py, stereographic_generator.py, svm_margin_generator.py, synthetic_division_generator.py, tangent_line_generator.py, taxicab_geometry_generator.py, taylor_series_generator.py, temperature_conversion_generator.py, tip_bill_split_generator.py, transfer_function_generator.py, transformation_generator.py, transportation_generator.py, triangle_solve_generator.py, trig_identity_eval_generator.py, trig_six_functions_generator.py, two_sample_test_generator.py, two_way_table_probability_generator.py, undetermined_coeff_generator.py, variation_parameters_generator.py, vector_ops_generator.py, venn_probability_generator.py, venn_region_count_generator.py, von_neumann_entropy_generator.py, wavefunction_generator.py, young_tableaux_generator.py, z_score_generator.py |
| `ABS` | 2 | `ABS\|-1/3\|1/3` | fixed_point_generator.py, matrix_norm_generator.py, rv_transform_generator.py |
| `ABSORB_EQ` | 2 | `ABSORB_EQ\|u0=p0A+p00*u0+p01*u1\|u1=p1A+p10*u0+p11*u1` | markov_chain_generator.py |
| `ABS_CASE` | 2 | `ABS_CASE\|Case 1\|x = 8` | absolute_value_equation_generator.py |
| `ABS_CHECK` | 2 | `ABS_CHECK\|-1 < 0\|Absolute value cannot be negative` | absolute_value_equation_generator.py |
| `ABS_ERROR` | 2 | `ABS_ERROR\|1\|1/100` | quantization_generator.py |
| `ABS_INEQ_CHECK` | 2 | `ABS_INEQ_CHECK\|-5 < 0\|Absolute value cannot be negative` | absolute_value_inequality_generator.py |
| `ABS_INEQ_PART` | 2 | `ABS_INEQ_PART\|Part 1\|2x - 10 ≥ 5 -> x ≥ 15/2` | absolute_value_inequality_generator.py |
| `ABS_INEQ_SETUP` | 1 | `ABS_INEQ_SETUP\|abs(2x - 10) ≥ 5` | absolute_value_inequality_generator.py |
| `ABS_INEQ_SPECIAL` | 2 | `ABS_INEQ_SPECIAL\|c = 0\|Check logic for <=` | absolute_value_inequality_generator.py |
| `ABS_INEQ_SPLIT` | 2 | `ABS_INEQ_SPLIT\|OR case\|2x - 10 ≥ 5 or 2x - 10 ≤ -5` | absolute_value_inequality_generator.py |
| `ABS_SETUP` | 1 | `ABS_SETUP\|abs(2x + 10) = 0` | absolute_value_equation_generator.py |
| `ABS_SPLIT` | 2, 3 | `ABS_SPLIT\|Single case\|2x + 10 = 0` | absolute_value_equation_generator.py |
| `ABS_VAL` | 2 | `ABS_VAL\|3\|3` | taxicab_geometry_generator.py |
| `AB_ADD` | 3 | `AB_ADD\|+4000\|5230\|9230` | abacus_addition_generator.py |
| `AB_SET` | 1 | `AB_SET\|5230` | abacus_addition_generator.py |
| `ACCEPT` | 1, 2 | `ACCEPT\|x = −49` | conditional_forms_generator.py, counterexample_search_generator.py, factor_trinomial_generator.py, knights_knaves_generator.py, log_conversion_generator.py, log_equation_generator.py, optimization_generator.py, polynomial_inequality_generator.py, radical_equation_generator.py, rational_equation_generator.py, rational_root_generator.py, set_builder_roster_generator.py, structure_isomorphism_generator.py |
| `ACT_DERIV` | 3 | `ACT_DERIV\|relu\|9\|1` | activation_generator.py |
| `ACT_SETUP` | 3 | `ACT_SETUP\|activation=relu\|x=-3\|w1=-4,b1=-3,w2=-3,b2=-2` | activation_generator.py |
| `ACT_VALUE` | 3 | `ACT_VALUE\|relu\|9\|9` | activation_generator.py |
| `AC_COMPLEX` | 3 | `AC_COMPLEX\|Z\|20\|0j` | ac_circuit_generator.py |
| `AC_FORMULA` | 1 | `AC_FORMULA\|omega0^2=1/(L*C)` | ac_circuit_generator.py |
| `AC_PRODUCT` | 2 | `AC_PRODUCT\|3 × 6\|18` | factor_trinomial_generator.py |
| `AC_SETUP` | 3 | `AC_SETUP\|resonance\|R=20, L=11\|C=1/704` | ac_circuit_generator.py |
| `ADAM_SETUP` | 3 | `ADAM_SETUP\|theta=-10,g=-3\|beta1=9/10,beta2=99/100\|lr=1/20,epsilon=0` | adam_step_generator.py |
| `ADAM_UPDATE` | 2 | `ADAM_UPDATE\|theta_new\|-199/20` | adam_step_generator.py |
| `ADD_COL` | 3 | `ADD_COL\|col_1\|0+0+0\|->0 (carry 0)` | multi_digit_addition_generator.py |
| `ADD_FORMULA` | 1 | `ADD_FORMULA\|P(A ∪ B) = P(A) + P(B) - P(A ∩ B)` | probability_addition_rule_generator.py |
| `ADD_PARTIALS` | 2 | `ADD_PARTIALS\|410370 + 3419750 + 61555500 + 68395000\|133780620` | decimal_mult_generator.py, multi_digit_multiplication_generator.py |
| `ADD_SETUP` | 2 | `ADD_SETUP\|P(A) = 2/12, P(B) = 3/12, P(A ∩ B) = 2/12\|P(A ∪ B)` | probability_addition_rule_generator.py |
| `ADJOINT` | 1 | `ADJOINT\|A^dagger=[[-13,-6],[-6,-13]]` | hermitian_check_generator.py |
| `ADJ_LIST` | 2 | `ADJ_LIST\|A\|B, C, D, E` | euler_circuit_generator.py, graph_traversal_generator.py |
| `ALG_SETUP` | 3 | `ALG_SETUP\|merge sort\|merges 5\|values 2, 34, 42, 44, 38, 47` | algorithm_trace_generator.py |
| `ALIGN_NUM` | 2 | `ALIGN_NUM\|046.36\|177.07` | number_comparison_generator.py |
| `ALPHA` | 2 | `ALPHA\|line 1\|2: x ∧ (¬x ∧ ¬x); 3: r ∧ (r ∧ ¬r)` | kernel_ridge_generator.py, semantic_tableau_generator.py |
| `ALPHA_RENAME` | 2 | `ALPHA_RENAME\|lambda p. (lambda p. (p b))\|lambda z. (lambda p. (p b))` | lambda_reduction_generator.py |
| `AMORT_ROW` | 3 | `AMORT_ROW\|1\|interest=$7404.00\|principal=$13671.00,balance=$48029.00` | annuity_generator.py |
| `AMPLITUDE` | 2 | `AMPLITUDE\|abs(4)\|4` | sinusoid_features_generator.py |
| `ANALOGY_SETUP` | 3 | `ANALOGY_SETUP\|man=(-1,2)\|woman=(-3,2)\|king=(-1,-1)` | embedding_similarity_generator.py |
| `ANALOGY_VECTOR` | 2 | `ANALOGY_VECTOR\|king-man+woman\|(-3,-1)` | embedding_similarity_generator.py |
| `ANGLE` | 2 | `ANGLE\|theta\|pi/6` | positional_encoding_generator.py |
| `ANGLE_DEFECT_SETUP` | 2 | `ANGLE_DEFECT_SETUP\|R=13\|angles=15,30,75` | angle_defect_generator.py |
| `ANGLE_EVAL` | 2 | `ANGLE_EVAL\|theta=0..2*pi\|2*pi` | triple_integral_generator.py |
| `ANGLE_FORMULA` | 1 | `ANGLE_FORMULA\|degrees = radians · 180/π` | angle_measure_generator.py |
| `ANGLE_RELATION` | 1 | `ANGLE_RELATION\|angle1 + angle2 = 180°` | angle_relationships_generator.py |
| `ANGLE_SETUP` | 2 | `ANGLE_SETUP\|supplementary\|angle1 = 116°` | angle_relationships_generator.py |
| `ANGLE_SOLVE` | 2 | `ANGLE_SOLVE\|180 - 116\|64` | angle_relationships_generator.py |
| `ANGLE_WRAP` | 2 | `ANGLE_WRAP\|275 deg\|-85 deg` | complex_log_generator.py |
| `ANNUITY_FORMULA` | 1 | `ANNUITY_FORMULA\|FV = PMT*((1+r)^n - 1)/r` | annuity_generator.py |
| `ANNUITY_SETUP` | 2, 3 | `ANNUITY_SETUP\|ordinary annuity future value\|PMT=8432,r=50%,n=7` | annuity_generator.py |
| `ANTICHAIN` | 2 | `ANTICHAIN\|{32, 40}\|size 2` | partial_order_generator.py |
| `ANTICOMM_ENTRY` | 3 | `ANTICOMM_ENTRY\|(1,1)\|0 + 0\|0` | pauli_algebra_generator.py |
| `ANTIDERIV` | 2 | `ANTIDERIV\|3 cos(x)\|3 sin(x)` | antiderivative_generator.py, arc_length_generator.py, area_between_curves_generator.py, definite_integral_generator.py, improper_integral_generator.py, integrating_factor_generator.py, integration_by_parts_generator.py, ode_substitution_generator.py, parametric_calculus_generator.py, partial_fractions_generator.py, separable_ode_generator.py, solid_revolution_generator.py, u_substitution_generator.py, variation_parameters_generator.py |
| `ANTIDERIVATIVE` | 1 | `ANTIDERIVATIVE\|-A*cos(nx)/n` | fourier_series_generator.py |
| `ANTISYM_CHECK` | 3 | `ANTISYM_CHECK\|(2, 3)\|reverse (3, 2)\|violation` | relation_check_generator.py |
| `APPLY` | 3 | `APPLY\|∧I\|1,2\|d ∧ p` | natural_deduction_generator.py |
| `APPLY_GATE` | 3 | `APPLY_GATE\|H\|e^(i233π/137)·ket1\|e^(i233π/137)·(ket0 - ket1)/sqrt(2)` | quantum_gate_generator.py |
| `APPLY_OPERATOR` | 2 | `APPLY_OPERATOR\|L[A]\|-3A = 3` | commutator_generator.py, undetermined_coeff_generator.py |
| `APPLY_PAULI` | 2 | `APPLY_PAULI\|sigma_x ket0\|ket1` | spin_half_generator.py |
| `APPLY_SUBST` | 1 | *(not observed in sampling)* | unification_generator.py |
| `APPROX` | 2 | `APPROX\|12*d^2*L\|44040192` | param_count_generator.py |
| `APPROX_ENTRY` | 2 | `APPROX_ENTRY\|(1,1)\|17` | low_rank_approx_generator.py |
| `APPROX_SETUP` | 2 | `APPROX_SETUP\|estimate √63\|linearize f(x) = √x at a = 64` | linear_approx_generator.py |
| `ARCCOS` | 2 | `ARCCOS\|cos(c)=1/2\|c=pi/3` | great_circle_generator.py |
| `ARCLEN_FORMULA` | 1 | `ARCLEN_FORMULA\|L = ∫ √((dx/dt)^2 + (dy/dt)^2) dt` | arc_length_generator.py, parametric_calculus_generator.py |
| `ARC_FORMULA` | 1 | `ARC_FORMULA\|L = (θ/360)·2πr` | arc_sector_generator.py |
| `ARC_LENGTH` | 3 | `ARC_LENGTH\|int_0^T speed dt\|5*2\|10` | curve_geometry_generator.py |
| `ARC_SETUP` | 2 | `ARC_SETUP\|circle r = 28, central angle 100°\|arc length` | arc_sector_generator.py |
| `AREA` | 1 | `AREA\|66` | geometry_area_perimeter_generator.py |
| `AREA_INT` | 3 | `AREA_INT\|A = int y dx\|2^3/3\|8/3` | centroid_generator.py |
| `AREA_INTEGRAL` | 2 | `AREA_INTEGRAL\|sqrt(EG-F^2)=R^2 sin(phi)\|area = R^2*theta*(cos phi1 - cos phi2)` | fundamental_form_generator.py |
| `AREA_SCALE` | 3 | `AREA_SCALE\|uv rectangle area\|6*9\|54` | jacobian_generator.py |
| `AREA_SETUP` | 2 | `AREA_SETUP\|y = x^2 - 4x + 2 and y = -8x + 7\|area between the curves` | area_between_curves_generator.py |
| `ARGUMENT` | 2 | `ARGUMENT\|(0,-6)\|270 deg` | complex_log_generator.py, euler_formula_generator.py |
| `ARG_SETUP` | 2 | `ARG_SETUP\|(p ∧ ¬q) → ¬(r ∨ q); ¬(r ∨ q)\|p ∧ ¬q` | argument_form_generator.py |
| `ARITH_INTERVAL` | 1 | `ARITH_INTERVAL\|[3/4,1)` | arithmetic_coding_generator.py |
| `ARITH_SETUP` | 2 | `ARITH_SETUP\|A=1/8, B=3/8, C=1/4, D=1/4\|message=DCDC` | arithmetic_coding_generator.py |
| `ARITH_SYMBOL` | 2 | `ARITH_SYMBOL\|D\|cum=[3/4,1)` | arithmetic_coding_generator.py |
| `ARRAY_STATE` | 2 | `ARRAY_STATE\|pass 1\|2, 24, 14, 9, 25, 30` | algorithm_trace_generator.py |
| `ASSIGN` | 2 | `ASSIGN\|P1\|C2` | kmeans_step_generator.py |
| `ASSUME` | 1 | `ASSUME\|assume e is the greatest integer` | direct_proof_algebra_generator.py, induction_verify_generator.py |
| `ASYMPTOTE` | 1 | `ASYMPTOTE\|y = ±(3/2)(x + 2)` | hyperbola_features_generator.py |
| `ATA` | 2 | `ATA\|A^T A\|[[3700, 1200], [1200, 3700]]` | svd_generator.py |
| `ATOM_CHECK` | 3 | `ATOM_CHECK\|C\|left=3\|right=3` | stoichiometry_generator.py |
| `ATTN_OUTPUT` | 2 | `ATTN_OUTPUT\|1\|[[-3/2,-3]]` | attention_generator.py |
| `ATTN_SCORE` | 2 | `ATTN_SCORE\|1,1\|0` | attention_generator.py |
| `ATTN_SETUP` | 1, 3 | `ATTN_SETUP\|tokens=2,d=2\|Q=[[0,0], [0,0]]\|K=[[0,0], [0,0]]` | attention_generator.py |
| `ATTR_CHECK` | 3 | `ATTR_CHECK\|4\|A: odd\|no` | attribute_sorting_generator.py |
| `AV_VECTOR` | 2 | `AV_VECTOR\|A*v1\|[70/√2, 70/√2]` | svd_generator.py |
| `AXIOM` | 2 | `AXIOM\|total probability\|Σ P(ω) = 1` | probability_axioms_finite_generator.py, probability_measure_generator.py |
| `AXIOM_MATCH` | 2 | `AXIOM_MATCH\|L1\|p := ((a ∨ c) → g), q := ((n → c) → (h ∨ e))` | hilbert_axiom_derivation_generator.py |
| `B` | 1, 3 | `B\|38\|1\|381` | decimal_div_generator.py, long_division_generator.py, percent_problem_generator.py, polynomial_long_division_generator.py |
| `BABY_STEP` | 2 | `BABY_STEP\|j=0\|1` | baby_step_giant_step_generator.py |
| `BACKPROP_DELTA` | 2 | `BACKPROP_DELTA\|h1\|delta=18` | backprop_generator.py |
| `BACKPROP_GRAD` | 2 | `BACKPROP_GRAD\|dL/dy_hat\|-9` | backprop_generator.py |
| `BACKPROP_SETUP` | 3 | `BACKPROP_SETUP\|x=(-3,-3)\|y=3\|eta=1/7` | backprop_generator.py |
| `BACK_SUB` | 2 | `BACK_SUB\|u = 1/y\|y = 1/(1 + e^(4x))` | ode_substitution_generator.py |
| `BACK_SUB_ROW` | 3 | `BACK_SUB_ROW\|r=68\|x=1\|y=0` | extended_euclid_generator.py, modular_inverse_generator.py, rsa_generator.py |
| `BALANCED_EQ` | 1 | `BALANCED_EQ\|C3H8 + 5 O2 -> 3 CO2 + 4 H2O` | stoichiometry_generator.py |
| `BALANCE_COEFFS` | 2 | `BALANCE_COEFFS\|reactants=1,5\|products=3,4` | stoichiometry_generator.py |
| `BASE` | 2 | `BASE\|rev(ε)\|ε` | recursive_definition_unfold_generator.py |
| `BASE_ADD_COL` | 3 | `BASE_ADD_COL\|col 0\|2 + 6 + carry 0\|8 -> digit 0, carry 1` | base_arithmetic_generator.py |
| `BASE_ARITH_SETUP` | 2 | `BASE_ARITH_SETUP\|base 8\|35 * 3` | base_arithmetic_generator.py |
| `BASE_CARRY` | 2 | `BASE_CARRY\|carry 1\|digit 1, carry 0` | base_arithmetic_generator.py |
| `BASE_MUL_COL` | 3 | `BASE_MUL_COL\|col 0\|5 * 3 + carry 0\|15 -> digit 7, carry 1` | base_arithmetic_generator.py |
| `BASE_SETUP` | 2 | `BASE_SETUP\|11110111_2\|decimal` | base_conversion_generator.py |
| `BAYES_CELL` | 3 | `BAYES_CELL\|true positive\|196 × 3/4\|147` | conditional_probability_generator.py |
| `BAYES_EVIDENCE` | 2 | `BAYES_EVIDENCE\|sum of Bayes terms\|11/108` | bayes_multiple_hypotheses_generator.py |
| `BAYES_FORMULA` | 1 | `BAYES_FORMULA\|P(disease=no given negative) = TN/(TN + FN)` | conditional_probability_generator.py |
| `BAYES_SETUP` | 3 | `BAYES_SETUP\|disease=yes 196, disease=no 910\|sensitivity 3/4, specificity 23/26\|P(disease=no given test negative)` | conditional_probability_generator.py |
| `BAYES_STAGE` | 2 | `BAYES_STAGE\|observe H, H, T\|prior × likelihood for every hypothesis` | bayes_multiple_hypotheses_generator.py |
| `BAYES_TERM` | 3 | `BAYES_TERM\|C1\|1/2 × 2/27\|1/27` | bayes_multiple_hypotheses_generator.py |
| `BAYES_UPDATE_SETUP` | 2, 3 | `BAYES_UPDATE_SETUP\|beta_binomial\|prior=Beta(5,3)\|successes=13, trials=18` | bayesian_update_generator.py |
| `BCH_FORM` | 2 | `BCH_FORM\|A+B+1/2[A,B]\|[[0, 0, 0], [1/2, 0, 1], [1, 0, 0]]` | bch_generator.py |
| `BCH_SETUP` | 3 | `BCH_SETUP\|A=E23\|B=E31\|order=2` | bch_generator.py |
| `BEC_FORMULA` | 1 | `BEC_FORMULA\|P(no erasures)=(1-epsilon)^n` | bec_channel_generator.py |
| `BEC_SETUP` | 1 | `BEC_SETUP\|epsilon=1/2` | bec_channel_generator.py |
| `BELL_ROW` | 3 | `BELL_ROW\|n=1\|1\|1` | set_counting_generator.py |
| `BEREZIN_RULE` | 2 | `BEREZIN_RULE\|int dtheta 1\|0` | grassmann_generator.py |
| `BETA` | 1, 3 | `BETA\|line 1\|1L: 2: r ∨ u\|1R: 3: ¬r ∨ ¬e` | lambda_reduction_generator.py, semantic_tableau_generator.py |
| `BETA_COUNT` | 1 | `BETA_COUNT\|4` | lambda_reduction_generator.py |
| `BEZOUT_CHECK` | 2 | `BEZOUT_CHECK\|68*4 + 54*-5\|2` | extended_euclid_generator.py |
| `BIAS_CORRECT` | 2 | `BIAS_CORRECT\|m_hat\|-3` | adam_step_generator.py |
| `BIJECTION_RULE` | 2 | `BIJECTION_RULE\|e(n)\|2n` | countability_bijection_generator.py |
| `BINARY` | 2 | `BINARY\|10652\|10100110011100` | countability_bijection_generator.py |
| `BINARY_EXPONENT` | 2 | `BINARY_EXPONENT\|14\|1110` | mod_exp_generator.py, quadratic_residue_generator.py |
| `BINOM_FORMULA` | 1 | `BINOM_FORMULA\|P(X ≥ 1) = 1 - (1-p)^n` | binomial_probability_generator.py |
| `BINOM_SETUP` | 2 | `BINOM_SETUP\|n = 100, p = 1/2\|P(X = 56)` | binomial_probability_generator.py, normal_approx_binomial_generator.py |
| `BISECTION_SETUP` | 3 | `BISECTION_SETUP\|f(x)=x^2-83\|interval=[9, 10]\|iterations=5` | bisection_generator.py |
| `BISECT_UPDATE` | 3 | `BISECT_UPDATE\|1\|product < 0\|[9, 19/2]` | bisection_generator.py |
| `BIT` | 1, 2 | `BIT\|b\|v=1` | characteristic_vector_generator.py |
| `BITWISE` | 1 | `BITWISE\|∧\|101001111\|111111111\|101001111` | characteristic_vector_generator.py |
| `BIT_ROW` | 2, 3 | `BIT_ROW\|bit 0\|1 OR 1\|1` | bitwise_ops_generator.py |
| `BIT_RULE` | 2 | `BIT_RULE\|OR\|1 when at least one bit is 1` | bitwise_ops_generator.py |
| `BIT_SETUP` | 2 | `BIT_SETUP\|1101 OR 1001\|4-bit mask` | bitwise_ops_generator.py |
| `BLACKBODY_FORMULA` | 1 | `BLACKBODY_FORMULA\|P=sigma*A*T^4` | blackbody_generator.py |
| `BLACKBODY_SETUP` | 3 | `BLACKBODY_SETUP\|stefan_power\|sigma=1, A=7\|T=14` | blackbody_generator.py |
| `BOND_FORMULA` | 1 | `BOND_FORMULA\|price=sum coupon/(1+y)^t + face/(1+y)^n` | bond_pricing_generator.py |
| `BOND_PRICE` | 1 | `BOND_PRICE\|$3697.28` | bond_pricing_generator.py |
| `BOND_SETUP` | 2 | `BOND_SETUP\|face=5300\|coupon=4%,ytm=25%,years=2` | bond_pricing_generator.py |
| `BOOL_SETUP` | 2 | `BOOL_SETUP\|variables R, S, T\|CNF from F=0 rows` | boolean_algebra_generator.py |
| `BORROW` | 3 | `BORROW\|col_1\|from_left\|1` | multi_digit_subtraction_generator.py |
| `BOX_FORMULA` | 1 | `BOX_FORMULA\|E_n=n^2*h^2/(8*m*L^2)` | particle_in_box_generator.py |
| `BOX_SETUP` | 1, 3 | `BOX_SETUP\|energy_level\|n=1, h=5\|m=8, L=10` | particle_in_box_generator.py |
| `BRAKET_FORMULA` | 1 | `BRAKET_FORMULA\|inner(phi,psi)=sum conj(phi_k)*psi_k` | braket_generator.py |
| `BRAKET_SETUP` | 3 | `BRAKET_SETUP\|inner_product\|phi=[-1+i,-1,-i]\|psi=[2,2-i,i]` | braket_generator.py |
| `BRANCH_CLOSE` | 2 | `BRANCH_CLOSE\|1\|x, ¬x` | semantic_tableau_generator.py |
| `BRANCH_OPEN` | 2 | `BRANCH_OPEN\|1LL\|e=F, r=T, u=F` | semantic_tableau_generator.py |
| `BRANCH_SUM` | 3 | `BRANCH_SUM\|SF + FS\|5/42 + 5/12\|15/28` | tree_diagram_probability_generator.py |
| `BRANCH_TEST` | 2 | `BRANCH_TEST\|-3 < -3\|no` | piecewise_evaluation_generator.py |
| `BRANCH_USE` | 1 | `BRANCH_USE\|$6.00` | piecewise_evaluation_generator.py |
| `BRING_DOWN` | 2 | `BRING_DOWN\|group 26\|current = 26` | composite_arithmetic_generator.py, manual_square_root_generator.py |
| `BSC_FORMULA` | 1 | `BSC_FORMULA\|H_b=p*(-log2 p)+(1-p)*(-log2(1-p))` | channel_capacity_generator.py |
| `BSC_SETUP` | 3 | `BSC_SETUP\|p=1/4\|-log2(p)=2\|-log2(1-p)=0.415` | channel_capacity_generator.py |
| `BSGS_MATCH` | 3 | `BSGS_MATCH\|i=4\|j=0\|x=24` | baby_step_giant_step_generator.py |
| `BSGS_SETUP` | 4 | `BSGS_SETUP\|p=31\|g=3\|h=2\|m=6` | baby_step_giant_step_generator.py |
| `BS_FORMULA` | 2 | `BS_FORMULA\|C=S*N(d1)-K*df*N(d2)\|P=K*df*N(-d2)-S*N(-d1)` | black_scholes_generator.py |
| `BS_RESULT` | 2 | `BS_RESULT\|call=7\|put=3` | black_scholes_generator.py |
| `BS_SETUP` | 3 | `BS_SETUP\|S=80,K=80\|df=0.95\|N_d1=0.8,N_d2=0.75` | black_scholes_generator.py |
| `C` | 3 | `C\|1/3\|21\|7/21` | complement_probability_generator.py, experimental_probability_generator.py, fraction_comparison_generator.py, fraction_op_generator.py, mixed_number_operation_generator.py, rational_expr_add_sub_generator.py |
| `CALC` | 1 | `CALC\|y = 1` | systems_elimination_generator.py, systems_substitution_generator.py |
| `CAL_DIVMOD` | 3 | `CAL_DIVMOD\|32\|7\|4 R4` | calendar_arithmetic_generator.py |
| `CAL_FORMULA` | 1 | `CAL_FORMULA\|warm ice: q1=m*c_ice*(0-Ti)` | calorimetry_generator.py |
| `CAL_SETUP` | 3 | `CAL_SETUP\|2024-05-12\|Sunday, offset 38 days\|weekday` | calendar_arithmetic_generator.py, calorimetry_generator.py |
| `CANCEL` | 2 | `CANCEL\|4x\|4x - 7` | derivative_limit_def_generator.py, derivative_transcendental_generator.py, limit_evaluation_generator.py, power_series_generator.py, rational_expr_mult_div_generator.py, rational_expr_simplify_generator.py, rational_function_features_generator.py, series_convergence_generator.py, trig_identity_verify_generator.py |
| `CANDIDATES` | 1 | `CANDIDATES\|±1/2, ±1, ±3/2, ±5/2, ±3, ±5, ±15/2, ±15` | rational_root_generator.py |
| `CANONICAL_ORDER` | 1 | `CANONICAL_ORDER\|D=1, A=2, B=4, C=4` | kraft_inequality_generator.py |
| `CANONICAL_SHIFT` | 3 | `CANONICAL_SHIFT\|code=0\|left=1\|0` | kraft_inequality_generator.py |
| `CARD_RULE` | 2 | `CARD_RULE\|infinite addition and multiplication\|κ + λ = κ · λ = max(κ, λ)` | cardinal_arithmetic_generator.py |
| `CARRY_FINAL` | 1 | `CARRY_FINAL\|1` | multi_digit_addition_generator.py |
| `CARTESIAN_RESULT` | 1 | `CARTESIAN_RESULT\|{(t, 4), (t, 5), (t, 14)}` | set_operations_generator.py |
| `CART_PAIR` | 3 | `CART_PAIR\|t\|4\|(t, 4)` | set_operations_generator.py |
| `CASE` | 1, 2, 3 | `CASE\|jade-jade token 1\|observed jade\|other jade` | classic_probability_puzzles_generator.py, countability_bijection_generator.py, knights_knaves_generator.py |
| `CASHFLOW_PV` | 2 | `CASHFLOW_PV\|coupon_t1\|169.6` | bond_pricing_generator.py |
| `CASIMIR_FORCE_SETUP` | 2 | `CASIMIR_FORCE_SETUP\|F/A=-π^2*hbar*c/(240*d^4)\|hbar=11,c=6,d=5` | casimir_force_generator.py |
| `CASIMIR_SETUP` | 3 | `CASIMIR_SETUP\|spin=5\|hbar=59/7\|J^2=j(j+1)hbar^2` | casimir_generator.py |
| `CAYLEY_HEADER` | 1 | `CAYLEY_HEADER\|e, r, r2, s, rs, r2s` | cayley_table_generator.py |
| `CAYLEY_ROW` | 2 | `CAYLEY_ROW\|row e\|e, r, r2, s, rs, r2s` | cayley_table_generator.py |
| `CBRT` | 2 | `CBRT\|64y^3\|4y` | factor_special_forms_generator.py, inverse_function_generator.py, rational_exponent_generator.py |
| `CDF_EVENT` | 3 | `CDF_EVENT\|Y<=y\|X^2<=y\|X<=sqrt(y)` | rv_transform_generator.py |
| `CDF_FORMULA` | 2 | `CDF_FORMULA\|F_Y(y)=sqrt(y)/28\|0<=y<=784` | rv_transform_generator.py |
| `CDF_ROW` | 2 | `CDF_ROW\|-25\|1/4` | distribution_of_sum_generator.py, pmf_cdf_quantile_generator.py |
| `CEIL` | 2 | `CEIL\|422.81640625\|423` | confidence_interval_generator.py |
| `CENTER` | 1, 2 | `CENTER\|(0, -1)` | circle_equation_generator.py, ellipse_features_generator.py, hyperbola_features_generator.py, pca_generator.py |
| `CENTROID_COORD` | 3 | `CENTROID_COORD\|xbar = M_y/A\|(4)/(8/3)\|3/2` | centroid_generator.py |
| `CENTROID_SETUP` | 3 | `CENTROID_SETUP\|0 <= y <= x^2\|0 <= x <= 2\|centroid` | centroid_generator.py |
| `CENTROID_UPDATE` | 2 | `CENTROID_UPDATE\|C1\|(-4,-2)` | kmeans_step_generator.py |
| `CF_PARTIAL` | 2 | `CF_PARTIAL\|a_0\|3` | continued_fraction_generator.py |
| `CF_RESULT` | 1 | `CF_RESULT\|[3; 7, 1, 10]` | continued_fraction_generator.py |
| `CF_SETUP` | 1 | `CF_SETUP\|272/87` | continued_fraction_generator.py |
| `CG_COEFF` | 2 | `CG_COEFF\|ket(1,-)\|-sqrt(2/3)` | clebsch_gordan_generator.py |
| `CG_SETUP` | 3 | `CG_SETUP\|j1=1/2\|j2=1/2\|phase=-` | clebsch_gordan_generator.py |
| `CG_STATE` | 2 | `CG_STATE\|J=1, M=-1\|-ket(-,-)` | clebsch_gordan_generator.py |
| `CHAIN` | 2 | `CHAIN\|{6, 40, 43, 55}\|length 4` | partial_order_generator.py |
| `CHAIN_DERIV` | 2 | `CHAIN_DERIV\|dy/dx\|12` | activation_generator.py |
| `CHAIN_RATE` | 2 | `CHAIN_RATE\|x_s\|3` | multivar_chain_rule_generator.py |
| `CHAIN_SUM` | 3 | `CHAIN_SUM\|f_x*x_s + f_y*y_s\|130*3 + (-98)*(-2)\|586` | multivar_chain_rule_generator.py |
| `CHAIN_VALUE` | 3 | `CHAIN_VALUE\|x(0,3)\|2*3 + 5\|11` | multivar_chain_rule_generator.py |
| `CHANGE_BASE` | 1 | `CHANGE_BASE\|log_27(81) = log_3(81)/log_3(27)` | log_conversion_generator.py |
| `CHAR_DIAG` | 2 | `CHAR_DIAG\|diagonal of λI - A\|(λ - 4), (λ + 1)` | eigenvalue_generator.py |
| `CHAR_EQ` | 2 | `CHAR_EQ\|assume y=e^(rx)\|r^2 - 8r + 16 = 0` | ode_system_generator.py, second_order_ode_generator.py, undetermined_coeff_generator.py, variation_parameters_generator.py |
| `CHAR_POLY` | 2 | `CHAR_POLY\|p(λ) = λ^2 - 3λ - 4\|(λ + 1)*(λ - 4)` | diagonalization_generator.py, eigenvalue_generator.py, recurrence_generator.py |
| `CHAR_ROOTS` | 2 | `CHAR_ROOTS\|r = 4\|repeated` | recurrence_generator.py, second_order_ode_generator.py, undetermined_coeff_generator.py, variation_parameters_generator.py |
| `CHAR_SETUP` | 2 | `CHAR_SETUP\|p(λ) = det(λI - A)\|triangular determinant` | eigenvalue_generator.py |
| `CHECK` | 1, 2, 3, 4 | `CHECK\|multiply_back\|23×98+45=2299\|2299` | annuity_generator.py, area_between_curves_generator.py, arithmetic_sequence_generator.py, baby_step_giant_step_generator.py, base_arithmetic_generator.py, bayes_multiple_hypotheses_generator.py, bch_generator.py, bitwise_ops_generator.py, boolean_algebra_generator.py, cantor_diagonal_generator.py, cantor_pairing_generator.py, cardinal_arithmetic_generator.py, casimir_generator.py, cauchy_riemann_generator.py, characteristic_vector_generator.py, chi_square_generator.py, cholesky_generator.py, classic_probability_puzzles_generator.py, clebsch_gordan_generator.py, combinatory_logic_generator.py, commutator_generator.py, complement_probability_generator.py, completing_square_generator.py, conditional_expectation_generator.py, conditional_probability_generator.py, convolutional_code_viterbi_generator.py, coset_generator.py, countability_bijection_generator.py, covariance_algebra_generator.py, cramers_rule_generator.py, cyclic_group_generator.py, cyk_parser_generator.py, dedekind_cut_generator.py, dfa_minimization_generator.py, dfa_simulation_generator.py, diagonalization_generator.py, diffie_hellman_generator.py, discrete_uniform_bernoulli_generator.py, distribution_of_sum_generator.py, ecdh_generator.py, ecdsa_generator.py, eigenvalue_generator.py, elliptic_curve_finite_field_generator.py, embedding_similarity_generator.py, equilibrium_ice_generator.py, error_spotting_generator.py, euler_circuit_generator.py, exact_ode_generator.py, expectation_of_function_generator.py, expected_value_generator.py, experimental_probability_generator.py, extended_euclid_generator.py, factor_gcf_generator.py, factor_grouping_generator.py, factor_special_forms_generator.py, factor_trinomial_generator.py, feature_map_generator.py, fill_in_step_generator.py, five_number_summary_generator.py, foundations_critic_generator.py, function_inner_product_generator.py, fundamental_counting_principle_generator.py, game_theory_generator.py, gamma_matrix_generator.py, gauss_bonnet_generator.py, gaussian_curvature_generator.py, geometric_mean_generator.py, geometric_probability_generator.py, geometric_sequence_generator.py, godel_numbering_generator.py, gradient_generator.py, gram_schmidt_generator.py, graph_counting_generator.py, hamming_code_generator.py, hereditarily_finite_set_generator.py, hermitian_check_generator.py, hessian_classify_generator.py, hilbert_axiom_derivation_generator.py, horner_evaluation_generator.py, hyperbolic_function_generator.py, hypergeometric_generator.py, hypothesis_test_generator.py, independence_check_generator.py, index_gymnastics_generator.py, induction_verify_generator.py, information_gain_generator.py, integers_as_pairs_generator.py, inverse_function_generator.py, kernel_perceptron_generator.py, kernel_validity_generator.py, kmeans_step_generator.py, knights_knaves_generator.py, knn_generator.py, ladder_operator_generator.py, lagrange_multiplier_generator.py, lambda_reduction_generator.py, law_of_total_probability_generator.py, least_squares_generator.py, legendre_construction_generator.py, lhopital_generator.py, lie_exponential_generator.py, likelihood_language_generator.py, limit_evaluation_generator.py, line_integral_generator.py, linear_fractional_generator.py, linearity_of_expectation_generator.py, lll_reduction_generator.py, log_equation_generator.py, logic_grid_puzzle_generator.py, logical_equivalence_laws_generator.py, long_division_generator.py, low_rank_approx_generator.py, lp_corner_generator.py, lu_decomposition_generator.py, lz_compression_generator.py, manual_square_root_generator.py, markov_chain_generator.py, matrix_exponential_generator.py, matrix_group_check_generator.py, matrix_inverse_generator.py, mean_value_theorem_generator.py, method_of_moments_generator.py, mle_generator.py, mobius_transform_generator.py, modular_arithmetic_generator.py, modular_inverse_generator.py, naive_bayes_generator.py, natural_deduction_generator.py, nfa_simulation_generator.py, normal_approx_binomial_generator.py, normal_table_generator.py, odds_probability_generator.py, ode_system_generator.py, operation_properties_generator.py, or_formula_generator.py, ordinal_arithmetic_generator.py, partial_derivative_generator.py, partial_order_generator.py, partial_trace_generator.py, pauli_algebra_generator.py, pca_generator.py, pda_simulation_generator.py, peano_arithmetic_generator.py, perceptron_generator.py, pmf_cdf_quantile_generator.py, pollard_factorization_generator.py, polynomial_inequality_generator.py, positive_definite_generator.py, power_series_generator.py, prenex_normal_form_generator.py, prime_factorization_generator.py, probability_axioms_finite_generator.py, probability_measure_generator.py, projector_generator.py, qr_decomposition_generator.py, quadratic_factoring_generator.py, quadratic_square_root_generator.py, quantifier_negation_generator.py, quaternion_generator.py, radical_variable_simplify_generator.py, ratio_table_generator.py, rationals_as_pairs_generator.py, recursive_explicit_generator.py, regex_to_automaton_generator.py, relation_closure_generator.py, resolution_proof_generator.py, riemann_tensor_generator.py, rotational_dynamics_generator.py, routh_hurwitz_generator.py, rsa_generator.py, running_coupling_generator.py, rv_transform_generator.py, sample_space_list_generator.py, semantic_tableau_generator.py, series_convergence_generator.py, set_algebra_laws_generator.py, shm_generator.py, signal_arithmetic_generator.py, similar_triangles_generator.py, simple_probability_generator.py, simplex_generator.py, special_solution_equation_generator.py, statics_generator.py, stereographic_generator.py, structure_constant_generator.py, structure_isomorphism_generator.py, svd_generator.py, svm_margin_generator.py, syllogism_generator.py, systems_elimination_generator.py, taylor_series_generator.py, tip_bill_split_generator.py, tonelli_shanks_generator.py, totient_generator.py, transportation_generator.py, tree_diagram_probability_generator.py, turing_machine_trace_generator.py, two_sample_test_generator.py, two_step_equation_generator.py, type_theory_generator.py, uncertainty_generator.py, venn_region_count_generator.py, young_tableaux_generator.py, z_score_generator.py, zf_axiom_identify_generator.py |
| `CHECK_POINT` | 3 | `CHECK_POINT\|x=0\|11·0 + 16 = 16\|11·0 + 11 = 11` | special_solution_equation_generator.py |
| `CHINCHILLA` | 2 | `CHINCHILLA\|20N\|400000000` | scaling_law_generator.py |
| `CHI_FORMULA` | 1 | `CHI_FORMULA\|E = (row·col)/N; χ² = Σ (O - E)^2/E` | chi_square_generator.py |
| `CHI_SETUP` | 2 | `CHI_SETUP\|row 1: 42, 18; row 2: 78, 62; N = 200\|independence; df = 1, critical value = 3.841` | chi_square_generator.py |
| `CHI_TERM` | 3 | `CHI_TERM\|42 - 36 = 6\|6^2 = 36\|36/36 = 1` | chi_square_generator.py |
| `CHOLESKY_ENTRY` | 2 | `CHOLESKY_ENTRY\|l11\|3` | cholesky_generator.py |
| `CHOL_SETUP` | 2 | `CHOL_SETUP\|A = [[9, 6, 6], [6, 8, 8], [6, 8, 9]]\|A = L L^T` | cholesky_generator.py |
| `CHRISTOFFEL_FORMULA` | 1 | `CHRISTOFFEL_FORMULA\|Gamma^i_jk = 1/2 g^im(d_j g_mk + d_k g_mj - d_m g_jk)` | christoffel_generator.py |
| `CHRISTOFFEL_SETUP` | 3 | `CHRISTOFFEL_SETUP\|polar\|g_rr=1, g_thetatheta=r^2\|r=74` | christoffel_generator.py |
| `CHRISTOFFEL_VALUE` | 2 | `CHRISTOFFEL_VALUE\|Gamma^phi_thetatheta\|-7140/22201` | riemann_tensor_generator.py |
| `CHURCH_NUMERAL` | 2 | `CHURCH_NUMERAL\|2\|lambda f. (lambda g. (f (f g)))` | lambda_reduction_generator.py |
| `CIRCLE_ANGLE_SETUP` | 2 | `CIRCLE_ANGLE_SETUP\|inscribed angle 16°\|central angle on the same arc` | circle_angle_generator.py |
| `CIRCLE_CALCULATE` | 2 | `CIRCLE_CALCULATE\|A = π × 324\|324π` | circle_generator.py |
| `CIRCLE_EQ` | 1 | `CIRCLE_EQ\|(x - 2)^2 + (y - 6)^2 = 1` | complex_locus_generator.py |
| `CIRCLE_FORMULA` | 1 | `CIRCLE_FORMULA\|A = πr²` | circle_generator.py |
| `CIRCLE_SETUP` | 2 | `CIRCLE_SETUP\|18\|radius` | circle_equation_generator.py, circle_generator.py |
| `CIRCLE_SUBSTITUTE` | 1 | `CIRCLE_SUBSTITUTE\|A = π × 18²` | circle_generator.py |
| `CIRCULATION_SUM` | 2 | `CIRCULATION_SUM\|(-8 - 0)*132\|-1056` | vector_theorem_generator.py |
| `CI_FORMULA` | 1 | `CI_FORMULA\|x̄ ± E` | confidence_interval_generator.py |
| `CI_SETUP` | 2 | `CI_SETUP\|p̂ = 0.5, E = 0.04, z* = 1.645\|minimum sample size for the proportion` | confidence_interval_generator.py |
| `CLASS` | 2 | `CLASS\|[5]\|{5, 11, 22, 40}` | equivalence_relation_generator.py |
| `CLASSIFY` | 2 | `CLASSIFY\|contingency\|T at 6 of 8 rows` | foundations_critic_generator.py, truth_table_generator.py |
| `CLAUSE` | 2 | `CLAUSE\|C1\|(¬P89196)` | resolution_proof_generator.py |
| `CLIFFORD_EXPECT` | 3 | `CLIFFORD_EXPECT\|2*eta=0\|I_entry=0\|0` | gamma_matrix_generator.py |
| `CLOSURE_ADD` | 2 | `CLOSURE_ADD\|(4, 26)\|symmetric` | relation_closure_generator.py |
| `CLUE_APPLY` | 3 | `CLUE_APPLY\|clue 1\|Gia has book\|24 → 6 candidates` | logic_grid_puzzle_generator.py |
| `CLUSTER_MEMBERS` | 2 | `CLUSTER_MEMBERS\|C1\|P2,P3` | kmeans_step_generator.py |
| `CMP` | 2, 3 | `CMP\|44\|9\|>` | dedekind_cut_generator.py, experimental_probability_generator.py, fraction_comparison_generator.py, graph_interpret_generator.py, integers_as_pairs_generator.py, likelihood_language_generator.py, logical_connective_eval_generator.py, pmf_cdf_quantile_generator.py, probability_measure_generator.py, rationals_as_pairs_generator.py, set_builder_roster_generator.py |
| `CMP_DIGIT` | 4 | `CMP_DIGIT\|pos_0\|0\|1\|<` | number_comparison_generator.py |
| `CMP_NUM` | 3 | `CMP_NUM\|46.36\|177.07\|<` | number_comparison_generator.py |
| `CNF` | 1 | `CNF\|ω^2 + ω + 2` | ordinal_arithmetic_generator.py |
| `CNF_FORM` | 1 | `CNF_FORM\|(R OR NOT S OR T) AND (R OR NOT S OR NOT T) AND (NOT R OR S OR T) AND (NOT R OR S OR NOT T) AND (NOT R OR NOT S OR T) AND (NOT R OR NOT S OR NOT T)` | boolean_algebra_generator.py |
| `CODEWORD` | 1, 3 | `CODEWORD\|0111100` | hamming_code_generator.py, kraft_inequality_generator.py |
| `CODE_LENGTH` | 2 | `CODE_LENGTH\|A\|l=5` | huffman_coding_generator.py |
| `COEFF` | 2 | `COEFF\|a_1\|4320` | laurent_series_generator.py, series_solution_generator.py |
| `COEFFS` | 1, 2 | `COEFFS\|2, 5, -28, -15` | horner_evaluation_generator.py, polynomial_zeros_generator.py, synthetic_division_generator.py |
| `COEFF_MATCH` | 2 | `COEFF_MATCH\|x^n\|(n+1)a_(n+1) = 3a_n` | series_solution_generator.py |
| `COEFF_PAIR` | 3 | `COEFF_PAIR\|i=1, j=3\|1+3=4\|6` | generating_function_generator.py |
| `COFACTOR` | 2 | `COFACTOR\|(1,1) sign +\|minor [[-2, 3], [2, -2]]` | determinant_generator.py |
| `COLLIDER_SETUP` | 3 | `COLLIDER_SETUP\|events_pb\|L=16 fb^-1\|sigma=2 pb` | cross_section_generator.py |
| `COLLISION` | 1 | `COLLISION\|f(d) = f(i) = 22` | function_properties_generator.py |
| `COLLISION_SETUP` | 3 | `COLLISION_SETUP\|inelastic_1d\|m1=18, u1=-9\|m2=9, u2=-10` | collision_generator.py |
| `COL_BASIS` | 2 | `COL_BASIS\|original columns 1, 2\|[[4, -3, 0], [-1, 1, 1]]` | subspace_basis_generator.py |
| `COMB` | 2 | `COMB\|C(5,1)\|5` | bec_channel_generator.py |
| `COMBO` | 2 | `COMBO\|x = 33*v1 - 9*v2\|[-3, -3]` | diagonalization_generator.py |
| `COMB_CONST` | 3 | `COMB_CONST\|-7\|-4\|-11` | derivative_product_quotient_generator.py, equation_from_two_points_generator.py, linear_complex_generator.py, rational_expr_add_sub_generator.py, simplify_expression_generator.py, special_solution_equation_generator.py |
| `COMB_FORMULA` | 1 | `COMB_FORMULA\|C(n, r) = P(n, r)/r!` | permutation_combination_generator.py |
| `COMB_RULE` | 2 | `COMB_RULE\|S x y z\|x z (y z)` | combinatory_logic_generator.py |
| `COMB_SETUP` | 2 | `COMB_SETUP\|choose 2 of 4\|order does not matter` | counting_classics_generator.py, permutation_combination_generator.py, stars_and_bars_generator.py |
| `COMB_X` | 3 | `COMB_X\|5x\|+2x\|7x` | derivative_product_quotient_generator.py, linear_complex_generator.py, rational_expr_add_sub_generator.py, simplify_expression_generator.py, special_solution_equation_generator.py |
| `COMMON_DIFF` | 2 | `COMMON_DIFF\|-7 - 1\|-8` | arithmetic_sequence_generator.py, recursive_explicit_generator.py |
| `COMMON_RATIO` | 2 | `COMMON_RATIO\|-9/(-3)\|3` | geometric_sequence_generator.py, recursive_explicit_generator.py |
| `COMMUTATOR` | 2 | `COMMUTATOR\|[A,B]\|[[0, 70i], [70i, 0]]` | structure_constant_generator.py |
| `COMM_ENTRY` | 3 | `COMM_ENTRY\|(1,1)\|0 - 0\|0` | structure_constant_generator.py |
| `COMM_FORMULA` | 1 | `COMM_FORMULA\|[A,B]f=A(Bf)-B(Af)` | commutator_generator.py |
| `COMM_RESULT` | 2 | `COMM_RESULT\|[D,x]f\|x^22` | commutator_generator.py |
| `COMM_SETUP` | 3 | `COMM_SETUP\|[D,x]f\|f=x^22\|D=d/dx` | commutator_generator.py |
| `COMPARE` | 2, 3 | `COMPARE\|7 > 2\|log_b(a) > k` | algorithm_trace_generator.py, equilibrium_ice_generator.py, fixed_point_generator.py, master_theorem_generator.py |
| `COMPLEMENT` | 1, 2, 3 | `COMPLEMENT\|P(Aᶜ) = 1 − P(A)\|1 − 4/13\|9/13` | classic_probability_puzzles_generator.py, complement_probability_generator.py, derangement_generator.py, hypergeometric_generator.py, odds_probability_generator.py, probability_axioms_finite_generator.py, reliability_system_generator.py |
| `COMPLETE_SQUARE` | 2 | `COMPLETE_SQUARE\|half of -6 = -3\|(-3)^2 = 9` | completing_square_generator.py, conic_standard_form_generator.py, polar_parametric_generator.py |
| `COMPOSE` | 3 | `COMPOSE\|a\|f(a) = 11\|g(11) = Z` | function_properties_generator.py |
| `COMPOSE_PAIR` | 3 | `COMPOSE_PAIR\|(b, 12)\|(12, H)\|(b, H)` | relation_operations_generator.py |
| `COMPOSITE_FACTOR` | 2 | `COMPOSITE_FACTOR\|5\|73` | divisibility_classification_generator.py |
| `COMPOSITE_SETUP` | 2 | `COMPOSITE_SETUP\|total the bill, then take the percent\|sum, percent-to-decimal, multiply` | composite_arithmetic_generator.py |
| `COMP_INEQ_PART` | 2 | `COMP_INEQ_PART\|Part 1\|5x - 1 < -36 -> x < -7` | compound_inequality_generator.py |
| `COMP_INEQ_SETUP` | 1 | `COMP_INEQ_SETUP\|0 < x - 7 < 9` | compound_inequality_generator.py |
| `CONCLUDE` | 1 | `CONCLUDE\|r ∣ x` | direct_proof_algebra_generator.py |
| `CONCLUSION_AT` | 2 | `CONCLUSION_AT\|p=T, q=F, r=F\|T` | argument_form_generator.py |
| `CONCLUSION_CHECK` | 1 | `CONCLUSION_CHECK\|not forced` | syllogism_generator.py |
| `COND_COUNT` | 2 | `COND_COUNT\|club=yes and commute=bus\|41` | conditional_probability_generator.py |
| `COND_ENTROPY` | 1 | `COND_ENTROPY\|H(Y given X)=H(X,Y)-H(X)` | mutual_information_generator.py |
| `COND_EXP` | 2, 3 | `COND_EXP\|E[X given Y=1]\|468/53` | conditional_expectation_generator.py |
| `COND_FORMULA` | 1 | `COND_FORMULA\|P(fare=flex given route=south) = count(both)/count(route=south)` | conditional_expectation_generator.py, conditional_probability_generator.py, joint_distribution_generator.py, two_way_table_probability_generator.py |
| `COND_PARTS` | 2 | `COND_PARTS\|p ∨ r\|(q ∧ p) ∨ (r ∨ p)` | conditional_forms_generator.py |
| `COND_SETUP` | 2, 3 | `COND_SETUP\|P(A given B) = 43/113\|P(A) = 128/201, P(B) = 113/201\|P(B given A)` | conditional_probability_generator.py |
| `COND_TOTAL` | 2 | `COND_TOTAL\|commute=bus total\|41 + 22 = 63` | conditional_probability_generator.py |
| `COND_VAR` | 2 | `COND_VAR\|Var(X given Y=1)\|2781/2809` | conditional_expectation_generator.py |
| `CONGRUENCE_REDUCE` | 2 | `CONGRUENCE_REDUCE\|27x congruent to 5\|mod 16` | modular_inverse_generator.py |
| `CONGRUENCE_SOLUTIONS` | 3 | `CONGRUENCE_SOLUTIONS\|base 15\|step 16\|15, 31, 47, 63` | modular_inverse_generator.py |
| `CONIC_SETUP` | 2 | `CONIC_SETUP\|y^2 = -16x\|vertex, focus, directrix` | conic_standard_form_generator.py, ellipse_features_generator.py, hyperbola_features_generator.py, parabola_features_generator.py |
| `CONJ` | 2 | `CONJ\|phi_1=-1+i\|-1-i` | braket_generator.py |
| `CONJUGATE` | 2 | `CONJUGATE\|-2 + 3i\|-2 - 3i` | complex_division_generator.py, quaternion_generator.py |
| `CONNECTIVE` | 2 | `CONNECTIVE\|¬q\|T` | logical_connective_eval_generator.py |
| `CONSERVATION_SETUP` | 2 | `CONSERVATION_SETUP\|gamma + pi0 + n -> e- + p + anti_nu_e + gamma\|check=Q,B,Le,Lmu` | conservation_law_generator.py |
| `CONSERVE_CHECK` | 3 | `CONSERVE_CHECK\|Q\|left=0,right=0\|conserved` | conservation_law_generator.py |
| `CONSTRAINT_SUBST` | 3 | `CONSTRAINT_SUBST\|x + y = 15\|x = 2*15/5\|6` | lagrange_multiplier_generator.py |
| `CONST_SOLVE` | 2 | `CONST_SOLVE\|C1 = 1\|C2 = 5` | recurrence_generator.py |
| `CONTOUR_SETUP` | 3 | `CONTOUR_SETUP\|abs(z)=7\|positive orientation\|f=6/(z-8) + 6/(z+5) - 6/(z+8)` | contour_integral_generator.py |
| `CONTRADICTION` | 2 | `CONTRADICTION\|r−d is nonnegative and in S\|r−d < r` | induction_verify_generator.py |
| `CONT_CORR` | 2 | `CONT_CORR\|P(X = 56)\|P(55.5 < Y < 56.5)` | normal_approx_binomial_generator.py |
| `CONT_DIST_SETUP` | 3 | `CONT_DIST_SETUP\|f(x)=k*x\|support=[0,3]\|interval=(2,3)` | continuous_distribution_generator.py |
| `CONVERGENT` | 2 | `CONVERGENT\|i=0\|3/1` | continued_fraction_generator.py |
| `CONVERGE_CHECK` | 2 | `CONVERGE_CHECK\|abs(r) = 4/11 < 1\|converges` | geometric_sequence_generator.py, series_convergence_generator.py |
| `CONV_ENCODE_STEP` | 3 | `CONV_ENCODE_STEP\|i=1\|prev=0,u=1\|11` | convolutional_code_viterbi_generator.py |
| `CONV_FACTOR` | 2 | `CONV_FACTOR\|1 hr\|60 min` | cross_section_generator.py, dimensional_analysis_generator.py, multi_step_unit_conversion_generator.py, rate_conversion_generator.py, unit_conversion_generator.py |
| `CONV_INIT` | 2 | `CONV_INIT\|h_-2=0,h_-1=1\|k_-2=1,k_-1=0` | continued_fraction_generator.py |
| `CONV_RECEIVED` | 2 | `CONV_RECEIVED\|111110\|flipped position 3` | convolutional_code_viterbi_generator.py |
| `CONV_RESULT` | 2 | `CONV_RESULT\|41 hr\|2460 min` | dimensional_analysis_generator.py, multi_step_unit_conversion_generator.py, rate_conversion_generator.py, temperature_conversion_generator.py, unit_conversion_generator.py |
| `CONV_SETUP` | 2, 3 | `CONV_SETUP\|x=[3,9,3,6]\|h=[5,3,2,5]` | convolution_generator.py, convolutional_code_viterbi_generator.py |
| `CONV_STEP` | 3 | `CONV_STEP\|i=0\|h=3\|k=1` | continued_fraction_generator.py |
| `CONV_SUM` | 2 | `CONV_SUM\|s=5\|87/1024` | convolution_generator.py, distribution_of_sum_generator.py |
| `CONV_WINDOW` | 2 | `CONV_WINDOW\|s=5\|27/64·5/32 + 39/128·1/16` | convolution_generator.py, distribution_of_sum_generator.py |
| `COORDS` | 2 | `COORDS\|c = P^-1 x\|[33, -9]` | diagonalization_generator.py |
| `CORRECT_BIT` | 3 | `CORRECT_BIT\|position=7\|0->1\|corrected=0110011` | hamming_code_generator.py |
| `CORR_FORMULA` | 1 | `CORR_FORMULA\|r = Sxy/√(Sxx·Syy)` | joint_distribution_generator.py, regression_generator.py |
| `COS` | 2 | `COS\|pi/6\|sqrt(3)/2` | positional_encoding_generator.py |
| `COSET` | 2 | `COSET\|1H\|{1, 38}` | coset_generator.py |
| `COSET_ELEM` | 2 | `COSET_ELEM\|1H\|1` | coset_generator.py |
| `COSET_SKIP` | 2 | `COSET_SKIP\|20\|already listed` | coset_generator.py |
| `COSET_START` | 2 | `COSET_START\|rep 1\|1H` | coset_generator.py |
| `COSINE` | 2 | `COSINE\|A,A\|1` | embedding_similarity_generator.py, lr_schedule_generator.py |
| `COST` | 1 | `COST\|initial` | transportation_generator.py |
| `COUNT` | 2 | `COUNT\|neither\|5` | attribute_sorting_generator.py, bayesian_update_generator.py, classic_probability_puzzles_generator.py, equivalence_relation_generator.py, likelihood_language_generator.py, logical_connective_eval_generator.py, method_of_moments_generator.py, mle_generator.py, one_to_one_correspondence_generator.py, probability_addition_rule_generator.py, random_digit_simulation_generator.py, set_builder_roster_generator.py, set_membership_subset_generator.py, set_operations_generator.py |
| `COUNTEREXAMPLE` | 2, 3 | `COUNTEREXAMPLE\|n = 128\|128 is divisible by 2 but not by 6` | argument_form_generator.py, conditional_forms_generator.py, counterexample_search_generator.py, truth_table_generator.py |
| `COUNTERMODEL` | 1 | `COUNTERMODEL\|pilots=TFF, farmers=FFF, teachers=FFF` | syllogism_generator.py |
| `COUNT_DP` | 3 | `COUNT_DP\|1\|1\|2` | decimal_mult_generator.py |
| `COUNT_RULE` | 2 | `COUNT_RULE\|symmetric relations\|2^(card(A)(card(A)+1)/2)` | function_properties_generator.py, set_counting_generator.py |
| `COUNT_SETUP` | 1, 2 | `COUNT_SETUP\|arrangements of 7 cards\|7!` | counting_classics_generator.py, counting_to_probability_generator.py |
| `COUPON` | 1 | `COUPON\|212` | bond_pricing_generator.py |
| `COVER` | 3 | `COVER\|1\|2\|no c strictly between` | partial_order_generator.py |
| `COV_ENTRY` | 2 | `COV_ENTRY\|xx\|25/2` | pca_generator.py |
| `COV_FORMULA` | 1 | `COV_FORMULA\|Cov=E[XY]-E[X]E[Y]` | joint_distribution_generator.py |
| `COV_RULE` | 1, 2 | `COV_RULE\|Var(X − Y)\|Var(X) + Var(Y) − 2Cov(X,Y)` | covariance_algebra_generator.py |
| `CRC_CHECK` | 3 | `CRC_CHECK\|codeword=1011111000\|remainder=0000\|valid` | crc_generator.py |
| `CRC_REMAINDER` | 1 | `CRC_REMAINDER\|1000` | crc_generator.py |
| `CRC_SETUP` | 3 | `CRC_SETUP\|data=101111\|poly=10011\|augmented=1011110000` | crc_generator.py |
| `CRC_SKIP` | 2 | `CRC_SKIP\|i=1\|leading bit 0` | crc_generator.py |
| `CRC_XOR` | 3 | `CRC_XOR\|i=0\|10111 xor 10011\|00100` | crc_generator.py |
| `CRIT_EQS` | 2 | `CRIT_EQS\|f_x = 0\|4*x + 2*y - 10 = 0` | hessian_classify_generator.py |
| `CRIT_SOLVE` | 3 | `CRIT_SOLVE\|det\|4*(-2) - 2^2\|-12` | hessian_classify_generator.py |
| `CROSS_ENTROPY` | 2 | `CROSS_ENTROPY\|target=2\|ln(13/7)` | perplexity_generator.py, softmax_gradient_generator.py |
| `CROSS_MULT` | 1 | `CROSS_MULT\|20·EF = 25·32` | similar_triangles_generator.py, triangle_solve_generator.py |
| `CROSS_RATIO` | 1 | `CROSS_RATIO\|-5` | mobius_transform_generator.py |
| `CROSS_RATIO_SETUP` | 4 | `CROSS_RATIO_SETUP\|z1=3\|z2=-1\|z3=-7\|z4=2` | mobius_transform_generator.py |
| `CRT_CHECK` | 3 | `CRT_CHECK\|i=1\|0\|0` | crt_generator.py |
| `CRT_CONGRUENCE` | 3 | `CRT_CONGRUENCE\|i=1\|x=0\|mod 4` | crt_generator.py |
| `CRT_FACTOR` | 3 | `CRT_FACTOR\|i=1\|M_i=11\|mod 4` | crt_generator.py |
| `CRT_SETUP` | 1 | `CRT_SETUP\|2 congruences` | crt_generator.py |
| `CRT_TERM` | 2 | `CRT_TERM\|i=1\|0` | crt_generator.py |
| `CRT_TOTAL_MODULUS` | 2 | `CRT_TOTAL_MODULUS\|4, 11\|44` | crt_generator.py |
| `CR_SETUP` | 2 | `CR_SETUP\|u=x^2 - y^2 + 5x - 2y\|v=2xy + 2x + 4y` | cauchy_riemann_generator.py |
| `CUM_INTERVAL` | 2 | `CUM_INTERVAL\|A\|[0,1/8)` | arithmetic_coding_generator.py |
| `CURL_COMPONENT` | 3 | `CURL_COMPONENT\|Q_x - P_y\|1 - 6\|-5` | div_curl_generator.py |
| `CURRENT_YIELD` | 1 | `CURRENT_YIELD\|25/436` | bond_pricing_generator.py |
| `CURVATURE_FORMULA` | 2 | `CURVATURE_FORMULA\|circle\|kappa = 1/R` | curve_geometry_generator.py |
| `CURVE_GEOM_SETUP` | 3 | `CURVE_GEOM_SETUP\|r(t) = <3*t - 1, 4*t + 4>\|0 <= t <= 2\|arc length` | curve_geometry_generator.py |
| `CURVE_SETUP` | 2 | `CURVE_SETUP\|f(x) = x^3 + 3x^2 - 24x + 4\|inflection point and concavity` | curve_analysis_generator.py |
| `CUT_RULE` | 2 | `CUT_RULE\|L(5/8)\|x < 5/8` | dedekind_cut_generator.py |
| `CW_START` | 2 | `CW_START\|leading 1\|1/1` | countability_bijection_generator.py |
| `CW_STEP` | 3 | `CW_STEP\|bit 0\|1/1\|1/2` | countability_bijection_generator.py |
| `CX_A` | 3 | `CX_A\|63/65\|0\|63/65` | braket_generator.py, spin_half_generator.py |
| `CX_M` | 3 | `CX_M\|1\|63/65\|63/65` | braket_generator.py, spin_half_generator.py |
| `CX_SETUP` | 2 | `CX_SETUP\|(-3 - i) - (-2 + 6i)\|subtract` | complex_division_generator.py, complex_number_ops_generator.py |
| `CYCLE` | 1 | `CYCLE\|(1 4 5 2 6)` | permutation_group_generator.py |
| `CYCLE_LENGTHS` | 1 | `CYCLE_LENGTHS\|5` | permutation_group_generator.py |
| `CYCLE_REJECT` | 2 | `CYCLE_REJECT\|BD\|endpoints already connected` | mst_generator.py |
| `CYCLE_TRACE` | 2 | `CYCLE_TRACE\|start 1\|1->4->5->2->6->1` | permutation_group_generator.py |
| `CYCLIC_START` | 2 | `CYCLIC_START\|7\|identity 0` | cyclic_group_generator.py |
| `CYCLIC_SUBGROUP` | 2 | `CYCLIC_SUBGROUP\|{0, 7, 4, 1, 8, 5, 2, 9, 6, 3}\|10` | cyclic_group_generator.py |
| `CYK_CELL` | 2 | `CYK_CELL\|1,2\|{T}` | cyk_parser_generator.py |
| `CYK_COMBINE` | 3 | `CYK_COMBINE\|C C\|{T}\|cell 1,2` | cyk_parser_generator.py |
| `CYK_RULE` | 2 | `CYK_RULE\|C\|a or b or e or T T` | cyk_parser_generator.py |
| `CYK_SETUP` | 2 | `CYK_SETUP\|string beaa\|length 4` | cyk_parser_generator.py |
| `CYK_SPAN` | 1 | `CYK_SPAN\|2` | cyk_parser_generator.py |
| `CYK_SPLIT` | 3 | `CYK_SPLIT\|cell 1,2\|1,1 x 2,2\|{C} x {C}` | cyk_parser_generator.py |
| `CYK_TERMINAL` | 3 | `CYK_TERMINAL\|cell 1,1\|b\|{C}` | cyk_parser_generator.py |
| `CYL_BOUNDS` | 2 | `CYL_BOUNDS\|z\|0..4` | triple_integral_generator.py |
| `CYL_CONVERT` | 2 | `CYL_CONVERT\|6*z dV\|6*z*r dz dr dtheta` | triple_integral_generator.py |
| `D` | 3 | `D\|632\|99\|6` | ac_circuit_generator.py, activation_generator.py, adam_step_generator.py, angle_defect_generator.py, annuity_generator.py, antiderivative_generator.py, arithmetic_coding_generator.py, arithmetic_sequence_generator.py, attention_generator.py, backprop_generator.py, bayes_multiple_hypotheses_generator.py, bayesian_update_generator.py, bisection_generator.py, blackbody_generator.py, bond_pricing_generator.py, branching_ratio_generator.py, cantor_pairing_generator.py, casimir_force_generator.py, cholesky_generator.py, christoffel_generator.py, circle_angle_generator.py, circle_equation_generator.py, classic_probability_puzzles_generator.py, classifier_metrics_generator.py, collision_generator.py, complex_number_ops_generator.py, composite_arithmetic_generator.py, conditional_expectation_generator.py, conditional_probability_generator.py, confidence_interval_generator.py, conic_standard_form_generator.py, continuous_distribution_generator.py, coset_generator.py, countability_bijection_generator.py, counting_classics_generator.py, covariance_algebra_generator.py, cramers_rule_generator.py, cross_section_generator.py, crt_generator.py, curve_analysis_generator.py, de_moivre_generator.py, decimal_div_generator.py, dedekind_cut_generator.py, definite_integral_generator.py, dimensional_analysis_generator.py, discrete_uniform_bernoulli_generator.py, distribution_of_sum_generator.py, doppler_generator.py, einstein_summation_generator.py, electrostatics_generator.py, embedding_similarity_generator.py, energy_conservation_generator.py, entropy_change_generator.py, entropy_generator.py, equilibrium_ice_generator.py, error_spotting_generator.py, exact_ode_generator.py, expectation_of_function_generator.py, exponential_equation_generator.py, exponential_model_generator.py, fill_in_step_generator.py, finite_difference_generator.py, flops_memory_generator.py, fourier_series_generator.py, function_inner_product_generator.py, function_operations_generator.py, game_theory_generator.py, gas_law_generator.py, gas_stoichiometry_generator.py, gauss_bonnet_generator.py, gauss_law_generator.py, gaussian_curvature_generator.py, generating_function_generator.py, geometric_distribution_generator.py, geometric_mean_generator.py, geometric_sequence_generator.py, geometry_area_perimeter_generator.py, gradient_descent_generator.py, gradient_step_generator.py, hamiltonian_generator.py, hawking_generator.py, heat_engine_generator.py, huffman_coding_generator.py, hydrogen_atom_generator.py, hyperbolic_distance_generator.py, hyperbolic_function_generator.py, hypergeometric_generator.py, hypothesis_test_generator.py, information_gain_generator.py, integrating_factor_generator.py, interference_generator.py, interpolation_generator.py, invariant_mass_generator.py, jacobi_symbol_generator.py, joint_distribution_generator.py, kernel_ridge_generator.py, kinematics_generator.py, kl_divergence_generator.py, kmeans_step_generator.py, kraft_inequality_generator.py, ladder_operator_generator.py, lagrangian_generator.py, laplace_ivp_generator.py, laurent_series_generator.py, layer_norm_generator.py, lcm_generator.py, least_squares_generator.py, legendre_construction_generator.py, limit_evaluation_generator.py, linear_simple_generator.py, linearity_of_expectation_generator.py, log_conversion_generator.py, logistic_growth_generator.py, long_division_generator.py, lr_schedule_generator.py, magnetism_generator.py, manual_square_root_generator.py, markov_chain_generator.py, matrix_inverse_generator.py, matrix_norm_generator.py, mean_value_theorem_generator.py, method_of_moments_generator.py, midpoint_generator.py, mle_generator.py, modular_inverse_generator.py, multi_step_unit_conversion_generator.py, naive_bayes_generator.py, named_distribution_generator.py, natural_units_generator.py, nets_surface_area_generator.py, newton_raphson_generator.py, newtons_laws_generator.py, npv_irr_generator.py, ode_substitution_generator.py, optics_generator.py, optimization_generator.py, or_formula_generator.py, orbital_mechanics_generator.py, order_of_operations_generator.py, order_statistics_generator.py, parabola_features_generator.py, param_count_generator.py, parametric_calculus_generator.py, particle_in_box_generator.py, partition_function_generator.py, pca_generator.py, percent_problem_generator.py, permutation_combination_generator.py, perplexity_generator.py, physics_formula_generator.py, planck_units_generator.py, polar_parametric_generator.py, primality_test_generator.py, probability_measure_generator.py, projectile_motion_generator.py, proportion_word_problem_generator.py, proportional_relationship_generator.py, quadratic_residue_generator.py, quantization_generator.py, quantum_formula_generator.py, radical_rationalize_generator.py, rate_conversion_generator.py, ratio_table_generator.py, recurrence_generator.py, regression_generator.py, regular_polygon_area_generator.py, relativistic_energy_generator.py, repeating_decimal_generator.py, riemann_sum_generator.py, riemann_tensor_generator.py, right_triangle_trig_generator.py, rotational_dynamics_generator.py, round_solids_generator.py, routh_hurwitz_generator.py, runge_kutta_generator.py, running_coupling_generator.py, rv_transform_generator.py, scaling_law_generator.py, schwarzschild_generator.py, second_order_ode_generator.py, segment_partition_generator.py, separable_pde_generator.py, series_convergence_generator.py, series_solution_generator.py, set_counting_generator.py, shm_generator.py, similar_triangles_generator.py, simplex_generator.py, sinusoid_features_generator.py, slope_two_points_generator.py, softmax_gradient_generator.py, solution_chem_generator.py, special_relativity_generator.py, special_right_triangle_generator.py, spherical_excess_generator.py, spherical_triangle_generator.py, spin_half_generator.py, standard_deviation_generator.py, standing_wave_generator.py, stars_and_bars_generator.py, statics_generator.py, stereographic_generator.py, stoichiometry_generator.py, svm_margin_generator.py, taylor_series_generator.py, telescoping_generator.py, temperature_conversion_generator.py, tip_bill_split_generator.py, totient_generator.py, transient_circuit_generator.py, triangle_area_sas_generator.py, triangle_solve_generator.py, trig_identity_eval_generator.py, trig_six_functions_generator.py, two_sample_test_generator.py, u_substitution_generator.py, undetermined_coeff_generator.py, unit_conversion_generator.py, variation_parameters_generator.py, vector_ops_generator.py, wavefunction_generator.py, young_tableaux_generator.py, z_score_generator.py |
| `DALEMBERT` | 1 | `DALEMBERT\|u=(f(x-ct)+f(x+ct))/2` | separable_pde_generator.py |
| `DATA_PRECISION` | 1 | `DATA_PRECISION\|n/sigma^2` | bayesian_update_generator.py |
| `DATE_ORDINAL` | 2 | `DATE_ORDINAL\|2027-02-05\|740017` | calendar_arithmetic_generator.py |
| `DB_FORMULA` | 1 | `DB_FORMULA\|G_dB=10*log10(P2/P1)` | signal_arithmetic_generator.py |
| `DECISION` | 2 | `DECISION\|f(x)\|-48` | kernel_perceptron_generator.py, svm_margin_generator.py |
| `DECODE` | 2 | `DECODE\|10001100100\|{b, l, m, w}` | characteristic_vector_generator.py |
| `DEC_ADD_COL` | 3 | `DEC_ADD_COL\|frac_0\|0+1+0\|->1 (carry 0)` | decimal_add_sub_generator.py |
| `DEC_ALIGN` | 2 | `DEC_ALIGN\|55.60\|69.81` | decimal_add_sub_generator.py |
| `DEC_CARRY_FINAL` | 1 | `DEC_CARRY_FINAL\|1` | decimal_add_sub_generator.py |
| `DEC_SHIFT` | 3 | `DEC_SHIFT\|33.0/0.2\|330/2\|1` | decimal_div_generator.py, percent_problem_generator.py |
| `DEC_SUB_COL` | 3 | `DEC_SUB_COL\|frac_0\|1-0 (borrow_in 0)\|->1 (borrow_out 0)` | decimal_add_sub_generator.py |
| `DEC_TO_FRAC` | 2 | `DEC_TO_FRAC\|4.17\|417/100` | fraction_decimal_percent_converter.py |
| `DEC_TO_PERCENT` | 2 | `DEC_TO_PERCENT\|1.075\|107.5%` | fraction_decimal_percent_converter.py, percent_problem_generator.py, simple_probability_generator.py, tip_bill_split_generator.py |
| `DEC_TYPE` | 2 | `DEC_TYPE\|151/228\|repeating` | repeating_decimal_generator.py |
| `DEC_VALUE` | 2 | `DEC_VALUE\|151/228\|0.66(228070175438596491)` | repeating_decimal_generator.py |
| `DEDUCE` | 3 | `DEDUCE\|Finn\|item = mug\|only solution left` | logic_grid_puzzle_generator.py |
| `DEDUP` | 2 | `DEDUP\|A raw [24, 57, 66, 52, 63, 66]\|{24, 52, 57, 63, 66}` | set_membership_subset_generator.py |
| `DEGREE` | 2, 3 | `DEGREE\|A\|C, D\|2` | euler_circuit_generator.py, graph_counting_generator.py |
| `DEGREE_COMPARE` | 2 | `DEGREE_COMPARE\|deg num = deg den = 2\|y = 1/1` | limit_evaluation_generator.py, rational_function_features_generator.py, series_convergence_generator.py |
| `DEGREE_SEQUENCE` | 1 | `DEGREE_SEQUENCE\|3, 3, 2, 2` | graph_counting_generator.py |
| `DELTA_VALUE` | 2 | `DELTA_VALUE\|delta_21\|0` | index_gymnastics_generator.py |
| `DEMOIVRE_POWER` | 1 | `DEMOIVRE_POWER\|81 cis(120 deg)` | de_moivre_generator.py |
| `DEMOIVRE_SETUP` | 2, 4 | `DEMOIVRE_SETUP\|roots_of_unity\|n=12` | de_moivre_generator.py |
| `DENSITY` | 2 | `DENSITY\|f_X(x)\|1/28` | rv_transform_generator.py |
| `DENSITY_MATRIX` | 1 | `DENSITY_MATRIX\|rho=[[7/16,0],[0,9/16]]` | density_matrix_generator.py |
| `DENSITY_SETUP` | 2, 3 | `DENSITY_SETUP\|state=Schmidt\|psi=(sqrt(49)ket00 - sqrt(143)ket11)/sqrt(192)` | density_matrix_generator.py, partial_trace_generator.py |
| `DEPTH` | 1, 2 | `DEPTH\|3` | wff_parsing_generator.py |
| `DEQUANT_VALUE` | 2 | `DEQUANT_VALUE\|1\|4/5` | quantization_generator.py |
| `DERANGE_PROB` | 2 | `DERANGE_PROB\|D_4/4!\|9/24` | derangement_generator.py |
| `DERANGE_SETUP` | 2 | `DERANGE_SETUP\|n = 11\|exactly 1 fixed` | derangement_generator.py |
| `DERANGE_VALUE` | 2 | `DERANGE_VALUE\|D_2\|1` | derangement_generator.py |
| `DERIV` | 2, 3 | `DERIV\|d_r g_thetatheta = 2r\|at r=74\|148` | christoffel_generator.py, gaussian_curvature_generator.py, riemann_tensor_generator.py |
| `DERIVATIVE` | 1, 2 | `DERIVATIVE\|g'(x)\|-1/3` | fixed_point_generator.py, mgf_generator.py, mle_generator.py |
| `DERIVED` | 2 | `DERIVED\|C6\|(P89196)` | resolution_proof_generator.py |
| `DERIV_FORM` | 2 | `DERIV_FORM\|y'\|(C2 + 4(C1 + C2x))e^(4x)` | second_order_ode_generator.py, undetermined_coeff_generator.py, variation_parameters_generator.py |
| `DERIV_RULE` | 2 | `DERIV_RULE\|power rule\|d/dx of c·x^n = c·n·x^(n-1)` | chain_rule_generator.py, derivative_power_rule_generator.py, derivative_product_quotient_generator.py, derivative_transcendental_generator.py, lhopital_generator.py, linear_approx_generator.py, log_diff_higher_order_generator.py, multivar_chain_rule_generator.py |
| `DERIV_SERIES` | 2 | `DERIV_SERIES\|y'\|sum (n+1)a_(n+1)x^n` | series_solution_generator.py |
| `DERIV_SETUP` | 2 | `DERIV_SETUP\|f(x) = -2x^3 + 4x^2 - 7x - 1\|f'(x)` | chain_rule_generator.py, derivative_power_rule_generator.py, derivative_product_quotient_generator.py, derivative_transcendental_generator.py, log_diff_higher_order_generator.py, tangent_line_generator.py |
| `DESIGN_MATRIX` | 2 | `DESIGN_MATRIX\|X = [[1, -3], [1, -1], [1, 1], [1, 3]]\|y = [0, 8, 10, 6]` | least_squares_generator.py |
| `DET` | 2 | `DET\|K\|20` | kernel_ridge_generator.py, kernel_validity_generator.py |
| `DET2` | 2 | `DET2\|ad - bc\|-16` | ode_system_generator.py |
| `DET_FORMULA` | 1 | `DET_FORMULA\|det = ad - bc` | cramers_rule_generator.py, determinant_generator.py, matrix_inverse_generator.py |
| `DEV_ROW` | 3 | `DEV_ROW\|28\|-2\|4` | standard_deviation_generator.py |
| `DFA_ACCEPT` | 1 | `DFA_ACCEPT\|q1` | dfa_minimization_generator.py, dfa_simulation_generator.py |
| `DFA_INPUT` | 1 | `DFA_INPUT\|1011` | dfa_simulation_generator.py |
| `DFA_MIN_SETUP` | 3 | `DFA_MIN_SETUP\|states A, B, C\|alphabet 0, 1\|start A` | dfa_minimization_generator.py |
| `DFA_MIN_TRANSITION` | 3 | `DFA_MIN_TRANSITION\|A\|0\|A` | dfa_minimization_generator.py |
| `DFA_READ` | 2 | `DFA_READ\|pos 1\|1` | dfa_simulation_generator.py |
| `DFA_SETUP` | 3 | `DFA_SETUP\|states q0, q1\|alphabet 0, 1\|start q0` | dfa_simulation_generator.py |
| `DFA_STATE` | 2 | `DFA_STATE\|start\|q0` | dfa_simulation_generator.py |
| `DFA_STEP` | 3 | `DFA_STEP\|q0\|1\|q1` | dfa_simulation_generator.py |
| `DFA_TRANSITION` | 3 | `DFA_TRANSITION\|q0\|0\|q0` | dfa_simulation_generator.py |
| `DFS_EDGE` | 2 | `DFS_EDGE\|E->A\|tree` | graph_traversal_generator.py |
| `DFT_BIN` | 1 | `DFT_BIN\|X0=x0+x1+x2+x3` | dft_generator.py |
| `DFT_SETUP` | 2 | `DFT_SETUP\|N=4\|x=[6,9,-5,5]` | dft_generator.py |
| `DH_PUBLIC` | 2 | `DH_PUBLIC\|Alice\|8` | diffie_hellman_generator.py |
| `DH_SECRET` | 2 | `DH_SECRET\|Alice\|10` | diffie_hellman_generator.py |
| `DH_SETUP` | 2 | `DH_SETUP\|p=17\|g=14` | diffie_hellman_generator.py |
| `DH_SHARED` | 2 | `DH_SHARED\|Alice\|1` | diffie_hellman_generator.py |
| `DIAG` | 2 | `DIAG\|row 1\|1` | cantor_diagonal_generator.py |
| `DIAGONAL` | 3 | `DIAGONAL\|w=13\|start=91\|offset=3` | cantor_pairing_generator.py |
| `DIAG_FORM` | 3 | `DIAG_FORM\|P = [[1, 2], [2, 3]]\|D = [[-5, 0], [0, -3]]\|P^-1 = [[-3, 2], [2, -1]]` | diagonalization_generator.py, matrix_exponential_generator.py |
| `DIFF_ROW` | 2 | `DIFF_ROW\|Delta y\|[-18, 36, 90]` | finite_difference_generator.py |
| `DIFF_SETUP` | 3 | `DIFF_SETUP\|f(x,y) = 3*x^2 + 4*y^2 + 4*x*y + 5*x - 3*y\|point (-3, 3)\|dx=-1/2, dy=2/5` | multivar_chain_rule_generator.py |
| `DIFF_SUM` | 3 | `DIFF_SUM\|f_x*dx + f_y*dy\|(-1)*(-1/2) + 9*2/5\|4.1` | multivar_chain_rule_generator.py |
| `DIGIT_MAP` | 2 | `DIGIT_MAP\|success\|0–0 (1 of 10 digits)` | random_digit_simulation_generator.py |
| `DIGIT_SCAN` | 3 | `DIGIT_SCAN\|299\|makes 0\|no` | random_digit_simulation_generator.py |
| `DIJKSTRA_INIT` | 2 | `DIJKSTRA_INIT\|start B\|A=inf, B=0, C=inf, D=inf` | dijkstra_generator.py |
| `DIM` | 2 | `DIM\|2*5+1\|11` | casimir_generator.py |
| `DIRECTRIX` | 1 | `DIRECTRIX\|x = 4` | parabola_features_generator.py |
| `DISC` | 2, 3 | `DISC\|196\|-213248\|213444` | complex_quadratic_generator.py, discriminant_generator.py, polynomial_zeros_generator.py, quadratic_generator.py |
| `DISC_CLASSIFY` | 2 | `DISC_CLASSIFY\|49 > 0\|two real solutions` | complex_quadratic_generator.py, discriminant_generator.py, polynomial_zeros_generator.py |
| `DIST` | 3 | `DIST\|-4\|x-4\|-4x+16` | derivative_limit_def_generator.py, derivative_product_quotient_generator.py, equation_from_two_points_generator.py, function_composition_generator.py, parallel_perpendicular_line_generator.py, point_slope_generator.py, polar_parametric_generator.py, radical_multiply_generator.py, radical_rationalize_generator.py, rational_expr_add_sub_generator.py, recursive_explicit_generator.py, simplify_expression_generator.py, solid_revolution_generator.py, special_solution_equation_generator.py, tangent_line_generator.py |
| `DIST2` | 2, 3 | `DIST2\|P1\|C1\|61` | embedding_similarity_generator.py, kernel_evaluation_generator.py, kmeans_step_generator.py |
| `DIST_COMBINE` | 1 | `DIST_COMBINE\|-21x + 4 = 4` | systems_substitution_generator.py |
| `DIST_FORMULA` | 1 | `DIST_FORMULA\|d = √((x2 - x1)^2 + (y2 - y1)^2)` | complex_locus_generator.py, distance_formula_generator.py, hypercube_counting_generator.py |
| `DIST_RULE` | 1, 2 | `DIST_RULE\|independent binomials with common p\|S~Binomial(5,3/4)` | distribution_of_sum_generator.py |
| `DIST_SETUP` | 2, 3 | `DIST_SETUP\|Bernoulli\|p = 3/5` | discrete_uniform_bernoulli_generator.py, named_distribution_generator.py, pmf_cdf_quantile_generator.py |
| `DIST_TABLE` | 2 | `DIST_TABLE\|visited B\|A=3, B=0, C=2, D=6` | dijkstra_generator.py |
| `DIST_TERM` | 2 | `DIST_TERM\|-5x\|15x^3 - 20x^2 - 10x` | multiplying_polynomials_generator.py |
| `DIVIDE_EQ` | 2 | `DIVIDE_EQ\|divide by y^2\|y^(-2)dy/dx + 4y^(-1) = 4` | ode_substitution_generator.py |
| `DIVMOD` | 3, 4 | `DIVMOD\|82\|2\|41\|r=0` | base_conversion_generator.py, induction_verify_generator.py, recursive_definition_unfold_generator.py |
| `DIV_CHECK` | 3 | `DIV_CHECK\|6\|2\|remainder 0` | conditional_forms_generator.py, counterexample_search_generator.py, divisibility_classification_generator.py, logical_connective_eval_generator.py, set_builder_roster_generator.py |
| `DIV_COEFF` | 3 | `DIV_COEFF\|-11\|7\|x=-11/7` | linear_complex_generator.py |
| `DIV_SETUP` | 2 | `DIV_SETUP\|330\|2` | decimal_div_generator.py, percent_problem_generator.py |
| `DIV_SUM` | 3 | `DIV_SUM\|P_x + Q_y\|-3 + 0\|-3` | div_curl_generator.py |
| `DIV_TERM` | 3 | `DIV_TERM\|3t^2\|3t\|t` | factor_gcf_generator.py, finite_field_generator.py, polynomial_long_division_generator.py |
| `DNF_FORM` | 1 | `DNF_FORM\|(NOT P AND NOT Q AND NOT R) OR (P AND NOT Q AND NOT R)` | boolean_algebra_generator.py |
| `DOMAIN` | 1, 2 | `DOMAIN\|x = −50..−38\|{−50, −49, −48, −47, −46, −45, −44, −43, −42, −41, −40, −39, −38}` | quantifier_finite_domain_generator.py, relation_operations_generator.py, set_builder_roster_generator.py |
| `DOMAIN_COND` | 2 | `DOMAIN_COND\|radicand ≥ 0\|3x - 21 ≥ 0` | domain_range_generator.py |
| `DOMAIN_NOTE` | 2 | `DOMAIN_NOTE\|x ≠ 7\|denominator cannot be zero` | domain_range_generator.py, log_equation_generator.py, logistic_growth_generator.py, probability_addition_rule_generator.py, rational_equation_generator.py, unit_circle_generator.py |
| `DOPPLER_FORMULA` | 1 | `DOPPLER_FORMULA\|f_obs=f*sqrt((1+beta)/(1-beta))` | doppler_generator.py |
| `DOPPLER_SETUP` | 3 | `DOPPLER_SETUP\|relativistic_approach\|f=893\|beta=63/65` | doppler_generator.py |
| `DOT` | 2, 3 | `DOT\|(11, 10) · (-3/5, 4/5)\|11*(-3/5) + 10*4/5\|1.4` | embedding_similarity_generator.py, feature_map_generator.py, fundamental_form_generator.py, gradient_generator.py, gram_schmidt_generator.py, kernel_evaluation_generator.py, line_integral_generator.py, lll_reduction_generator.py, qr_decomposition_generator.py |
| `DOT4` | 4 | `DOT4\|gamma0gamma3\|(4,1)\|0*0 + 0*-1 + 0*0 + -1*0\|0` | gamma_matrix_generator.py |
| `DOT_FORMULA` | 1 | `DOT_FORMULA\|u ⊥ v exactly when u·v = 0` | dot_product_generator.py |
| `DOUBLE_SETUP` | 2, 3 | `DOUBLE_SETUP\|integrand x^2 + y^2\|upper-half disk radius 5` | double_integral_generator.py |
| `DPLL_BACKTRACK` | 2 | `DPLL_BACKTRACK\|A\|True` | dpll_trace_generator.py |
| `DPLL_BRANCH` | 3 | `DPLL_BRANCH\|depth 0\|A\|True` | dpll_trace_generator.py |
| `DPLL_CONFLICT` | 1 | `DPLL_CONFLICT\|A=True, B=True` | dpll_trace_generator.py |
| `DPLL_SAT` | 1 | `DPLL_SAT\|A=True, B=True, C=True` | dpll_trace_generator.py |
| `DPLL_SETUP` | 3 | `DPLL_SETUP\|(A) AND (not A OR B) AND (not B OR C)\|variables A, B, C\|True first` | dpll_trace_generator.py |
| `DPLL_SIMPLIFY` | 2 | `DPLL_SIMPLIFY\|A=True\|2 clauses left` | dpll_trace_generator.py |
| `DPLL_STATE` | 3 | `DPLL_STATE\|depth 0\|none\|3 clauses left` | dpll_trace_generator.py |
| `DPLL_UNIT` | 2 | `DPLL_UNIT\|(A)\|A=True` | dpll_trace_generator.py |
| `DP_CELL` | 3 | `DP_CELL\|i=1,j=0\|base\|0` | dp_table_generator.py |
| `DP_COINS` | 1 | `DP_COINS\|1, 3, 4` | dp_table_generator.py |
| `DP_ITEMS` | 1 | `DP_ITEMS\|1:(w=5,v=3); 2:(w=1,v=6); 3:(w=5,v=10); 4:(w=4,v=10)` | dp_table_generator.py |
| `DP_ROW` | 2 | `DP_ROW\|i=0\|0, 0, 0, 0, 0` | dp_table_generator.py |
| `DP_SETUP` | 2, 3 | `DP_SETUP\|LCS\|X=BDAB\|Y=BDCD` | dp_table_generator.py |
| `D_POWER` | 2 | `D_POWER\|D^2\|[[49, 0], [0, 81]]` | diagonalization_generator.py |
| `E` | 3 | `E\|9\|2\|81` | ac_circuit_generator.py, adam_step_generator.py, angle_defect_generator.py, annuity_generator.py, arc_sector_generator.py, backprop_generator.py, bayes_multiple_hypotheses_generator.py, bec_channel_generator.py, blackbody_generator.py, bond_pricing_generator.py, casimir_force_generator.py, casimir_generator.py, christoffel_generator.py, circle_equation_generator.py, complex_division_generator.py, complex_locus_generator.py, conditional_expectation_generator.py, confidence_interval_generator.py, conic_standard_form_generator.py, continuous_distribution_generator.py, counting_to_probability_generator.py, covariance_algebra_generator.py, de_moivre_generator.py, dedekind_cut_generator.py, definite_integral_generator.py, density_matrix_generator.py, derivative_limit_def_generator.py, diagonalization_generator.py, discrete_uniform_bernoulli_generator.py, distance_formula_generator.py, doppler_generator.py, electrostatics_generator.py, ellipse_features_generator.py, embedding_similarity_generator.py, energy_conservation_generator.py, euler_formula_generator.py, expectation_of_function_generator.py, exponential_equation_generator.py, exponential_model_generator.py, factor_special_forms_generator.py, feature_map_generator.py, finance_generator.py, four_vector_generator.py, fractal_iteration_generator.py, function_composition_generator.py, function_evaluation_generator.py, function_operations_generator.py, function_table_generator.py, fundamental_form_generator.py, gauss_bonnet_generator.py, gauss_law_generator.py, gaussian_curvature_generator.py, geometric_mean_generator.py, geometric_sequence_generator.py, gradient_descent_generator.py, gradient_step_generator.py, hamiltonian_generator.py, hawking_generator.py, hermitian_check_generator.py, huffman_coding_generator.py, hydrogen_atom_generator.py, hyperbola_features_generator.py, hyperbolic_function_generator.py, hypercube_counting_generator.py, invariant_mass_generator.py, kernel_evaluation_generator.py, kmeans_step_generator.py, knn_generator.py, kraft_inequality_generator.py, lagrangian_generator.py, laurent_series_generator.py, layer_norm_generator.py, limit_evaluation_generator.py, log_conversion_generator.py, log_equation_generator.py, log_properties_generator.py, low_rank_approx_generator.py, matrix_group_check_generator.py, matrix_norm_generator.py, mean_value_theorem_generator.py, metric_arc_length_generator.py, mgf_generator.py, minkowski_interval_generator.py, mobius_transform_generator.py, named_distribution_generator.py, natural_units_generator.py, npv_irr_generator.py, optimization_generator.py, or_formula_generator.py, orbital_mechanics_generator.py, order_statistics_generator.py, particle_in_box_generator.py, pca_generator.py, piecewise_evaluation_generator.py, planck_units_generator.py, polar_parametric_generator.py, portfolio_generator.py, projectile_motion_generator.py, pythag_hyp_generator.py, radical_equation_generator.py, radical_multiply_generator.py, radical_rationalize_generator.py, rational_exponent_generator.py, recursive_explicit_generator.py, regression_generator.py, related_rates_generator.py, relativistic_energy_generator.py, remainder_factor_theorem_generator.py, riemann_tensor_generator.py, rotational_dynamics_generator.py, round_solids_generator.py, rv_transform_generator.py, schwarzschild_generator.py, set_counting_generator.py, set_operations_generator.py, shm_generator.py, spherical_excess_generator.py, spin_half_generator.py, stereographic_generator.py, svm_margin_generator.py, tangent_line_generator.py, taylor_series_generator.py, triangle_solve_generator.py, trig_identity_eval_generator.py, trig_six_functions_generator.py, uncertainty_generator.py, vector_ops_generator.py, wavefunction_generator.py, z_transform_generator.py |
| `ECDH_SETUP` | 2 | `ECDH_SETUP\|E:y^2=x^3+2x+2 over F_17\|G=(5,1)` | ecdh_generator.py |
| `ECDSA_NONCE` | 2 | `ECDSA_NONCE\|kG=(6,3)\|r=6` | ecdsa_generator.py |
| `ECDSA_PUBLIC` | 1 | `ECDSA_PUBLIC\|Q=dG=(13,7)` | ecdsa_generator.py |
| `ECDSA_SETUP` | 4 | `ECDSA_SETUP\|E/F_17, G=(5,1), n=19\|d=8\|z=1\|k=2` | ecdsa_generator.py |
| `ECDSA_SIGN` | 2 | `ECDSA_SIGN\|s=k^-1(z+rd) mod n\|s=15` | ecdsa_generator.py |
| `ECDSA_VERIFY` | 2 | `ECDSA_VERIFY\|u1=14\|u2=8` | ecdsa_generator.py |
| `EC_ACCUM` | 2 | `EC_ACCUM\|1P\|(3,16)` | elliptic_curve_finite_field_generator.py |
| `EC_ADD` | 1 | `EC_ADD\|(6,3)` | ecdsa_generator.py |
| `EC_IDENTITY` | 2 | `EC_IDENTITY\|O + Q\|(3,16)` | elliptic_curve_finite_field_generator.py |
| `EC_INVERSE` | 3 | `EC_INVERSE\|(2,12)\|(2,7)\|O` | elliptic_curve_finite_field_generator.py |
| `EC_POINT_CHECK` | 3 | `EC_POINT_CHECK\|P\|O\|identity` | elliptic_curve_finite_field_generator.py |
| `EC_PUBLIC` | 2 | `EC_PUBLIC\|A=(3,1)\|B=(7,6)` | ecdh_generator.py |
| `EC_SCALAR` | 2 | `EC_SCALAR\|a=4\|aG=(3,1)` | ecdh_generator.py, ecdsa_generator.py |
| `EC_SCALAR_SETUP` | 2 | `EC_SCALAR_SETUP\|k=5\|P=(3,16)` | elliptic_curve_finite_field_generator.py |
| `EC_SETUP` | 3 | `EC_SETUP\|p=17\|a=2\|b=2` | elliptic_curve_finite_field_generator.py |
| `EC_SHARED` | 2 | `EC_SHARED\|aB=(6,14)\|bA=(6,14)` | ecdh_generator.py |
| `EC_SLOPE` | 2 | `EC_SLOPE\|2P\|11` | elliptic_curve_finite_field_generator.py |
| `EC_SLOPE_FORMULA` | 2 | `EC_SLOPE_FORMULA\|2P\|(3x1^2+a)/(2y1)` | elliptic_curve_finite_field_generator.py |
| `EC_X3` | 2 | `EC_X3\|2P\|13` | elliptic_curve_finite_field_generator.py |
| `EC_Y3` | 2 | `EC_Y3\|2P\|10` | elliptic_curve_finite_field_generator.py |
| `EDGE_CHECK` | 3 | `EDGE_CHECK\|(5553, 5553)\|(y, y)\|absent` | structure_isomorphism_generator.py |
| `EDGE_CHOOSE` | 3 | `EDGE_CHOOSE\|AC\|weight 1\|add A` | mst_generator.py |
| `EDGE_CONSIDER` | 2 | `EDGE_CONSIDER\|BD\|weight 1` | mst_generator.py |
| `EDGE_COUNT` | 2 | `EDGE_COUNT\|m\|5` | euler_circuit_generator.py, graph_counting_generator.py |
| `EDGE_LIST` | 1 | `EDGE_LIST\|AB, AC, AD, AE, BC, BD, BE, CD, CE, DE` | euler_circuit_generator.py |
| `EDGE_WEIGHT` | 2 | `EDGE_WEIGHT\|AB\|3` | dijkstra_generator.py, mst_generator.py |
| `EIGENPAIR` | 2 | `EIGENPAIR\|lambda = -4\|[1, 1]` | ode_system_generator.py |
| `EIGENVALUE` | 1, 2 | `EIGENVALUE\|λ = -1\|p(-1) = 0` | diagonalization_generator.py, eigenvalue_generator.py, matrix_exponential_generator.py, separable_pde_generator.py, svd_generator.py |
| `EIGENVALUES` | 2 | `EIGENVALUES\|A^T A\|36,16` | low_rank_approx_generator.py, matrix_norm_generator.py, pca_generator.py |
| `EIGENVECTOR` | 2 | `EIGENVECTOR\|A + 1I times v = 0\|[1, 5]` | diagonalization_generator.py, eigenvalue_generator.py, matrix_exponential_generator.py, svd_generator.py |
| `EIGEN_CHECK` | 3 | `EIGEN_CHECK\|sigma_x psi\|1*psi\|lambda=1` | spin_half_generator.py |
| `EIGEN_MATRIX` | 2 | `EIGEN_MATRIX\|A + 1I\|[[5, -1], [0, 0]]` | eigenvalue_generator.py |
| `EINSTEIN_SETUP` | 2, 3 | `EINSTEIN_SETUP\|contract\|A_ij=[[-5, 4], [-5, 2]]\|B_jk=[[-1, -4], [-2, 3]]` | einstein_summation_generator.py |
| `ELEC_FORMULA` | 1 | `ELEC_FORMULA\|left charge: E1=q1/r1^2` | electrostatics_generator.py |
| `ELEC_SETUP` | 2, 3 | `ELEC_SETUP\|field_axis\|q1=4, x1=-12\|q2=-9, x2=6` | electrostatics_generator.py |
| `ELEMENT_ORDER` | 2 | `ELEMENT_ORDER\|s\|2` | cayley_table_generator.py |
| `ELEMENT_SCAN` | 3 | `ELEMENT_SCAN\|30\|A\|found` | set_expression_generator.py, set_membership_subset_generator.py, set_operations_generator.py |
| `ELIMINATE` | 1, 3 | `ELIMINATE\|clue 1\|Finn: book; Cleo: compass; Nico: drum; Gia: mug\|violates clue` | logic_grid_puzzle_generator.py, newtons_laws_generator.py |
| `ELIMINATE_LAMBDA` | 2 | `ELIMINATE_LAMBDA\|f_x = f_y\|2*y = 3*x` | lagrange_multiplier_generator.py |
| `EL_EQUATION` | 1 | `EL_EQUATION\|d/dt(dL/dxdot)-dL/dx=0` | lagrangian_generator.py |
| `EL_SOLVE` | 2 | `EL_SOLVE\|xddot\|-(1/3)*x` | lagrangian_generator.py |
| `EMBED_SETUP` | 1 | `EMBED_SETUP\|A=(12,-5), B=(8,15), C=(5,12)` | embedding_similarity_generator.py |
| `ENERGY_FORMULA` | 1 | `ENERGY_FORMULA\|vf^2=vi^2+2W/m` | energy_conservation_generator.py |
| `ENERGY_LEVEL` | 2 | `ENERGY_LEVEL\|E_17=hbar*omega*(n+1/2)\|840` | ladder_operator_generator.py |
| `ENERGY_SETUP` | 3 | `ENERGY_SETUP\|work_energy\|m=7\|vi=15, W=3913/2` | energy_conservation_generator.py |
| `ENERGY_TERM` | 1 | `ENERGY_TERM\|T=1/2*m*xdot^2` | lagrangian_generator.py |
| `ENGINE_FORMULA` | 1 | `ENGINE_FORMULA\|Qh=Qc+W` | heat_engine_generator.py |
| `ENGINE_SETUP` | 3 | `ENGINE_SETUP\|refrigerator_cop\|Qc=49\|W=31` | heat_engine_generator.py |
| `ENQUEUE` | 3 | `ENQUEUE\|A\|from D\|A` | graph_traversal_generator.py |
| `ENTER` | 2 | `ENTER\|x\|most negative reduced cost -8` | simplex_generator.py |
| `ENTROPY_FORMULA` | 1 | `ENTROPY_FORMULA\|DeltaS_mix=-sum n_i ln(x_i)` | entropy_change_generator.py |
| `ENTROPY_SETUP` | 2, 3 | `ENTROPY_SETUP\|eigenvalues=[1/8,1/128,1/32,1/32,1/256,1/64,1/32,1/4,1/32,1/16,1/32,1/4,1/8,1/256]\|S=-sum lambda log2(lambda)` | entropy_change_generator.py, entropy_generator.py, huffman_coding_generator.py, information_gain_generator.py, mutual_information_generator.py, von_neumann_entropy_generator.py |
| `ENTROPY_SKIP` | 2 | `ENTROPY_SKIP\|H(X,Y)\|p=0` | mutual_information_generator.py |
| `ENTROPY_TERM` | 4 | `ENTROPY_TERM\|row 0\|p=1/2\|I=1\|1/2` | entropy_rate_markov_generator.py |
| `ENTROPY_VALUE` | 2 | `ENTROPY_VALUE\|parent\|0.8963125` | information_gain_generator.py |
| `ENTROPY_ZERO` | 2 | `ENTROPY_ZERO\|region_right\|count=0` | information_gain_generator.py |
| `EPSILON_VALUE` | 2 | `EPSILON_VALUE\|eps_122\|0` | index_gymnastics_generator.py |
| `EPS_CLOSURE` | 2 | `EPS_CLOSURE\|{u0}\|{u0}` | nfa_simulation_generator.py |
| `EQUATE_EXP` | 1 | `EQUATE_EXP\|5x = 2` | exponential_equation_generator.py |
| `EQUILIBRIA` | 2 | `EQUILIBRIA\|f(y) = 0\|y=-8, y=-3, y=12` | stability_generator.py |
| `EQ_2PT_SETUP` | 2 | `EQ_2PT_SETUP\|(-9, 4)\|(-10, 2)` | equation_from_two_points_generator.py |
| `EQ_OP_BOTH` | 3, 4 | `EQ_OP_BOTH\|multiply\|4\|x\|28` | absolute_value_equation_generator.py, area_between_curves_generator.py, completing_square_generator.py, curve_analysis_generator.py, error_spotting_generator.py, exponential_equation_generator.py, fill_in_step_generator.py, implicit_diff_generator.py, inverse_function_generator.py, linear_fractional_generator.py, log_diff_higher_order_generator.py, log_equation_generator.py, mean_value_theorem_generator.py, one_step_equation_generator.py, optimization_generator.py, partial_fractions_generator.py, polar_parametric_generator.py, quadratic_factoring_generator.py, quadratic_square_root_generator.py, radical_equation_generator.py, rational_equation_generator.py, related_rates_generator.py, remainder_factor_theorem_generator.py, separable_ode_generator.py, special_solution_equation_generator.py, systems_elimination_generator.py, systems_substitution_generator.py, trig_equation_generator.py, two_step_equation_generator.py |
| `EQ_OP_NOTE` | 3 | `EQ_OP_NOTE\|subtract\|c\|from both sides` | equation_from_two_points_generator.py, literal_equation_generator.py, parallel_perpendicular_line_generator.py, point_slope_generator.py, standard_form_conversion_generator.py |
| `EQ_RESULT` | 2 | `EQ_RESULT\|x\|28` | completing_square_generator.py, error_spotting_generator.py, fill_in_step_generator.py, linear_fractional_generator.py, linear_simple_generator.py, one_step_equation_generator.py, quadratic_factoring_generator.py, quadratic_square_root_generator.py, radical_equation_generator.py, rational_equation_generator.py, special_solution_equation_generator.py, two_step_equation_generator.py |
| `EQ_SETUP` | 1, 2 | `EQ_SETUP\|x = 6/2` | area_between_curves_generator.py, completing_square_generator.py, complex_quadratic_generator.py, cramers_rule_generator.py, discriminant_generator.py, error_spotting_generator.py, exponential_equation_generator.py, fill_in_step_generator.py, linear_fractional_generator.py, literal_equation_generator.py, log_equation_generator.py, one_step_equation_generator.py, polynomial_zeros_generator.py, proportion_word_problem_generator.py, proportional_relationship_generator.py, quadratic_factoring_generator.py, quadratic_generator.py, quadratic_square_root_generator.py, radical_equation_generator.py, rational_equation_generator.py, remainder_factor_theorem_generator.py, special_solution_equation_generator.py, standard_form_conversion_generator.py, trig_equation_generator.py, two_step_equation_generator.py |
| `EQ_SIMPLIFY` | 1 | `EQ_SIMPLIFY\|3x = 6` | error_spotting_generator.py, fill_in_step_generator.py, linear_fractional_generator.py, two_step_equation_generator.py |
| `ESCAPE_CHECK` | 3 | `ESCAPE_CHECK\|n=1\|norm2=45/16\|bounded` | fractal_iteration_generator.py |
| `ESTIMATE` | 2 | `ESTIMATE\|66127 × 42366 ≈ 70000 × 40000\|2800000000` | long_division_generator.py, multi_digit_multiplication_generator.py |
| `ESTIMATE_CHECK` | 3 | `ESTIMATE_CHECK\|1.9 × 10^4\|19008\|rounded estimate` | fermi_estimation_generator.py, long_division_generator.py, multi_digit_multiplication_generator.py |
| `EUCLID_DIV` | 4 | `EUCLID_DIV\|68\|54\|1\|14` | continued_fraction_generator.py, extended_euclid_generator.py, modular_inverse_generator.py, rsa_generator.py |
| `EULER_BACKTRACK` | 3 | `EULER_BACKTRACK\|A\|route suffix A\|stack A-B-C-A-D-B-E` | euler_circuit_generator.py |
| `EULER_CRITERION` | 2 | `EULER_CRITERION\|21^9 mod 19\|18` | quadratic_residue_generator.py |
| `EULER_FORMULA` | 1 | `EULER_FORMULA\|χ = V - E + F` | euler_characteristic_generator.py, euler_formula_generator.py |
| `EULER_NOTE` | 2 | `EULER_NOTE\|2\|sphere-family polyhedron: χ is always 2` | euler_characteristic_generator.py |
| `EULER_ROUTE` | 2 | `EULER_ROUTE\|A-B-C-A-D-B-E-C-D-E-A\|uses 10 edges` | euler_circuit_generator.py |
| `EULER_SETUP` | 2, 3 | `EULER_SETUP\|tetrahedron: V = 4, E = 6, F = 4\|V - E + F` | euler_characteristic_generator.py, euler_formula_generator.py |
| `EULER_STACK` | 2 | `EULER_STACK\|initial\|A` | euler_circuit_generator.py |
| `EULER_START` | 2 | `EULER_START\|A\|alphabetically first vertex` | euler_circuit_generator.py |
| `EULER_TRAVERSE` | 3 | `EULER_TRAVERSE\|A->B\|AB\|stack A-B` | euler_circuit_generator.py |
| `EVAL` | 1, 2, 3 | `EVAL\|p(-6)\|-11` | arc_length_generator.py, area_between_curves_generator.py, circle_equation_generator.py, complex_division_generator.py, composite_arithmetic_generator.py, conic_standard_form_generator.py, cramers_rule_generator.py, definite_integral_generator.py, derivative_limit_def_generator.py, determinant_generator.py, dot_product_generator.py, ellipse_features_generator.py, euler_method_generator.py, exact_ode_generator.py, five_number_summary_generator.py, function_composition_generator.py, function_operations_generator.py, horner_evaluation_generator.py, hyperbola_features_generator.py, improper_integral_generator.py, lagrange_multiplier_generator.py, legendre_construction_generator.py, limit_evaluation_generator.py, line_integral_generator.py, linear_approx_generator.py, log_conversion_generator.py, log_properties_generator.py, matrix_inverse_generator.py, mean_value_theorem_generator.py, ode_substitution_generator.py, parabola_features_generator.py, parametric_calculus_generator.py, partial_fractions_generator.py, power_series_generator.py, recursive_explicit_generator.py, regular_polygon_area_generator.py, related_rates_generator.py, remainder_factor_theorem_generator.py, riemann_sum_generator.py, row_reduction_generator.py, runge_kutta_generator.py, solid_revolution_generator.py, standard_deviation_generator.py, tangent_line_generator.py, taylor_series_generator.py, triangle_solve_generator.py, trig_equation_generator.py, trig_identity_eval_generator.py, trig_six_functions_generator.py, vector_ops_generator.py |
| `EVAL_AT_ZERO` | 2 | `EVAL_AT_ZERO\|e^0=1\|e^(2*0)=1` | mgf_generator.py |
| `EVAL_PARTIAL` | 3 | `EVAL_PARTIAL\|f_x\|8*1 + 3*3 - 6\|11` | gradient_generator.py, multivar_chain_rule_generator.py |
| `EVAL_SUB` | 3 | `EVAL_SUB\|p=T, q=T\|formula: ¬p\|F` | set_identity_membership_table_generator.py, truth_table_generator.py |
| `EVENT` | 2, 3 | `EVENT\|A\|first 11 tickets\|11` | complement_probability_generator.py, discrete_uniform_bernoulli_generator.py, fundamental_counting_principle_generator.py, independence_check_generator.py, probability_axioms_finite_generator.py, sample_space_list_generator.py, simple_probability_generator.py |
| `EV_FORMULA` | 1, 2 | `EV_FORMULA\|E[I] = P(I=1)\|13/27` | discrete_uniform_bernoulli_generator.py, expectation_of_function_generator.py, expected_value_generator.py |
| `EV_SETUP` | 2 | `EV_SETUP\|P(X=4) = 1/2; P(X=3) = 1/4; P(X=6) = 1/4\|Var(X)` | expected_value_generator.py |
| `EXACT_MATCH` | 2 | `EXACT_MATCH\|F_y = N\|x + g'(y) = x + 4*y + 2` | exact_ode_generator.py |
| `EXPAND` | 1, 2 | `EXPAND\|x = jw\|x = (rh)w` | complex_locus_generator.py, direct_proof_algebra_generator.py, mobius_transform_generator.py, zf_axiom_identify_generator.py |
| `EXPECTATION` | 3 | `EXPECTATION\|E[X]=19/33\|E[Y]=19/33\|E[XY]=76/363` | joint_distribution_generator.py |
| `EXPECTED_PAYOFF` | 1 | `EXPECTED_PAYOFF\|row1 against q` | game_theory_generator.py |
| `EXP_APPLY` | 2 | `EXP_APPLY\|x(t) = e^(At)x(0)\|x(0) = [6, 0]` | matrix_exponential_generator.py |
| `EXP_CELL` | 2 | `EXP_CELL\|(60·120)/200\|36` | chi_square_generator.py |
| `EXP_DIAG` | 2 | `EXP_DIAG\|e^(Dt)\|[[e^(-5t), 0], [0, e^(-t)]]` | matrix_exponential_generator.py |
| `EXP_ENTRY` | 3 | `EXP_ENTRY\|(1,1)\|e^(-t)\|e^(-t)` | matrix_exponential_generator.py |
| `EXP_EXPAND` | 1 | `EXP_EXPAND\|4 × 4 × 4` | exponent_generator.py |
| `EXP_FORM` | 1 | `EXP_FORM\|e^(At) = P*e^(Dt)*P^-1` | euler_formula_generator.py, matrix_exponential_generator.py |
| `EXP_PARTIAL` | 3 | `EXP_PARTIAL\|4\|4\|16` | exponent_generator.py |
| `EXP_RULE_APPLY` | 3, 4 | `EXP_RULE_APPLY\|subtract\|14\|1\|13` | exponent_generator.py, exponent_mixed_rules_generator.py |
| `EXP_RULE_IDENTIFY` | 2 | `EXP_RULE_IDENTIFY\|zero_exponent\|x^0 = 1 (for x ≠ 0)` | exponent_generator.py, exponent_mixed_rules_generator.py, rational_exponent_generator.py |
| `EXP_RULE_SETUP` | 1 | `EXP_RULE_SETUP\|u^0` | exponent_generator.py, exponent_mixed_rules_generator.py, rational_exponent_generator.py |
| `EXP_RULE_SIMPLIFY` | 1 | `EXP_RULE_SIMPLIFY\|1` | exponent_generator.py, exponent_mixed_rules_generator.py |
| `EXP_SETUP` | 2 | `EXP_SETUP\|4\|3` | exponent_generator.py |
| `EXP_SUB` | 3 | `EXP_SUB\|t/tau\|3\|e^-3` | transient_circuit_generator.py |
| `EXP_VALUE` | 2 | `EXP_VALUE\|exp(-z)\|1` | activation_generator.py |
| `EXT_GCD_SETUP` | 2 | `EXT_GCD_SETUP\|68\|54` | extended_euclid_generator.py, modular_inverse_generator.py, rsa_generator.py |
| `F` | 2, 3 | `F\|4/6\|2/3` | complement_probability_generator.py, composite_arithmetic_generator.py, counting_to_probability_generator.py, derangement_generator.py, discrete_uniform_bernoulli_generator.py, fraction_decimal_percent_converter.py, fraction_op_generator.py, fundamental_counting_principle_generator.py, independence_check_generator.py, likelihood_language_generator.py, mixed_number_operation_generator.py, mobius_transform_generator.py, order_of_operations_generator.py, quaternion_generator.py, radical_rationalize_generator.py, random_digit_simulation_generator.py, rational_exponent_generator.py, rational_expr_add_sub_generator.py, repeating_decimal_generator.py, sample_space_list_generator.py, simple_probability_generator.py, slope_two_points_generator.py, two_way_table_probability_generator.py, venn_probability_generator.py |
| `FACT` | 2 | `FACT\|7\|5040` | counting_to_probability_generator.py, derangement_generator.py, named_distribution_generator.py, order_statistics_generator.py, young_tableaux_generator.py |
| `FACTOR` | 1, 2 | `FACTOR\|x = r(hw)` | direct_proof_algebra_generator.py, polynomial_inequality_generator.py, second_order_ode_generator.py, transfer_function_generator.py, undetermined_coeff_generator.py, variation_parameters_generator.py |
| `FACTOR_FORM` | 2 | `FACTOR_FORM\|12\|2^2 * 3` | totient_generator.py |
| `FACTOR_FOUND` | 2 | `FACTOR_FOUND\|2\|2` | totient_generator.py |
| `FACTOR_GROUP` | 3 | `FACTOR_GROUP\|3y^2 + 9y\|3y\|(y + 3)` | conic_standard_form_generator.py, curve_analysis_generator.py, derivative_limit_def_generator.py, factor_grouping_generator.py, factor_trinomial_generator.py |
| `FACTOR_PAIR_GOAL` | 2 | `FACTOR_PAIR_GOAL\|m·n = -24\|m + n = -2` | factor_trinomial_generator.py |
| `FACTOR_SETUP` | 1 | `FACTOR_SETUP\|12` | totient_generator.py |
| `FACT_CHECK` | 3 | `FACT_CHECK\|375\|1\|0` | factors_generator.py |
| `FACT_FORMULA` | 1 | `FACT_FORMULA\|7! = 1·2·3·4·5·6·7` | derangement_generator.py, permutation_combination_generator.py |
| `FACT_PAIR` | 2 | `FACT_PAIR\|1\|375` | factors_generator.py |
| `FACT_SETUP` | 2 | `FACT_SETUP\|7!\|expand the factorial` | permutation_combination_generator.py |
| `FACT_VALUE` | 2 | `FACT_VALUE\|8!\|40320` | stars_and_bars_generator.py |
| `FCP` | 3 | `FCP\|fruits\|11\|11` | classic_probability_puzzles_generator.py, counting_to_probability_generator.py, fundamental_counting_principle_generator.py |
| `FEATURE_MAP_SETUP` | 3 | `FEATURE_MAP_SETUP\|K(x,z)=(xz+2)^2\|phi(t)=(t^2,2t,2)\|x=-13,z=19` | feature_map_generator.py |
| `FEATURE_VECTOR` | 2 | `FEATURE_VECTOR\|phi(x)\|(169,-26,2)` | feature_map_generator.py |
| `FEEDBACK` | 1 | `FEEDBACK\|T=G/(1+G)` | transfer_function_generator.py |
| `FERMAT_SETUP` | 3 | `FERMAT_SETUP\|prime 23\|base 31\|exponent 53` | totient_generator.py |
| `FERMI_FACTOR` | 2 | `FERMI_FACTOR\|sections\|24` | fermi_estimation_generator.py |
| `FERMI_SETUP` | 2 | `FERMI_SETUP\|stadium seats\|seats` | fermi_estimation_generator.py |
| `FIELD_SETUP` | 2 | `FIELD_SETUP\|GF(2)[x]\|addition is XOR` | finite_field_generator.py |
| `FIND_SLOPE` | 2 | `FIND_SLOPE\|Given slope (m1)\|-1/2` | parallel_perpendicular_line_generator.py |
| `FINITE_DIFF_SETUP` | 3 | `FINITE_DIFF_SETUP\|table\|x=[-3, 0, 3, 6]\|y=[23, 5, 41, 131]` | finite_difference_generator.py |
| `FIN_FORMULA` | 1 | `FIN_FORMULA\|category amount = income * category percent` | finance_generator.py |
| `FIN_SETUP` | 3 | `FIN_SETUP\|income = 3600\|needs 50%, savings 20%, fun 30%\|budget amounts` | finance_generator.py |
| `FIRSTLAW_FORMULA` | 1 | `FIRSTLAW_FORMULA\|DeltaU=Q-W` | first_law_generator.py |
| `FIRSTLAW_SETUP` | 3 | `FIRSTLAW_SETUP\|adiabatic\|Q=0\|W=60` | first_law_generator.py |
| `FIXED_CHECK` | 3 | `FIXED_CHECK\|c\|f(c) = n\|not fixed` | function_properties_generator.py |
| `FIXED_EQ` | 1 | `FIXED_EQ\|z=(az+b)/(cz+d)` | mobius_transform_generator.py |
| `FIXED_POINT` | 1 | `FIXED_POINT\|-5` | mobius_transform_generator.py |
| `FIXED_POINT_SETUP` | 3 | `FIXED_POINT_SETUP\|g(x)=-1/3*x-7/5\|x0=0\|iterations=4` | fixed_point_generator.py |
| `FIXED_POINT_UPDATE` | 3 | `FIXED_POINT_UPDATE\|1\|x_0=0\|x_1=-7/5` | fixed_point_generator.py |
| `FLAG` | 2 | `FLAG\|4\|F` | error_spotting_generator.py, foundations_critic_generator.py |
| `FLIP` | 2 | `FLIP\|1\|1 → 0` | cantor_diagonal_generator.py |
| `FLOOR_DIV` | 3 | `FLOOR_DIV\|5\|2\|2` | algorithm_trace_generator.py |
| `FLOPS_SETUP` | 2 | `FLOPS_SETUP\|rule=2mnk\|m=128,d=128,h=2048,o=32` | flops_memory_generator.py |
| `FLUX_SUM` | 2 | `FLUX_SUM\|(-1 + 0 - 1)*144\|-288` | vector_theorem_generator.py |
| `FOCUS` | 1 | `FOCUS\|(-4, 0)` | ellipse_features_generator.py, hyperbola_features_generator.py, parabola_features_generator.py |
| `FOIL_F` | 2 | `FOIL_F\|First: (-8) * (-7)\|56` | complex_division_generator.py, complex_number_ops_generator.py, multiplying_binomials_generator.py |
| `FOIL_I` | 2 | `FOIL_I\|Inner: (-9i) * (-7)\|63i` | complex_division_generator.py, complex_number_ops_generator.py, multiplying_binomials_generator.py |
| `FOIL_L` | 2 | `FOIL_L\|Last: (-9i) * 3i\|-27i^2` | complex_division_generator.py, complex_number_ops_generator.py, multiplying_binomials_generator.py |
| `FOIL_O` | 2 | `FOIL_O\|Outer: (-8) * 3i\|-24i` | complex_division_generator.py, complex_number_ops_generator.py, multiplying_binomials_generator.py |
| `FOIL_SETUP` | 1 | `FOIL_SETUP\|(5 + √13)(6 + √13)` | complex_division_generator.py, complex_number_ops_generator.py, multiplying_binomials_generator.py, radical_multiply_generator.py, trig_identity_verify_generator.py |
| `FOLD` | 2 | `FOLD\|rev("f")\|f` | peano_arithmetic_generator.py, recursive_definition_unfold_generator.py |
| `FORCE_COMPONENT` | 1 | `FORCE_COMPONENT\|parallel=m*g*sin` | newtons_laws_generator.py |
| `FORCE_EQ` | 1 | `FORCE_EQ\|m*a=parallel-friction` | newtons_laws_generator.py |
| `FORM` | 2 | `FORM\|forward\|(p ∨ r) → ((q ∧ p) ∨ (r ∨ p))` | conditional_forms_generator.py, zf_axiom_identify_generator.py |
| `FORMULA` | 1, 2 | `FORMULA\|sinh x = (e^x - e^(-x))/2` | collision_generator.py, gaussian_curvature_generator.py, hyperbolic_distance_generator.py, hyperbolic_function_generator.py, or_formula_generator.py, projectile_motion_generator.py, stereographic_generator.py, uncertainty_generator.py |
| `FORM_IDENTIFY` | 2 | `FORM_IDENTIFY\|difference_of_cubes\|a^3 - b^3 = (a - b)(a^2 + ab + b^2)` | completing_square_generator.py, conic_standard_form_generator.py, ellipse_features_generator.py, factor_special_forms_generator.py, hyperbola_features_generator.py, parabola_features_generator.py, radical_multiply_generator.py, radical_rationalize_generator.py, rational_equation_generator.py, rational_exponent_generator.py, rational_expr_add_sub_generator.py, rational_expr_mult_div_generator.py |
| `FOURIER_COEF` | 1 | `FOURIER_COEF\|b_12=-4/3` | fourier_series_generator.py |
| `FOURIER_SETUP` | 3 | `FOURIER_SETUP\|sawtooth\|A=8\|n=12` | fourier_series_generator.py |
| `FOUR_VECTOR_SETUP` | 3 | `FOUR_VECTOR_SETUP\|signature=+---\|p=[-2,0,5,8]\|q=[-2,-2,-3,-4]` | four_vector_generator.py |
| `FRACTAL_SETUP` | 4 | `FRACTAL_SETUP\|julia\|z0=(3/2,1)\|c=(-1/2,-3/2)\|N=4` | fractal_iteration_generator.py |
| `FRAC_BUILD` | 2 | `FRAC_BUILD\|50/110\|5/11` | classic_probability_puzzles_generator.py, conditional_probability_generator.py, geometric_probability_generator.py, hypergeometric_generator.py, two_way_table_probability_generator.py |
| `FRAC_REDUCE` | 2 | `FRAC_REDUCE\|42/-13\|-42/13` | angle_measure_generator.py, arc_length_generator.py, arc_sector_generator.py, complex_division_generator.py, frequency_table_generator.py, function_operations_generator.py, hyperbola_features_generator.py, implicit_diff_generator.py, improper_integral_generator.py, probability_addition_rule_generator.py, related_rates_generator.py, right_triangle_trig_generator.py |
| `FRAC_TO_DEC` | 2 | `FRAC_TO_DEC\|43/40\|1.075` | fraction_decimal_percent_converter.py, simple_probability_generator.py |
| `FREQ_SETUP` | 2 | `FREQ_SETUP\|table — Apple: 2, Banana: 7, Cherry: 4, Grape: 10, Melon: 11\|relative frequency of Apple` | frequency_table_generator.py |
| `FUNC_OP` | 2 | `FUNC_OP\|(p/q)(-6)\|p(-6)/q(-6)` | function_composition_generator.py, function_operations_generator.py |
| `FUNC_SETUP` | 2 | `FUNC_SETUP\|g(x) = 4x + 2\|g(6)` | domain_range_generator.py, function_composition_generator.py, function_evaluation_generator.py, function_operations_generator.py, function_table_generator.py, inverse_function_generator.py, piecewise_evaluation_generator.py, rational_function_features_generator.py |
| `FUNDAMENTAL_FORM_SETUP` | 3 | `FUNDAMENTAL_FORM_SETUP\|sphere\|R=3\|theta in [0,pi/2], phi in [0,180]` | fundamental_form_generator.py |
| `GAME_SETUP` | 2 | `GAME_SETUP\|payoffs=(9,2;2,4)\|row player maximizes, column player minimizes` | game_theory_generator.py |
| `GAMMA_SETUP` | 3 | `GAMMA_SETUP\|anticommutator_entry\|gamma0,gamma3\|entry=(4,1)` | gamma_matrix_generator.py |
| `GAS_FORMULA` | 1 | `GAS_FORMULA\|PV=nRT so n=PV/T` | gas_law_generator.py, gas_stoichiometry_generator.py |
| `GAS_SETUP` | 3 | `GAS_SETUP\|ideal_moles\|P=17, V=20\|T=16, R=1` | gas_law_generator.py |
| `GAS_STOICH_SETUP` | 3 | `GAS_STOICH_SETUP\|gas_to_mass\|2 CO + O2 -> 2 CO2\|gas=CO, target=CO2` | gas_stoichiometry_generator.py |
| `GATE_MATRIX` | 2 | `GATE_MATRIX\|H\|(1/sqrt(2))*[[1,1],[1,-1]]` | quantum_gate_generator.py |
| `GAUSSIAN_CURVATURE_SETUP` | 2, 3 | `GAUSSIAN_CURVATURE_SETUP\|saddle\|z=(14x^2-1y^2)/2\|point=(0,0)` | gaussian_curvature_generator.py |
| `GAUSS_BONNET_SETUP` | 3 | `GAUSS_BONNET_SETUP\|sphere\|R=26\|chi=2` | gauss_bonnet_generator.py |
| `GAUSS_FORMULA` | 1 | `GAUSS_FORMULA\|E*(4πr^2)=Q` | gauss_law_generator.py |
| `GAUSS_SETUP` | 3 | `GAUSS_SETUP\|sphere\|Q=46\|r=11` | gauss_law_generator.py |
| `GCD` | 2 | `GCD\|gcd(9,24)\|3` | derangement_generator.py, pollard_factorization_generator.py |
| `GCD_DIV` | 4 | `GCD_DIV\|140\|312\|0\|140` | rationals_as_pairs_generator.py |
| `GCD_DONE` | 1 | `GCD_DONE\|4` | rationals_as_pairs_generator.py |
| `GCD_RESULT` | 1, 2 | `GCD_RESULT\|1` | lcm_generator.py, modular_inverse_generator.py, permutation_group_generator.py, rsa_generator.py, totient_generator.py |
| `GCD_START` | 2 | `GCD_START\|45\|118` | gcf_generator.py, lcm_generator.py, rationals_as_pairs_generator.py |
| `GCD_STEP` | 3 | `GCD_STEP\|45\|118\|45` | gcf_generator.py, lcm_generator.py |
| `GCF_COEFF` | 2 | `GCF_COEFF\|3, 9\|3` | factor_gcf_generator.py, quadratic_factoring_generator.py, rational_expr_simplify_generator.py |
| `GCF_RESULT` | 1 | `GCF_RESULT\|3t` | factor_gcf_generator.py, quadratic_factoring_generator.py, rational_expr_simplify_generator.py |
| `GCF_VAR` | 2 | `GCF_VAR\|t^2, t\|t` | factor_gcf_generator.py, quadratic_factoring_generator.py, rational_expr_simplify_generator.py |
| `GD_SETUP` | 3 | `GD_SETUP\|f(x,y)=1/2*(3x^2+3y^2)\|start=(7,-8)\|eta=1/10` | gradient_descent_generator.py |
| `GD_UPDATE` | 3 | `GD_UPDATE\|w_old=(0,-2)\|eta=1/3\|w_new=(-2,2)` | gradient_step_generator.py |
| `GELLMANN_IDENTITY` | 3 | `GELLMANN_IDENTITY\|Tr(lambda_2 lambda_4)\|2 delta_ab\|0` | pauli_algebra_generator.py |
| `GELLMANN_SETUP` | 3 | `GELLMANN_SETUP\|trace\|A=-4lambda_2\|B=-lambda_4` | pauli_algebra_generator.py |
| `GENERAL` | 2 | `GENERAL\|a_n\|C1(-2)^n + C2(-3)^n` | recurrence_generator.py |
| `GEOMETRIC_FORMULA` | 2 | `GEOMETRIC_FORMULA\|c_n = A*(-1)^n/d^(n+1)\|A=1, d=-4` | laurent_series_generator.py |
| `GEOM_FORMULA` | 1 | `GEOM_FORMULA\|P(X > k) = (1-p)^k` | geometric_distribution_generator.py |
| `GEOM_SETUP` | 2 | `GEOM_SETUP\|p = 1/4, q = 3/4\|P(X > 1)` | geometric_distribution_generator.py |
| `GEO_PROB_FORMULA` | 1 | `GEO_PROB_FORMULA\|probability = favorable length / total length` | geometric_probability_generator.py |
| `GEO_PROB_SETUP` | 2 | `GEO_PROB_SETUP\|number line from 0 to 59\|lands between 13 and 31` | geometric_probability_generator.py |
| `GEO_SETUP` | 2 | `GEO_SETUP\|mean proportional between a = 115 and b = 74\|x with a/x = x/b` | geometric_mean_generator.py |
| `GF2_XOR` | 3 | `GF2_XOR\|quotient x\|0 xor 1\|1` | finite_field_generator.py |
| `GF_DIV_CHECK` | 3 | `GF_DIV_CHECK\|36 / 5\|not integer\|reject` | generating_function_generator.py |
| `GF_EXPAND` | 2 | `GF_EXPAND\|(1 + x)^6\|sum C(a,i)x^i` | generating_function_generator.py |
| `GF_SETUP` | 2 | `GF_SETUP\|[x^4]\|(1 + x)^6(1 + x)^3` | generating_function_generator.py |
| `GIANT_FACTOR` | 2 | `GIANT_FACTOR\|g^-m mod p\|2` | baby_step_giant_step_generator.py |
| `GIANT_STEP` | 2 | `GIANT_STEP\|i=0\|2` | baby_step_giant_step_generator.py |
| `GLB` | 1 | `GLB\|32` | partial_order_generator.py |
| `GOAL` | 1 | `GOAL\|show r² is odd` | direct_proof_algebra_generator.py, point_slope_generator.py, standard_form_conversion_generator.py |
| `GODEL_DECODE` | 2 | `GODEL_DECODE\|3, 4, 2\|) q ¬` | godel_numbering_generator.py |
| `GODEL_TERM` | 2 | `GODEL_TERM\|2^7\|128` | godel_numbering_generator.py |
| `GRAD` | 2 | `GRAD\|1\|4/13` | softmax_gradient_generator.py |
| `GRADIENT_FORMULA` | 1 | `GRADIENT_FORMULA\|grad=(3x,3y)` | gradient_descent_generator.py, matrix_calculus_generator.py |
| `GRAD_ENTRY` | 2 | `GRAD_ENTRY\|g1\|-23` | matrix_calculus_generator.py |
| `GRAD_RESULT` | 2 | `GRAD_RESULT\|grad g\|(1, 1)` | lagrange_multiplier_generator.py |
| `GRAD_SETUP` | 3 | `GRAD_SETUP\|f(x,y) = 4*x^2 + y^2 + 3*x*y - 6*x + y\|point (1, 3)\|directional` | gradient_generator.py |
| `GRAPH_CHANGE` | 3 | `GRAPH_CHANGE\|Jan\|Feb\|-2` | graph_interpret_generator.py |
| `GRAPH_DATA` | 2 | `GRAPH_DATA\|pictograph\|key:▲=10` | graph_interpret_generator.py |
| `GRAPH_MAX` | 2 | `GRAPH_MAX\|Giraffes\|70` | graph_interpret_generator.py |
| `GRAPH_MAX_CHANGE` | 3 | `GRAPH_MAX_CHANGE\|May\|Jun\|8` | graph_interpret_generator.py |
| `GRAPH_MIN` | 2 | `GRAPH_MIN\|Orange\|8` | graph_interpret_generator.py |
| `GRAPH_READ` | 2 | `GRAPH_READ\|Tue\|24` | graph_interpret_generator.py |
| `GRAPH_SETUP` | 2 | `GRAPH_SETUP\|directed adjacency matrix\|4 vertices` | dijkstra_generator.py, euler_circuit_generator.py, graph_counting_generator.py, graph_traversal_generator.py |
| `GRASSMANN_RESULT` | 3 | `GRASSMANN_RESULT\|constant=-30\|theta=16\|-30 + 16theta` | grassmann_generator.py |
| `GRASSMANN_SETUP` | 3 | `GRASSMANN_SETUP\|integrate\|expr=2 - 5theta\|int1=0,inttheta=1` | grassmann_generator.py |
| `GREATEST` | 1 | `GREATEST\|none` | partial_order_generator.py |
| `GREAT_CIRCLE_SETUP` | 3 | `GREAT_CIRCLE_SETUP\|R=12\|A=(90,-150)\|B=(30,-90)` | great_circle_generator.py |
| `GROUP` | 2 | `GROUP\|(3y^2 + 9y)\|(2y + 6)` | factor_grouping_generator.py, factor_trinomial_generator.py |
| `GROUP_MULT` | 3 | `GROUP_MULT\|e\|e\|e` | coset_generator.py |
| `GROUP_SETUP` | 2, 3 | `GROUP_SETUP\|D3\|symmetries of a triangle` | cayley_table_generator.py, coset_generator.py, cyclic_group_generator.py |
| `GS_SETUP` | 2 | `GS_SETUP\|vectors [[-1, -1], [0, -4]]\|orthogonal basis, not normalized` | gram_schmidt_generator.py |
| `GS_SUBTRACT` | 2 | `GS_SUBTRACT\|remove projection on u1\|[2, -2]` | gram_schmidt_generator.py, qr_decomposition_generator.py |
| `GS_VECTOR` | 2 | `GS_VECTOR\|u1 = v1\|[-1, -1]` | gram_schmidt_generator.py |
| `G_ROW` | 3 | `G_ROW\|x=-10\|g = -10\|-10 × 45/256 = -225/128` | expectation_of_function_generator.py |
| `HA` | 1 | `HA\|y = 1` | rational_function_features_generator.py |
| `HAMILTON` | 2 | `HAMILTON\|i*i\|-1` | quaternion_generator.py |
| `HAMILTONIAN` | 1 | `HAMILTONIAN\|H=p_theta^2/(2mL^2)+mgL*(1-cos(theta))` | hamiltonian_generator.py |
| `HAMMING_PLACE` | 2 | `HAMMING_PLACE\|positions 1,2,3,4,5,6,7\|p1,p2,d1,p4,d2,d3,d4` | hamming_code_generator.py |
| `HAMMING_RECEIVED` | 1 | `HAMMING_RECEIVED\|r=0110010` | hamming_code_generator.py |
| `HAMMING_SETUP` | 2 | `HAMMING_SETUP\|data=1100\|even parity` | hamming_code_generator.py |
| `HAM_EQ` | 2 | `HAM_EQ\|thetadot=dH/dp_theta\|thetadot=p_theta/8` | hamiltonian_generator.py |
| `HAM_SETUP` | 3 | `HAM_SETUP\|pendulum\|m=2, L=2\|g=10, q=theta` | hamiltonian_generator.py |
| `HARMONIC_SETUP` | 1 | `HARMONIC_SETUP\|u=-2x^2 + 2y^2 - 4x + 5y` | cauchy_riemann_generator.py |
| `HAWKING_SETUP` | 3 | `HAWKING_SETUP\|entropy\|S_BH=k_B*c^3*A/(4*hbar*G)\|k_B=5,c=5,A=6,hbar=2,G=5` | hawking_generator.py |
| `HESSIAN_DET` | 3 | `HESSIAN_DET\|D = f_xx*f_yy - f_xy^2\|4*(-2) - 2^2\|-12` | hessian_classify_generator.py |
| `HESSIAN_SETUP` | 2 | `HESSIAN_SETUP\|f(x,y) = 2*x^2 - y^2 + 2*x*y - 10*x - 14*y\|find and classify the critical point` | hessian_classify_generator.py |
| `HESSIAN_TEST` | 3 | `HESSIAN_TEST\|D = -12\|f_xx = 4\|saddle point` | hessian_classify_generator.py |
| `HIDDEN_PRE` | 2 | `HIDDEN_PRE\|h1\|z=3` | backprop_generator.py |
| `HIT_EQ` | 2 | `HIT_EQ\|t0=1+p00*t0+p01*t1\|t1=1+p10*t0+p11*t1` | markov_chain_generator.py |
| `HMM_SETUP` | 2 | `HMM_SETUP\|states H,L\|observations BAA` | viterbi_generator.py |
| `HMM_START` | 1 | `HMM_START\|H=1/2, L=1/2` | viterbi_generator.py |
| `HOLE` | 1 | `HOLE\|x = 4` | rational_function_features_generator.py |
| `HOM_SOL` | 2 | `HOM_SOL\|y_h\|y_h = C1e^(-x) + C2e^(3x)` | undetermined_coeff_generator.py, variation_parameters_generator.py |
| `HOOK` | 4 | `HOOK\|(1,1)\|right=6\|below=1\|hook=8` | young_tableaux_generator.py |
| `HORNER_SETUP` | 2 | `HORNER_SETUP\|3x^4 - 5x^3 + 4x^2 + x + 3\|x = 4` | horner_evaluation_generator.py |
| `HT_SETUP` | 2 | `HT_SETUP\|H0: μ = 41; Ha: μ ≠ 41\|n = 25, x̄ = 30, s = 20, critical value = 1.96` | hypothesis_test_generator.py, two_sample_test_generator.py |
| `HUFFMAN_FORMULA` | 1 | `HUFFMAN_FORMULA\|L=sum p_i*l_i` | huffman_coding_generator.py |
| `HUFFMAN_MERGE` | 2 | `HUFFMAN_MERGE\|A:1/32 + G:1/32\|AG:1/16` | huffman_coding_generator.py |
| `HUFFMAN_SETUP` | 1 | `HUFFMAN_SETUP\|A=1/32, B=1/16, C=1/8, D=1/4, E=1/4, F=1/8, G=1/32, H=1/8` | huffman_coding_generator.py |
| `HYDROGEN_FORMULA` | 1 | `HYDROGEN_FORMULA\|1/lambda=R_L*(1/n_low^2-1/n_high^2)` | hydrogen_atom_generator.py |
| `HYDROGEN_SETUP` | 3 | `HYDROGEN_SETUP\|transition_wavelength\|n_low=6, n_high=7\|R_L=14 1/m` | hydrogen_atom_generator.py |
| `HYPERBOLIC_DISTANCE_SETUP` | 3 | `HYPERBOLIC_DISTANCE_SETUP\|half-plane\|P=(-2,19)\|Q=(-2,399/16)` | hyperbolic_distance_generator.py |
| `HYPERBOLIC_SETUP` | 2 | `HYPERBOLIC_SETUP\|e^x=31/23\|e^(-x)=23/31` | hyperbolic_function_generator.py |
| `HYPERCUBE_FORMULA` | 1 | `HYPERCUBE_FORMULA\|diagonal = s·√n` | hypercube_counting_generator.py |
| `HYPERCUBE_SETUP` | 2 | `HYPERCUBE_SETUP\|5-cube with side 3\|main diagonal` | hypercube_counting_generator.py |
| `HYPERGEO_FORMULA` | 1 | `HYPERGEO_FORMULA\|P(counts) = product of type combinations/C(N,n)` | hypergeometric_generator.py |
| `HYPERGEO_SETUP` | 2 | `HYPERGEO_SETUP\|N = 11, n = 6\|1 black, 3 silver, 2 gold` | hypergeometric_generator.py |
| `HYPERGEO_TERM` | 2 | `HYPERGEO_TERM\|X = 5\|2/11` | hypergeometric_generator.py |
| `I` | 2 | `I\|7/2\|2/7` | fraction_op_generator.py, mixed_number_operation_generator.py, rational_expr_mult_div_generator.py |
| `ICE_ROW` | 2 | `ICE_ROW\|current\|[A]=7, [B]=7` | equilibrium_ice_generator.py |
| `IDENTIFY` | 2 | `IDENTIFY\|order does not matter\|use C(n, r)` | permutation_combination_generator.py |
| `IDENTITY` | 2 | `IDENTITY\|hockey-stick\|Σ i=5..89 C(i,5) = C(90,6)` | counting_classics_generator.py, function_inner_product_generator.py, index_gymnastics_generator.py |
| `IDENTITY_SETUP` | 2 | `IDENTITY_SETUP\|verify: 1/(1 - cos t) + 1/(1 + cos t) = 2/sin^2 t\|transform the left side` | trig_identity_verify_generator.py |
| `IDENT_MATCH` | 1 | `IDENT_MATCH\|2/sin^2 t = 2/sin^2 t` | trig_identity_verify_generator.py |
| `IDENT_SUB` | 1, 2 | `IDENT_SUB\|1 - cos^2 t = sin^2 t` | parametric_calculus_generator.py, trig_identity_verify_generator.py |
| `IE_FORMULA` | 1, 2 | `IE_FORMULA\|count(R or C) = count(R) + count(C) − count(R and C)` | inclusion_exclusion_generator.py, probability_measure_generator.py, two_way_table_probability_generator.py, venn_probability_generator.py |
| `IE_SETUP` | 2 | `IE_SETUP\|n(A)=44, n(B)=43\|n(A intersect B)=11` | inclusion_exclusion_generator.py |
| `IFACTOR` | 2 | `IFACTOR\|mu = e^(∫ 4 dx)\|e^(4x)` | integrating_factor_generator.py, ode_substitution_generator.py |
| `IG_SETUP` | 3 | `IG_SETUP\|parent pos=11, neg=5\|total=16\|splits=region,texture` | information_gain_generator.py |
| `IMAGE` | 2 | `IMAGE\|b\|23` | function_properties_generator.py, mobius_transform_generator.py |
| `IMPLICIT_DIFF` | 2 | `IMPLICIT_DIFF\|d/dx of x^2\|2x` | implicit_diff_generator.py, log_diff_higher_order_generator.py, related_rates_generator.py |
| `IMPLICIT_SETUP` | 2 | `IMPLICIT_SETUP\|x^2 + xy + y^2 = 3\|dy/dx` | implicit_diff_generator.py |
| `IMPROPER_TO_MIX` | 2 | `IMPROPER_TO_MIX\|477/55\|8 37/55` | composite_arithmetic_generator.py, mixed_number_operation_generator.py, order_of_operations_generator.py |
| `INDEGREE` | 2 | `INDEGREE\|A\|0` | graph_traversal_generator.py |
| `INDEGREE_UPDATE` | 2 | `INDEGREE_UPDATE\|B\|0` | graph_traversal_generator.py |
| `INDEP_CHECK` | 3 | `INDEP_CHECK\|P(A ∩ B) = 19/135\|product = 377/1215\|no` | independence_check_generator.py, joint_distribution_generator.py |
| `INDEP_FORMULA` | 1 | `INDEP_FORMULA\|independent iff P(A ∩ B) = P(A)·P(B)` | independence_check_generator.py, joint_distribution_generator.py |
| `INDEX` | 3 | `INDEX\|G size 24\|H size 2\|12` | coset_generator.py |
| `INDEX_METRIC` | 3 | `INDEX_METRIC\|raise\|Minkowski\|g^ii=[-1,1,1,1]` | index_raising_generator.py |
| `INDEX_SETUP` | 3 | `INDEX_SETUP\|c=2\|j=2, k=2\|l=1, m=2` | index_gymnastics_generator.py |
| `INDICATOR` | 2 | `INDICATOR\|I_j = 1 if bin j is empty\|P(I_j = 1) = (5/6)^3` | linearity_of_expectation_generator.py |
| `INDUCT_ASSUME` | 1, 2 | `INDUCT_ASSUME\|n = 4a + 5b\|a,b nonnegative` | induction_verify_generator.py |
| `INDUCT_BASE` | 2 | `INDUCT_BASE\|n=12\|12 = 4·3 + 5·0` | induction_verify_generator.py |
| `INDUCT_STEP` | 1, 2 | `INDUCT_STEP\|n → n+4\|n+4 = 4(a+1) + 5b` | induction_verify_generator.py |
| `INEQ_FLIP` | 1 | `INEQ_FLIP\|Multiplying by negative number reverses inequality` | domain_range_generator.py, linear_fractional_generator.py, one_step_inequality_generator.py, two_step_inequality_generator.py |
| `INEQ_OP_ALL` | 3 | `INEQ_OP_ALL\|subtract\|8\|-22 < 4x < 6` | absolute_value_inequality_generator.py, compound_inequality_generator.py |
| `INEQ_OP_BOTH` | 4 | `INEQ_OP_BOTH\|add\|8\|x\|13` | domain_range_generator.py, linear_fractional_generator.py, one_step_inequality_generator.py, two_step_inequality_generator.py |
| `INEQ_RESULT` | 3 | `INEQ_RESULT\|x\|>\|13` | domain_range_generator.py, linear_fractional_generator.py, one_step_inequality_generator.py, two_step_inequality_generator.py |
| `INEQ_SETUP` | 1 | `INEQ_SETUP\|x - 8 > 5` | linear_fractional_generator.py, one_step_inequality_generator.py, polynomial_inequality_generator.py, two_step_inequality_generator.py |
| `INEQ_SIMPLIFY` | 1 | `INEQ_SIMPLIFY\|x/-5 > -1` | domain_range_generator.py, linear_fractional_generator.py, two_step_inequality_generator.py |
| `INEX_TERM` | 3 | `INEX_TERM\|0\|1×1^1\|1` | function_properties_generator.py |
| `INFO_GAIN` | 2 | `INFO_GAIN\|region\|0.419125` | information_gain_generator.py |
| `INFO_SETUP` | 2 | `INFO_SETUP\|p=1/65536\|I=-log2(p)` | entropy_generator.py |
| `INFO_TABLE` | 1 | `INFO_TABLE\|1/4=2, 5/16=1.678, 3/8=1.415, 5/8=0.678, 11/16=0.541, 3/4=0.415, 1=0` | information_gain_generator.py |
| `INFO_VALUE` | 2 | `INFO_VALUE\|p=11/16\|I=0.541` | information_gain_generator.py |
| `INITIAL` | 2 | `INITIAL\|D_0 = 1\|D_1 = 0` | derangement_generator.py |
| `INITIAL_COEFF` | 2 | `INITIAL_COEFF\|a_0\|1440` | series_solution_generator.py |
| `INITIAL_EQ` | 2 | `INITIAL_EQ\|C1 + C2\|6` | recurrence_generator.py |
| `INITIAL_SYSTEM` | 2 | `INITIAL_SYSTEM\|C1[1, 1] + C2[0, 1]\|[2, 3]` | ode_system_generator.py |
| `INNER_ANTIDERIV` | 2 | `INNER_ANTIDERIV\|dr\|r^4/4` | double_integral_generator.py, triple_integral_generator.py |
| `INNER_EVAL` | 2, 3 | `INNER_EVAL\|r=0..5\|5^4/4\|625/4` | double_integral_generator.py, triple_integral_generator.py |
| `INNER_PRODUCT` | 2 | `INNER_PRODUCT\|inner(phi,psi)\|-5-i` | braket_generator.py |
| `INNER_PRODUCT_SETUP` | 3 | `INNER_PRODUCT_SETUP\|interval=[0,2pi]\|f=cos(5x)\|g=cos(25x)` | function_inner_product_generator.py |
| `INSERT_KEY` | 3 | `INSERT_KEY\|pass 1\|24\|index 1` | algorithm_trace_generator.py |
| `INSERT_PLACE` | 2 | `INSERT_PLACE\|index 1\|2, 24, 14, 9, 25, 30` | algorithm_trace_generator.py |
| `INTEGRAL` | 1, 2 | `INTEGRAL\|integral cos(20x) on [0,2pi]\|0` | fourier_series_generator.py, function_inner_product_generator.py, legendre_construction_generator.py |
| `INTEGRAL_SETUP` | 1 | `INTEGRAL_SETUP\|L = integral from r0 to r1 of 1 dr` | metric_arc_length_generator.py |
| `INTEGRATE` | 2 | `INTEGRATE\|v_y = u_x\|v=-4xy - 5x - 4y + phi(x)` | cauchy_riemann_generator.py |
| `INTEGRATION_BY_PARTS` | 2 | `INTEGRATION_BY_PARTS\|u=x\|dv=sin(nx)dx` | fourier_series_generator.py |
| `INTEG_RULE` | 2 | `INTEG_RULE\|trig rule\|∫ cos(u) du = sin(u) + C` | antiderivative_generator.py, definite_integral_generator.py, ode_substitution_generator.py, partial_fractions_generator.py, separable_ode_generator.py, solid_revolution_generator.py, u_substitution_generator.py |
| `INTEG_SETUP` | 2 | `INTEG_SETUP\|∫ 3 cos(x) dx\|antiderivative` | antiderivative_generator.py, arc_length_generator.py, definite_integral_generator.py, improper_integral_generator.py, integration_by_parts_generator.py, parametric_calculus_generator.py, partial_fractions_generator.py, u_substitution_generator.py |
| `INTERCEPT_FORMULA` | 1 | `INTERCEPT_FORMULA\|a = ȳ - b·x̄` | regression_generator.py |
| `INTERFERENCE_FORMULA` | 1 | `INTERFERENCE_FORMULA\|2*n*t=m*lambda` | interference_generator.py |
| `INTERFERENCE_SETUP` | 3 | `INTERFERENCE_SETUP\|thin_film\|m=6, lambda=14\|n=2` | interference_generator.py |
| `INTERP_SETUP` | 3 | `INTERP_SETUP\|lagrange\|points=(0,6), (2,12), (4,34)\|x=-4` | interpolation_generator.py |
| `INTERVAL_CLASS` | 2 | `INTERVAL_CLASS\|s2=63\|timelike` | minkowski_interval_generator.py |
| `INT_ABS` | 2 | `INT_ABS\|5\|5` | integer_operations_generator.py |
| `INT_ALIGN` | 2 | `INT_ALIGN\|82320\|65750` | multi_digit_addition_generator.py, multi_digit_subtraction_generator.py |
| `INT_APPLY_SIGN` | 3 | `INT_APPLY_SIGN\|12\|positive\|12` | integer_operations_generator.py |
| `INT_OP` | 4 | `INT_OP\|-\|5\|5\|0` | integer_operations_generator.py |
| `INT_REWRITE` | 2 | `INT_REWRITE\|-15 - (-19)\|-15 + 19` | integer_operations_generator.py |
| `INT_SIGN_RULE` | 2 | `INT_SIGN_RULE\|different_signs\|Different signs: subtract absolute values, take sign of larger absolute value` | integer_operations_generator.py |
| `INVARIANT` | 3 | `INVARIANT\|sizes\|3\|3` | structure_isomorphism_generator.py |
| `INVERSE_LAPLACE` | 2 | `INVERSE_LAPLACE\|3/(s + 5)\|3e^(-5t)` | laplace_ivp_generator.py |
| `INVERSE_MAP` | 2 | `INVERSE_MAP\|x=(u+v)/2\|y=(u-v)/2` | rv_transform_generator.py |
| `INVERSE_METRIC` | 2 | `INVERSE_METRIC\|g^rr=1\|g^thetatheta=1/r^2` | christoffel_generator.py, riemann_tensor_generator.py |
| `INVERSE_PAIR` | 2 | `INVERSE_PAIR\|(j, 4)\|(4, j)` | function_properties_generator.py, relation_operations_generator.py |
| `INV_FORMULA` | 1 | `INV_FORMULA\|A⁻¹ = (1/det)·[[d, -b], [-c, a]]` | matrix_inverse_generator.py |
| `IRR_SETUP` | 2 | `IRR_SETUP\|c0=-2900,c1=3480\|r0=1/5,iterations=2` | npv_irr_generator.py |
| `IRR_VALUE` | 2 | `IRR_VALUE\|f1\|0` | npv_irr_generator.py |
| `ITERATE` | 2 | `ITERATE\|n=1\|z=(3/4,3/2)` | fractal_iteration_generator.py, gradient_descent_generator.py |
| `IVT_SETUP` | 2 | `IVT_SETUP\|f(x) = x^3 - 4x + 7 on [-4, -2]\|does the IVT guarantee a root?` | mean_value_theorem_generator.py |
| `I_CYCLE` | 2 | `I_CYCLE\|i^3\|-i` | complex_number_ops_generator.py |
| `I_SQUARE` | 2 | `I_SQUARE\|-27i^2\|27` | complex_division_generator.py, complex_log_generator.py, complex_number_ops_generator.py |
| `JACOBIAN` | 2 | `JACOBIAN\|dA\|r dr dtheta` | double_integral_generator.py |
| `JACOBI_END` | 2 | `JACOBI_END\|gcd(35,91)>1\|0` | jacobi_symbol_generator.py |
| `JACOBI_RECIPROCITY` | 3 | `JACOBI_RECIPROCITY\|a mod 4 = 3\|n mod 4 = 3\|flip sign` | jacobi_symbol_generator.py |
| `JACOBI_SETUP` | 3 | `JACOBI_SETUP\|a=35\|n=91\|n odd` | jacobi_symbol_generator.py |
| `JACOBI_SWAP` | 3 | `JACOBI_SWAP\|a=91\|n=35\|sign -1` | jacobi_symbol_generator.py |
| `JACOBI_TWO_RULE` | 3 | `JACOBI_TWO_RULE\|n mod 8 = 5\|flip sign\|sign 1` | jacobi_symbol_generator.py |
| `JAC_DET` | 3 | `JAC_DET\|x_u*y_v - x_v*y_u\|(-5)*5 - 2*2\|-29` | jacobian_generator.py |
| `JAC_MATRIX` | 2 | `JAC_MATRIX\|[[x_u, x_v], [y_u, y_v]]\|[[-5, 2], [2, 5]]` | jacobian_generator.py, rv_transform_generator.py |
| `JAC_SETUP` | 3 | `JAC_SETUP\|x = -5*u + 2*v\|y = 2*u + 5*v\|d(x,y)/d(u,v)` | jacobian_generator.py |
| `JOINT_ROW` | 2 | `JOINT_ROW\|x=0, y=0\|19/128` | conditional_expectation_generator.py, covariance_algebra_generator.py |
| `JOINT_SETUP` | 3 | `JOINT_SETUP\|X,Y in {0,1}\|p00=7/121, p01=133/363\|p10=133/363, p11=76/363` | joint_distribution_generator.py |
| `KERNEL_BASE` | 3 | `KERNEL_BASE\|A,A\|dot+c=1+0\|1` | feature_map_generator.py, kernel_evaluation_generator.py |
| `KERNEL_EXPONENT` | 2 | `KERNEL_EXPONENT\|A,A\|0` | kernel_evaluation_generator.py |
| `KERNEL_SETUP` | 3 | `KERNEL_SETUP\|type=rbf\|points=A=(0,2), B=(2,-3)\|gamma=1/2` | kernel_evaluation_generator.py |
| `KERNEL_VALIDITY` | 1 | `KERNEL_VALIDITY\|psd=true` | kernel_validity_generator.py |
| `KERNEL_VALUE` | 2 | `KERNEL_VALUE\|A,A\|1` | feature_map_generator.py, kernel_evaluation_generator.py, kernel_perceptron_generator.py, kernel_ridge_generator.py |
| `KIN_FORMULA` | 1 | `KIN_FORMULA\|t = d/v` | invariant_mass_generator.py, kinematics_generator.py |
| `KIN_SETUP` | 3, 4 | `KIN_SETUP\|d = 325 meters\|v = 65 m/s\|time` | invariant_mass_generator.py, kinematics_generator.py |
| `KL_FORMULA` | 1 | `KL_FORMULA\|D=sum source_i*log2(source_i/target_i)` | kl_divergence_generator.py |
| `KL_SETUP` | 3 | `KL_SETUP\|P=[192/511,1/2,127/1022]\|Q=[3/1022,1/2,254/511]\|direction=Q to P` | kl_divergence_generator.py |
| `KMAP_GROUP` | 2 | `KMAP_GROUP\|101\|K AND NOT L AND M` | boolean_algebra_generator.py |
| `KMAP_ROW` | 2 | `KMAP_ROW\|K=0\|0, 0, 0, 0` | boolean_algebra_generator.py |
| `KMAP_SETUP` | 2 | `KMAP_SETUP\|rows K=0,K=1\|columns LM=00,LM=01,LM=11,LM=10` | boolean_algebra_generator.py |
| `KMAP_SIMPLIFY` | 1 | `KMAP_SIMPLIFY\|(K AND NOT L AND M) OR (K AND L AND NOT M)` | boolean_algebra_generator.py |
| `KMEANS_SETUP` | 2 | `KMEANS_SETUP\|points=P1=(5,3), P2=(-3,1), P3=(-5,-5), P4=(-1,1)\|centroids=C1=(0,-3), C2=(2,2)` | kmeans_step_generator.py |
| `KNN_DISTANCE` | 3 | `KNN_DISTANCE\|P1\|label=A\|d2=73` | knn_generator.py |
| `KNN_NEIGHBORS` | 1 | `KNN_NEIGHBORS\|P4:20:A,P2:50:A,P1:73:A` | knn_generator.py |
| `KNN_SETUP` | 3 | `KNN_SETUP\|q=(3,3)\|k=3\|training=P1=(-5,0,A), P2=(-4,2,A), P3=(-4,-5,A), P4=(5,-1,A), P5=(-2,-5,A)` | knn_generator.py |
| `KNN_SORT` | 1 | `KNN_SORT\|P4:20:A,P2:50:A,P1:73:A,P5:89:A,P3:113:A` | knn_generator.py |
| `KP_EXAMPLE` | 3 | `KP_EXAMPLE\|1\|x=6,y=1\|alpha=(0,0,0)` | kernel_perceptron_generator.py |
| `KP_SETUP` | 3 | `KP_SETUP\|kernel=linear\|data=[(6,1), (4,1), (-1,1)]\|alpha0=(0,0,0)` | kernel_perceptron_generator.py |
| `KP_TERM` | 2 | `KP_TERM\|j=1\|0` | kernel_perceptron_generator.py |
| `KRAFT_CHECK` | 2, 3 | `KRAFT_CHECK\|sum=1\|complete` | huffman_coding_generator.py, kraft_inequality_generator.py |
| `KRAFT_CLASSIFY` | 2 | `KRAFT_CLASSIFY\|excess=37/64\|no prefix code` | kraft_inequality_generator.py |
| `KRAFT_FORMULA` | 1 | `KRAFT_FORMULA\|sum 2^-l_i` | huffman_coding_generator.py, kraft_inequality_generator.py |
| `KRAFT_SETUP` | 2 | `KRAFT_SETUP\|A=1, B=1, C=6, D=4, E=1\|binary prefix code` | kraft_inequality_generator.py |
| `KRAFT_TERM` | 3 | `KRAFT_TERM\|A\|l=1\|1/2` | kraft_inequality_generator.py |
| `KRR_SETUP` | 3 | `KRR_SETUP\|kernel=linear\|data=[(-1,2), (-6,3)]\|lambda=3,x*=-3` | kernel_ridge_generator.py |
| `KV_CACHE` | 2 | `KV_CACHE\|values\|47185920` | flops_memory_generator.py |
| `K_EXPR` | 1, 2 | `K_EXPR\|K = [B]^2/[A]\|0.4 = (2x)^2/(11-x)` | equilibrium_ice_generator.py |
| `L` | 2, 3 | `L\|3\|7\|21` | complement_probability_generator.py, experimental_probability_generator.py, fraction_comparison_generator.py, fraction_op_generator.py, linear_fractional_generator.py, mixed_number_operation_generator.py, rational_expr_add_sub_generator.py |
| `LABEL_COUNT` | 2 | `LABEL_COUNT\|A\|3` | knn_generator.py |
| `LADDER_APPLY` | 2 | `LADDER_APPLY\|a ket18\|sqrt(18) ket17` | ladder_operator_generator.py |
| `LADDER_COMM` | 2 | `LADDER_COMM\|[a,adag] ketn\|ket18` | ladder_operator_generator.py |
| `LADDER_RULE` | 2 | `LADDER_RULE\|J_- = J1_- + J2_-\|lower from highest weights` | clebsch_gordan_generator.py, ladder_operator_generator.py |
| `LADDER_SETUP` | 3 | `LADDER_SETUP\|single_step_energy\|state=ket18\|hbar=6, omega=8` | ladder_operator_generator.py |
| `LAGRANGE_EQ` | 2 | `LAGRANGE_EQ\|f_x = lambda\|2*x*y^3` | lagrange_multiplier_generator.py |
| `LAGRANGE_FACTOR` | 3 | `LAGRANGE_FACTOR\|L_0\|j=1\|3` | interpolation_generator.py |
| `LAGRANGE_SETUP` | 3 | `LAGRANGE_SETUP\|f(x,y) = x^2*y^3\|constraint x + y = 15\|maximize` | lagrange_multiplier_generator.py |
| `LAGRANGIAN` | 1, 2 | `LAGRANGIAN\|L=T-V\|1/2*m*xdot^2 - 1/2*k*x^2` | lagrangian_generator.py |
| `LAG_SETUP` | 3 | `LAG_SETUP\|mass_spring\|m=6, k=2\|q=x` | lagrangian_generator.py |
| `LAMBDA_SETUP` | 2 | `LAMBDA_SETUP\|(((lambda p. (lambda b. (lambda p. (lambda p. (p b))))) (lambda f. (p f))) p)\|leftmost-outermost` | lambda_reduction_generator.py |
| `LAPLACE` | 2 | `LAPLACE\|L[y' + 5y]\|(sY - 7) + 5Y` | laplace_ivp_generator.py, transfer_function_generator.py |
| `LAPLACE_TABLE` | 1 | `LAPLACE_TABLE\|L{y'} = sY - y(0); L{e^(kt)} = 1/(s-k); L^-1{1/(s-k)} = e^(kt)` | laplace_ivp_generator.py |
| `LATTICE_PAIR` | 3 | `LATTICE_PAIR\|(16, 16)\|lub 16\|glb 16` | partial_order_generator.py |
| `LAURENT_SETUP` | 3 | `LAURENT_SETUP\|center a=0\|w=z\|f=(-6 + 3z - 6z^2 - 5z^3 - z^4 - 6z^5)/z^3` | laurent_series_generator.py |
| `LAURENT_TERM` | 1 | `LAURENT_TERM\|-3(z+3)^-1` | residue_generator.py |
| `LAW` | 3 | `LAW\|distributive ∧ over ∨\|t ∧ (¬s ∨ ¬s)\|(t ∧ ¬s) ∨ (t ∧ ¬s)` | logical_equivalence_laws_generator.py, set_algebra_laws_generator.py |
| `LAYERNORM_SETUP` | 3 | `LAYERNORM_SETUP\|x=(-10,0)\|gamma=(3,3)\|beta=(-5,5)` | layer_norm_generator.py |
| `LB` | 2 | `LB\|{32, 53}\|{14, 29, 32}` | partial_order_generator.py |
| `LCM_FROM_GCD` | 3 | `LCM_FROM_GCD\|90*53\|1\|4770` | lcm_generator.py |
| `LCM_STEP` | 3 | `LCM_STEP\|1\|2\|2` | permutation_group_generator.py, pollard_factorization_generator.py |
| `LEADING_MINOR` | 2 | `LEADING_MINOR\|Delta1\|0` | positive_definite_generator.py |
| `LEAST` | 1 | `LEAST\|none` | induction_verify_generator.py, partial_order_generator.py |
| `LEGENDRE_RESULT` | 3 | `LEGENDRE_RESULT\|18\|-1\|quadratic nonresidue` | quadratic_residue_generator.py |
| `LEGENDRE_SETUP` | 2 | `LEGENDRE_SETUP\|a=21\|p=19` | legendre_construction_generator.py, quadratic_residue_generator.py |
| `LEVEL` | 2 | `LEVEL\|t\|50650` | type_theory_generator.py |
| `LIE_EXP_FORM` | 2 | `LIE_EXP_FORM\|e^(theta J)\|cos(theta)I + sin(theta)J` | lie_exponential_generator.py |
| `LIE_EXP_SETUP` | 4 | `LIE_EXP_SETUP\|SO3\|axis=z\|theta=540 deg\|K=[[0, -1, 0], [1, 0, 0], [0, 0, 0]]` | lie_exponential_generator.py |
| `LIKELIHOOD` | 2, 3 | `LIKELIHOOD\|1/2\|even chance` | bayes_multiple_hypotheses_generator.py, likelihood_language_generator.py |
| `LIMITING_REAGENT` | 2 | `LIMITING_REAGENT\|N2\|NH3=10 mol` | stoichiometry_generator.py |
| `LIMIT_CHECK` | 2 | `LIMIT_CHECK\|NH3 from N2=10 mol\|NH3 from H2=58/3 mol` | stoichiometry_generator.py |
| `LIMIT_SETUP` | 1, 2 | `LIMIT_SETUP\|lim x→0 of (√(x + 4) - 2)/x\|0/0: rationalize` | derivative_limit_def_generator.py, improper_integral_generator.py, lhopital_generator.py, limit_evaluation_generator.py, power_series_generator.py, series_convergence_generator.py |
| `LINEARITY` | 1, 2 | `LINEARITY\|E[X] = Σ E[I_j]\|6 × 125/216` | linearity_of_expectation_generator.py |
| `LINEAR_SYSTEM` | 2 | `LINEAR_SYSTEM\|a=1, b=-5/16\|c=-1/7, d=1` | markov_chain_generator.py |
| `LINE_EQ` | 1 | `LINE_EQ\|-4x + 6y + 1 = 0` | complex_locus_generator.py |
| `LINE_INTEGRAL` | 3 | `LINE_INTEGRAL\|int_0^1 dot dt\|-1/2 + 1\|1/2` | line_integral_generator.py |
| `LINE_RELATION_SETUP` | 3 | `LINE_RELATION_SETUP\|perpendicular\|y = -1/2x + 5\|(-6, 1)` | parallel_perpendicular_line_generator.py |
| `LINE_SETUP` | 2 | `LINE_SETUP\|F(x,y) = <4*x - 3*y + 2, 2*y - 3*x - 5>\|from (0, 0) to (1, -2)` | line_integral_generator.py |
| `LIST_MAX` | 2 | `LIST_MAX\|5/16, 61/58, 7/5\|7/5` | dedekind_cut_generator.py |
| `LLL_DONE` | 1 | `LLL_DONE\|[(11,-4),(-4,-13)]` | lll_reduction_generator.py |
| `LLL_SETUP` | 1 | `LLL_SETUP\|[(-4,-13),(11,-4)]` | lll_reduction_generator.py |
| `LOCUS_SETUP` | 3 | `LOCUS_SETUP\|z=x+iy\|center=(2,6)\|radius=1` | complex_locus_generator.py |
| `LOG2` | 2 | `LOG2\|1/8\|-3` | entropy_generator.py, huffman_coding_generator.py, mutual_information_generator.py, von_neumann_entropy_generator.py |
| `LOG2_RATIO` | 3 | `LOG2_RATIO\|i=0\|ratio=1/128\|log=-7` | kl_divergence_generator.py |
| `LOG_BOTH_SIDES` | 1 | `LOG_BOTH_SIDES\|log_7(7^x) = log_7(37)` | exponential_equation_generator.py, log_diff_higher_order_generator.py, separable_ode_generator.py |
| `LOG_EVAL` | 2 | `LOG_EVAL\|21/16\|ln(21/16)` | hyperbolic_distance_generator.py |
| `LOG_EXACT` | 2 | `LOG_EXACT\|log_11(19487171)\|7` | master_theorem_generator.py |
| `LOG_FORM` | 1 | `LOG_FORM\|log_6(1296) = y ⟺ 6^y = 1296` | log_conversion_generator.py, log_equation_generator.py |
| `LOG_FORMULA` | 1 | `LOG_FORMULA\|log z = ln r + i(arg + 2pi*k)` | complex_log_generator.py |
| `LOG_IDENT` | 2 | `LOG_IDENT\|ln(e) = 1\|1` | exponential_equation_generator.py, log_conversion_generator.py |
| `LOG_LIKELIHOOD` | 1 | `LOG_LIKELIHOOD\|ell(lambda)=5*log(lambda)-30*lambda` | mle_generator.py |
| `LOG_ONE_TO_ONE` | 1 | `LOG_ONE_TO_ONE\|2x - 7 = x + 5` | log_equation_generator.py |
| `LOG_POWER` | 2 | `LOG_POWER\|log_10(x^4)\|4log_10(x)` | derivative_transcendental_generator.py, log_diff_higher_order_generator.py, log_properties_generator.py, ph_calculation_generator.py |
| `LOG_PRODUCT` | 1, 2 | `LOG_PRODUCT\|log_10(10x^4)\|log_10(10) + log_10(x^4)` | log_equation_generator.py, log_properties_generator.py, ph_calculation_generator.py |
| `LOG_QUOTIENT` | 2 | `LOG_QUOTIENT\|log_10(10x^4/y)\|log_10(10x^4) - log_10(y)` | log_properties_generator.py |
| `LOG_SETUP` | 1, 2 | `LOG_SETUP\|log_10(10x^4/y)\|expand` | complex_log_generator.py, log_properties_generator.py |
| `LOG_SOFTMAX` | 2 | `LOG_SOFTMAX\|1\|ln(4/13)` | softmax_gradient_generator.py |
| `LOG_SUPPLIED` | 2 | `LOG_SUPPLIED\|log10(1/100)\|-2` | signal_arithmetic_generator.py |
| `LOG_TERM` | 3 | `LOG_TERM\|24\|ln(2)\|24*ln(2)` | entropy_change_generator.py |
| `LOOKUP_SUPPLIED` | 2 | `LOOKUP_SUPPLIED\|e^(-lambda*t)\|8/17` | named_distribution_generator.py |
| `LORA_COUNT` | 2 | `LORA_COUNT\|r*(d_in+d_out)\|63936` | param_count_generator.py |
| `LOWRANK_SETUP` | 2 | `LOWRANK_SETUP\|A=[[17,0], [0,4]]\|rank=1` | low_rank_approx_generator.py |
| `LP_CORNER_SETUP` | 3 | `LP_CORNER_SETUP\|max z=10x+12y\|0<=x<=17, 0<=y<=24\|x+y<=30` | lp_corner_generator.py |
| `LR_PHASE` | 1 | `LR_PHASE\|warmup` | lr_schedule_generator.py |
| `LR_SETUP` | 3 | `LR_SETUP\|base=1/10\|min=0\|warmup=10,total=210,t=1` | lr_schedule_generator.py |
| `LR_VALUE` | 1 | `LR_VALUE\|1/100` | lr_schedule_generator.py |
| `LS_LINE` | 2 | `LS_LINE\|a = 6, b = 1\|ŷ = 6 + x` | least_squares_generator.py |
| `LS_SETUP` | 2 | `LS_SETUP\|points [(-3, 0), (-1, 8), (1, 10), (3, 6)]\|model y = a + bx` | least_squares_generator.py |
| `LUB` | 1 | `LUB\|53` | partial_order_generator.py |
| `LUHN_DIGIT` | 3 | `LUHN_DIGIT\|digit 6\|keep\|6 -> 6` | modular_arithmetic_generator.py |
| `LU_ENTRY` | 3 | `LU_ENTRY\|u11\|a11 = -3\|-3` | lu_decomposition_generator.py |
| `LU_RESULT` | 2 | `LU_RESULT\|L\|[[1, 0, 0], [4, 1, 0], [0, 2, 1]]` | lu_decomposition_generator.py |
| `LU_SETUP` | 2 | `LU_SETUP\|A = [[-3, -4, -1], [-12, -13, -6], [0, 6, -7]]\|unit lower L` | lu_decomposition_generator.py |
| `LZ77_EMIT` | 1 | `LZ77_EMIT\|(0,0,t)` | lz_compression_generator.py |
| `LZ77_EXPAND` | 4 | `LZ77_EXPAND\|(0,0,x)\|no copy\|then add x\|out = x` | lz_compression_generator.py |
| `LZ77_MATCH` | 4 | `LZ77_MATCH\|pos 0\|literal\|offset 0, len 0\|next t` | lz_compression_generator.py |
| `LZ77_SEARCH` | 3 | `LZ77_SEARCH\|pos 1\|start 0\|len 0` | lz_compression_generator.py |
| `LZ78_APPEND` | 2 | `LZ78_APPEND\|empty + t\|out = t` | lz_compression_generator.py |
| `LZ78_DICT` | 2 | `LZ78_DICT\|0\|empty` | lz_compression_generator.py |
| `LZ78_EMIT` | 1 | `LZ78_EMIT\|(0,o)` | lz_compression_generator.py |
| `LZ78_LOOKUP` | 2 | `LZ78_LOOKUP\|index 0\|phrase empty` | lz_compression_generator.py |
| `LZ78_MATCH` | 4 | `LZ78_MATCH\|pos 0\|phrase empty\|index 0\|next o` | lz_compression_generator.py |
| `LZ_SETUP` | 2 | `LZ_SETUP\|LZ78 decode\|(0,t), (0,n), (2,n), (1,n), (3,n), (2,$)` | lz_compression_generator.py |
| `M` | 3 | `M\|6\|99\|594` | ac_circuit_generator.py, activation_generator.py, adam_step_generator.py, angle_defect_generator.py, angle_measure_generator.py, annuity_generator.py, arc_length_generator.py, arc_sector_generator.py, arithmetic_coding_generator.py, arithmetic_sequence_generator.py, attention_generator.py, backprop_generator.py, bayes_multiple_hypotheses_generator.py, bec_channel_generator.py, binomial_probability_generator.py, bisection_generator.py, black_scholes_generator.py, blackbody_generator.py, bond_pricing_generator.py, calorimetry_generator.py, cantor_pairing_generator.py, cardinal_arithmetic_generator.py, casimir_force_generator.py, casimir_generator.py, cayley_table_generator.py, chain_rule_generator.py, channel_capacity_generator.py, christoffel_generator.py, circle_angle_generator.py, classic_probability_puzzles_generator.py, classifier_metrics_generator.py, collision_generator.py, commutator_generator.py, complement_probability_generator.py, complex_locus_generator.py, complex_log_generator.py, composite_arithmetic_generator.py, conditional_expectation_generator.py, conditional_probability_generator.py, confidence_interval_generator.py, conic_standard_form_generator.py, continued_fraction_generator.py, continuous_distribution_generator.py, contour_integral_generator.py, convolution_generator.py, coset_generator.py, countability_bijection_generator.py, counterexample_search_generator.py, counting_classics_generator.py, counting_to_probability_generator.py, covariance_algebra_generator.py, cramers_rule_generator.py, cross_section_generator.py, crt_generator.py, curve_analysis_generator.py, cyclic_group_generator.py, de_moivre_generator.py, decimal_div_generator.py, definite_integral_generator.py, density_matrix_generator.py, derangement_generator.py, derivative_limit_def_generator.py, derivative_power_rule_generator.py, derivative_transcendental_generator.py, determinant_generator.py, dimensional_analysis_generator.py, discrete_uniform_bernoulli_generator.py, distribution_of_sum_generator.py, doppler_generator.py, dot_product_generator.py, einstein_summation_generator.py, electrostatics_generator.py, elliptic_curve_finite_field_generator.py, embedding_similarity_generator.py, energy_conservation_generator.py, entropy_change_generator.py, entropy_generator.py, entropy_rate_markov_generator.py, equilibrium_ice_generator.py, equivalence_relation_generator.py, error_spotting_generator.py, euler_method_generator.py, evaluate_expression_generator.py, expectation_of_function_generator.py, expected_value_generator.py, experimental_probability_generator.py, exponential_model_generator.py, extended_euclid_generator.py, factor_special_forms_generator.py, feature_map_generator.py, fermi_estimation_generator.py, fill_in_step_generator.py, finance_generator.py, finite_difference_generator.py, finite_field_generator.py, first_law_generator.py, five_number_summary_generator.py, fixed_point_generator.py, flops_memory_generator.py, four_vector_generator.py, fourier_series_generator.py, fractal_iteration_generator.py, fraction_op_generator.py, function_composition_generator.py, function_evaluation_generator.py, function_operations_generator.py, function_properties_generator.py, function_table_generator.py, fundamental_form_generator.py, game_theory_generator.py, gas_law_generator.py, gas_stoichiometry_generator.py, gauss_bonnet_generator.py, gauss_law_generator.py, gaussian_curvature_generator.py, generating_function_generator.py, geometric_distribution_generator.py, geometric_mean_generator.py, geometric_sequence_generator.py, geometry_area_perimeter_generator.py, godel_numbering_generator.py, gradient_descent_generator.py, gradient_step_generator.py, graph_counting_generator.py, graph_interpret_generator.py, grassmann_generator.py, great_circle_generator.py, hamiltonian_generator.py, hawking_generator.py, hermitian_check_generator.py, horner_evaluation_generator.py, huffman_coding_generator.py, hydrogen_atom_generator.py, hypercube_counting_generator.py, hypergeometric_generator.py, hypothesis_test_generator.py, independence_check_generator.py, index_gymnastics_generator.py, index_raising_generator.py, information_gain_generator.py, integers_as_pairs_generator.py, interference_generator.py, interpolation_generator.py, invariant_mass_generator.py, joint_distribution_generator.py, kernel_evaluation_generator.py, kernel_perceptron_generator.py, kernel_ridge_generator.py, kernel_validity_generator.py, kinematics_generator.py, kl_divergence_generator.py, ladder_operator_generator.py, lagrangian_generator.py, laplace_ivp_generator.py, laurent_series_generator.py, law_of_total_probability_generator.py, layer_norm_generator.py, lcm_generator.py, legendre_construction_generator.py, lhopital_generator.py, limit_evaluation_generator.py, linear_approx_generator.py, linearity_of_expectation_generator.py, log_conversion_generator.py, log_diff_higher_order_generator.py, logistic_growth_generator.py, long_division_generator.py, lp_corner_generator.py, lr_schedule_generator.py, magnetism_generator.py, markov_chain_generator.py, matrix_calculus_generator.py, matrix_group_check_generator.py, matrix_inverse_generator.py, matrix_ops_generator.py, mean_value_theorem_generator.py, method_of_moments_generator.py, metric_arc_length_generator.py, mgf_generator.py, midpoint_generator.py, mixed_number_operation_generator.py, mobius_transform_generator.py, mod_exp_generator.py, modular_inverse_generator.py, multi_step_unit_conversion_generator.py, mutual_information_generator.py, naive_bayes_generator.py, named_distribution_generator.py, natural_units_generator.py, nets_surface_area_generator.py, newton_raphson_generator.py, newtons_laws_generator.py, normal_approx_binomial_generator.py, normal_table_generator.py, npv_irr_generator.py, ode_system_generator.py, operation_properties_generator.py, optics_generator.py, optimization_generator.py, or_formula_generator.py, orbital_mechanics_generator.py, order_of_operations_generator.py, order_statistics_generator.py, ordinal_arithmetic_generator.py, param_count_generator.py, parametric_calculus_generator.py, particle_in_box_generator.py, partition_function_generator.py, pca_generator.py, percent_problem_generator.py, percent_word_problem_generator.py, perceptron_generator.py, permutation_combination_generator.py, physics_formula_generator.py, piecewise_evaluation_generator.py, planck_units_generator.py, polar_parametric_generator.py, polynomial_zeros_generator.py, portfolio_generator.py, positive_definite_generator.py, primality_test_generator.py, projectile_motion_generator.py, proportion_word_problem_generator.py, proportional_relationship_generator.py, quadratic_residue_generator.py, quantization_generator.py, quantum_formula_generator.py, quark_composition_generator.py, quaternion_generator.py, radical_multiply_generator.py, radical_rationalize_generator.py, rate_conversion_generator.py, ratio_table_generator.py, rational_equation_generator.py, rational_exponent_generator.py, rationals_as_pairs_generator.py, recurrence_generator.py, recursive_definition_unfold_generator.py, recursive_explicit_generator.py, reed_solomon_generator.py, regression_generator.py, regular_polygon_area_generator.py, related_rates_generator.py, relativistic_energy_generator.py, reliability_system_generator.py, remainder_factor_theorem_generator.py, riemann_sum_generator.py, riemann_tensor_generator.py, right_triangle_trig_generator.py, rotational_dynamics_generator.py, round_solids_generator.py, routh_hurwitz_generator.py, row_reduction_generator.py, rsa_generator.py, runge_kutta_generator.py, running_coupling_generator.py, rv_transform_generator.py, scaling_law_generator.py, schwarzschild_generator.py, second_order_ode_generator.py, segment_partition_generator.py, separable_pde_generator.py, series_solution_generator.py, set_builder_roster_generator.py, set_counting_generator.py, set_operations_generator.py, shm_generator.py, signal_arithmetic_generator.py, similar_triangles_generator.py, simplex_generator.py, solid_revolution_generator.py, solution_chem_generator.py, special_relativity_generator.py, special_right_triangle_generator.py, spherical_excess_generator.py, spherical_triangle_generator.py, standing_wave_generator.py, stars_and_bars_generator.py, statics_generator.py, stereographic_generator.py, stoichiometry_generator.py, svm_margin_generator.py, synthetic_division_generator.py, tangent_line_generator.py, taxicab_geometry_generator.py, taylor_series_generator.py, temperature_conversion_generator.py, tensor_product_generator.py, tip_bill_split_generator.py, totient_generator.py, transfer_function_generator.py, transformation_generator.py, transient_circuit_generator.py, transportation_generator.py, triangle_area_sas_generator.py, triangle_solve_generator.py, trig_identity_eval_generator.py, two_sample_test_generator.py, uncertainty_generator.py, undetermined_coeff_generator.py, unit_circle_generator.py, unit_conversion_generator.py, vector_ops_generator.py, volume_rect_prism_generator.py, von_neumann_entropy_generator.py, wavefunction_generator.py, young_tableaux_generator.py, z_score_generator.py, z_transform_generator.py |
| `MAG_FORMULA` | 1 | `MAG_FORMULA\|magnitude = √(x^2 + y^2)` | magnetism_generator.py, vector_ops_generator.py |
| `MAG_SETUP` | 3 | `MAG_SETUP\|force\|q=9, v=30\|B=4, sin=4/5` | magnetism_generator.py |
| `MAIN_CONNECTIVE` | 1 | `MAIN_CONNECTIVE\|¬` | wff_parsing_generator.py |
| `MAP` | 2 | `MAP\|c\|f(c) = n` | function_properties_generator.py |
| `MARGIN` | 2 | `MARGIN\|2/norm(w)\|2/17` | svm_margin_generator.py |
| `MARGINAL` | 1, 3 | `MARGINAL\|P(Y=1)\|3/128 + 103/128\|53/64` | conditional_expectation_generator.py, joint_distribution_generator.py, mutual_information_generator.py |
| `MARKOV_SETUP` | 2, 3 | `MARKOV_SETUP\|two_state\|P00=1/5, P01=4/5\|P10=2/7, P11=5/7` | entropy_rate_markov_generator.py, markov_chain_generator.py |
| `MASTER_CASE` | 2 | `MASTER_CASE\|case 3\|Θ(n^7)` | master_theorem_generator.py |
| `MATMUL_FLOPS` | 2 | `MATMUL_FLOPS\|XW1\|67108864` | flops_memory_generator.py |
| `MATRIX_ADD` | 2 | `MATRIX_ADD\|P0+P1\|[[1,0],[0,1]]` | bch_generator.py, casimir_generator.py, projector_generator.py |
| `MATRIX_ENTRY` | 1 | `MATRIX_ENTRY\|P2_01=P00*P01 + P01*P11` | markov_chain_generator.py |
| `MATRIX_ENTRY_SUM` | 3 | `MATRIX_ENTRY_SUM\|(4,1)\|0 + 0\|0` | gamma_matrix_generator.py |
| `MATRIX_EXP` | 3 | `MATRIX_EXP\|e^A\|I + A\|[[1, 0, 0], [0, 1, 1], [0, 0, 1]]` | bch_generator.py |
| `MATRIX_GROUP_SETUP` | 2 | `MATRIX_GROUP_SETUP\|O2\|M=[[-4/5,-3/5],[3/5,-4/5]]` | matrix_group_check_generator.py |
| `MATRIX_MULT` | 2, 3 | `MATRIX_MULT\|row1 dot col1\|361/32761*361/32761+3420/32761*3420/32761\|361/32761` | projector_generator.py |
| `MATRIX_POWER` | 2 | `MATRIX_POWER\|K^2\|[[-1, 0, 0], [0, -1, 0], [0, 0, 0]]` | lie_exponential_generator.py |
| `MATRIX_PRODUCT` | 2 | `MATRIX_PRODUCT\|AB\|[[0, 35i], [35i, 0]]` | bch_generator.py, casimir_generator.py, gamma_matrix_generator.py, pauli_algebra_generator.py, structure_constant_generator.py |
| `MATRIX_ROW` | 2 | `MATRIX_ROW\|f\|0 1` | graph_counting_generator.py, relation_operations_generator.py |
| `MATRIX_SCALE` | 2 | `MATRIX_SCALE\|1/2 ladder sum\|[[8/121, 0], [0, 8/121]]` | bch_generator.py, casimir_generator.py |
| `MATRIX_SETUP` | 2 | `MATRIX_SETUP\|hermitian\|A=[[-13,-6],[-6,-13]]` | hermitian_check_generator.py |
| `MATRIX_SUB` | 2 | `MATRIX_SUB\|AB - BA\|[[0, 0, 0], [1, 0, 0], [0, 0, 0]]` | bch_generator.py |
| `MATRIX_SUM` | 1 | `MATRIX_SUM\|B=A+A^T` | matrix_calculus_generator.py |
| `MATRIX_VALUE` | 2 | `MATRIX_VALUE\|A\|[[-7/2, 0], [0, 7/2]]` | pauli_algebra_generator.py, structure_constant_generator.py |
| `MAT_ENTRY` | 2, 3 | `MAT_ENTRY\|(1,1)\|5` | lie_exponential_generator.py, matrix_calculus_generator.py, matrix_ops_generator.py |
| `MAT_SETUP` | 2 | `MAT_SETUP\|A = [[5, 2], [-3, 5]], B = [[1, 5], [0, -1]]\|AB` | determinant_generator.py, diagonalization_generator.py, eigenvalue_generator.py, matrix_exponential_generator.py, matrix_inverse_generator.py, matrix_ops_generator.py, row_reduction_generator.py, subspace_basis_generator.py, svd_generator.py |
| `MAX` | 2, 3 | `MAX\|3, 5\|5` | dp_table_generator.py, matrix_norm_generator.py, taxicab_geometry_generator.py |
| `MAXIMAL` | 1 | `MAXIMAL\|{5, 36, 42, 51}` | partial_order_generator.py |
| `MAXTERM` | 2 | `MAXTERM\|010\|R OR NOT S OR T` | boolean_algebra_generator.py |
| `MC_SETUP` | 3 | `MC_SETUP\|expression=x^T A x\|A=[[-2,4], [-1,-1]]\|x=(5,-1)` | matrix_calculus_generator.py |
| `MEAN` | 1 | `MEAN\|-5` | layer_norm_generator.py |
| `MEAN_DIV` | 3 | `MEAN_DIV\|63\|9\|7` | composite_arithmetic_generator.py, five_number_summary_generator.py, regression_generator.py, simple_stats_generator.py, standard_deviation_generator.py |
| `MEASURE` | 3 | `MEASURE\|B\|{d, e, f}\|71/153` | probability_measure_generator.py |
| `MEASURE_BASIS` | 3 | `MEASURE_BASIS\|x\|ket+x=(ket0+ket1)/sqrt(2)\|ket-x=(ket0-ket1)/sqrt(2)` | spin_half_generator.py |
| `MEASURE_FAVORABLE` | 2 | `MEASURE_FAVORABLE\|interval length\|31 - 13 = 18` | geometric_probability_generator.py |
| `MEASURE_PROB` | 3 | `MEASURE_PROB\|computational basis\|P(0)=1/2\|P(1)=1/2` | quantum_gate_generator.py |
| `MEASURE_TOTAL` | 2 | `MEASURE_TOTAL\|total length\|59` | geometric_probability_generator.py |
| `MEDIAN_PAIR` | 2 | `MEDIAN_PAIR\|7\|8` | five_number_summary_generator.py, simple_stats_generator.py |
| `MEDIAN_PICK` | 1, 2 | `MEDIAN_PICK\|9` | five_number_summary_generator.py, simple_stats_generator.py |
| `MEMBER` | 1 | `MEMBER\|3/16 ∈ L(5/8)` | dedekind_cut_generator.py |
| `MEMBERSHIP_BAD` | 2 | `MEMBERSHIP_BAD\|need 6249\|got 6251` | type_theory_generator.py |
| `MEMBERSHIP_OK` | 1 | `MEMBERSHIP_OK\|type(x) = type(a) + 1` | type_theory_generator.py |
| `MEMBER_ROW` | 1, 3 | `MEMBER_ROW\|x∈C, x∈M, x∈V` | foundations_critic_generator.py, set_identity_membership_table_generator.py |
| `MEMORY_SETUP` | 3 | `MEMORY_SETUP\|kv_cache\|L=24,h=12,d_k=80\|seq=1024,precision_bytes=2` | flops_memory_generator.py |
| `MEMORY_UNIT` | 2 | `MEMORY_UNIT\|MiB\|90` | flops_memory_generator.py |
| `MERGE_BEGIN` | 3 | `MERGE_BEGIN\|merge 1\|lo=1,mid=2,hi=3\|left 34; right 42` | algorithm_trace_generator.py |
| `MERGE_COMPARE` | 3 | `MERGE_COMPARE\|34\|42\|take left` | algorithm_trace_generator.py |
| `MERGE_DONE` | 3 | `MERGE_DONE\|merge 1\|range 1-2\|array 2, 34, 42, 44, 38, 47` | algorithm_trace_generator.py |
| `MERGE_TAKE` | 2 | `MERGE_TAKE\|34\|merged 34` | algorithm_trace_generator.py |
| `METRIC` | 2 | `METRIC\|taxicab circle\|all points with abs(x) + abs(y) = 11` | taxicab_geometry_generator.py |
| `METRICS_SETUP` | 1 | `METRICS_SETUP\|TP=29, FP=6, FN=10, TN=13` | classifier_metrics_generator.py |
| `METRIC_ARC_SETUP` | 3 | `METRIC_ARC_SETUP\|polar metric\|ds^2=dr^2+r^2 dtheta^2\|theta=120 deg, r:19->45` | metric_arc_length_generator.py |
| `METRIC_FORMULA` | 1 | `METRIC_FORMULA\|precision=TP/(TP+FP)` | classifier_metrics_generator.py |
| `METRIC_RESTRICT` | 2 | `METRIC_RESTRICT\|dtheta=0\|ds^2=dr^2` | metric_arc_length_generator.py |
| `MGF_SETUP` | 3 | `MGF_SETUP\|P(X=0)=8/17\|P(X=1)=6/17\|P(X=2)=3/17` | mgf_generator.py |
| `MGF_TERM` | 3 | `MGF_TERM\|x=0\|p0*e^(0t)\|8/17` | mgf_generator.py |
| `MIDDLE_EVAL` | 3 | `MIDDLE_EVAL\|r=0..8\|8^2/2\|32` | triple_integral_generator.py |
| `MIDLINE` | 1 | `MIDLINE\|y = 3` | sinusoid_features_generator.py |
| `MIDPOINT` | 2 | `MIDPOINT\|iter 1\|2` | algorithm_trace_generator.py |
| `MID_FORMULA` | 1 | `MID_FORMULA\|M = ((x1 + x2)/2, (y1 + y2)/2)` | circle_equation_generator.py, midpoint_generator.py |
| `MIN` | 2 | `MIN\|36,16\|16` | matrix_norm_generator.py |
| `MIN3` | 4 | `MIN3\|2\|2\|1\|1` | dp_table_generator.py |
| `MINIMAL` | 1 | `MINIMAL\|{5, 28, 32}` | partial_order_generator.py |
| `MINKOWSKI_FORMULA` | 1 | `MINKOWSKI_FORMULA\|s2=ct^2-x^2` | minkowski_interval_generator.py |
| `MINKOWSKI_SETUP` | 3 | `MINKOWSKI_SETUP\|interval_classification\|ct=-12\|x=-9` | minkowski_interval_generator.py |
| `MINTERM` | 2 | `MINTERM\|000\|NOT P AND NOT Q AND NOT R` | boolean_algebra_generator.py |
| `MIN_INITIAL` | 3 | `MIN_INITIAL\|nonaccept A, B\|accept C\|{A,B}, {C}` | dfa_minimization_generator.py |
| `MIN_REFINE` | 2 | `MIN_REFINE\|round 1\|{A}, {B}, {C}` | dfa_minimization_generator.py |
| `MIN_SIGNATURE` | 3 | `MIN_SIGNATURE\|round 1\|A\|0->B0,1->B0` | dfa_minimization_generator.py |
| `MIN_STABLE` | 1 | `MIN_STABLE\|{A}, {B}, {C}` | dfa_minimization_generator.py |
| `MIN_TRANSITION` | 3 | `MIN_TRANSITION\|{A}\|0\|{A}` | dfa_minimization_generator.py |
| `MISSED` | 1 | `MISSED\|3` | function_properties_generator.py |
| `MIX_FORMULA` | 2 | `MIX_FORMULA\|q=(d-b)/(a-b-c+d)\|p=(d-c)/(a-b-c+d)` | game_theory_generator.py |
| `MIX_IMPROPER` | 2 | `MIX_IMPROPER\|2 2/7\|16/7` | composite_arithmetic_generator.py, mixed_number_operation_generator.py, order_of_operations_generator.py |
| `MI_FORMULA` | 1 | `MI_FORMULA\|I=H(X)+H(Y)-H(X,Y)` | mutual_information_generator.py |
| `MI_SETUP` | 2 | `MI_SETUP\|rows=[[0,1/4,1/4,0];[1/4,0,0,1/4]]\|task=I(X;Y)` | mutual_information_generator.py |
| `MLE_SETUP` | 2, 3 | `MLE_SETUP\|exponential\|parameter=lambda\|data=[10,3,9,4,4]` | mle_generator.py |
| `MOBIUS_SETUP` | 2 | `MOBIUS_SETUP\|T(z)=(30)/(3z + 9)\|fixed points` | mobius_transform_generator.py |
| `MODE` | 2 | `MODE\|2\|10, 13` | frequency_table_generator.py, simple_stats_generator.py |
| `MODEL` | 1 | `MODEL\|A = P · (1/2)^(t/h)` | exponential_model_generator.py |
| `MODEL_APPLY` | 1 | `MODEL_APPLY\|A = 296 · (1/2)^(360/120)` | exponential_model_generator.py |
| `MODEL_OUTPUT` | 1 | `MODEL_OUTPUT\|-29` | activation_generator.py |
| `MODEXP_MULTIPLY` | 2 | `MODEXP_MULTIPLY\|bit 1=1\|34` | mod_exp_generator.py, quadratic_residue_generator.py |
| `MODEXP_SETUP` | 3 | `MODEXP_SETUP\|base 34\|exponent 14\|modulus 47` | mod_exp_generator.py |
| `MODEXP_SQUARE` | 2 | `MODEXP_SQUARE\|bit 1=1\|1` | mod_exp_generator.py, quadratic_residue_generator.py |
| `MODEXP_STATE` | 2 | `MODEXP_STATE\|after bit 1\|34` | mod_exp_generator.py, quadratic_residue_generator.py |
| `MODE_COUNT` | 2 | `MODE_COUNT\|1\|1` | simple_stats_generator.py |
| `MOD_INVERSE` | 2 | `MOD_INVERSE\|58 mod 39\|37` | crt_generator.py, ecdsa_generator.py, elliptic_curve_finite_field_generator.py, modular_inverse_generator.py, rsa_generator.py |
| `MOD_NORMALIZE` | 3 | `MOD_NORMALIZE\|-2\|mod 39\|37` | modular_inverse_generator.py, rsa_generator.py |
| `MOD_POWER` | 3 | `MOD_POWER\|14^12\|mod 45\|1` | diffie_hellman_generator.py, pollard_factorization_generator.py, primality_test_generator.py, rsa_generator.py, tonelli_shanks_generator.py, totient_generator.py |
| `MOD_REDUCE` | 3 | `MOD_REDUCE\|32\|mod 10\|2` | calendar_arithmetic_generator.py, cayley_table_generator.py, coset_generator.py, crt_generator.py, cyclic_group_generator.py, de_moivre_generator.py, elliptic_curve_finite_field_generator.py, finite_field_generator.py, jacobi_symbol_generator.py, lie_exponential_generator.py, mod_exp_generator.py, modular_arithmetic_generator.py, modular_inverse_generator.py, primality_test_generator.py, quadratic_residue_generator.py, reed_solomon_generator.py, rsa_generator.py, totient_generator.py |
| `MOD_SETUP` | 2, 3, 4 | `MOD_SETUP\|Luhn modulus 10\|prefix 65236213` | modular_arithmetic_generator.py, modular_inverse_generator.py |
| `MOD_SOLVE` | 2 | `MOD_SOLVE\|d ≡ -2 mod 10\|8` | modular_arithmetic_generator.py |
| `MOD_TERM` | 2 | `MOD_TERM\|10 * 1\|10` | modular_arithmetic_generator.py |
| `MOE_FORMULA` | 1 | `MOE_FORMULA\|E = z*·σ/√n` | confidence_interval_generator.py |
| `MOLAR_MASS` | 2 | `MOLAR_MASS\|KClO3\|122 g/mol` | gas_stoichiometry_generator.py, stoichiometry_generator.py |
| `MOLAR_VOLUME` | 2 | `MOLAR_VOLUME\|1 mol gas\|24 L` | stoichiometry_generator.py |
| `MOMENT` | 2 | `MOMENT\|m1\|-3/10` | adam_step_generator.py |
| `MOMENTUM` | 1 | `MOMENTUM\|p1=m1*u1` | collision_generator.py |
| `MOMENT_TERM` | 3 | `MOMENT_TERM\|E[X]\|x=0, y=0\|0` | covariance_algebra_generator.py |
| `MOMENT_X` | 3 | `MOMENT_X\|M_x = 1/2 int y^2 dx\|2^5/10\|16/5` | centroid_generator.py |
| `MOMENT_Y` | 3 | `MOMENT_Y\|M_y = int x*y dx\|2^4/4\|4` | centroid_generator.py |
| `MOM_EQUATION` | 2 | `MOM_EQUATION\|E[X]=theta/2\|xbar=theta/2` | method_of_moments_generator.py |
| `MOM_SETUP` | 3 | `MOM_SETUP\|uniform_zero_theta\|parameter=theta\|data=[3,20,19,17]` | method_of_moments_generator.py |
| `MONO_ADD_EXP` | 2 | `MONO_ADD_EXP\|x^6 * x^2 = x^(6+2)\|x^8` | monomial_mult_div_generator.py |
| `MONO_DIV_COEFF` | 2 | `MONO_DIV_COEFF\|-30 / -5\|6` | monomial_mult_div_generator.py |
| `MONO_MULT_COEFF` | 2 | `MONO_MULT_COEFF\|-3 * -8\|24` | monomial_mult_div_generator.py |
| `MONO_SETUP` | 1 | `MONO_SETUP\|(-3x^6)(-8x^2)` | monomial_mult_div_generator.py |
| `MONO_SUB_EXP` | 2 | `MONO_SUB_EXP\|x^6 / x^3 = x^(6-3)\|x^3` | monomial_mult_div_generator.py |
| `MONTY_SETUP` | 2 | `MONTY_SETUP\|doors=5, opened=2, pick=4\|host never opens the prize door` | classic_probability_puzzles_generator.py |
| `MOOD` | 2 | `MOOD\|AOA\|figure 1` | syllogism_generator.py |
| `MOVE_TERM` | 2, 3 | `MOVE_TERM\|-2x\|left\|5x+4+2x = -7` | area_between_curves_generator.py, completing_square_generator.py, conic_standard_form_generator.py, linear_complex_generator.py, polar_parametric_generator.py, quadratic_factoring_generator.py, quadratic_square_root_generator.py, radical_equation_generator.py, special_solution_equation_generator.py, standard_form_conversion_generator.py |
| `MP` | 2 | `MP\|lines 1,2\|(n → k) → ((b ∨ g) → ((b → h) → (b ∨ g)))` | hilbert_axiom_derivation_generator.py |
| `MR_DECOMPOSE` | 2 | `MR_DECOMPOSE\|52\|2^2 * 13` | primality_test_generator.py |
| `MR_SETUP` | 2 | `MR_SETUP\|n=53\|witnesses 2, 9` | primality_test_generator.py |
| `MR_SQUARE` | 2 | `MR_SQUARE\|r=1\|52` | primality_test_generator.py |
| `MR_WITNESS` | 1 | `MR_WITNESS\|2` | primality_test_generator.py |
| `MR_WITNESS_RESULT` | 2 | `MR_WITNESS_RESULT\|2\|passes at r=1` | primality_test_generator.py |
| `MSE_FORMULA` | 2 | `MSE_FORMULA\|L=(1/n) sum r_i^2\|grad=(2/n) sum r_i*[1,x_i]` | gradient_step_generator.py |
| `MSE_GRADIENT` | 2 | `MSE_GRADIENT\|g0=6\|g1=-12` | gradient_step_generator.py |
| `MSE_SAMPLE` | 3 | `MSE_SAMPLE\|i=1\|pred=6\|r=4` | gradient_step_generator.py |
| `MSE_SETUP` | 3 | `MSE_SETUP\|model y_hat=w0+w1*x\|samples=[(-3,2), (0,-2)]\|w=(0,-2), eta=1/3` | gradient_step_generator.py |
| `MST_ADD` | 2 | `MST_ADD\|AC\|total 1` | mst_generator.py |
| `MST_SET` | 1 | `MST_SET\|AC` | mst_generator.py |
| `MST_SETUP` | 2 | `MST_SETUP\|weighted undirected graph\|vertices A, B, C, D` | mst_generator.py |
| `MU` | 2 | `MU\|8/185\|round=0` | lll_reduction_generator.py |
| `MULTIPLY_IF` | 2 | `MULTIPLY_IF\|e^(4x)y' + 4e^(4x)y\|12e^(4x)` | integrating_factor_generator.py, ode_substitution_generator.py |
| `MULTIVALUED_LOG` | 2 | `MULTIVALUED_LOG\|ln(146) + i*(19pi/180 + 2pi*k)\|k in Z` | complex_log_generator.py |
| `MULTI_FORMULA` | 2 | `MULTI_FORMULA\|n!/(a!b!c!...)\|8! / repeats` | stars_and_bars_generator.py |
| `MULTI_SETUP` | 2 | `MULTI_SETUP\|3 F's, 1 T, 4 X's\|total 8` | stars_and_bars_generator.py |
| `MUL_PARTIAL` | 3 | `MUL_PARTIAL\|6\|68395\|410370` | decimal_mult_generator.py, multi_digit_multiplication_generator.py |
| `MUL_SETUP` | 2 | `MUL_SETUP\|68395\|1956` | decimal_mult_generator.py, multi_digit_multiplication_generator.py |
| `MUL_TERM` | 3 | `MUL_TERM\|10\|-9.6x\|-96x` | linear_fractional_generator.py, polynomial_long_division_generator.py, rational_equation_generator.py |
| `MVT_SETUP` | 2 | `MVT_SETUP\|f(x) = x^2 - 3x + 5 on [-1, 1]\|find the c guaranteed by the MVT` | mean_value_theorem_generator.py |
| `MV_CHAIN_SETUP` | 3 | `MV_CHAIN_SETUP\|z = f(x,y) = 5*x^2 + 4*y^2 - 2*x*y + 2*x - 4*y\|x = 3*s + 2*t + 5, y = -2*s - 3*t\|(s,t) = (0, 3)` | multivar_chain_rule_generator.py |
| `NATURAL_SETUP` | 3 | `NATURAL_SETUP\|length\|hbar=1,c=1\|L=1/2 keV^-1` | natural_units_generator.py |
| `NB_FEATURE_COUNT` | 3 | `NB_FEATURE_COUNT\|Spam\|known=0\|count=3` | naive_bayes_generator.py |
| `NB_LIKELIHOOD` | 3 | `NB_LIKELIHOOD\|Spam\|known=0\|4/15` | naive_bayes_generator.py |
| `NB_PRIOR` | 2 | `NB_PRIOR\|Spam\|13/29` | naive_bayes_generator.py |
| `NB_SCORE` | 2 | `NB_SCORE\|Spam\|start=13/29` | naive_bayes_generator.py |
| `NB_SETUP` | 3 | `NB_SETUP\|query=known=0, money=0\|alpha=1\|classes=Spam,Ham` | naive_bayes_generator.py |
| `NCR` | 2 | `NCR\|C(4, 1)\|4` | binomial_probability_generator.py, classic_probability_puzzles_generator.py, derangement_generator.py, distribution_of_sum_generator.py, generating_function_generator.py, hypercube_counting_generator.py, hypergeometric_generator.py, linearity_of_expectation_generator.py |
| `NEAREST` | 2 | `NEAREST\|queen\|(-3,-1)` | embedding_similarity_generator.py |
| `NEED` | 2 | `NEED\|the equation is 5x + 2 = -43\|line 3 shows 5x = -45` | fill_in_step_generator.py |
| `NEGATE` | 2 | `NEGATE\|995\|-995` | countability_bijection_generator.py |
| `NEG_CONNECTIVE` | 2 | `NEG_CONNECTIVE\|¬¬C(y)\|C(y)` | prenex_normal_form_generator.py, quantifier_negation_generator.py |
| `NEG_LOG` | 2 | `NEG_LOG\|p=1/256\|ln(256)` | perplexity_generator.py |
| `NEG_QUANT` | 2 | `NEG_QUANT\|¬∀y\|∃y ¬` | prenex_normal_form_generator.py, quantifier_negation_generator.py |
| `NEST` | 2 | `NEST\|{a}\|{{∅, {∅, {∅}, {{∅}}}, {{{∅}}}, {{∅}, {∅, {∅}}, {{∅}}, {{{∅}}}}, {{∅}, {{{∅}}}}}}` | hereditarily_finite_set_generator.py |
| `NET_SETUP` | 2 | `NET_SETUP\|2 right triangles with legs 9 and 12; rectangles 9 by 8, 12 by 8, and 15 by 8\|total surface area` | nets_surface_area_generator.py |
| `NEWTON_DD` | 2 | `NEWTON_DD\|f[x0,x1]\|-11` | interpolation_generator.py |
| `NEWTON_SETUP` | 2, 3 | `NEWTON_SETUP\|f(x)=x^2-42\|f'(x)=2x\|x0=6,iterations=3` | newton_raphson_generator.py, newtons_laws_generator.py |
| `NEWTON_STEP` | 2 | `NEWTON_STEP\|1\|1/5` | npv_irr_generator.py |
| `NEWTON_UPDATE` | 3 | `NEWTON_UPDATE\|1\|x_0=6\|x_1=13/2` | newton_raphson_generator.py |
| `NEW_SLOPE` | 2 | `NEW_SLOPE\|New slope (m2) = 2\|Perpendicular lines have negative reciprocal slopes` | parallel_perpendicular_line_generator.py |
| `NEW_STRING` | 1 | `NEW_STRING\|0110101` | cantor_diagonal_generator.py |
| `NFA_ACCEPT` | 1 | `NFA_ACCEPT\|u6` | nfa_simulation_generator.py |
| `NFA_ACTIVE` | 2 | `NFA_ACTIVE\|start\|{u0}` | nfa_simulation_generator.py |
| `NFA_EPSILON` | 2 | `NFA_EPSILON\|q0\|{q2}` | nfa_simulation_generator.py |
| `NFA_INPUT` | 1 | `NFA_INPUT\|ccabab` | nfa_simulation_generator.py |
| `NFA_MOVE` | 4 | `NFA_MOVE\|{u0}\|c\|u0->{u0}\|{u0}` | nfa_simulation_generator.py |
| `NFA_READ` | 2 | `NFA_READ\|pos 1\|c` | nfa_simulation_generator.py |
| `NFA_SETUP` | 3 | `NFA_SETUP\|states u0, u1, u6\|alphabet a, b, c\|start u0` | nfa_simulation_generator.py |
| `NFA_TRANSITION` | 3 | `NFA_TRANSITION\|u0\|a\|{u0,u1}` | nfa_simulation_generator.py |
| `NILPOTENT` | 3 | `NILPOTENT\|theta^2=0\|32theta^2\|0` | grassmann_generator.py |
| `NLL` | 2 | `NLL\|177 tokens\|177*ln(256)` | perplexity_generator.py |
| `NORM2` | 2 | `NORM2\|b1\|185` | lll_reduction_generator.py |
| `NORMALIZE` | 2 | `NORMALIZE\|1\|1` | clebsch_gordan_generator.py, layer_norm_generator.py |
| `NORMALIZE_SIGN` | 2 | `NORMALIZE_SIGN\|(-2,8)\|(2,-8)` | lll_reduction_generator.py |
| `NORMAL_EQ` | 2 | `NORMAL_EQ\|X^T X\|[[4, 0], [0, 20]]` | least_squares_generator.py |
| `NORMAL_SLOPE` | 2 | `NORMAL_SLOPE\|-1/(-3)\|1/3` | tangent_line_generator.py |
| `NORMAL_SYMMETRY` | 2 | `NORMAL_SYMMETRY\|N_neg_d1=0.2\|N_neg_d2=0.25` | black_scholes_generator.py |
| `NORM_CHECK` | 2 | `NORM_CHECK\|P(+x)+P(-x)\|1` | spin_half_generator.py |
| `NORM_SETUP` | 2 | `NORM_SETUP\|X ~ N(68, 4)\|raw value for z = -1.25` | matrix_norm_generator.py, normal_table_generator.py, z_score_generator.py |
| `NORM_SQUARED` | 2 | `NORM_SQUARED\|p\|13` | quaternion_generator.py |
| `NO_COLLISION` | 1 | `NO_COLLISION\|all outputs distinct` | function_properties_generator.py |
| `NO_MISSED` | 1 | `NO_MISSED\|all codomain values hit` | function_properties_generator.py |
| `NO_REDEX` | 2 | `NO_REDEX\|lambda z. (lambda z. (z p))\|no beta redex remains` | lambda_reduction_generator.py |
| `NO_WITNESS` | 2, 3 | `NO_WITNESS\|x=33\|tried y in {3, 7, 8, 24, 33, 35}` | peano_arithmetic_generator.py, quantifier_finite_domain_generator.py |
| `NPV_SETUP` | 2 | `NPV_SETUP\|c0=-500,c1=200,c2=1650,c3=650\|rate=25%` | npv_irr_generator.py |
| `NPV_TERM` | 2 | `NPV_TERM\|t=0\|-500` | npv_irr_generator.py |
| `NULL_REL` | 2 | `NULL_REL\|x1 + x3 + 4*x4 = 0\|x1 = -x3 - 4*x4` | subspace_basis_generator.py |
| `NULL_VECTOR` | 2 | `NULL_VECTOR\|x3=1, x4=0\|[-1, -3, 1, 0]` | subspace_basis_generator.py |
| `NUMBER_OPERATOR` | 2 | `NUMBER_OPERATOR\|N ket12\|12 ket12` | ladder_operator_generator.py |
| `NW_ALLOC` | 1, 3 | `NW_ALLOC\|cell x11\|min(34,20)\|20` | transportation_generator.py |
| `NYQUIST` | 1 | `NYQUIST\|required rate = 2*f_max` | signal_arithmetic_generator.py |
| `OBJECTIVE` | 1 | `OBJECTIVE\|at (0,0)` | lp_corner_generator.py |
| `OCCURS_CHECK` | 3 | `OCCURS_CHECK\|X\|f(X)\|fail` | unification_generator.py |
| `ODDS` | 2 | `ODDS\|for complement\|1:102` | bayes_multiple_hypotheses_generator.py, odds_probability_generator.py |
| `ODDS_FORMULA` | 1 | `ODDS_FORMULA\|odds for Aᶜ = P(Aᶜ) : P(A)` | odds_probability_generator.py |
| `ODDS_REDUCE` | 2 | `ODDS_REDUCE\|856:174\|428:87` | odds_probability_generator.py |
| `ODD_VERTICES` | 2 | `ODD_VERTICES\|none\|0` | euler_circuit_generator.py |
| `ODE_SETUP` | 2, 3 | `ODE_SETUP\|dy/dt = ky; y doubles every 14 hours\|find k exactly` | euler_method_generator.py, exact_ode_generator.py, integrating_factor_generator.py, laplace_ivp_generator.py, logistic_growth_generator.py, ode_substitution_generator.py, ode_system_generator.py, runge_kutta_generator.py, second_order_ode_generator.py, separable_ode_generator.py, series_solution_generator.py, stability_generator.py, undetermined_coeff_generator.py, variation_parameters_generator.py |
| `OPTICS_FORMULA` | 1 | `OPTICS_FORMULA\|1/f=1/d_o+1/d_i` | optics_generator.py |
| `OPTICS_SETUP` | 3 | `OPTICS_SETUP\|mirror_magnification\|f=14, d_o=56\|h_o=14` | optics_generator.py |
| `OPT_SETUP` | 2 | `OPT_SETUP\|48 m of fence, barn forms the fourth side; sides x, x, and 48 - 2x\|maximize area` | optimization_generator.py |
| `ORBIT_FORMULA` | 1 | `ORBIT_FORMULA\|a_c=v^2/r` | orbital_mechanics_generator.py |
| `ORBIT_SETUP` | 3 | `ORBIT_SETUP\|centripetal_force\|m=6\|r=15, v=7` | orbital_mechanics_generator.py |
| `ORDER_PAIR` | 2 | `ORDER_PAIR\|1 ≤ 2\|2 is a multiple of 1` | partial_order_generator.py |
| `ORDER_PDF` | 1 | `ORDER_PDF\|f_{4:9}(x)=504*x^3*(1-x)^5` | order_statistics_generator.py |
| `ORDER_SETUP` | 3 | `ORDER_SETUP\|n=9\|k=4\|q=2/3` | order_statistics_generator.py |
| `ORDER_START` | 2 | `ORDER_START\|s\|identity e` | cayley_table_generator.py |
| `ORDER_STEP` | 2 | `ORDER_STEP\|k=1\|s` | cayley_table_generator.py |
| `ORD_CMP` | 2 | `ORD_CMP\|coefficients at exponent 2\|3 > 2` | ordinal_arithmetic_generator.py |
| `ORD_RULE` | 2, 3 | `ORD_RULE\|addition\|retain left terms above exponent 0` | ordinal_arithmetic_generator.py |
| `ORTHOGONALITY` | 2 | `ORTHOGONALITY\|lower multiplet\|orthogonal to higher J` | clebsch_gordan_generator.py |
| `OR_SETUP` | 3 | `OR_SETUP\|M/M/1\|lambda=10\|mu=28` | or_formula_generator.py |
| `OUTCOME_CHECK` | 3 | `OUTCOME_CHECK\|17\|the two-digit number is greater than 81\|no` | sample_space_list_generator.py |
| `OUTER_ANTIDERIV` | 2 | `OUTER_ANTIDERIV\|dx\|3*x^2 + 16*x` | double_integral_generator.py |
| `OUTER_EVAL` | 3 | `OUTER_EVAL\|x=3..6\|3*(6^2 - 3^2) + 16*(6 - 3)\|129` | double_integral_generator.py |
| `OUTER_PRODUCT` | 1 | `OUTER_PRODUCT\|rho=49/192ket00bra00 - sqrt(7007)/192(ket00bra11+ket11bra00) + 143/192ket11bra11` | partial_trace_generator.py |
| `OUTPUT` | 1 | `OUTPUT\|y_hat=-6` | backprop_generator.py |
| `PAIR` | 2 | `PAIR\|apricot\|badger` | one_to_one_correspondence_generator.py |
| `PAIRING` | 2 | `PAIRING\|(147, 183)\|(m + n)(m + n + 1)/2 + n` | cantor_pairing_generator.py |
| `PAIR_RULE` | 1, 2 | `PAIR_RULE\|(a, b) ~ (c, d)\|a + d = b + c` | integers_as_pairs_generator.py, rationals_as_pairs_generator.py |
| `PARALLEL_RELATION` | 1 | `PARALLEL_RELATION\|5x + 32 = 3x + 46` | angle_relationships_generator.py |
| `PARALLEL_SETUP` | 2 | `PARALLEL_SETUP\|alternate_interior\|Alternate interior angles are equal` | angle_relationships_generator.py |
| `PARALLEL_SOLVE` | 2 | `PARALLEL_SOLVE\|2x = 14\|x = 7` | angle_relationships_generator.py |
| `PARAMS` | 3 | `PARAMS\|W1=[[0,-1], [1,1]]\|b1=(0,2)\|v=(-2,-2), c=0` | backprop_generator.py |
| `PARAM_PART` | 2 | `PARAM_PART\|attention_per_layer\|262144` | param_count_generator.py |
| `PARAM_PATH` | 3 | `PARAM_PATH\|r(t)\|(2, t - 3)\|0 <= t <= 1` | line_integral_generator.py |
| `PARAM_SETUP` | 2, 3 | `PARAM_SETUP\|x = 6t + 7, y = 6t - 13\|eliminate t` | param_count_generator.py, parametric_calculus_generator.py, polar_parametric_generator.py |
| `PARITY` | 1, 2 | `PARITY\|transpositions 4\|even` | fourier_series_generator.py, permutation_group_generator.py |
| `PARITY_CALC` | 2 | `PARITY_CALC\|p1=d1 xor d2 xor d4\|1 xor 1 xor 0=0` | hamming_code_generator.py |
| `PARSE` | 2, 3 | `PARSE\|p\|atom` | wff_parsing_generator.py |
| `PARTFRAC_SETUP` | 1 | `PARTFRAC_SETUP\|(-x + 6)/(x(x + 2)) = A/x + B/(x + 2)` | partial_fractions_generator.py, telescoping_generator.py |
| `PARTIAL` | 2 | `PARTIAL\|u_x\|-4x - 4` | cauchy_riemann_generator.py, fundamental_form_generator.py, hamiltonian_generator.py, lagrangian_generator.py |
| `PARTIAL_FRAC` | 2 | `PARTIAL_FRAC\|Y(s)\|3/(s + 5) + 4/(s - 3)` | laplace_ivp_generator.py |
| `PARTIAL_RESULT` | 2 | `PARTIAL_RESULT\|f_y\|2*x^3 + 5*x` | div_curl_generator.py, exact_ode_generator.py, gradient_generator.py, hessian_classify_generator.py, jacobian_generator.py, lagrange_multiplier_generator.py, line_integral_generator.py, multivar_chain_rule_generator.py, partial_derivative_generator.py, vector_theorem_generator.py |
| `PARTIAL_RULE` | 3 | `PARTIAL_RULE\|5*x*y\|d/dy\|5*x` | partial_derivative_generator.py |
| `PARTIAL_SETUP` | 2 | `PARTIAL_SETUP\|f(x,y) = 2*x^3*y + 5*x*y\|f_yy` | partial_derivative_generator.py |
| `PARTIAL_TRACE` | 2 | `PARTIAL_TRACE\|ket00bra00\|ket0bra0` | partial_trace_generator.py |
| `PARTICLE_TABLE` | 1 | `PARTICLE_TABLE\|gamma(Q=0,B=0,Le=0,Lmu=0); pi0(Q=0,B=0,Le=0,Lmu=0); n(Q=0,B=1,Le=0,Lmu=0); e-(Q=-1,B=0,Le=1,Lmu=0); p(Q=1,B=1,Le=0,Lmu=0); anti_nu_e(Q=0,B=0,Le=-1,Lmu=0)` | conservation_law_generator.py |
| `PARTICULAR` | 2 | `PARTICULAR\|y_p\|-1` | undetermined_coeff_generator.py, variation_parameters_generator.py |
| `PARTICULAR_CHECK` | 2 | `PARTICULAR_CHECK\|K = -4\|5K - 6K - 8 = K` | recurrence_generator.py |
| `PARTICULAR_TRY` | 2 | `PARTICULAR_TRY\|a_n = K\|constant forcing` | recurrence_generator.py |
| `PARTITION` | 1 | `PARTITION\|{{5, 11, 22, 40}, {48, 51}}` | equivalence_relation_generator.py |
| `PARTITION_FORMULA` | 1 | `PARTITION_FORMULA\|Z=g0+g1*b` | partition_function_generator.py |
| `PARTITION_SETUP` | 3 | `PARTITION_SETUP\|two_level\|g0=1, g1=1\|epsilon=19, b=1/9` | partition_function_generator.py |
| `PARTS_CHOOSE` | 2 | `PARTS_CHOOSE\|u = ln(x), dv = -95 dx\|du = dx/x, v = -95x` | integration_by_parts_generator.py |
| `PARTS_FORMULA` | 1 | `PARTS_FORMULA\|∫ u dv = uv - ∫ v du` | integration_by_parts_generator.py |
| `PASCAL_ROW` | 2 | `PASCAL_ROW\|0\|1` | pascal_triangle_generator.py |
| `PASCAL_SETUP` | 1 | `PASCAL_SETUP\|row 17` | pascal_triangle_generator.py |
| `PATH` | 2 | `PATH\|4→8→15\|add (4, 15)` | relation_closure_generator.py |
| `PATH_DERIV` | 2 | `PATH_DERIV\|r'(t)\|(0, 1)` | curve_geometry_generator.py, line_integral_generator.py |
| `PAULI_IDENTITY` | 3 | `PAULI_IDENTITY\|sigma_x sigma_y\|i epsilon_ijk sigma_k\|-12isigma_z` | pauli_algebra_generator.py |
| `PAULI_MATRIX` | 2 | `PAULI_MATRIX\|sigma_x\|[[0,1],[1,0]]` | spin_half_generator.py |
| `PAULI_SETUP` | 3 | `PAULI_SETUP\|product\|A=3sigma_x\|B=-4sigma_y` | pauli_algebra_generator.py |
| `PCA_SETUP` | 2 | `PCA_SETUP\|points=[(2,-5), (-8,-5), (-3,-1), (-3,-9)]\|population covariance` | pca_generator.py |
| `PC_VECTOR` | 2 | `PC_VECTOR\|e1\|(1,0)` | pca_generator.py |
| `PDA_POP` | 2 | `PDA_POP\|(\|stack=$(` | pda_simulation_generator.py |
| `PDA_PUSH` | 2 | `PDA_PUSH\|(\|stack=$(` | pda_simulation_generator.py |
| `PDA_READ` | 1 | `PDA_READ\|(` | pda_simulation_generator.py |
| `PDA_REJECT` | 1 | `PDA_REJECT\|too many b symbols` | pda_simulation_generator.py |
| `PDA_SETUP` | 2 | `PDA_SETUP\|balanced_parentheses\|stack=$` | pda_simulation_generator.py |
| `PDA_STATE` | 3 | `PDA_STATE\|pos 1\|q\|stack=$` | pda_simulation_generator.py |
| `PDE_SETUP` | 2 | `PDE_SETUP\|u_t = 9u_xx on [0,5]\|u(x,0)=3sin(1πx/5)` | separable_pde_generator.py |
| `PDF_FORMULA` | 1 | `PDF_FORMULA\|f_Y(y)=1/(56*sqrt(y))` | rv_transform_generator.py |
| `PD_SETUP` | 2 | `PD_SETUP\|A=[[0,1], [1,4]]\|Sylvester criterion` | positive_definite_generator.py |
| `PEANO_BASE` | 2 | `PEANO_BASE\|S0 ∸ 0\|S0` | peano_arithmetic_generator.py |
| `PEANO_EQ` | 2 | `PEANO_EQ\|S0 ∸ S0\|pred(S0 ∸ 0)` | peano_arithmetic_generator.py |
| `PERCENT_CALC_PART` | 3 | `PERCENT_CALC_PART\|0.375\|1075\|403.125` | percent_problem_generator.py |
| `PERCENT_TO_DEC` | 2 | `PERCENT_TO_DEC\|87%\|0.87` | annuity_generator.py, bond_pricing_generator.py, composite_arithmetic_generator.py, exponential_model_generator.py, fill_in_step_generator.py, finance_generator.py, fraction_decimal_percent_converter.py, npv_irr_generator.py, percent_problem_generator.py, percent_word_problem_generator.py, piecewise_evaluation_generator.py, portfolio_generator.py, tip_bill_split_generator.py |
| `PERCEPTRON_RULE` | 2 | `PERCEPTRON_RULE\|score=w0+w1*x1+w2*x2\|if y*score <= 0 update` | perceptron_generator.py |
| `PERCEPTRON_SAMPLE` | 3 | `PERCEPTRON_SAMPLE\|i=1\|x=(-2,2)\|y=1` | perceptron_generator.py |
| `PERCEPTRON_SCORE` | 2 | `PERCEPTRON_SCORE\|i=1\|score=2` | perceptron_generator.py |
| `PERCEPTRON_SETUP` | 3 | `PERCEPTRON_SETUP\|eta=2\|w=(-2,-1,1)\|samples=[(-2,2,1), (3,2,1), (2,0,-1)]` | perceptron_generator.py |
| `PERCEPTRON_UPDATE` | 2, 3 | `PERCEPTRON_UPDATE\|i=1\|no change\|w=(-2,-1,1)` | perceptron_generator.py |
| `PERIM` | 1 | `PERIM\|42` | geometry_area_perimeter_generator.py, polygon_perimeter_generator.py |
| `PERIOD` | 1 | `PERIOD\|60°` | sinusoid_features_generator.py |
| `PERM_COMPOSE` | 3 | `PERM_COMPOSE\|i=1\|tau(i)=3\|sigma(tau(i))=4` | permutation_group_generator.py |
| `PERM_FORMULA` | 1 | `PERM_FORMULA\|P(n, r) = n·(n-1)···(n-r+1), 4 factors` | permutation_combination_generator.py |
| `PERM_RESULT` | 1 | `PERM_RESULT\|[4, 6, 3, 5, 2, 1]` | permutation_group_generator.py |
| `PERM_SETUP` | 2, 3 | `PERM_SETUP\|P(7, 4)\|n!/(n-r)!` | permutation_combination_generator.py, permutation_group_generator.py |
| `PERPLEXITY` | 2 | `PERPLEXITY\|exp(CE)\|256` | perplexity_generator.py |
| `PERPLEXITY_SETUP` | 2 | `PERPLEXITY_SETUP\|tokens=177\|p=1/256` | perplexity_generator.py |
| `PE_ENTRY` | 2 | `PE_ENTRY\|0\|1/2` | positional_encoding_generator.py |
| `PE_SETUP` | 3 | `PE_SETUP\|position=6\|d=2\|theta=pi/6` | positional_encoding_generator.py |
| `PF_PRIME` | 1 | `PF_PRIME\|347` | godel_numbering_generator.py, prime_factorization_generator.py, repeating_decimal_generator.py |
| `PF_STEP` | 3 | `PF_STEP\|1041\|3\|347` | godel_numbering_generator.py, prime_factorization_generator.py, repeating_decimal_generator.py |
| `PHASE_SHIFT` | 1 | `PHASE_SHIFT\|45° right` | sinusoid_features_generator.py |
| `PHI_STEP` | 2 | `PHI_STEP\|p=2\|6` | totient_generator.py |
| `PHYS_FORMULA` | 1 | `PHYS_FORMULA\|P = W/t` | physics_formula_generator.py |
| `PHYS_SETUP` | 3 | `PHYS_SETUP\|W = 35040 joules\|t = 4 minutes\|power` | physics_formula_generator.py |
| `PH_FORMULA` | 1 | `PH_FORMULA\|pOH=-log10([OH-]), pH=14-pOH` | ph_calculation_generator.py |
| `PH_SETUP` | 2, 3 | `PH_SETUP\|hydroxide_with_log\|[OH-]=2*10^-5\|log10(2)=0.3` | ph_calculation_generator.py |
| `PI2_NUM` | 3 | `PI2_NUM\|-11/25000\|π^2\|-11π^2/25000` | casimir_force_generator.py |
| `PICTO_COUNT` | 2 | `PICTO_COUNT\|Burgers\|4` | graph_interpret_generator.py |
| `PICTO_KEY` | 2 | `PICTO_KEY\|▲\|10` | graph_interpret_generator.py |
| `PIVOT` | 3 | `PIVOT\|row=s1\|column=x\|pivot=1` | simplex_generator.py |
| `PIVOT_COLS` | 2 | `PIVOT_COLS\|columns 1, 2\|rank = 2` | subspace_basis_generator.py |
| `PI_COEFF` | 2 | `PI_COEFF\|9π/5\|9/5` | arc_sector_generator.py |
| `PI_DEN` | 3 | `PI_DEN\|1/256\|π\|1/(256π)` | gauss_law_generator.py, hawking_generator.py, magnetism_generator.py |
| `PI_MULT` | 3 | `PI_MULT\|1\|π\|π` | shm_generator.py |
| `PLACE_DP` | 3 | `PLACE_DP\|2262\|2\|22.62` | decimal_mult_generator.py |
| `PLACE_DP_Q` | 3 | `PLACE_DP_Q\|165\|3\|165` | decimal_div_generator.py, percent_problem_generator.py |
| `PLACE_VALUE` | 2 | `PLACE_VALUE\|1 * 2^0\|1` | base_conversion_generator.py |
| `PLANCK_SETUP` | 4 | `PLANCK_SETUP\|time\|hbar=25\|G=9\|c=4` | planck_units_generator.py |
| `PLUS_MINUS` | 2 | `PLUS_MINUS\|x = ±4\|x = 4 or x = -4` | completing_square_generator.py, quadratic_square_root_generator.py, rational_equation_generator.py |
| `POINT_FROM_LAMBDA` | 3 | `POINT_FROM_LAMBDA\|x\|160*5/8\|100` | lagrange_multiplier_generator.py |
| `POINT_SLOPE_SETUP` | 1 | `POINT_SLOPE_SETUP\|y - 4 = 2(x + 9)` | equation_from_two_points_generator.py, parallel_perpendicular_line_generator.py, point_slope_generator.py |
| `POLAR_AREA_FORMULA` | 1 | `POLAR_AREA_FORMULA\|A = (1/2) ∫ r^2 dθ` | parametric_calculus_generator.py |
| `POLAR_BOUNDS` | 2 | `POLAR_BOUNDS\|r\|0..5` | double_integral_generator.py |
| `POLAR_CONVERT` | 2 | `POLAR_CONVERT\|x^2 + y^2\|r^2` | double_integral_generator.py |
| `POLAR_EVAL` | 3 | `POLAR_EVAL\|theta range * radial integral\|pi * 625/4\|625/4*pi` | double_integral_generator.py |
| `POLAR_FORM` | 1 | `POLAR_FORM\|6 cis(270 deg)` | euler_formula_generator.py |
| `POLAR_FORMULA` | 1 | `POLAR_FORMULA\|x = r cos θ, y = r sin θ` | polar_parametric_generator.py |
| `POLAR_SETUP` | 2, 3 | `POLAR_SETUP\|(r, θ) = (62, 34440°)\|rectangular coordinates` | parametric_calculus_generator.py, polar_parametric_generator.py |
| `POLES` | 1 | `POLES\|s=-4, -12` | transfer_function_generator.py |
| `POLE_ORDER` | 1 | `POLE_ORDER\|1` | residue_generator.py |
| `POLE_TEST` | 3 | `POLE_TEST\|pole 8\|abs(8) < 7\|outside` | contour_integral_generator.py |
| `POLISH` | 1 | `POLISH\|AECpqrEAqqCqp` | wff_parsing_generator.py |
| `POLLARD_FACTOR` | 2 | `POLLARD_FACTOR\|11\|17` | pollard_factorization_generator.py |
| `POLLARD_PM1_SETUP` | 3 | `POLLARD_PM1_SETUP\|n=187\|base=5\|B=6` | pollard_factorization_generator.py |
| `POLLARD_RHO_SETUP` | 3 | `POLLARD_RHO_SETUP\|n=323\|c=2\|x0=9` | pollard_factorization_generator.py |
| `POLYDIV_SETUP` | 2 | `POLYDIV_SETUP\|3x^3 - 8x^2 + x - 3\|3x - 2` | finite_field_generator.py, polynomial_long_division_generator.py |
| `POLY_ACCUM` | 2 | `POLY_ACCUM\|x^0\|0` | finite_field_generator.py |
| `POLY_ADD_START` | 1 | `POLY_ADD_START\|max degree 2` | finite_field_generator.py |
| `POLY_COEFF` | 3 | `POLY_COEFF\|sum\|x^0\|0` | finite_field_generator.py |
| `POLY_COMBINE` | 1 | `POLY_COMBINE\|-15x^2 - x - 5` | multiplying_binomials_generator.py, polynomial_add_sub_generator.py |
| `POLY_DIST_NEG` | 1 | `POLY_DIST_NEG\|Distribute negative sign to second polynomial` | polynomial_add_sub_generator.py |
| `POLY_DIV_SETUP` | 1 | `POLY_DIV_SETUP\|(18x^4 + 18x^3 + 27x^2 + 18x) / (9x)` | polynomial_div_monomial_generator.py |
| `POLY_DIV_SPLIT` | 1 | `POLY_DIV_SPLIT\|(18x^4) / (9x) + (18x^3) / (9x) + (27x^2) / (9x) + (18x) / (9x)` | polynomial_div_monomial_generator.py |
| `POLY_FORMULA` | 1 | `POLY_FORMULA\|A = (1/2)·a·P` | regular_polygon_area_generator.py |
| `POLY_GROUP_LIKE` | 1 | `POLY_GROUP_LIKE\|(-6x^2 -9x^2) + (-3x +2x) + (-5)` | multiplying_polynomials_generator.py, polynomial_add_sub_generator.py |
| `POLY_INPUT` | 2 | `POLY_INPUT\|f(x)\|x^2 + x` | finite_field_generator.py |
| `POLY_MULT_SETUP` | 1 | `POLY_MULT_SETUP\|(-5x + 5)(-3x^2 + 4x + 2)` | multiplying_polynomials_generator.py |
| `POLY_MUL_START` | 2 | `POLY_MUL_START\|degree 2\|degree 2` | finite_field_generator.py |
| `POLY_REMAINDER` | 1 | `POLY_REMAINDER\|x^2 + 1` | finite_field_generator.py |
| `POLY_SCALE` | 3 | `POLY_SCALE\|x^3 - 3x/5\|5/2\|(5x^3 - 3x)/2` | legendre_construction_generator.py |
| `POLY_SETUP` | 1, 2 | `POLY_SETUP\|(-6x^2 - 3x) + (-9x^2 + 2x - 5)` | factor_gcf_generator.py, factor_grouping_generator.py, factor_special_forms_generator.py, factor_trinomial_generator.py, polynomial_add_sub_generator.py, rational_expr_add_sub_generator.py, rational_expr_mult_div_generator.py, rational_expr_simplify_generator.py, regular_polygon_area_generator.py |
| `POLY_SUB` | 2, 3 | `POLY_SUB\|(3x^3 - 8x^2) - (3x^3 - 2x^2)\|-6x^2` | legendre_construction_generator.py, polynomial_long_division_generator.py |
| `PORT_FORMULA` | 2 | `PORT_FORMULA\|E=wA*rA+wB*rB\|Var=wA^2*varA+wB^2*varB+2*wA*wB*cov` | portfolio_generator.py |
| `PORT_RESULT` | 2 | `PORT_RESULT\|expected_return=13/150\|variance=1/90` | portfolio_generator.py |
| `PORT_SETUP` | 3 | `PORT_SETUP\|wA=2/3,wB=1/3\|rA=4%,rB=18%\|varA=0.01,varB=0.09,cov=-0.0075` | portfolio_generator.py |
| `POSTERIOR` | 3 | `POSTERIOR\|C1\|(1/27)/(11/108)\|4/11` | bayes_multiple_hypotheses_generator.py |
| `POSTERIOR_PARAM` | 1 | `POSTERIOR_PARAM\|alpha' = alpha + successes` | bayesian_update_generator.py |
| `POST_PRECISION` | 1 | `POST_PRECISION\|prior precision + data precision` | bayesian_update_generator.py |
| `POTENTIAL_BUILD` | 3 | `POTENTIAL_BUILD\|integrate P dx\|2*x^2 - 3*x*y + 2*x + g(y)\|g'(y) remains` | exact_ode_generator.py, line_integral_generator.py |
| `POTENTIAL_RESULT` | 2 | `POTENTIAL_RESULT\|phi(x,y)\|2*x^2 + y^2 - 3*x*y + 2*x - 5*y` | exact_ode_generator.py, line_integral_generator.py |
| `POW` | 2 | `POW\|60^3\|216000` | binomial_probability_generator.py, classic_probability_puzzles_generator.py, distribution_of_sum_generator.py, geometric_distribution_generator.py, linearity_of_expectation_generator.py, recurrence_generator.py |
| `POWER_ENTRY` | 3 | `POWER_ENTRY\|(1,1)\|147*7 + 810*(-2)\|-591` | diagonalization_generator.py |
| `POWER_FORM` | 1 | `POWER_FORM\|A^2 = P*D^2*P^-1` | diagonalization_generator.py |
| `POWER_INTEGRAL` | 2 | `POWER_INTEGRAL\|int_0^a x dx\|a^2/2` | continuous_distribution_generator.py, wavefunction_generator.py |
| `POWER_REDUCE` | 2 | `POWER_REDUCE\|14^60\|14^12 mod 45` | totient_generator.py |
| `POWER_RULE` | 2 | `POWER_RULE\|-2x^3\|-6x^2` | chain_rule_generator.py, commutator_generator.py, curve_analysis_generator.py, derivative_power_rule_generator.py, derivative_product_quotient_generator.py, derivative_transcendental_generator.py, lhopital_generator.py, linear_approx_generator.py, log_diff_higher_order_generator.py, mean_value_theorem_generator.py, optimization_generator.py, tangent_line_generator.py |
| `POWER_SETUP` | 2 | `POWER_SETUP\|(e^(i*220 deg))^(4i)\|principal logarithm` | complex_log_generator.py |
| `POWER_SET_RESULT` | 1 | `POWER_SET_RESULT\|{∅, {m}, {s}, {t}, {m, s}, {m, t}, {s, t}, {m, s, t}}` | set_operations_generator.py |
| `POWER_SHIFT` | 3 | `POWER_SHIFT\|k=0\|0-3\|-3` | laurent_series_generator.py |
| `PREDICATES` | 1 | `PREDICATES\|X(x): x is a baker; W(x): x is vigilant; T(x): x is curious` | english_to_logic_generator.py |
| `PREDICT` | 2 | `PREDICT\|x*\|3/2` | kernel_ridge_generator.py |
| `PREIMAGE` | 2 | `PREIMAGE\|23\|{b, p}` | function_properties_generator.py |
| `PREMISE` | 2 | `PREMISE\|1\|d` | natural_deduction_generator.py |
| `PREMISES_ALL_T` | 2 | `PREMISES_ALL_T\|p=T, q=T, r=T\|no` | argument_form_generator.py |
| `PRIME` | 1 | `PRIME\|41` | divisibility_classification_generator.py |
| `PRIM_CANDIDATES` | 2 | `PRIM_CANDIDATES\|visited C\|AC=1, CD=15, BC=19` | mst_generator.py |
| `PRIM_START` | 1 | `PRIM_START\|C` | mst_generator.py |
| `PRINCIPAL_LOG` | 1 | `PRINCIPAL_LOG\|ln(146) + i*19pi/180` | complex_log_generator.py |
| `PRINCIPAL_MINOR` | 2 | `PRINCIPAL_MINOR\|K11\|12` | kernel_validity_generator.py |
| `PRIOR_PRECISION` | 1 | `PRIOR_PRECISION\|1/tau^2` | bayesian_update_generator.py |
| `PROBABILITY` | 2 | `PROBABILITY\|P(+x)\|529/578` | spin_half_generator.py |
| `PROB_CONDITIONAL` | 2 | `PROB_CONDITIONAL\|P(silver given first was yellow)\|5/12` | compound_probability_generator.py |
| `PROB_DEPENDENT` | 1 | `PROB_DEPENDENT\|Drawing without replacement means dependent events` | compound_probability_generator.py |
| `PROB_DESCRIBE` | 1 | `PROB_DESCRIBE\|Two fair coin flips: heads then tails` | compound_probability_generator.py |
| `PROB_IDENTIFY` | 2 | `PROB_IDENTIFY\|P(first heads)\|1/2` | compound_probability_generator.py |
| `PROB_INDEPENDENT` | 1 | `PROB_INDEPENDENT\|Separate coin flips are independent events` | compound_probability_generator.py |
| `PROB_MULTIPLY` | 3 | `PROB_MULTIPLY\|1/2\|1/2\|1/4` | compound_probability_generator.py |
| `PROB_SETUP` | 2 | `PROB_SETUP\|11\|16` | complement_probability_generator.py, counting_to_probability_generator.py, discrete_uniform_bernoulli_generator.py, fundamental_counting_principle_generator.py, independence_check_generator.py, likelihood_language_generator.py, odds_probability_generator.py, random_digit_simulation_generator.py, sample_space_list_generator.py, simple_probability_generator.py, venn_probability_generator.py |
| `PROB_SIMPLIFY` | 2 | `PROB_SIMPLIFY\|40/156\|10/39` | compound_probability_generator.py |
| `PROB_WEIGHT` | 2 | `PROB_WEIGHT\|-sqrt(2/3)^2\|2/3` | clebsch_gordan_generator.py |
| `PRODUCT` | 2 | `PRODUCT\|Delta x^2 * Delta p^2\|17689pi^2/12 - 1/2` | uncertainty_generator.py |
| `PROJECT` | 2 | `PROJECT\|P1\|5` | pca_generator.py |
| `PROJECTILE_SETUP` | 3 | `PROJECTILE_SETUP\|vx=58\|vy=42\|g=10` | projectile_motion_generator.py |
| `PROJECTION` | 2 | `PROJECTION\|X*beta\|[3, 5, 7, 9]` | least_squares_generator.py, legendre_construction_generator.py |
| `PROJECTOR_SETUP` | 2 | `PROJECTOR_SETUP\|v=(19/181, 180/181)\|P=vv^T=[[361/32761,3420/32761],[3420/32761,32400/32761]]` | projector_generator.py |
| `PROJ_COEFF` | 3 | `PROJ_COEFF\|v2 on u1\|4/2\|2` | gram_schmidt_generator.py |
| `PROJ_VECTOR` | 2 | `PROJ_VECTOR\|2*u1\|[-2, -2]` | gram_schmidt_generator.py |
| `PROPERTY_MATCH` | 3 | `PROPERTY_MATCH\|multiplicative identity property\|a × 1 = a\|5771 × 1` | operation_properties_generator.py |
| `PROPERTY_RESULT` | 2 | `PROPERTY_RESULT\|reflexive\|no` | relation_check_generator.py |
| `PROP_SETUP` | 1 | `PROP_SETUP\|2/2 = x/3` | proportion_word_problem_generator.py, proportional_relationship_generator.py, similar_triangles_generator.py, triangle_solve_generator.py |
| `PSD_SETUP` | 2 | `PSD_SETUP\|K=[[12,8], [8,7]]\|criterion=all principal minors >= 0` | kernel_validity_generator.py |
| `PULL` | 2 | `PULL\|∀u\|from left past ∧` | prenex_normal_form_generator.py |
| `PURITY` | 1 | `PURITY\|Tr(rho^2)=65/128` | density_matrix_generator.py |
| `PYTHAG_CALCULATE` | 2 | `PYTHAG_CALCULATE\|d² = 5184 + 900 = 6084\|6084` | pythag_leg_generator.py |
| `PYTHAG_CONTEXT` | 3 | `PYTHAG_CONTEXT\|rectangle_diagonal\|length=72, width=30\|diagram=TCB` | pythag_leg_generator.py |
| `PYTHAG_FORMULA` | 1 | `PYTHAG_FORMULA\|a² + b² = c²` | pythag_hyp_generator.py, pythag_leg_generator.py |
| `PYTHAG_MODEL` | 3 | `PYTHAG_MODEL\|length=72\|width=30\|diagonal=?` | pythag_leg_generator.py |
| `PYTHAG_ROOT` | 2 | `PYTHAG_ROOT\|625\|25` | pythag_leg_generator.py |
| `PYTHAG_SETUP` | 2, 3 | `PYTHAG_SETUP\|legs=1050,880\|hypotenuse NE=?` | pythag_hyp_generator.py, pythag_leg_generator.py |
| `PYTHAG_SOLVE` | 2 | `PYTHAG_SOLVE\|b² = 4225 - 3600\|625` | pythag_leg_generator.py |
| `PYTHAG_SQUARE` | 2 | `PYTHAG_SQUARE\|60\|3600` | pythag_leg_generator.py |
| `PYTHAG_SUBSTITUTE` | 1 | `PYTHAG_SUBSTITUTE\|60² + b² = 65²` | pythag_leg_generator.py |
| `Q1` | 4 | `Q1\|14\|462\|28\|17` | complex_quadratic_generator.py, polynomial_zeros_generator.py, quadratic_generator.py |
| `Q2` | 4 | `Q2\|14\|462\|28\|-16` | complex_quadratic_generator.py, polynomial_zeros_generator.py, quadratic_generator.py |
| `QN_ADD` | 4 | `QN_ADD\|Q\|left\|0 + gamma(0)\|0` | conservation_law_generator.py |
| `QR_ENTRY` | 2 | `QR_ENTRY\|q1\|[3/5, 4/5]` | qr_decomposition_generator.py |
| `QR_SETUP` | 2 | `QR_SETUP\|A = [[3, -9], [4, 13]]\|Gram-Schmidt columns` | qr_decomposition_generator.py |
| `QUADRANT` | 2 | `QUADRANT\|108°\|quadrant II` | angle_measure_generator.py, polar_parametric_generator.py, unit_circle_generator.py |
| `QUADRATIC` | 3 | `QUADRATIC\|3\|9\|-30` | mobius_transform_generator.py |
| `QUANTILE` | 3 | `QUANTILE\|3/4\|first x with F(x) ≥ q\|36` | pmf_cdf_quantile_generator.py |
| `QUANTUM_FORMULA` | 1 | `QUANTUM_FORMULA\|Delta_lambda=h/(m*c)*(1-cos(theta))` | quantum_formula_generator.py |
| `QUANTUM_SETUP` | 2, 3 | `QUANTUM_SETUP\|gate=H\|input=e^(i233π/137)·ket1` | quantum_formula_generator.py, quantum_gate_generator.py |
| `QUANT_CASE` | 1, 2 | `QUANT_CASE\|x=5, y=5, z=5\|matrix=T` | quantifier_finite_domain_generator.py |
| `QUANT_CHOICE` | 1 | `QUANT_CHOICE\|every → ∀` | english_to_logic_generator.py |
| `QUANT_RESULT` | 2, 3 | `QUANT_RESULT\|∀x ∃y ∀z\|true\|atomic column=TTTTTTTTTTTTFTFTTTTTTTTTTTTTTTFTTTTTTTTTTTTTFTFTTTTFTTTTTTTFTTTT` | quantifier_finite_domain_generator.py |
| `QUANT_SETUP` | 3 | `QUANT_SETUP\|x=(81/100,-67/100,-8/5)\|scale=1/10\|zero_point=-4` | quantization_generator.py |
| `QUANT_VALUE` | 2 | `QUANT_VALUE\|1\|4` | quantization_generator.py |
| `QUARK_CHARGE` | 2 | `QUARK_CHARGE\|anti_d\|1/3` | quark_composition_generator.py |
| `QUARK_SETUP` | 3 | `QUARK_SETUP\|antibaryon,count=696\|anti_d anti_c anti_c\|u=2/3,d=-1/3,s=-1/3,c=2/3,b=-1/3; anti=-charge` | quark_composition_generator.py |
| `QUARTILE` | 3 | `QUARTILE\|Q1\|7,8,19\|8` | five_number_summary_generator.py |
| `QUAT_COMPONENT` | 3 | `QUAT_COMPONENT\|p*q\|real\|2` | quaternion_generator.py |
| `QUAT_INVERSE` | 2 | `QUAT_INVERSE\|p\|(2/13,2/13,-1/13,-2/13)` | quaternion_generator.py |
| `QUAT_MUL_START` | 3 | `QUAT_MUL_START\|p*q\|p\|q` | quaternion_generator.py |
| `QUAT_RESULT` | 2 | `QUAT_RESULT\|p*q\|(2,4,9,-9)` | quaternion_generator.py |
| `QUAT_SETUP` | 2 | `QUAT_SETUP\|p=(2,-2,1,2)\|q=(-1,3,2,0)` | quaternion_generator.py |
| `QUEUE_STATE` | 2 | `QUEUE_STATE\|initial\|D` | graph_traversal_generator.py |
| `QUOTIENT` | 1 | `QUOTIENT\|x + 1` | finite_field_generator.py |
| `Q_EXPR` | 1 | `Q_EXPR\|Q = [B]/[A]` | equilibrium_ice_generator.py |
| `R` | 1 | `R\|21` | complex_number_ops_generator.py, finite_field_generator.py, long_division_generator.py, polynomial_long_division_generator.py, polynomial_zeros_generator.py, synthetic_division_generator.py |
| `RANGE` | 1 | `RANGE\|{6, 9, 16, 27}` | relation_operations_generator.py |
| `RANK` | 2 | `RANK\|∅\|0` | hereditarily_finite_set_generator.py |
| `RAPIDITY_SUM` | 2 | `RAPIDITY_SUM\|collinear boosts\|2/3` | minkowski_interval_generator.py |
| `RATE_MONTHLY` | 2 | `RATE_MONTHLY\|18% / 12\|0.015` | finance_generator.py |
| `RATE_SETUP` | 2 | `RATE_SETUP\|cube: ds/dt = 12 m/min; s = 16 m\|dV/dt` | related_rates_generator.py |
| `RATIO` | 2, 3 | `RATIO\|2*y = 3*x\|y = 3/2*x` | lagrange_multiplier_generator.py, simplex_generator.py |
| `RATIONALIZE` | 1 | `RATIONALIZE\|(21 - √227)/(21 - √227)` | dot_product_generator.py, limit_evaluation_generator.py, radical_rationalize_generator.py, special_right_triangle_generator.py |
| `RATIO_BASE` | 3 | `RATIO_BASE\|3:7\|1\|3:7` | error_spotting_generator.py, fill_in_step_generator.py, ratio_table_generator.py |
| `RATIO_TABLE` | 2 | `RATIO_TABLE\|Red (liters): 3, 6, 9, 30\|Blue (liters): 7, 14, 21, ?` | error_spotting_generator.py, fill_in_step_generator.py, ratio_table_generator.py |
| `RAW_FORMULA` | 1 | `RAW_FORMULA\|x = μ + z·σ` | normal_table_generator.py, z_score_generator.py |
| `REARRANGE_EQ` | 1 | `REARRANGE_EQ\|whole = 42159 / 1.41` | percent_problem_generator.py |
| `RECIPROCAL` | 2 | `RECIPROCAL\|csc θ = 1/sin θ\|-5/3` | trig_six_functions_generator.py |
| `RECOVER_DATA` | 2 | `RECOVER_DATA\|positions 3,5,6,7\|1011` | hamming_code_generator.py |
| `RECT_FORM` | 1 | `RECT_FORM\|12sqrt2 + 12sqrt2i` | de_moivre_generator.py, euler_formula_generator.py |
| `RECUR` | 3 | `RECUR\|5P_5 = 9x P_4 - 4P_3\|P_4 = (35x^4 - 30x^2 + 3)/8\|P_3 = (5x^3 - 3x)/2` | legendre_construction_generator.py |
| `RECURRENCE` | 2 | `RECURRENCE\|a_(n+1)\|3a_n/(n+1)` | derangement_generator.py, series_solution_generator.py |
| `REC_SETUP` | 1, 2 | `REC_SETUP\|a_n = -5 a_(n-1) - 6 a_(n-2)\|a_0 = 6, a_1 = -17` | master_theorem_generator.py, recurrence_generator.py |
| `REDUCE` | 2, 3 | `REDUCE\|(225, 302)\|(0, 77)` | integers_as_pairs_generator.py, rationals_as_pairs_generator.py |
| `REDUCED_DENSITY` | 1 | `REDUCED_DENSITY\|rho_A=[[49/192,0],[0,143/192]]` | partial_trace_generator.py |
| `REFLEXIVE_CHECK` | 2 | `REFLEXIVE_CHECK\|(5, 5)\|present` | equivalence_relation_generator.py, relation_check_generator.py |
| `REGEX_ACCEPT` | 1 | `REGEX_ACCEPT\|q61508_3, q61508_4` | regex_to_automaton_generator.py |
| `REGEX_SETUP` | 3 | `REGEX_SETUP\|(a or b)*(ab or ba)\|alphabet a,b\|canonical progress DFA` | regex_to_automaton_generator.py |
| `REGEX_STATE` | 2 | `REGEX_STATE\|q61508_0\|start` | regex_to_automaton_generator.py |
| `REGEX_TRANSITION` | 3 | `REGEX_TRANSITION\|q61508_0\|a\|q61508_1` | regex_to_automaton_generator.py |
| `REGION` | 2 | `REGION\|both\|{17, 19, 25}` | attribute_sorting_generator.py, venn_region_count_generator.py |
| `REGION_EQ` | 2 | `REGION_EQ\|A ∩ B\|30` | venn_region_count_generator.py |
| `REGION_MEASURE` | 3 | `REGION_MEASURE\|area\|12*11\|132` | vector_theorem_generator.py |
| `REGION_REWRITE` | 2 | `REGION_REWRITE\|0 <= y <= 14\|y/2 <= x <= 7` | double_integral_generator.py |
| `REG_ROW` | 3 | `REG_ROW\|x-x̄=-2\|y-ȳ=0\|product=0` | regression_generator.py |
| `REG_SETUP` | 2 | `REG_SETUP\|line ŷ = 59.1 + 0.3x\|predict ŷ at x = 6` | regression_generator.py |
| `REJECT` | 1, 2 | `REJECT\|x = −50` | cantor_pairing_generator.py, conditional_forms_generator.py, counterexample_search_generator.py, factor_trinomial_generator.py, knights_knaves_generator.py, log_conversion_generator.py, log_equation_generator.py, optimization_generator.py, polynomial_inequality_generator.py, radical_equation_generator.py, rational_equation_generator.py, rational_root_generator.py, set_builder_roster_generator.py, structure_isomorphism_generator.py |
| `RELAX` | 3 | `RELAX\|B->A\|update inf to 3\|via weight 3` | dijkstra_generator.py |
| `RELIABILITY` | 3 | `RELIABILITY\|series\|2/5 × 3/4 × 1/4 × 9/10\|27/400` | reliability_system_generator.py |
| `RELU` | 3 | `RELU\|z=3\|h=3\|deriv=1` | backprop_generator.py |
| `REL_ENERGY_FORMULA` | 1 | `REL_ENERGY_FORMULA\|w=(u+v)/(1+u*v), c=1` | relativistic_energy_generator.py |
| `REL_ENERGY_SETUP` | 3 | `REL_ENERGY_SETUP\|velocity_addition\|u=1/2\|v=1/3` | relativistic_energy_generator.py |
| `REL_FORMULA` | 1 | `REL_FORMULA\|ct_prime=gamma*(ct-beta*x), x_prime=gamma*(x-beta*ct)` | special_relativity_generator.py |
| `REL_FREQ` | 3 | `REL_FREQ\|amber\|33/57\|11/19` | experimental_probability_generator.py |
| `REL_PAIR` | 2 | `REL_PAIR\|(15, 15)\|same block` | equivalence_relation_generator.py |
| `REL_SETUP` | 2, 3 | `REL_SETUP\|A = {5, 11, 22, 40, 48, 51}\|R = {(5, 5), (5, 11), (5, 22), (5, 40), (11, 5), (11, 11), (11, 22), (11, 40), (22, 5), (22, 11), (22, 22), (22, 40), (40, 5), (40, 11), (40, 22), (40, 40), (48, 48), (48, 51), (51, 48), (51, 51)}` | equivalence_relation_generator.py, relation_check_generator.py, relation_closure_generator.py, relation_operations_generator.py, special_relativity_generator.py |
| `RENAME` | 2 | `RENAME\|∀w\|∀w1` | prenex_normal_form_generator.py |
| `RENORMALIZE` | 3 | `RENORMALIZE\|d\|(14/153)/(71/153)\|14/71` | probability_measure_generator.py |
| `REPEAT_DETECT` | 2 | `REPEAT_DETECT\|remainder 52 repeats\|repetend 228070175438596491` | repeating_decimal_generator.py |
| `REPRESENT` | 2 | `REPRESENT\|r ∣ j\|j = rh` | direct_proof_algebra_generator.py |
| `REP_DIM` | 2 | `REP_DIM\|8\|8` | young_tableaux_generator.py |
| `RESIDUAL` | 2 | `RESIDUAL\|y - X*beta\|[-3, 3, 3, -3]` | least_squares_generator.py |
| `RESIDUE` | 1, 3 | `RESIDUE\|-3` | contour_integral_generator.py, residue_generator.py |
| `RESIDUE_SETUP` | 2 | `RESIDUE_SETUP\|a=-3\|f=-3/(z+3) + 2 - 5(z+3)` | residue_generator.py |
| `RESIDUE_SUM` | 1 | `RESIDUE_SUM\|6` | contour_integral_generator.py |
| `RESID_SETUP` | 2 | `RESID_SETUP\|point (2, 56), line ŷ = 53.8 + 1.4x\|residual = observed − predicted` | regression_generator.py |
| `RESOLVE` | 3 | `RESOLVE\|C2\|C5\|P32736` | resolution_proof_generator.py |
| `RESTRICT_CHECK` | 3 | `RESTRICT_CHECK\|(a, 17)\|a in D=no\|skip` | relation_operations_generator.py |
| `RES_EMPTY` | 1 | `RES_EMPTY\|C7` | resolution_proof_generator.py |
| `RES_SETUP` | 1 | `RES_SETUP\|C1=(¬P89196), C2=(P32736 ∨ P89196), C3=(¬P93782), C4=(P32736), C5=(¬P32736)` | resolution_proof_generator.py |
| `RES_SKIP` | 3 | `RES_SKIP\|C1\|C2\|(P32736)` | resolution_proof_generator.py |
| `REVERSE` | 2 | `REVERSE\|0,1,0,0,1,0,1\|1010010` | base_arithmetic_generator.py, base_conversion_generator.py, bitwise_ops_generator.py |
| `REWRITE` | 1, 2 | `REWRITE\|5771 × 1\|5771` | antiderivative_generator.py, arc_length_generator.py, area_between_curves_generator.py, cardinal_arithmetic_generator.py, chain_rule_generator.py, circle_equation_generator.py, combinatory_logic_generator.py, completing_square_generator.py, complex_division_generator.py, complex_log_generator.py, complex_number_ops_generator.py, complex_quadratic_generator.py, confidence_interval_generator.py, conic_standard_form_generator.py, cramers_rule_generator.py, curve_analysis_generator.py, definite_integral_generator.py, derivative_limit_def_generator.py, derivative_power_rule_generator.py, derivative_product_quotient_generator.py, derivative_transcendental_generator.py, domain_range_generator.py, dot_product_generator.py, english_to_logic_generator.py, euler_formula_generator.py, evaluate_expression_generator.py, exponent_generator.py, exponent_mixed_rules_generator.py, exponential_equation_generator.py, factor_gcf_generator.py, factor_grouping_generator.py, factor_special_forms_generator.py, factor_trinomial_generator.py, frequency_table_generator.py, function_composition_generator.py, function_operations_generator.py, horner_evaluation_generator.py, implicit_diff_generator.py, improper_integral_generator.py, induction_verify_generator.py, integrating_factor_generator.py, integration_by_parts_generator.py, inverse_function_generator.py, lambda_reduction_generator.py, laurent_series_generator.py, lhopital_generator.py, limit_evaluation_generator.py, linear_approx_generator.py, linear_complex_generator.py, linear_fractional_generator.py, literal_equation_generator.py, log_conversion_generator.py, log_diff_higher_order_generator.py, log_equation_generator.py, log_properties_generator.py, logical_equivalence_laws_generator.py, logistic_growth_generator.py, master_theorem_generator.py, matrix_inverse_generator.py, method_of_moments_generator.py, mgf_generator.py, midpoint_generator.py, mle_generator.py, normal_approx_binomial_generator.py, normal_table_generator.py, ode_substitution_generator.py, operation_properties_generator.py, optimization_generator.py, order_of_operations_generator.py, ordinal_arithmetic_generator.py, parametric_calculus_generator.py, partial_fractions_generator.py, permutation_combination_generator.py, polar_parametric_generator.py, polynomial_zeros_generator.py, power_series_generator.py, prenex_normal_form_generator.py, quadratic_factoring_generator.py, quantifier_negation_generator.py, radical_add_sub_generator.py, radical_equation_generator.py, radical_multiply_generator.py, radical_rationalize_generator.py, radical_variable_simplify_generator.py, rational_equation_generator.py, rational_exponent_generator.py, rational_expr_add_sub_generator.py, rational_expr_mult_div_generator.py, rational_expr_simplify_generator.py, rational_function_features_generator.py, recursive_explicit_generator.py, regression_generator.py, related_rates_generator.py, right_triangle_trig_generator.py, row_reduction_generator.py, separable_ode_generator.py, separable_pde_generator.py, series_convergence_generator.py, series_solution_generator.py, set_algebra_laws_generator.py, set_expression_generator.py, set_operations_generator.py, simplify_expression_generator.py, sinusoid_features_generator.py, solid_revolution_generator.py, special_right_triangle_generator.py, special_solution_equation_generator.py, spin_half_generator.py, standard_form_conversion_generator.py, stars_and_bars_generator.py, synthetic_division_generator.py, tangent_line_generator.py, taxicab_geometry_generator.py, taylor_series_generator.py, trig_equation_generator.py, trig_identity_eval_generator.py, trig_identity_verify_generator.py, trig_six_functions_generator.py, u_substitution_generator.py, vector_ops_generator.py, z_transform_generator.py |
| `RG_SETUP` | 3 | `RG_SETUP\|one_loop\|alpha0=5/56\|beta=1,L=2/3` | running_coupling_generator.py |
| `RHO_ITER` | 4 | `RHO_ITER\|1\|x=83, y=108\|abs(r)=25\|gcd=1` | pollard_factorization_generator.py |
| `RICCI_ENTRY` | 2 | `RICCI_ENTRY\|R_phiphi\|1` | riemann_tensor_generator.py |
| `RIDGE_ENTRY` | 2 | `RIDGE_ENTRY\|K\|[[1,6], [6,36]]` | kernel_ridge_generator.py |
| `RIEMANN_ENTRY` | 2 | `RIEMANN_ENTRY\|R^phi_theta phi theta\|2601/22201` | riemann_tensor_generator.py |
| `RIEMANN_SETUP` | 2, 3 | `RIEMANN_SETUP\|f(x) = x^2 + 2 on [0, 4], n = 4\|left Riemann sum` | riemann_sum_generator.py, riemann_tensor_generator.py |
| `RK_COMBINE` | 2 | `RK_COMBINE\|k1+2k2+2k3+k4\|8511/125` | runge_kutta_generator.py |
| `RK_STAGE` | 3 | `RK_STAGE\|k1\|t=0\|y=6` | runge_kutta_generator.py |
| `RODRIGUES_FORM` | 2 | `RODRIGUES_FORM\|e^(theta K)\|I + sin(theta)K + (1-cos(theta))K^2` | lie_exponential_generator.py |
| `ROOT` | 1, 2, 3 | `ROOT\|100\|2\|10` | ac_circuit_generator.py, adam_step_generator.py, cholesky_generator.py, completing_square_generator.py, confidence_interval_generator.py, countability_bijection_generator.py, covariance_algebra_generator.py, de_moivre_generator.py, doppler_generator.py, embedding_similarity_generator.py, energy_conservation_generator.py, expectation_of_function_generator.py, factor_special_forms_generator.py, four_vector_generator.py, fundamental_form_generator.py, hypothesis_test_generator.py, invariant_mass_generator.py, joint_distribution_generator.py, ladder_operator_generator.py, layer_norm_generator.py, low_rank_approx_generator.py, matrix_norm_generator.py, metric_arc_length_generator.py, normal_approx_binomial_generator.py, or_formula_generator.py, orbital_mechanics_generator.py, planck_units_generator.py, pythag_hyp_generator.py, qr_decomposition_generator.py, quadratic_generator.py, quadratic_square_root_generator.py, radical_add_sub_generator.py, radical_multiply_generator.py, radical_rationalize_generator.py, radical_variable_simplify_generator.py, rational_equation_generator.py, rational_exponent_generator.py, regression_generator.py, relativistic_energy_generator.py, round_solids_generator.py, rv_transform_generator.py, schwarzschild_generator.py, shm_generator.py, svd_generator.py, svm_margin_generator.py, two_sample_test_generator.py |
| `ROOT_ANGLE` | 2 | `ROOT_ANGLE\|k=0\|0 deg` | de_moivre_generator.py |
| `ROOT_EXTRACT` | 2 | `ROOT_EXTRACT\|12` | exponent_generator.py |
| `ROOT_IDENTIFY` | 3 | `ROOT_IDENTIFY\|1728\|perfect_cube\|12` | exponent_generator.py |
| `ROOT_SETUP` | 1 | `ROOT_SETUP\|∛1728` | exponent_generator.py, radical_add_sub_generator.py, radical_multiply_generator.py, radical_rationalize_generator.py, radical_variable_simplify_generator.py |
| `ROOT_SIMPLIFY` | 1, 2 | `ROOT_SIMPLIFY\|6√19` | complex_quadratic_generator.py, distance_formula_generator.py, dot_product_generator.py, euler_formula_generator.py, exponent_generator.py, geometric_mean_generator.py, hypercube_counting_generator.py, polar_parametric_generator.py, vector_ops_generator.py |
| `ROSTER` | 2 | `ROSTER\|S\|{−49, −47, −45, −43, −41, −39}` | set_builder_roster_generator.py |
| `ROTATED_VECTOR` | 1 | `ROTATED_VECTOR\|(-3,-2,-1)` | quaternion_generator.py |
| `ROT_FORMULA` | 1 | `ROT_FORMULA\|I=I_cm+m*d^2` | rotational_dynamics_generator.py |
| `ROT_SETUP` | 3 | `ROT_SETUP\|parallel_axis\|I_cm=15, m=11\|d=4` | rotational_dynamics_generator.py |
| `ROUND` | 2 | `ROUND\|41/10\|4` | quantization_generator.py |
| `ROUNDTRIP_ERROR` | 2 | `ROUNDTRIP_ERROR\|sum_abs\|1/25` | quantization_generator.py |
| `ROUND_CHECK` | 3 | `ROUND_CHECK\|4\|8\|>=5` | place_value_rounding_generator.py |
| `ROUND_RESULT` | 2 | `ROUND_RESULT\|19148\|19150` | place_value_rounding_generator.py |
| `ROUTH_ROW` | 2 | `ROUTH_ROW\|s^3\|1, 3` | routh_hurwitz_generator.py |
| `ROUTH_SETUP` | 1 | `ROUTH_SETUP\|p(s)=s^3+5s^2+3s+60` | routh_hurwitz_generator.py |
| `ROW` | 2 | `ROW\|a=T, d=F, k=F\|F` | foundations_critic_generator.py |
| `ROW_ENTROPY` | 2 | `ROW_ENTROPY\|H0\|1` | entropy_rate_markov_generator.py |
| `ROW_OP` | 1, 2 | `ROW_OP\|R2 → R2 - 3·R1\|[0, 1, 1]` | row_reduction_generator.py, simplex_generator.py, subspace_basis_generator.py |
| `RREF_RESULT` | 2 | `RREF_RESULT\|RREF(A)\|[[1, 0, 1, 4], [0, 1, 3, 0], [0, 0, 0, 0]]` | subspace_basis_generator.py |
| `RSA_DECRYPT` | 2 | `RSA_DECRYPT\|54\|139` | rsa_generator.py |
| `RSA_ENCRYPT` | 2 | `RSA_ENCRYPT\|139\|54` | rsa_generator.py |
| `RSA_PRIVATE_KEY` | 1 | `RSA_PRIVATE_KEY\|d=45` | rsa_generator.py |
| `RSA_PUBLIC_KEY` | 2 | `RSA_PUBLIC_KEY\|n=145\|e=5` | rsa_generator.py |
| `RSA_SETUP` | 3 | `RSA_SETUP\|p=5\|q=29\|message=139` | rsa_generator.py |
| `RSQ_FORMULA` | 1 | `RSQ_FORMULA\|r^2 = Sxy^2/(Sxx·Syy)` | regression_generator.py |
| `RS_CORRECT` | 2 | `RS_CORRECT\|position=3\|[8,42,17,33]` | reed_solomon_generator.py |
| `RS_EVAL` | 2 | `RS_EVAL\|x=31\|0` | reed_solomon_generator.py |
| `RS_LINE` | 3 | `RS_LINE\|m0=22\|m1=41\|agree=3` | reed_solomon_generator.py |
| `RS_PAIR` | 2 | `RS_PAIR\|x=16,25\|y=8,42` | reed_solomon_generator.py |
| `RS_RECEIVED` | 1 | `RS_RECEIVED\|[8,42,39,33]` | reed_solomon_generator.py |
| `RS_SETUP` | 3 | `RS_SETUP\|F_67\|RS(4,2)\|points 16,25,44,64; one error allowed` | reed_solomon_generator.py |
| `RUNNING_TOTAL` | 3 | `RUNNING_TOTAL\|0\|1\|1` | function_properties_generator.py |
| `S` | 3 | `S\|632\|594\|38` | ac_circuit_generator.py, activation_generator.py, adam_step_generator.py, angle_defect_generator.py, angle_measure_generator.py, annuity_generator.py, arc_length_generator.py, area_between_curves_generator.py, arithmetic_coding_generator.py, arithmetic_sequence_generator.py, backprop_generator.py, bayesian_update_generator.py, bec_channel_generator.py, binomial_probability_generator.py, bisection_generator.py, black_scholes_generator.py, calendar_arithmetic_generator.py, calorimetry_generator.py, cantor_pairing_generator.py, casimir_force_generator.py, casimir_generator.py, channel_capacity_generator.py, cholesky_generator.py, circle_angle_generator.py, circle_equation_generator.py, classic_probability_puzzles_generator.py, collision_generator.py, commutator_generator.py, complement_probability_generator.py, complex_locus_generator.py, complex_log_generator.py, complex_number_ops_generator.py, complex_quadratic_generator.py, composite_arithmetic_generator.py, conditional_expectation_generator.py, confidence_interval_generator.py, continued_fraction_generator.py, continuous_distribution_generator.py, countability_bijection_generator.py, counting_classics_generator.py, covariance_algebra_generator.py, cramers_rule_generator.py, decimal_div_generator.py, definite_integral_generator.py, density_matrix_generator.py, derangement_generator.py, determinant_generator.py, dft_generator.py, discrete_uniform_bernoulli_generator.py, distance_formula_generator.py, distribution_of_sum_generator.py, doppler_generator.py, ellipse_features_generator.py, elliptic_curve_finite_field_generator.py, embedding_similarity_generator.py, entropy_generator.py, equilibrium_ice_generator.py, euler_characteristic_generator.py, euler_circuit_generator.py, euler_method_generator.py, expectation_of_function_generator.py, expected_value_generator.py, exponential_model_generator.py, extended_euclid_generator.py, finance_generator.py, finite_difference_generator.py, first_law_generator.py, five_number_summary_generator.py, four_vector_generator.py, fourier_series_generator.py, fractal_iteration_generator.py, fraction_op_generator.py, function_inner_product_generator.py, function_operations_generator.py, fundamental_counting_principle_generator.py, fundamental_form_generator.py, game_theory_generator.py, gaussian_curvature_generator.py, generating_function_generator.py, geometric_distribution_generator.py, geometric_sequence_generator.py, gradient_descent_generator.py, gradient_step_generator.py, graph_interpret_generator.py, graph_traversal_generator.py, hamiltonian_generator.py, heat_engine_generator.py, hermitian_check_generator.py, hydrogen_atom_generator.py, hyperbola_features_generator.py, hyperbolic_distance_generator.py, hyperbolic_function_generator.py, hypercube_counting_generator.py, hypergeometric_generator.py, hypothesis_test_generator.py, inclusion_exclusion_generator.py, index_gymnastics_generator.py, information_gain_generator.py, integrating_factor_generator.py, interpolation_generator.py, invariant_mass_generator.py, joint_distribution_generator.py, kernel_evaluation_generator.py, kernel_ridge_generator.py, kernel_validity_generator.py, kinematics_generator.py, kmeans_step_generator.py, knn_generator.py, kraft_inequality_generator.py, ladder_operator_generator.py, lagrangian_generator.py, layer_norm_generator.py, legendre_construction_generator.py, linear_simple_generator.py, linearity_of_expectation_generator.py, logistic_growth_generator.py, long_division_generator.py, low_rank_approx_generator.py, lp_corner_generator.py, lr_schedule_generator.py, manual_square_root_generator.py, markov_chain_generator.py, matrix_group_check_generator.py, matrix_inverse_generator.py, matrix_ops_generator.py, mean_value_theorem_generator.py, metric_arc_length_generator.py, mgf_generator.py, midpoint_generator.py, minkowski_interval_generator.py, mixed_number_operation_generator.py, mle_generator.py, mobius_transform_generator.py, modular_inverse_generator.py, mutual_information_generator.py, naive_bayes_generator.py, named_distribution_generator.py, newton_raphson_generator.py, newtons_laws_generator.py, normal_approx_binomial_generator.py, normal_table_generator.py, npv_irr_generator.py, ode_substitution_generator.py, ode_system_generator.py, optics_generator.py, optimization_generator.py, or_formula_generator.py, order_of_operations_generator.py, order_statistics_generator.py, parabola_features_generator.py, parametric_calculus_generator.py, particle_in_box_generator.py, pca_generator.py, percent_problem_generator.py, percent_word_problem_generator.py, permutation_group_generator.py, ph_calculation_generator.py, piecewise_evaluation_generator.py, pmf_cdf_quantile_generator.py, polar_parametric_generator.py, pollard_factorization_generator.py, positive_definite_generator.py, probability_addition_rule_generator.py, probability_axioms_finite_generator.py, probability_measure_generator.py, quadratic_residue_generator.py, quantization_generator.py, quantum_formula_generator.py, quaternion_generator.py, radical_add_sub_generator.py, radical_rationalize_generator.py, rational_expr_add_sub_generator.py, recurrence_generator.py, regression_generator.py, related_rates_generator.py, reliability_system_generator.py, riemann_sum_generator.py, riemann_tensor_generator.py, rotational_dynamics_generator.py, routh_hurwitz_generator.py, row_reduction_generator.py, rsa_generator.py, runge_kutta_generator.py, rv_transform_generator.py, schwarzschild_generator.py, second_order_ode_generator.py, segment_partition_generator.py, separable_pde_generator.py, series_convergence_generator.py, set_counting_generator.py, shm_generator.py, signal_arithmetic_generator.py, slope_two_points_generator.py, softmax_gradient_generator.py, solid_revolution_generator.py, special_relativity_generator.py, spherical_excess_generator.py, spin_half_generator.py, standing_wave_generator.py, stars_and_bars_generator.py, statics_generator.py, stereographic_generator.py, taxicab_geometry_generator.py, taylor_series_generator.py, telescoping_generator.py, temperature_conversion_generator.py, tip_bill_split_generator.py, totient_generator.py, transformation_generator.py, transportation_generator.py, triangle_solve_generator.py, trig_identity_eval_generator.py, trig_six_functions_generator.py, two_sample_test_generator.py, two_way_table_probability_generator.py, undetermined_coeff_generator.py, unit_circle_generator.py, vector_ops_generator.py, venn_probability_generator.py, venn_region_count_generator.py, z_score_generator.py |
| `SAMPLE_MOMENT` | 2 | `SAMPLE_MOMENT\|xbar\|59/4` | method_of_moments_generator.py |
| `SAMPLE_SIZE_FORMULA` | 1 | `SAMPLE_SIZE_FORMULA\|n = (z*/E)^2·p̂(1-p̂)` | confidence_interval_generator.py |
| `SAMPLE_SPACE` | 1, 2, 3 | `SAMPLE_SPACE\|ordered digit cards\|17, 18, 71, 78, 81, 87\|6` | classic_probability_puzzles_generator.py, sample_space_list_generator.py |
| `SA_BASES` | 2 | `SA_BASES\|2π(14)² = 2π × 196\|392π` | volume_3d_generator.py |
| `SA_FACES` | 3 | `SA_FACES\|top/bottom\|10 × 10\|100` | volume_3d_generator.py |
| `SA_FORMULA` | 1 | `SA_FORMULA\|SA = 2(lw + lh + wh)` | round_solids_generator.py, volume_3d_generator.py |
| `SA_LATERAL` | 2 | `SA_LATERAL\|2π × 14 × 35\|980π` | volume_3d_generator.py |
| `SA_SETUP` | 2 | `SA_SETUP\|rectangular_prism\|l=10, w=10, h=12` | volume_3d_generator.py |
| `SA_TOTAL` | 2 | `SA_TOTAL\|SA = 2(100 + 120 + 120)\|680` | round_solids_generator.py, volume_3d_generator.py |
| `SB_FORMULA` | 1 | `SB_FORMULA\|C(n+k-1, k-1)` | stars_and_bars_generator.py |
| `SB_SETUP` | 2 | `SB_SETUP\|x1+...+x10 = 28\|xi >= 0` | stars_and_bars_generator.py |
| `SCALE_DIV` | 3 | `SCALE_DIV\|1824\|57\|32` | scaling_generator.py |
| `SCALE_EXACT` | 2 | `SCALE_EXACT\|24*cos\|12sqrt2` | de_moivre_generator.py, euler_formula_generator.py |
| `SCALE_IDENTIFY` | 2 | `SCALE_IDENTIFY\|2.5 inches\|actual_dimension` | scaling_generator.py |
| `SCALE_MODE` | 3 | `SCALE_MODE\|λ = 1\|33\|33` | diagonalization_generator.py |
| `SCALE_MULT` | 3 | `SCALE_MULT\|2.5\|133\|332.5` | scaling_generator.py |
| `SCALE_SETUP` | 3 | `SCALE_SETUP\|1 inch\|133 feet\|133` | scaling_generator.py |
| `SCALE_SHIFT` | 2 | `SCALE_SHIFT\|1\|-8` | layer_norm_generator.py |
| `SCALING_COMPUTE` | 2 | `SCALING_COMPUTE\|6ND\|2040000000000000000` | scaling_law_generator.py |
| `SCALING_SETUP` | 3 | `SCALING_SETUP\|N=20000000\|D=17000000000\|F=18000000000000000` | scaling_law_generator.py |
| `SCAN` | 2 | `SCAN\|¬\|parenthesis depth 0` | wff_parsing_generator.py |
| `SCHWARZSCHILD_SETUP` | 3, 4 | `SCHWARZSCHILD_SETUP\|time_dilation\|r_s=162\|r=450` | schwarzschild_generator.py |
| `SCI_IDENTIFY` | 2 | `SCI_IDENTIFY\|7.81\|10` | exponent_generator.py |
| `SCI_MOVE_DECIMAL` | 2 | `SCI_MOVE_DECIMAL\|right\|10` | exponent_generator.py |
| `SCI_OPERATION` | 4 | `SCI_OPERATION\|multiply_coefficients\|4.4\|7.3\|32.12` | exponent_generator.py |
| `SCI_SETUP` | 1 | `SCI_SETUP\|(4.4 × 10^-4) × (7.3 × 10^12)` | exponent_generator.py |
| `SCORE_EQ` | 1 | `SCORE_EQ\|5/lambda=30` | mle_generator.py |
| `SEARCH_BOUNDS` | 3 | `SEARCH_BOUNDS\|iter 1\|lo=0\|hi=5` | algorithm_trace_generator.py |
| `SEARCH_STATE` | 2 | `SEARCH_STATE\|lo=0\|hi=1` | algorithm_trace_generator.py |
| `SECOND_DERIV_TEST` | 2 | `SECOND_DERIV_TEST\|f'' < 0 for x < -1, f'' > 0 for x > -1\|concavity changes` | curve_analysis_generator.py, optimization_generator.py |
| `SECOND_PARTIAL` | 2 | `SECOND_PARTIAL\|f_xx\|4` | hessian_classify_generator.py |
| `SECTION_FORMULA` | 1 | `SECTION_FORMULA\|P = (x1 + m/(m+n)·(x2 - x1), y1 + m/(m+n)·(y2 - y1))` | segment_partition_generator.py |
| `SECTION_SETUP` | 2 | `SECTION_SETUP\|A(5, 7), B(-16, 28); ratio 3:4 from A\|point P` | segment_partition_generator.py |
| `SECTOR_FORMULA` | 1 | `SECTOR_FORMULA\|A = (θ/360)·πr^2` | arc_sector_generator.py |
| `SELECT_MIN` | 2 | `SELECT_MIN\|B\|0` | dijkstra_generator.py |
| `SELECT_RELEVANT` | 2 | `SELECT_RELEVANT\|base = 47, rate = 15%\|ignore 44 (irrelevant)` | percent_word_problem_generator.py, proportion_word_problem_generator.py |
| `SEPARATE` | 1, 2 | `SEPARATE\|y^2 dy = x^2 dx` | ode_substitution_generator.py, separable_ode_generator.py, separable_pde_generator.py |
| `SEPARATOR` | 3 | `SEPARATOR\|13/9\|in L(3/2)\|not in L(√2)` | dedekind_cut_generator.py |
| `SEQ_APPLY` | 1 | `SEQ_APPLY\|a_27 = 1 + (27 - 1)·-8` | arithmetic_sequence_generator.py, geometric_sequence_generator.py, recursive_explicit_generator.py |
| `SEQ_FORMULA` | 1 | `SEQ_FORMULA\|a_n = a_1 + (n - 1)d` | arithmetic_sequence_generator.py, geometric_sequence_generator.py, recursive_explicit_generator.py |
| `SEQ_SETUP` | 2 | `SEQ_SETUP\|1, -7, -15, -23, ...\|27th term` | arithmetic_sequence_generator.py, geometric_sequence_generator.py, recursive_explicit_generator.py |
| `SERIES` | 1 | `SERIES\|G=G1*G2` | transfer_function_generator.py |
| `SERIES_ASSUME` | 2 | `SERIES_ASSUME\|y\|sum a_n x^n` | series_solution_generator.py |
| `SERIES_GROUP` | 2 | `SERIES_GROUP\|even powers\|cos(theta)I` | lie_exponential_generator.py |
| `SERIES_SETUP` | 2 | `SERIES_SETUP\|Σ (-1)^(n+1)·1/n^(33/8), n ≥ 1\|absolutely convergent, conditionally convergent, or divergent?` | legendre_construction_generator.py, power_series_generator.py, series_convergence_generator.py |
| `SERIES_TERM` | 3 | `SERIES_TERM\|n=0\|1\|1` | grassmann_generator.py |
| `SETUP` | 1, 2 | `SETUP\|assume e is the greatest integer; consider e + 1` | direct_proof_algebra_generator.py, induction_verify_generator.py |
| `SETUP_PERCENT_EQ` | 1 | `SETUP_PERCENT_EQ\|42159 = 1.41 * whole` | percent_problem_generator.py |
| `SET_SETUP` | 2, 3, 4 | `SET_SETUP\|S = {m, s, t}\|power set` | set_expression_generator.py, set_operations_generator.py |
| `SET_SIDE` | 2 | `SET_SIDE\|left\|∅` | counterexample_search_generator.py |
| `SHAPE` | 1 | `SHAPE\|universal restriction → implication` | english_to_logic_generator.py |
| `SHIFT` | 1, 2 | `SHIFT\|yi = xi - 1\|y1+...+y4 = 21` | algorithm_trace_generator.py, recurrence_generator.py, stars_and_bars_generator.py, z_transform_generator.py |
| `SHM_FORMULA` | 1 | `SHM_FORMULA\|omega^2=g/L` | shm_generator.py |
| `SHM_SETUP` | 3 | `SHM_SETUP\|pendulum_period\|g=10\|L=5/2` | shm_generator.py |
| `SHORTEST` | 2 | `SHORTEST\|(11,-4)\|norm^2=137` | lll_reduction_generator.py |
| `SIDE` | 2 | `SIDE\|left\|∉` | set_identity_membership_table_generator.py |
| `SIGFIG_ROUND` | 3 | `SIGFIG_ROUND\|19008\|2 significant figures\|1.9 × 10^4` | fermi_estimation_generator.py |
| `SIGMA_EXPAND` | 1 | `SIGMA_EXPAND\|(-56) + (-44) + (-32) + (-20) + (-8) + 4` | sigma_notation_generator.py |
| `SIGMA_SETUP` | 2 | `SIGMA_SETUP\|Σ_(k=-4)^(1) (12k - 8)\|expand and evaluate` | sigma_notation_generator.py |
| `SIGMA_TERM` | 3 | `SIGMA_TERM\|k=-4\|12(-4) - 8\|-56` | sigma_notation_generator.py |
| `SIGN` | 3 | `SIGN\|left\|-2\|negative` | bisection_generator.py |
| `SIGNAL_SETUP` | 2, 3 | `SIGNAL_SETUP\|sampling\|f_max=599 Hz\|f_s=2466 Hz` | signal_arithmetic_generator.py |
| `SIGN_CHART` | 2 | `SIGN_CHART\|critical values\|-4, 4` | polynomial_inequality_generator.py |
| `SIGN_RULE` | 2 | `SIGN_RULE\|cos, quadrant IV\|positive` | trig_equation_generator.py, trig_identity_eval_generator.py, trig_six_functions_generator.py, unit_circle_generator.py |
| `SIGN_TEST` | 4 | `SIGN_TEST\|(-inf, -8)\|y = -9\|f(y) = -126 (negative)\|down` | stability_generator.py |
| `SIMILAR_APPLY` | 3 | `SIMILAR_APPLY\|6\|4\|24` | scaling_generator.py |
| `SIMILAR_SCALE` | 3 | `SIMILAR_SCALE\|20\|5\|4` | scaling_generator.py |
| `SIMILAR_SETUP` | 3 | `SIMILAR_SETUP\|parallelogram\|5,6\|20 (others unknown)` | scaling_generator.py |
| `SIMPLEX_SETUP` | 3 | `SIMPLEX_SETUP\|max z=8x+5y\|x<=10\|y<=18` | simplex_generator.py |
| `SIM_SETUP` | 2 | `SIM_SETUP\|△ABC ~ △DEF; AB = 20, DE = 25, BC = 32\|find EF` | similar_triangles_generator.py |
| `SIN` | 2 | `SIN\|pi/6\|1/2` | positional_encoding_generator.py |
| `SINGULAR_VALUE` | 2 | `SINGULAR_VALUE\|sigma1\|17` | low_rank_approx_generator.py |
| `SINUSOID_SETUP` | 2 | `SINUSOID_SETUP\|y = 4cos(6(x - 45°)) + 3\|amplitude, period, phase shift, midline` | sinusoid_features_generator.py |
| `SIZE_REDUCE` | 2 | `SIZE_REDUCE\|b2=(-14, 9)\|b2-1b1=(-12, 1)` | lll_reduction_generator.py |
| `SLOPE_CALC` | 2 | *(not observed in sampling)* | equation_from_two_points_generator.py |
| `SLOPE_FORMULA` | 1 | `SLOPE_FORMULA\|m = (y2 - y1) / (x2 - x1)` | equation_from_two_points_generator.py, regression_generator.py, slope_two_points_generator.py |
| `SLOPE_INT_IDENTIFY` | 2 | `SLOPE_INT_IDENTIFY\|Slope (m)\|-95` | slope_intercept_form_generator.py |
| `SLOPE_INT_MATCH` | 2 | `SLOPE_INT_MATCH\|Compare to Slope-Intercept Form\|y = mx + b` | slope_intercept_form_generator.py |
| `SLOPE_INT_SETUP` | 1 | `SLOPE_INT_SETUP\|y = -55 - 95x` | slope_intercept_form_generator.py |
| `SLOPE_RESULT` | 1 | `SLOPE_RESULT\|2` | equation_from_two_points_generator.py |
| `SLOPE_SETUP` | 2 | `SLOPE_SETUP\|(0, 6)\|(1, 6)` | slope_two_points_generator.py |
| `SLOPE_SUBST` | 1 | `SLOPE_SUBST\|m = (6 - 6) / (1 - 0)` | equation_from_two_points_generator.py, slope_two_points_generator.py |
| `SLOPE_UNDEFINED` | 1 | `SLOPE_UNDEFINED\|Division by zero` | slope_two_points_generator.py |
| `SOFTMAX_EXP` | 2 | `SOFTMAX_EXP\|1,1\|1` | attention_generator.py, softmax_gradient_generator.py |
| `SOFTMAX_PROB` | 2 | `SOFTMAX_PROB\|1\|4/13` | softmax_gradient_generator.py |
| `SOFTMAX_SETUP` | 3 | `SOFTMAX_SETUP\|z=(2*ln(4),2*ln(7),2*ln(2))\|T=2\|target=2` | softmax_gradient_generator.py |
| `SOFTMAX_WEIGHT` | 2 | `SOFTMAX_WEIGHT\|1,1\|1/2` | attention_generator.py |
| `SOLUTIONS` | 2 | `SOLUTIONS\|cos x = √3/2\|30°, 330°, 390°, 690°, 750°, 1050°, 1110°, 1410°, 1470°, 1770°, 1830°, 2130°, 2190°, 2490°, 2550°, 2850°, 2910°, 3210°, 3270°, 3570°, 3630°, 3930°, 3990°, 4290°, 4350°, 4650°, 4710°, 5010°, 5070°, 5370°, 5430°, 5730°, 5790°, 6090°, 6150°, 6450°, 6510°, 6810°, 6870°, 7170°, 7230°, 7530°, 7590°, 7890°, 7950°, 8250°, 8310°, 8610°, 8670°, 8970°, 9030°, 9330°, 9390°, 9690°, 9750°, 10050°, 10110°, 10410°` | trig_equation_generator.py |
| `SOLUTION_FORMULA` | 1 | `SOLUTION_FORMULA\|M_final=(Ma*Va+Mb*Vb)/(Va+Vb)` | solution_chem_generator.py |
| `SOLUTION_SETUP` | 3 | `SOLUTION_SETUP\|mixing_molarity\|Ma=9/2, Va=194\|Mb=5/2, Vb=54` | solution_chem_generator.py |
| `SOLVE_CONST` | 2 | `SOLVE_CONST\|C1 = -3\|C2 = -2` | ode_system_generator.py, second_order_ode_generator.py, undetermined_coeff_generator.py |
| `SOLVE_U` | 2 | `SOLVE_U\|e^(-4x)u = e^(-4x) + C\|u = 1 + Ce^(4x)` | ode_substitution_generator.py |
| `SOLVE_Y` | 2 | `SOLVE_Y\|e^(4x)y = 3e^(4x) + C\|y = 3 + Ce^(-4x)` | integrating_factor_generator.py, laplace_ivp_generator.py, ode_substitution_generator.py |
| `SOL_ENTRY` | 3 | `SOL_ENTRY\|x1(t)\|(e^(-6t))*6 + (0)*0\|6*e^(-6t)` | matrix_exponential_generator.py |
| `SOL_FORM` | 1, 2 | `SOL_FORM\|y = (C1 + C2x)e^(4x)` | ode_system_generator.py, second_order_ode_generator.py, undetermined_coeff_generator.py, variation_parameters_generator.py |
| `SORT` | 2 | `SORT\|9,15,20,2,1\|1,2,9,15,20` | five_number_summary_generator.py, simple_stats_generator.py |
| `SORT_EDGES` | 1 | `SORT_EDGES\|BD=1, BC=3, AF=9, AE=13, AB=15, DF=17, CE=19` | mst_generator.py |
| `SPECIAL_SOLUTION` | 2 | `SPECIAL_SOLUTION\|16 = 11\|contradiction: no value of x works` | radical_equation_generator.py, special_solution_equation_generator.py |
| `SPEED` | 2, 3 | `SPEED\|sqrt(a^2 + b^2)\|sqrt(3^2 + 4^2)\|5` | curve_geometry_generator.py |
| `SPHERICAL_BOUNDS` | 2 | `SPHERICAL_BOUNDS\|rho\|0..9` | triple_integral_generator.py |
| `SPHERICAL_CONVERT` | 2 | `SPHERICAL_CONVERT\|5 dV\|5*rho^2*sin(phi) drho dphi dtheta` | triple_integral_generator.py |
| `SPHERICAL_COSINES` | 1 | `SPHERICAL_COSINES\|cos(c)=sin(lat1)sin(lat2)+cos(lat1)cos(lat2)cos(dlon)` | great_circle_generator.py |
| `SPHERICAL_COSINE_LAW` | 1 | `SPHERICAL_COSINE_LAW\|cos(a)=cos(b)cos(c)+sin(b)sin(c)cos(A)` | spherical_triangle_generator.py |
| `SPHERICAL_EXCESS_SETUP` | 2 | `SPHERICAL_EXCESS_SETUP\|R=20\|angles=60,135,45` | spherical_excess_generator.py |
| `SPHERICAL_SINE_LAW` | 1 | `SPHERICAL_SINE_LAW\|sin(A)/sin(a)=sin(B)/sin(b)` | spherical_triangle_generator.py |
| `SPHERICAL_TRIANGLE_SETUP` | 2 | `SPHERICAL_TRIANGLE_SETUP\|a=45 deg, b=135 deg, A=45 deg\|find sin(B)` | spherical_triangle_generator.py |
| `SPIN_COMPONENT` | 2 | `SPIN_COMPONENT\|row=1\|63/65` | spin_half_generator.py |
| `SPIN_SETUP` | 3 | `SPIN_SETUP\|measurement_probability\|axis=x\|psi=[-15/17,-8/17]` | spin_half_generator.py |
| `SPLIT_MIDDLE` | 2 | `SPLIT_MIDDLE\|11y = 9y + 2y\|3y^2 + 9y + 2y + 6` | factor_trinomial_generator.py |
| `SPLIT_SETUP` | 3 | `SPLIT_SETUP\|region\|left pos=3, neg=5\|right pos=8, neg=0` | information_gain_generator.py |
| `SQRT_BOTH_SIDES` | 2 | `SQRT_BOTH_SIDES\|x^2 = 16\|x = ±4` | completing_square_generator.py, quadratic_square_root_generator.py, rational_equation_generator.py |
| `SQRT_DIGIT` | 2 | `SQRT_DIGIT\|5\|root = 5` | manual_square_root_generator.py |
| `SQRT_NEG` | 2 | `SQRT_NEG\|√(-144)\|12i` | complex_quadratic_generator.py, polynomial_zeros_generator.py |
| `SQRT_SETUP` | 2 | `SQRT_SETUP\|N = 262144\|groups 26, 21, 44` | manual_square_root_generator.py |
| `SQRT_TRIAL` | 3 | `SQRT_TRIAL\|x = 5\|(0 + 5)*5 = 25\|fits` | manual_square_root_generator.py |
| `SQUARE_BOTH_SIDES` | 2 | `SQUARE_BOTH_SIDES\|√(x + 73) = x + 1\|x + 73 = (x + 1)^2` | radical_equation_generator.py |
| `SQUARE_FACTOR` | 3 | `SQUARE_FACTOR\|405\|81 × 5\|81` | radical_add_sub_generator.py, radical_multiply_generator.py, radical_rationalize_generator.py, radical_variable_simplify_generator.py |
| `SQUARE_TEST` | 3 | `SQUARE_TEST\|49\|7^2 = 49\|perfect square` | discriminant_generator.py |
| `STABILITY` | 3 | `STABILITY\|y=-8\|left down, right up\|unstable` | stability_generator.py |
| `STANDING_BOUNDARY` | 1 | `STANDING_BOUNDARY\|open-open pipe allows n=1,2,3,...` | standing_wave_generator.py |
| `STANDING_FORMULA` | 1 | `STANDING_FORMULA\|lambda=2L/n, f=v/lambda` | standing_wave_generator.py |
| `STANDING_SETUP` | 3 | `STANDING_SETUP\|open_pipe\|n=3\|L=11, v=188` | standing_wave_generator.py |
| `STATEMENT_EVAL` | 3 | `STATEMENT_EVAL\|Pia says Iris and Oona are different types\|F\|contradiction` | knights_knaves_generator.py |
| `STATICS_FORMULA` | 1 | `STATICS_FORMULA\|sum_tau_left=0 => RB*L=W*x` | statics_generator.py |
| `STATICS_SETUP` | 3 | `STATICS_SETUP\|supported_beam\|W=188, L=19\|x=8` | statics_generator.py |
| `STATIONARY` | 2 | `STATIONARY\|pi0=1/3\|pi1=2/3` | entropy_rate_markov_generator.py |
| `STAT_ABS_DEV` | 2 | `STAT_ABS_DEV\|-5\|5` | statistics_generator.py |
| `STAT_AVERAGE` | 2 | `STAT_AVERAGE\|(74 + 91) / 2\|82.5` | statistics_generator.py |
| `STAT_COUNT` | 1 | `STAT_COUNT\|5` | statistics_generator.py |
| `STAT_DEVIATION` | 3 | `STAT_DEVIATION\|42\|47\|-5` | statistics_generator.py |
| `STAT_DIVIDE` | 2 | `STAT_DIVIDE\|305 / 5\|61` | statistics_generator.py |
| `STAT_FREQUENCY` | 2 | `STAT_FREQUENCY\|21\|3` | statistics_generator.py |
| `STAT_MAD` | 3 | `STAT_MAD\|42\|7\|6` | statistics_generator.py |
| `STAT_MAX` | 1 | `STAT_MAX\|92` | statistics_generator.py |
| `STAT_MEAN` | 2 | `STAT_MEAN\|329 / 7\|47` | statistics_generator.py |
| `STAT_MIDDLE` | 2 | `STAT_MIDDLE\|position 4\|53` | statistics_generator.py |
| `STAT_MIN` | 1 | `STAT_MIN\|11` | statistics_generator.py |
| `STAT_MODE` | 2 | `STAT_MODE\|21 and 63\|3` | statistics_generator.py |
| `STAT_ORDER` | 1 | `STAT_ORDER\|23, 34, 39, 53, 57, 60, 86` | statistics_generator.py |
| `STAT_RANGE` | 2 | `STAT_RANGE\|92 - 11\|81` | statistics_generator.py |
| `STAT_SETUP` | 1 | `STAT_SETUP\|61, 16, 78, 78, 72` | statistics_generator.py |
| `STAT_SUM` | 2 | `STAT_SUM\|61 + 16 + 78 + 78 + 72\|305` | statistics_generator.py |
| `STD` | 1 | `STD\|5` | layer_norm_generator.py |
| `STEADY_EQUATION` | 2 | `STEADY_EQUATION\|pi0*pi01=pi1*pi10\|pi0+pi1=1` | markov_chain_generator.py |
| `STEPPING_STONE` | 2 | `STEPPING_STONE\|enter x21\|+x21 -x22 +x12 -x11` | transportation_generator.py |
| `STEREO_SETUP` | 3, 4 | `STEREO_SETUP\|plane_to_sphere\|u=-5/2\|v=-5` | stereographic_generator.py |
| `STIRLING_CELL` | 3 | `STIRLING_CELL\|S(1,1)\|1×0+1\|1` | set_counting_generator.py |
| `STMT_EVAL` | 3 | `STMT_EVAL\|p\|6 is prime\|F` | logical_connective_eval_generator.py |
| `STOICH_RATIO` | 2 | `STOICH_RATIO\|N2->NH3\|2/1=2` | gas_stoichiometry_generator.py, stoichiometry_generator.py |
| `STOICH_SETUP` | 2, 3 | `STOICH_SETUP\|limiting_reagent\|N2 + 3 H2 -> 2 NH3\|given=N2=5 mol, H2=29 mol` | stoichiometry_generator.py |
| `STRUCTURE_CONSTANT` | 3 | `STRUCTURE_CONSTANT\|epsilon_zyx\|-1\|140iJx` | structure_constant_generator.py |
| `STRUCTURE_SETUP` | 3 | `STRUCTURE_SETUP\|A=-7Jz\|B=20Jy\|epsilon_zyx=-1` | structure_constant_generator.py |
| `SU3_SETUP` | 2 | `SU3_SETUP\|left=3\|right=3bar` | young_tableaux_generator.py |
| `SUBEXPR` | 2 | `SUBEXPR\|A ∪ B\|{c, d}` | probability_measure_generator.py, set_expression_generator.py, set_operations_generator.py |
| `SUBGROUP` | 2 | `SUBGROUP\|H={1, 38}\|size 2` | coset_generator.py |
| `SUBGROUP_ELEM` | 2 | `SUBGROUP_ELEM\|k=1\|7` | coset_generator.py, cyclic_group_generator.py |
| `SUBGROUP_START` | 2 | `SUBGROUP_START\|H=<38>\|identity 1` | coset_generator.py |
| `SUBPROOF_CLOSE` | 3 | `SUBPROOF_CLOSE\|→I\|lines 2–3\|j → p` | natural_deduction_generator.py |
| `SUBPROOF_OPEN` | 2 | `SUBPROOF_OPEN\|assume\|j` | natural_deduction_generator.py |
| `SUBSET_CHECK` | 3 | `SUBSET_CHECK\|{26}\|subset of A?\|yes` | set_membership_subset_generator.py |
| `SUBSET_SIZE` | 2 | `SUBSET_SIZE\|0\|∅` | set_operations_generator.py |
| `SUBST` | 2, 3 | `SUBST\|x\|4\|5(4)-5y-4` | arc_length_generator.py, chain_rule_generator.py, curve_analysis_generator.py, derivative_limit_def_generator.py, evaluate_expression_generator.py, function_composition_generator.py, function_evaluation_generator.py, function_operations_generator.py, function_table_generator.py, implicit_diff_generator.py, integrating_factor_generator.py, legendre_construction_generator.py, lhopital_generator.py, limit_evaluation_generator.py, line_integral_generator.py, linear_approx_generator.py, log_diff_higher_order_generator.py, logistic_growth_generator.py, mean_value_theorem_generator.py, ode_substitution_generator.py, optimization_generator.py, parametric_calculus_generator.py, partial_fractions_generator.py, piecewise_evaluation_generator.py, polar_parametric_generator.py, power_series_generator.py, recursive_explicit_generator.py, related_rates_generator.py, remainder_factor_theorem_generator.py, second_order_ode_generator.py, separable_ode_generator.py, tangent_line_generator.py, taylor_series_generator.py, trig_equation_generator.py, u_substitution_generator.py, undetermined_coeff_generator.py |
| `SUBSTITUTE` | 2, 3 | `SUBSTITUTE\|p → (q → p)\|p := (a ∨ c) → g; q := (n → c) → (h ∨ e)\|((a ∨ c) → g) → (((n → c) → (h ∨ e)) → ((a ∨ c) → g))` | hilbert_axiom_derivation_generator.py, lambda_reduction_generator.py |
| `SUBSTITUTION` | 2 | `SUBSTITUTION\|u = y^(-1)\|u' = -y^(-2) dy/dx` | ode_substitution_generator.py |
| `SUB_COL` | 3 | `SUB_COL\|col_1\|5-6-borrow0\|->9 (borrow_out 1)` | multi_digit_subtraction_generator.py |
| `SUM` | 2, 3 | `SUM\|20 + 16 + 26\|62` | bayesian_update_generator.py, experimental_probability_generator.py, likelihood_language_generator.py, method_of_moments_generator.py, mle_generator.py, random_digit_simulation_generator.py, regression_generator.py, reliability_system_generator.py |
| `SUM_ORDER` | 2 | `SUM_ORDER\|Σ i^8\|n^9` | master_theorem_generator.py |
| `SUPPORT` | 2 | `SUPPORT\|0<=x<=28\|0<=y<=784` | rv_transform_generator.py |
| `SUPPORT_TERM` | 2 | `SUPPORT_TERM\|1\|(-8,0)` | svm_margin_generator.py |
| `SVM_SETUP` | 3 | `SVM_SETUP\|x1=(8,0),y1=-1,alpha1=1\|x2=(0,-15),y2=-1,alpha2=1\|b=-1,x=(4,-1)` | svm_margin_generator.py |
| `SWAP` | 2 | `SWAP\|norm b2=137\|norm b1=185` | lll_reduction_generator.py |
| `SWAP_VARS` | 1 | `SWAP_VARS\|x = y^3 - 7` | inverse_function_generator.py |
| `SYMBOL_CODE` | 2 | `SYMBOL_CODE\|(\|3` | godel_numbering_generator.py |
| `SYMMETRIC_CHECK` | 3 | `SYMMETRIC_CHECK\|(5, 5)\|reverse (5, 5)\|present` | equivalence_relation_generator.py, relation_check_generator.py |
| `SYMMETRY` | 2 | `SYMMETRY\|odd function\|a0=0, a_n=0` | fourier_series_generator.py |
| `SYNDIV_SETUP` | 2 | `SYNDIV_SETUP\|2x^3 + 5x^2 - 28x - 15\|r = -5` | polynomial_zeros_generator.py, synthetic_division_generator.py |
| `SYNDROME_CALC` | 2 | `SYNDROME_CALC\|s1=b1 xor b3 xor b5 xor b7\|0 xor 1 xor 0 xor 0=1` | hamming_code_generator.py |
| `SYNDROME_VALUE` | 2 | `SYNDROME_VALUE\|s1=1, s2=1, s4=1\|position=7` | hamming_code_generator.py |
| `SYN_DROP` | 1 | `SYN_DROP\|2` | horner_evaluation_generator.py, polynomial_zeros_generator.py, synthetic_division_generator.py |
| `SYN_ROW` | 1 | `SYN_ROW\|2, -5, -3, 0` | polynomial_zeros_generator.py, synthetic_division_generator.py |
| `SYS_ADD` | 1 | `SYS_ADD\|Add equations: -5x = 50` | systems_elimination_generator.py |
| `SYS_EQ_NEW` | 1 | `SYS_EQ_NEW\|New equation with x only` | systems_substitution_generator.py |
| `SYS_ISOLATE` | 2 | `SYS_ISOLATE\|Isolate x in Eq 1\|x = 2y - 8` | systems_substitution_generator.py |
| `SYS_MULT` | 1 | `SYS_MULT\|Eq1 * -4, Eq2 * -1` | systems_elimination_generator.py |
| `SYS_REWRITE` | 2 | `SYS_REWRITE\|-4x + 12y = -20\|-x - 12y = 70` | systems_elimination_generator.py |
| `SYS_SETUP` | 2 | `SYS_SETUP\|y = -5x + 1\|-x + 4y = 4` | systems_elimination_generator.py, systems_substitution_generator.py |
| `SYS_SUBST` | 1 | `SYS_SUBST\|Substitute (-5x + 1) for y in Eq 2` | systems_substitution_generator.py |
| `SYS_SUBST_BACK` | 1 | `SYS_SUBST_BACK\|Substitute x=0 into Eq 1` | systems_elimination_generator.py, systems_substitution_generator.py |
| `TABLEAU` | 2, 3 | `TABLEAU\|initial\|s1: x + s1 = 10\|s2: y + s2 = 18` | simplex_generator.py |
| `TABLEAU_ROOT` | 1 | `TABLEAU_ROOT\|(x ∧ (¬x ∧ ¬x)) ∧ (r ∧ (r ∧ ¬r))` | semantic_tableau_generator.py |
| `TABLEAU_RULE` | 3 | `TABLEAU_RULE\|3 x 3bar\|box plus antibox gives adjoint plus singlet\|8 + 1` | young_tableaux_generator.py |
| `TABLE_CELL` | 2 | `TABLE_CELL\|format=print, genre=fiction\|44` | independence_check_generator.py, two_way_table_probability_generator.py |
| `TABLE_COMPARE` | 1, 2 | `TABLE_COMPARE\|differ\|x ∈ C, x ∉ M, x ∈ V` | foundations_critic_generator.py, set_identity_membership_table_generator.py |
| `TABLE_ENTRY` | 2 | `TABLE_ENTRY\|h(0)\|6` | euler_method_generator.py, function_table_generator.py, taylor_series_generator.py |
| `TABLE_LOOKUP` | 2 | `TABLE_LOOKUP\|F(49)\|5/8` | de_moivre_generator.py, dot_product_generator.py, euler_formula_generator.py, function_evaluation_generator.py, lie_exponential_generator.py, normal_approx_binomial_generator.py, normal_table_generator.py, pascal_triangle_generator.py, pmf_cdf_quantile_generator.py, polar_parametric_generator.py, right_triangle_trig_generator.py, triangle_solve_generator.py, trig_equation_generator.py, trig_identity_eval_generator.py, unit_circle_generator.py |
| `TABLE_TOTAL` | 2 | `TABLE_TOTAL\|grand\|44 + 36 + 21 + 79 = 180` | two_way_table_probability_generator.py |
| `TALLY` | 2 | `TALLY\|amber\|33` | experimental_probability_generator.py |
| `TANGENT_PLANE` | 2 | `TANGENT_PLANE\|z = z0 + fx(x-a) + fy(y-b)\|z = 136 + 32*(x - 2) + 49*(y - 4)` | gradient_generator.py |
| `TARGET_STATE` | 2 | `TARGET_STATE\|J=1\|M=-1` | clebsch_gordan_generator.py |
| `TAYLOR_FORMULA` | 1 | `TAYLOR_FORMULA\|P_n(x) = Σ f^(k)(a)/k!·(x - a)^k` | taylor_series_generator.py |
| `TAYLOR_SETUP` | 2 | `TAYLOR_SETUP\|f(x) = ln(1 + x), center a = 0\|Maclaurin polynomial of degree 3` | taylor_series_generator.py |
| `TELESCOPE_CANCEL` | 2 | `TELESCOPE_CANCEL\|all middle factors cancel\|39/64` | telescoping_generator.py |
| `TELE_SETUP` | 1 | `TELE_SETUP\|Π k=39..63 k/(k+1)` | telescoping_generator.py |
| `TEMP_SCALE` | 2 | `TEMP_SCALE\|z1/T\|ln(4)` | softmax_gradient_generator.py |
| `TENSOR_ENTRY` | 2 | `TENSOR_ENTRY\|C_11\|-3` | einstein_summation_generator.py, index_raising_generator.py |
| `TENSOR_RULE` | 1 | `TENSOR_RULE\|diag(a,b) tensor diag(c,d)=diag(ac,ad,bc,bd)` | tensor_product_generator.py |
| `TENSOR_SETUP` | 3 | `TENSOR_SETUP\|A=diag(-4,3)\|B=diag(-2,0)\|u=[-2,4], v=[2,-1]` | tensor_product_generator.py |
| `TENSOR_STATE` | 2 | `TENSOR_STATE\|u tensor v\|[-4,2,8,-4]` | tensor_product_generator.py |
| `TERM` | 2, 3 | `TERM\|4 makes\|(7/10)^4\|2401/10000` | binomial_probability_generator.py, random_digit_simulation_generator.py |
| `TERMS` | 1 | `TERMS\|x[0..3]=[31,62,124,248]` | z_transform_generator.py |
| `TEST_CHOOSE` | 2 | `TEST_CHOOSE\|alternating series test\|signs alternate` | power_series_generator.py, series_convergence_generator.py |
| `TEST_STAT_FORMULA` | 1 | `TEST_STAT_FORMULA\|t = (x̄ - μ0)/(s/√n)` | hypothesis_test_generator.py, two_sample_test_generator.py |
| `TF_SETUP` | 3 | `TF_SETUP\|ode\|y''+16y'+48y=3x'+33x\|zero initial conditions` | transfer_function_generator.py |
| `THEOREM` | 1, 2 | `THEOREM\|quadratic formula\|t = (-b ± √(b^2 - 4ac))/(2a)` | angle_defect_generator.py, circle_angle_generator.py, gauss_bonnet_generator.py, geometric_mean_generator.py, logistic_growth_generator.py, mean_value_theorem_generator.py, parametric_calculus_generator.py, polar_parametric_generator.py, quadratic_generator.py, rational_root_generator.py, remainder_factor_theorem_generator.py, series_convergence_generator.py, special_right_triangle_generator.py, spherical_excess_generator.py, taylor_series_generator.py, triangle_solve_generator.py, trig_identity_eval_generator.py, trig_six_functions_generator.py |
| `THEOREM_REWRITE` | 2 | `THEOREM_REWRITE\|circulation\|double integral of Q_x - P_y` | vector_theorem_generator.py |
| `THEOREM_SETUP` | 3 | `THEOREM_SETUP\|Green\|F=<0, -8*x>\|rectangle 12 by 11` | vector_theorem_generator.py |
| `THETA` | 2 | `THETA\|min(16,20)\|16` | transportation_generator.py |
| `THROUGHPUT` | 2 | `THROUGHPUT\|tokens_per_second\|150000000` | scaling_law_generator.py |
| `TIME_COMPONENT` | 2 | `TIME_COMPONENT\|k=1\|-1+i` | braket_generator.py |
| `TIME_DERIV` | 2 | `TIME_DERIV\|d/dt(m*xdot)\|m*xddot` | lagrangian_generator.py |
| `TIME_EVOLVE` | 2 | `TIME_EVOLVE\|U psi\|[-1+i,-i,2]` | braket_generator.py |
| `TM_CONFIG` | 4 | `TM_CONFIG\|step 0\|state=q0\|head=0\|tape=1111` | turing_machine_trace_generator.py |
| `TM_HALT` | 2 | `TM_HALT\|step 5\|halted` | turing_machine_trace_generator.py |
| `TM_MOVE` | 3 | `TM_MOVE\|0\|R\|1` | turing_machine_trace_generator.py |
| `TM_READ` | 2 | `TM_READ\|head=0\|1` | turing_machine_trace_generator.py |
| `TM_RULE` | 2 | `TM_RULE\|q0,1\|q0,1,R` | turing_machine_trace_generator.py |
| `TM_SETUP` | 3 | `TM_SETUP\|unary_increment\|input=1111\|limit=7` | turing_machine_trace_generator.py |
| `TM_WRITE` | 2 | `TM_WRITE\|head=0\|1` | turing_machine_trace_generator.py |
| `TOPO_AVAILABLE` | 1 | `TOPO_AVAILABLE\|A` | graph_traversal_generator.py |
| `TOPO_PICK` | 2 | `TOPO_PICK\|available {1, 2, 10}\|pick 1` | partial_order_generator.py |
| `TOPO_READY` | 1 | `TOPO_READY\|B` | graph_traversal_generator.py |
| `TOPO_SELECT` | 2 | `TOPO_SELECT\|A\|A` | graph_traversal_generator.py |
| `TOTAL_PROB_FORMULA` | 1 | `TOTAL_PROB_FORMULA\|P(second target) = Σ P(cause)·P(second target given cause)` | law_of_total_probability_generator.py |
| `TOTAL_PROB_TERM` | 3 | `TOTAL_PROB_TERM\|first yellow\|19/47 × 37/93\|703/4371` | law_of_total_probability_generator.py |
| `TOTAL_VARIANCE` | 2 | `TOTAL_VARIANCE\|Var(S) = E[N]Var(B) + Var(N)(E[B])²\|15543/16384` | conditional_expectation_generator.py |
| `TOTIENT_RESULT` | 2 | `TOTIENT_RESULT\|phi(12)\|4` | totient_generator.py |
| `TOWER` | 1, 2 | `TOWER\|E[X] = Σ P(Y=y)E[X given Y=y]\|27/8` | conditional_expectation_generator.py |
| `TRACE` | 2 | `TRACE\|-4 + 4\|0` | ode_system_generator.py |
| `TRACE_ADD` | 4 | `TRACE_ADD\|gamma0gamma0\|(1,1)\|0 + 1\|1` | gamma_matrix_generator.py |
| `TRACE_ENTRY` | 2 | `TRACE_ENTRY\|(1,1)\|0` | einstein_summation_generator.py, pauli_algebra_generator.py |
| `TRACE_EXPECT` | 1, 3 | `TRACE_EXPECT\|Tr(rho A)=p0*a+p1*b` | density_matrix_generator.py, gamma_matrix_generator.py |
| `TRACE_SUM` | 2 | `TRACE_SUM\|0 + 0\|0` | pauli_algebra_generator.py |
| `TRANSFER` | 1 | `TRANSFER\|H(s)=(3s+33)/(s^2+16s+48)` | transfer_function_generator.py |
| `TRANSFORM_APPLY` | 2 | `TRANSFORM_APPLY\|(-(4), (7))\|(-4, 7)` | transformation_generator.py |
| `TRANSFORM_RULE` | 1 | `TRANSFORM_RULE\|(x, y) → (-x, y)` | transformation_generator.py |
| `TRANSFORM_SETUP` | 2, 3 | `TRANSFORM_SETUP\|P(4, 7)\|reflection over the y-axis` | rv_transform_generator.py, transformation_generator.py |
| `TRANSIENT_FORMULA` | 1 | `TRANSIENT_FORMULA\|tau=L/R` | transient_circuit_generator.py |
| `TRANSIENT_SETUP` | 3 | `TRANSIENT_SETUP\|rl_rise\|R=9, L=54\|V=47, t=18` | transient_circuit_generator.py |
| `TRANSITIVE_CHECK` | 2, 3 | `TRANSITIVE_CHECK\|(5, 5) and (5, 5)\|need (5, 5)\|present` | equivalence_relation_generator.py, hereditarily_finite_set_generator.py, relation_check_generator.py |
| `TRANSLATE` | 2 | `TRANSLATE\|Some scientist is rested\|∃y (W(y) ∧ N(y))` | quantifier_negation_generator.py |
| `TRANSPORT_SETUP` | 3 | `TRANSPORT_SETUP\|supply=(34,16)\|demand=(20,30)\|costs=(5,4;4,7)` | transportation_generator.py |
| `TREE_BRANCH` | 3 | `TREE_BRANCH\|SF\|5/12 × 2/7\|5/42` | tree_diagram_probability_generator.py |
| `TRIG_RATIO` | 2 | `TRIG_RATIO\|cos\|adjacent/hypotenuse` | right_triangle_trig_generator.py |
| `TRIG_SETUP` | 2 | `TRIG_SETUP\|right triangle: leg opposite A = 16, leg adjacent to A = 12, hypotenuse = 20\|cos A` | right_triangle_trig_generator.py, trig_identity_eval_generator.py, trig_six_functions_generator.py, unit_circle_generator.py |
| `TRIG_VALUE` | 2, 3 | `TRIG_VALUE\|sin(lat1)=1\|sin(lat2)=1/2\|cos(dlon)=1/2` | christoffel_generator.py, great_circle_generator.py, spherical_triangle_generator.py |
| `TRIPLE_EVAL` | 3 | `TRIPLE_EVAL\|z_part * r_part * angle\|6*8*32*2*pi\|3072*pi` | triple_integral_generator.py |
| `TRIPLE_SETUP` | 3 | `TRIPLE_SETUP\|integrand 6*z\|cylinder radius 8, height 4\|cylindrical` | triple_integral_generator.py |
| `TRI_ANGLE_SETUP` | 3 | `TRI_ANGLE_SETUP\|3x + 7\|2x + 16\|3x + 61` | angle_relationships_generator.py |
| `TRI_ANGLE_SOLVE` | 2 | `TRI_ANGLE_SOLVE\|8x + 84 = 180\|x = 12` | angle_relationships_generator.py |
| `TRI_ANGLE_SUM` | 1 | `TRI_ANGLE_SUM\|(3x + 7) + (2x + 16) + (3x + 61) = 180` | angle_relationships_generator.py |
| `TRI_AREA_FORMULA` | 1 | `TRI_AREA_FORMULA\|Area = (1/2)·a·b·sin C` | triangle_area_sas_generator.py |
| `TRI_SETUP` | 2 | `TRI_SETUP\|45-45-90 triangle, leg = 180\|hypotenuse` | special_right_triangle_generator.py, triangle_area_sas_generator.py, triangle_solve_generator.py |
| `TRUNCATE` | 2 | `TRUNCATE\|rank=1\|discard=4` | low_rank_approx_generator.py |
| `TRUTH_ROW` | 1, 2 | `TRUTH_ROW\|row 1\|p=T, q=T` | argument_form_generator.py, boolean_algebra_generator.py, truth_table_generator.py |
| `TRY` | 1, 2, 3 | `TRY\|x = −50\|−50 ≤ x < −37 and x is odd\|false` | cantor_pairing_generator.py, conditional_forms_generator.py, counterexample_search_generator.py, factor_trinomial_generator.py, log_conversion_generator.py, log_equation_generator.py, polynomial_inequality_generator.py, radical_equation_generator.py, rational_equation_generator.py, rational_root_generator.py, set_builder_roster_generator.py, structure_isomorphism_generator.py |
| `TS_FACTOR` | 3 | `TS_FACTOR\|p-1=16\|q=1\|s=4` | tonelli_shanks_generator.py |
| `TS_INIT` | 4 | `TS_INIT\|m=4\|c=3\|t=16\|r=16` | tonelli_shanks_generator.py |
| `TS_LOOP` | 2 | `TS_LOOP\|i=1\|b=13` | tonelli_shanks_generator.py |
| `TS_NONRESIDUE` | 1 | `TS_NONRESIDUE\|3` | tonelli_shanks_generator.py |
| `TS_SETUP` | 2 | `TS_SETUP\|a=16\|p=17` | tonelli_shanks_generator.py |
| `TT_COLUMN` | 2 | `TT_COLUMN\|formula\|TTFT` | truth_table_generator.py |
| `TT_SETUP` | 2 | `TT_SETUP\|variables p, q\|4` | truth_table_generator.py |
| `TWIDDLE` | 1, 3 | `TWIDDLE\|W4=-i\|W4^2=-1\|W4^3=i` | dft_generator.py |
| `TWOS_SETUP` | 2 | `TWOS_SETUP\|8-bit two's complement\|offset = 2^8 = 256` | base_conversion_generator.py |
| `TYPE_ABS` | 2 | `TYPE_ABS\|lambda g\|b → a` | type_theory_generator.py |
| `TYPE_APP` | 3 | `TYPE_APP\|(h q)\|unify\|c → d` | type_theory_generator.py |
| `TYPE_ASSIGN` | 2 | `TYPE_ASSIGN\|u\|a` | type_theory_generator.py |
| `UB` | 2 | `UB\|{32, 53}\|{53}` | partial_order_generator.py |
| `UC_GUESS` | 2 | `UC_GUESS\|constant forcing\|y_p = A` | undetermined_coeff_generator.py |
| `UC_POINT` | 2 | `UC_POINT\|0°\|(1, 0)` | unit_circle_generator.py |
| `UNCERTAINTY_SETUP` | 3 | `UNCERTAINTY_SETUP\|particle in a box\|L=1, hbar=1\|n=133` | uncertainty_generator.py |
| `UNFOLD` | 2 | `UNFOLD\|rev("ifiggigfgff")\|rev("figgigfgff") + "i"` | recursive_definition_unfold_generator.py |
| `UNIFY_BIND` | 3 | `UNIFY_BIND\|X\|b\|{X=b}` | unification_generator.py |
| `UNIFY_DECOMPOSE` | 2 | `UNIFY_DECOMPOSE\|f\|2 arguments` | unification_generator.py |
| `UNIFY_FAIL` | 1 | `UNIFY_FAIL\|occurs-check X in f(X)` | unification_generator.py |
| `UNIFY_PAIR` | 2 | `UNIFY_PAIR\|f(X,a)\|f(b,Y)` | unification_generator.py |
| `UNIFY_SETUP` | 3 | `UNIFY_SETUP\|f(X,a)\|f(b,Y)\|occurs-check` | unification_generator.py |
| `UNIF_FORMULA` | 1 | `UNIF_FORMULA\|E[X] = (a + b)/2; Var(X) = (n² − 1)/12` | discrete_uniform_bernoulli_generator.py |
| `UNIF_SETUP` | 2 | `UNIF_SETUP\|X uniform on integers 49 through 58\|n = 10` | discrete_uniform_bernoulli_generator.py |
| `UNION_ELEMENT` | 2 | `UNION_ELEMENT\|{{∅, {∅}}, {{∅}}, {∅, {{∅}}, {{{∅}}}}}\|contributes {{∅, {∅}}, {{∅}}, {∅, {{∅}}, {{{∅}}}}}` | hereditarily_finite_set_generator.py |
| `UNIT_ATTACH` | 3 | `UNIT_ATTACH\|5\|seconds\|5 seconds` | cross_section_generator.py, kinematics_generator.py, physics_formula_generator.py |
| `UNIT_CONVERT` | 2 | `UNIT_CONVERT\|4 minutes\|240 seconds` | physics_formula_generator.py |
| `UNIT_NORMAL` | 2 | `UNIT_NORMAL\|T'(0)/norm T'(0)\|<-1, 0>` | curve_geometry_generator.py |
| `UNIT_RATE_DIV` | 3 | `UNIT_RATE_DIV\|48 minutes\|4\|12 minutes` | unit_rate_generator.py |
| `UNIT_RATE_PICK` | 2 | `UNIT_RATE_PICK\|2\|8` | unit_rate_generator.py |
| `UNIT_RATE_SETUP` | 3 | `UNIT_RATE_SETUP\|4\|pages\|48 minutes` | unit_rate_generator.py |
| `UNIT_RATE_TABLE` | 2 | `UNIT_RATE_TABLE\|2,7,9,10\|8,28,36,40` | unit_rate_generator.py |
| `UNIT_RULE` | 3 | `UNIT_RULE\|hbar=1\|E=1/L\|keV` | natural_units_generator.py |
| `UNIT_TANGENT` | 2 | `UNIT_TANGENT\|r'(0)/speed\|<0, 1>` | curve_geometry_generator.py |
| `UNLIKE_RADICALS` | 2 | `UNLIKE_RADICALS\|√2 ≠ √11\|unlike radicands — cannot combine` | radical_add_sub_generator.py |
| `UNPAIR` | 2 | `UNPAIR\|8614\|(31, 99)` | cantor_pairing_generator.py |
| `UNPAIRED` | 2 | `UNPAIRED\|neither\|∅` | one_to_one_correspondence_generator.py |
| `UNROLL` | 2 | `UNROLL\|-19, 95, -475, 2375\|geometric, r = -5` | recursive_explicit_generator.py |
| `UPDATE` | 2 | `UPDATE\|W1_11\|54/7` | backprop_generator.py, kernel_perceptron_generator.py |
| `U_VECTOR` | 2 | `U_VECTOR\|u1 = A*v1/σ1\|[1/√2, 1/√2]` | svd_generator.py |
| `VA` | 1 | `VA\|x = 1` | rational_function_features_generator.py |
| `VALIDITY` | 2 | `VALIDITY\|invalid\|affirming the consequent` | argument_form_generator.py |
| `VALUE_FORMULA` | 1 | `VALUE_FORMULA\|v=(ad-bc)/(a-b-c+d)` | game_theory_generator.py |
| `VARIANCE` | 1, 2 | `VARIANCE\|Delta x^2\|1/12 - 1/(35378pi^2)` | layer_norm_generator.py, uncertainty_generator.py |
| `VAR_FORMULA` | 1 | `VAR_FORMULA\|Var(X) = p(1 − p)` | discrete_uniform_bernoulli_generator.py, expectation_of_function_generator.py, expected_value_generator.py |
| `VAR_ROW` | 3 | `VAR_ROW\|4 - 4.25 = -0.25\|(-0.25)^2 = 0.0625\|1/2·0.0625 = 0.03125` | expected_value_generator.py |
| `VECTOR_NORM` | 2 | `VECTOR_NORM\|A\|13` | embedding_similarity_generator.py |
| `VECTOR_SETUP` | 2 | `VECTOR_SETUP\|F(x,y) = <-3*x + 6*y, x>\|divergence and scalar curl` | div_curl_generator.py |
| `VEC_ENTRY` | 3 | `VEC_ENTRY\|(1)\|33 + (-72)*4\|-255` | diagonalization_generator.py |
| `VEC_SETUP` | 2 | `VEC_SETUP\|v = ⟨12, 16⟩\|unit vector` | dot_product_generator.py, vector_ops_generator.py |
| `VENN_MARK` | 2 | `VENN_MARK\|pilots ∩ ¬farmers\|x2` | syllogism_generator.py |
| `VENN_REGION` | 2 | `VENN_REGION\|A ∩ B\|4` | venn_probability_generator.py |
| `VENN_SHADE` | 2 | `VENN_SHADE\|farmers − teachers\|empty` | syllogism_generator.py |
| `VERIFY` | 2 | `VERIFY\|1\|ok` | error_spotting_generator.py, foundations_critic_generator.py |
| `VERTEX` | 1 | `VERTEX\|(0, 0)` | ellipse_features_generator.py, hyperbola_features_generator.py, lp_corner_generator.py, parabola_features_generator.py |
| `VERTEX_SOLVE` | 2 | `VERTEX_SOLVE\|x=0\|y=0` | lp_corner_generator.py |
| `VISIT` | 2 | `VISIT\|D\|D` | graph_traversal_generator.py |
| `VITERBI_BACKTRACE` | 2 | `VITERBI_BACKTRACE\|L->H->H\|27/512` | viterbi_generator.py |
| `VITERBI_CAND` | 3 | `VITERBI_CAND\|t=2,state=H\|from H\|9/128` | convolutional_code_viterbi_generator.py, viterbi_generator.py |
| `VITERBI_INIT` | 3 | `VITERBI_INIT\|H\|obs=B\|1/8` | viterbi_generator.py |
| `VITERBI_PICK` | 2, 3 | `VITERBI_PICK\|t=2,state=H\|from L\|3/32` | convolutional_code_viterbi_generator.py, viterbi_generator.py |
| `VOLUME` | 1 | `VOLUME\|200` | volume_rect_prism_generator.py |
| `VOLUME_SETUP` | 2 | `VOLUME_SETUP\|region under y = x(355 - x) on [0, 355], rotated about the y-axis\|shell method` | solid_revolution_generator.py |
| `VOL_BASE_AREA` | 2 | `VOL_BASE_AREA\|Base Area = (1/2) × 6 × 10\|30.0` | round_solids_generator.py, volume_3d_generator.py |
| `VOL_CALCULATE` | 2 | `VOL_CALCULATE\|V = 14 × 3 × 8\|336` | round_solids_generator.py, volume_3d_generator.py |
| `VOL_FORMULA` | 1 | `VOL_FORMULA\|V = l × w × h` | round_solids_generator.py, solid_revolution_generator.py, volume_3d_generator.py |
| `VOL_SETUP` | 2 | `VOL_SETUP\|rectangular_prism\|l=14, w=3, h=8` | volume_3d_generator.py |
| `VOP_FORM` | 2 | `VOP_FORM\|u1' = -y2*g/W\|96/6 * e^(4x)` | variation_parameters_generator.py |
| `WALK_ENTRY` | 2 | `WALK_ENTRY\|A^2[4,3]\|1` | graph_counting_generator.py |
| `WALK_GOAL` | 2 | `WALK_GOAL\|length 2\|4 to 3` | graph_counting_generator.py |
| `WALK_TERM` | 3 | `WALK_TERM\|via 1\|A[4,1]*A[1,3]\|1` | graph_counting_generator.py |
| `WARSHALL_K` | 2 | `WARSHALL_K\|k=9\|0 0 0 0; 0 0 1 0; 0 0 0 1; 0 1 0 0` | relation_closure_generator.py |
| `WAVE_FORMULA` | 1 | `WAVE_FORMULA\|1=N^2*integral_0^L (x/L)^(2k) dx` | wavefunction_generator.py |
| `WAVE_SETUP` | 3 | `WAVE_SETUP\|power_interval\|psi=N*(x/L)^3\|0<=x<=17` | wavefunction_generator.py |
| `WEEKDAY_SCAN` | 2, 3 | `WEEKDAY_SCAN\|index 2\|Wednesday` | calendar_arithmetic_generator.py |
| `WEIGHT` | 2 | `WEIGHT\|blue\|57/98` | complement_probability_generator.py, expectation_of_function_generator.py, pmf_cdf_quantile_generator.py, probability_axioms_finite_generator.py, probability_measure_generator.py |
| `WEIGHT_VECTOR` | 2 | `WEIGHT_VECTOR\|w\|(-8,15)` | svm_margin_generator.py |
| `WIDTH_SETUP` | 3 | `WIDTH_SETUP\|combined\|Gamma_a=2, Gamma_b=8, Gamma_c=16,hbar=1\|target=BR_c,tau` | branching_ratio_generator.py |
| `WITNESS` | 2, 3 | `WITNESS\|n=2\|Prime(2)=T\|Odd(2)=F` | induction_verify_generator.py, peano_arithmetic_generator.py, quantifier_finite_domain_generator.py, quantifier_negation_generator.py |
| `WORK_DIFF` | 3 | `WORK_DIFF\|phi(end) - phi(start)\|24 - 0\|24` | line_integral_generator.py |
| `WRONSKIAN` | 2 | `WRONSKIAN\|y1*y2' - y1'*y2\|6e^(2x)` | variation_parameters_generator.py |
| `XOR` | 3 | `XOR\|control=0\|target=0\|0` | quantum_gate_generator.py |
| `YOUNG_SETUP` | 3 | `YOUNG_SETUP\|partition=[7,1]\|n=8\|group=S_8` | young_tableaux_generator.py |
| `Z` | 1 | `Z\|63 R84` | abacus_addition_generator.py, absolute_value_equation_generator.py, absolute_value_inequality_generator.py, ac_circuit_generator.py, activation_generator.py, adam_step_generator.py, algorithm_trace_generator.py, angle_defect_generator.py, angle_measure_generator.py, angle_relationships_generator.py, annuity_generator.py, antiderivative_generator.py, arc_length_generator.py, arc_sector_generator.py, area_between_curves_generator.py, argument_form_generator.py, arithmetic_coding_generator.py, arithmetic_sequence_generator.py, attention_generator.py, attribute_sorting_generator.py, baby_step_giant_step_generator.py, backprop_generator.py, base_arithmetic_generator.py, base_conversion_generator.py, bayes_multiple_hypotheses_generator.py, bayesian_update_generator.py, bch_generator.py, bec_channel_generator.py, binomial_probability_generator.py, bisection_generator.py, bitwise_ops_generator.py, black_scholes_generator.py, blackbody_generator.py, bond_pricing_generator.py, boolean_algebra_generator.py, braket_generator.py, branching_ratio_generator.py, calendar_arithmetic_generator.py, calorimetry_generator.py, cantor_diagonal_generator.py, cantor_pairing_generator.py, cardinal_arithmetic_generator.py, casimir_force_generator.py, casimir_generator.py, cauchy_riemann_generator.py, cayley_table_generator.py, centroid_generator.py, chain_rule_generator.py, channel_capacity_generator.py, characteristic_vector_generator.py, chi_square_generator.py, cholesky_generator.py, christoffel_generator.py, circle_angle_generator.py, circle_equation_generator.py, circle_generator.py, classic_probability_puzzles_generator.py, classifier_metrics_generator.py, clebsch_gordan_generator.py, collision_generator.py, combinatory_logic_generator.py, commutator_generator.py, complement_probability_generator.py, completing_square_generator.py, complex_division_generator.py, complex_locus_generator.py, complex_log_generator.py, complex_number_ops_generator.py, complex_quadratic_generator.py, composite_arithmetic_generator.py, compound_inequality_generator.py, compound_probability_generator.py, conditional_expectation_generator.py, conditional_forms_generator.py, conditional_probability_generator.py, confidence_interval_generator.py, conic_standard_form_generator.py, conservation_law_generator.py, continued_fraction_generator.py, continuous_distribution_generator.py, contour_integral_generator.py, convolution_generator.py, convolutional_code_viterbi_generator.py, coset_generator.py, countability_bijection_generator.py, counterexample_search_generator.py, counting_classics_generator.py, counting_to_probability_generator.py, covariance_algebra_generator.py, cramers_rule_generator.py, crc_generator.py, cross_section_generator.py, crt_generator.py, curve_analysis_generator.py, curve_geometry_generator.py, cyclic_group_generator.py, cyk_parser_generator.py, de_moivre_generator.py, decimal_add_sub_generator.py, decimal_div_generator.py, decimal_mult_generator.py, dedekind_cut_generator.py, definite_integral_generator.py, density_matrix_generator.py, derangement_generator.py, derivative_limit_def_generator.py, derivative_power_rule_generator.py, derivative_product_quotient_generator.py, derivative_transcendental_generator.py, determinant_generator.py, dfa_minimization_generator.py, dfa_simulation_generator.py, dft_generator.py, diagonalization_generator.py, diffie_hellman_generator.py, dijkstra_generator.py, dimensional_analysis_generator.py, direct_proof_algebra_generator.py, discrete_uniform_bernoulli_generator.py, discriminant_generator.py, distance_formula_generator.py, distribution_of_sum_generator.py, div_curl_generator.py, divisibility_classification_generator.py, domain_range_generator.py, doppler_generator.py, dot_product_generator.py, double_integral_generator.py, dp_table_generator.py, dpll_trace_generator.py, ecdh_generator.py, ecdsa_generator.py, eigenvalue_generator.py, einstein_summation_generator.py, electrostatics_generator.py, ellipse_features_generator.py, elliptic_curve_finite_field_generator.py, embedding_similarity_generator.py, energy_conservation_generator.py, english_to_logic_generator.py, entropy_change_generator.py, entropy_generator.py, entropy_rate_markov_generator.py, equation_from_two_points_generator.py, equilibrium_ice_generator.py, equivalence_relation_generator.py, error_spotting_generator.py, euler_characteristic_generator.py, euler_circuit_generator.py, euler_formula_generator.py, euler_method_generator.py, evaluate_expression_generator.py, exact_ode_generator.py, expectation_of_function_generator.py, expected_value_generator.py, experimental_probability_generator.py, exponent_generator.py, exponent_mixed_rules_generator.py, exponential_equation_generator.py, exponential_model_generator.py, extended_euclid_generator.py, factor_gcf_generator.py, factor_grouping_generator.py, factor_special_forms_generator.py, factor_trinomial_generator.py, factors_generator.py, feature_map_generator.py, fermi_estimation_generator.py, fill_in_step_generator.py, finance_generator.py, finite_difference_generator.py, finite_field_generator.py, first_law_generator.py, five_number_summary_generator.py, fixed_point_generator.py, flops_memory_generator.py, foundations_critic_generator.py, four_vector_generator.py, fourier_series_generator.py, fractal_iteration_generator.py, fraction_comparison_generator.py, fraction_decimal_percent_converter.py, fraction_op_generator.py, frequency_table_generator.py, function_composition_generator.py, function_evaluation_generator.py, function_inner_product_generator.py, function_operations_generator.py, function_properties_generator.py, function_table_generator.py, fundamental_counting_principle_generator.py, fundamental_form_generator.py, game_theory_generator.py, gamma_matrix_generator.py, gas_law_generator.py, gas_stoichiometry_generator.py, gauss_bonnet_generator.py, gauss_law_generator.py, gaussian_curvature_generator.py, gcf_generator.py, generating_function_generator.py, geometric_distribution_generator.py, geometric_mean_generator.py, geometric_probability_generator.py, geometric_sequence_generator.py, geometry_area_perimeter_generator.py, godel_numbering_generator.py, gradient_descent_generator.py, gradient_generator.py, gradient_step_generator.py, gram_schmidt_generator.py, graph_counting_generator.py, graph_interpret_generator.py, graph_traversal_generator.py, grassmann_generator.py, great_circle_generator.py, hamiltonian_generator.py, hamming_code_generator.py, hawking_generator.py, heat_engine_generator.py, hereditarily_finite_set_generator.py, hermitian_check_generator.py, hessian_classify_generator.py, hilbert_axiom_derivation_generator.py, horner_evaluation_generator.py, huffman_coding_generator.py, hydrogen_atom_generator.py, hyperbola_features_generator.py, hyperbolic_distance_generator.py, hyperbolic_function_generator.py, hypercube_counting_generator.py, hypergeometric_generator.py, hypothesis_test_generator.py, implicit_diff_generator.py, improper_integral_generator.py, inclusion_exclusion_generator.py, independence_check_generator.py, index_gymnastics_generator.py, index_raising_generator.py, induction_verify_generator.py, information_gain_generator.py, integer_operations_generator.py, integers_as_pairs_generator.py, integrating_factor_generator.py, integration_by_parts_generator.py, interference_generator.py, interpolation_generator.py, invariant_mass_generator.py, inverse_function_generator.py, jacobi_symbol_generator.py, jacobian_generator.py, joint_distribution_generator.py, kernel_evaluation_generator.py, kernel_perceptron_generator.py, kernel_ridge_generator.py, kernel_validity_generator.py, kinematics_generator.py, kl_divergence_generator.py, kmeans_step_generator.py, knights_knaves_generator.py, knn_generator.py, kraft_inequality_generator.py, ladder_operator_generator.py, lagrange_multiplier_generator.py, lagrangian_generator.py, lambda_reduction_generator.py, laplace_ivp_generator.py, laurent_series_generator.py, law_of_total_probability_generator.py, layer_norm_generator.py, lcm_generator.py, least_squares_generator.py, legendre_construction_generator.py, lhopital_generator.py, lie_exponential_generator.py, likelihood_language_generator.py, limit_evaluation_generator.py, line_integral_generator.py, linear_approx_generator.py, linear_complex_generator.py, linear_fractional_generator.py, linear_simple_generator.py, linearity_of_expectation_generator.py, literal_equation_generator.py, lll_reduction_generator.py, log_conversion_generator.py, log_diff_higher_order_generator.py, log_equation_generator.py, log_properties_generator.py, logic_grid_puzzle_generator.py, logical_connective_eval_generator.py, logical_equivalence_laws_generator.py, logistic_growth_generator.py, long_division_generator.py, low_rank_approx_generator.py, lp_corner_generator.py, lr_schedule_generator.py, lu_decomposition_generator.py, lz_compression_generator.py, magnetism_generator.py, manual_square_root_generator.py, markov_chain_generator.py, master_theorem_generator.py, matrix_calculus_generator.py, matrix_exponential_generator.py, matrix_group_check_generator.py, matrix_inverse_generator.py, matrix_norm_generator.py, matrix_ops_generator.py, mean_value_theorem_generator.py, method_of_moments_generator.py, metric_arc_length_generator.py, mgf_generator.py, midpoint_generator.py, minkowski_interval_generator.py, mixed_number_operation_generator.py, mle_generator.py, mobius_transform_generator.py, mod_exp_generator.py, modular_arithmetic_generator.py, modular_inverse_generator.py, monomial_mult_div_generator.py, mst_generator.py, multi_digit_addition_generator.py, multi_digit_multiplication_generator.py, multi_digit_subtraction_generator.py, multi_step_unit_conversion_generator.py, multiplying_binomials_generator.py, multiplying_polynomials_generator.py, multivar_chain_rule_generator.py, mutual_information_generator.py, naive_bayes_generator.py, named_distribution_generator.py, natural_deduction_generator.py, natural_units_generator.py, nets_surface_area_generator.py, newton_raphson_generator.py, newtons_laws_generator.py, nfa_simulation_generator.py, normal_approx_binomial_generator.py, normal_table_generator.py, npv_irr_generator.py, number_comparison_generator.py, odds_probability_generator.py, ode_substitution_generator.py, ode_system_generator.py, one_step_equation_generator.py, one_step_inequality_generator.py, one_to_one_correspondence_generator.py, operation_properties_generator.py, optics_generator.py, optimization_generator.py, or_formula_generator.py, orbital_mechanics_generator.py, order_of_operations_generator.py, order_statistics_generator.py, ordinal_arithmetic_generator.py, parabola_features_generator.py, parallel_perpendicular_line_generator.py, param_count_generator.py, parametric_calculus_generator.py, partial_derivative_generator.py, partial_fractions_generator.py, partial_order_generator.py, partial_trace_generator.py, particle_in_box_generator.py, partition_function_generator.py, pascal_triangle_generator.py, pauli_algebra_generator.py, pca_generator.py, pda_simulation_generator.py, peano_arithmetic_generator.py, percent_problem_generator.py, percent_word_problem_generator.py, perceptron_generator.py, permutation_combination_generator.py, permutation_group_generator.py, perplexity_generator.py, ph_calculation_generator.py, physics_formula_generator.py, piecewise_evaluation_generator.py, place_value_rounding_generator.py, planck_units_generator.py, pmf_cdf_quantile_generator.py, point_slope_generator.py, polar_parametric_generator.py, pollard_factorization_generator.py, polygon_perimeter_generator.py, polynomial_add_sub_generator.py, polynomial_div_monomial_generator.py, polynomial_inequality_generator.py, polynomial_long_division_generator.py, polynomial_zeros_generator.py, portfolio_generator.py, positional_encoding_generator.py, positive_definite_generator.py, power_series_generator.py, prenex_normal_form_generator.py, primality_test_generator.py, prime_factorization_generator.py, probability_addition_rule_generator.py, probability_axioms_finite_generator.py, probability_measure_generator.py, projectile_motion_generator.py, projector_generator.py, proportion_word_problem_generator.py, proportional_relationship_generator.py, pythag_hyp_generator.py, pythag_leg_generator.py, qr_decomposition_generator.py, quadratic_factoring_generator.py, quadratic_generator.py, quadratic_residue_generator.py, quadratic_square_root_generator.py, quantifier_finite_domain_generator.py, quantifier_negation_generator.py, quantization_generator.py, quantum_formula_generator.py, quantum_gate_generator.py, quark_composition_generator.py, quaternion_generator.py, radical_add_sub_generator.py, radical_equation_generator.py, radical_multiply_generator.py, radical_rationalize_generator.py, radical_variable_simplify_generator.py, random_digit_simulation_generator.py, rate_conversion_generator.py, ratio_table_generator.py, rational_equation_generator.py, rational_exponent_generator.py, rational_expr_add_sub_generator.py, rational_expr_mult_div_generator.py, rational_expr_simplify_generator.py, rational_function_features_generator.py, rational_root_generator.py, rationals_as_pairs_generator.py, recurrence_generator.py, recursive_definition_unfold_generator.py, recursive_explicit_generator.py, reed_solomon_generator.py, regex_to_automaton_generator.py, regression_generator.py, regular_polygon_area_generator.py, related_rates_generator.py, relation_check_generator.py, relation_closure_generator.py, relation_operations_generator.py, relativistic_energy_generator.py, reliability_system_generator.py, remainder_factor_theorem_generator.py, repeating_decimal_generator.py, residue_generator.py, resolution_proof_generator.py, riemann_sum_generator.py, riemann_tensor_generator.py, right_triangle_trig_generator.py, rotational_dynamics_generator.py, round_solids_generator.py, routh_hurwitz_generator.py, row_reduction_generator.py, rsa_generator.py, runge_kutta_generator.py, running_coupling_generator.py, rv_transform_generator.py, sample_space_list_generator.py, scaling_generator.py, scaling_law_generator.py, schwarzschild_generator.py, second_order_ode_generator.py, segment_partition_generator.py, semantic_tableau_generator.py, separable_ode_generator.py, separable_pde_generator.py, series_convergence_generator.py, series_solution_generator.py, set_algebra_laws_generator.py, set_builder_roster_generator.py, set_counting_generator.py, set_expression_generator.py, set_identity_membership_table_generator.py, set_membership_subset_generator.py, set_operations_generator.py, shm_generator.py, sigma_notation_generator.py, signal_arithmetic_generator.py, similar_triangles_generator.py, simple_probability_generator.py, simple_stats_generator.py, simplex_generator.py, simplify_expression_generator.py, sinusoid_features_generator.py, slope_intercept_form_generator.py, slope_two_points_generator.py, softmax_gradient_generator.py, solid_revolution_generator.py, solution_chem_generator.py, special_relativity_generator.py, special_right_triangle_generator.py, special_solution_equation_generator.py, spherical_excess_generator.py, spherical_triangle_generator.py, spin_half_generator.py, stability_generator.py, standard_deviation_generator.py, standard_form_conversion_generator.py, standing_wave_generator.py, stars_and_bars_generator.py, statics_generator.py, statistics_generator.py, stereographic_generator.py, stoichiometry_generator.py, structure_constant_generator.py, structure_isomorphism_generator.py, subspace_basis_generator.py, svd_generator.py, svm_margin_generator.py, syllogism_generator.py, synthetic_division_generator.py, systems_elimination_generator.py, systems_substitution_generator.py, tangent_line_generator.py, taxicab_geometry_generator.py, taylor_series_generator.py, telescoping_generator.py, temperature_conversion_generator.py, tensor_product_generator.py, tip_bill_split_generator.py, tonelli_shanks_generator.py, totient_generator.py, transfer_function_generator.py, transformation_generator.py, transient_circuit_generator.py, transportation_generator.py, tree_diagram_probability_generator.py, triangle_area_sas_generator.py, triangle_solve_generator.py, trig_equation_generator.py, trig_identity_eval_generator.py, trig_identity_verify_generator.py, trig_six_functions_generator.py, triple_integral_generator.py, truth_table_generator.py, turing_machine_trace_generator.py, two_sample_test_generator.py, two_step_equation_generator.py, two_step_inequality_generator.py, two_way_table_probability_generator.py, type_theory_generator.py, u_substitution_generator.py, uncertainty_generator.py, undetermined_coeff_generator.py, unification_generator.py, unit_circle_generator.py, unit_conversion_generator.py, unit_rate_generator.py, variation_parameters_generator.py, vector_ops_generator.py, vector_theorem_generator.py, venn_probability_generator.py, venn_region_count_generator.py, viterbi_generator.py, volume_3d_generator.py, volume_rect_prism_generator.py, von_neumann_entropy_generator.py, wavefunction_generator.py, wff_parsing_generator.py, young_tableaux_generator.py, z_score_generator.py, z_transform_generator.py, zf_axiom_identify_generator.py |
| `ZERO` | 1 | `ZERO\|s=-11` | transfer_function_generator.py |
| `ZERO_PRODUCT` | 2 | `ZERO_PRODUCT\|(x - 4) = 0\|x = 4` | area_between_curves_generator.py, curve_analysis_generator.py, domain_range_generator.py, log_equation_generator.py, optimization_generator.py, polynomial_inequality_generator.py, polynomial_zeros_generator.py, quadratic_factoring_generator.py, radical_equation_generator.py, trig_equation_generator.py |
| `ZSCORE` | 2 | `ZSCORE\|(55.5 − 50)/5\|1.10` | normal_approx_binomial_generator.py, normal_table_generator.py, z_score_generator.py |
| `ZSCORE_FORMULA` | 1 | `ZSCORE_FORMULA\|z = (x - μ)/σ` | z_score_generator.py |
| `ZT_PAIR` | 1 | `ZT_PAIR\|Z{r^n u[n]}=1/(1-r z^-1)` | z_transform_generator.py |
| `ZT_SETUP` | 2, 3 | `ZT_SETUP\|geometric\|x[n]=31*2^n u[n]` | z_transform_generator.py |
