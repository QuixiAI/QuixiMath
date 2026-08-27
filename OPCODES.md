# Op-Code Legend

**Generated file — do not hand-edit.** Regenerate with `python tools/gen_opcode_legend.py` (verify freshness with `--check`).

The scratchpad vocabulary belongs to the model and evolves organically: generators may introduce new op-codes freely, and this legend is *descriptive*, not prescriptive. Steps are pipe-delimited strings (`CODE|field|field|...`, at most 4 payload fields) built with `helpers.step()`; the final step of every problem is `Z|<final_answer>`.

1709 distinct op-codes observed.

| Code | Payload fields | Example | Used by |
|---|---|---|---|
| `A` | 3 | `A\|46\|46\|92` | ac_circuit_generator.py, activation_generator.py, adam_step_generator.py, algorithm_trace_generator.py, angle_defect_generator.py, angle_measure_generator.py, annuity_generator.py, arithmetic_coding_generator.py, arithmetic_sequence_generator.py, attention_generator.py, backprop_generator.py, base_conversion_generator.py, bayesian_update_generator.py, binomial_probability_generator.py, bisection_generator.py, bond_pricing_generator.py, branching_ratio_generator.py, calendar_arithmetic_generator.py, calorimetry_generator.py, casimir_generator.py, cayley_table_generator.py, channel_capacity_generator.py, chi_square_generator.py, circle_equation_generator.py, classifier_metrics_generator.py, collision_generator.py, commutator_generator.py, complex_division_generator.py, complex_locus_generator.py, complex_number_ops_generator.py, composite_arithmetic_generator.py, conditional_probability_generator.py, confidence_interval_generator.py, conic_standard_form_generator.py, continued_fraction_generator.py, contour_integral_generator.py, convolution_generator.py, coset_generator.py, counterexample_search_generator.py, counting_classics_generator.py, crt_generator.py, curve_analysis_generator.py, cyclic_group_generator.py, de_moivre_generator.py, definite_integral_generator.py, density_matrix_generator.py, derangement_generator.py, derivative_limit_def_generator.py, determinant_generator.py, dft_generator.py, dijkstra_generator.py, distance_formula_generator.py, doppler_generator.py, dot_product_generator.py, dp_table_generator.py, einstein_summation_generator.py, electrostatics_generator.py, ellipse_features_generator.py, embedding_similarity_generator.py, energy_conservation_generator.py, entropy_change_generator.py, entropy_generator.py, entropy_rate_markov_generator.py, equivalence_relation_generator.py, euler_characteristic_generator.py, euler_formula_generator.py, euler_method_generator.py, evaluate_expression_generator.py, expected_value_generator.py, exponential_model_generator.py, extended_euclid_generator.py, feature_map_generator.py, fill_in_step_generator.py, finance_generator.py, finite_field_generator.py, five_number_summary_generator.py, fixed_point_generator.py, flops_memory_generator.py, four_vector_generator.py, fractal_iteration_generator.py, fraction_op_generator.py, frequency_table_generator.py, function_composition_generator.py, function_evaluation_generator.py, function_inner_product_generator.py, function_operations_generator.py, function_table_generator.py, game_theory_generator.py, gaussian_curvature_generator.py, generating_function_generator.py, geometric_mean_generator.py, geometry_area_perimeter_generator.py, gradient_descent_generator.py, gradient_step_generator.py, graph_counting_generator.py, graph_interpret_generator.py, grassmann_generator.py, great_circle_generator.py, hamiltonian_generator.py, heat_engine_generator.py, hermitian_check_generator.py, horner_evaluation_generator.py, huffman_coding_generator.py, hyperbola_features_generator.py, hyperbolic_distance_generator.py, hyperbolic_function_generator.py, hypercube_counting_generator.py, inclusion_exclusion_generator.py, index_gymnastics_generator.py, information_gain_generator.py, integrating_factor_generator.py, interpolation_generator.py, invariant_mass_generator.py, joint_distribution_generator.py, kernel_evaluation_generator.py, kernel_perceptron_generator.py, kernel_ridge_generator.py, kl_divergence_generator.py, kmeans_step_generator.py, knn_generator.py, kraft_inequality_generator.py, ladder_operator_generator.py, lagrangian_generator.py, laplace_ivp_generator.py, layer_norm_generator.py, legendre_construction_generator.py, lhopital_generator.py, limit_evaluation_generator.py, linear_approx_generator.py, low_rank_approx_generator.py, lp_corner_generator.py, lr_schedule_generator.py, manual_square_root_generator.py, markov_chain_generator.py, matrix_calculus_generator.py, matrix_group_check_generator.py, matrix_norm_generator.py, matrix_ops_generator.py, mean_value_theorem_generator.py, mgf_generator.py, midpoint_generator.py, minkowski_interval_generator.py, mixed_number_operation_generator.py, mobius_transform_generator.py, modular_arithmetic_generator.py, mst_generator.py, mutual_information_generator.py, naive_bayes_generator.py, named_distribution_generator.py, nets_surface_area_generator.py, newtons_laws_generator.py, npv_irr_generator.py, operation_properties_generator.py, or_formula_generator.py, order_of_operations_generator.py, order_statistics_generator.py, parabola_features_generator.py, param_count_generator.py, partition_function_generator.py, pascal_triangle_generator.py, pca_generator.py, percent_word_problem_generator.py, perceptron_generator.py, permutation_group_generator.py, piecewise_evaluation_generator.py, polar_parametric_generator.py, polygon_perimeter_generator.py, polynomial_zeros_generator.py, portfolio_generator.py, probability_addition_rule_generator.py, pythag_hyp_generator.py, quantization_generator.py, quark_composition_generator.py, quaternion_generator.py, radical_add_sub_generator.py, radical_multiply_generator.py, rational_expr_add_sub_generator.py, recurrence_generator.py, recursive_definition_unfold_generator.py, recursive_explicit_generator.py, reed_solomon_generator.py, regression_generator.py, relativistic_energy_generator.py, remainder_factor_theorem_generator.py, riemann_sum_generator.py, riemann_tensor_generator.py, rotational_dynamics_generator.py, round_solids_generator.py, runge_kutta_generator.py, running_coupling_generator.py, rv_transform_generator.py, segment_partition_generator.py, separable_pde_generator.py, set_counting_generator.py, shm_generator.py, sigma_notation_generator.py, simple_stats_generator.py, simplex_generator.py, softmax_gradient_generator.py, solution_chem_generator.py, spherical_excess_generator.py, spherical_triangle_generator.py, spin_half_generator.py, standard_deviation_generator.py, stars_and_bars_generator.py, statics_generator.py, stereographic_generator.py, svm_margin_generator.py, synthetic_division_generator.py, tangent_line_generator.py, taxicab_geometry_generator.py, taylor_series_generator.py, temperature_conversion_generator.py, tip_bill_split_generator.py, transfer_function_generator.py, transformation_generator.py, transportation_generator.py, triangle_solve_generator.py, trig_identity_eval_generator.py, trig_six_functions_generator.py, two_sample_test_generator.py, undetermined_coeff_generator.py, variation_parameters_generator.py, vector_ops_generator.py, venn_region_count_generator.py, von_neumann_entropy_generator.py, wavefunction_generator.py, young_tableaux_generator.py, z_score_generator.py |
| `ABS` | 2 | `ABS\|4/5\|4/5` | fixed_point_generator.py, matrix_norm_generator.py, rv_transform_generator.py |
| `ABSORB_EQ` | 2 | `ABSORB_EQ\|u0=p0A+p00*u0+p01*u1\|u1=p1A+p10*u0+p11*u1` | markov_chain_generator.py |
| `ABS_CASE` | 2 | `ABS_CASE\|Case 1\|2x + 1 = 11` | absolute_value_equation_generator.py |
| `ABS_CHECK` | 2 | `ABS_CHECK\|-7 < 0\|Absolute value cannot be negative` | absolute_value_equation_generator.py |
| `ABS_ERROR` | 2 | `ABS_ERROR\|1\|0` | quantization_generator.py |
| `ABS_INEQ_CHECK` | 2 | `ABS_INEQ_CHECK\|-2 < 0\|Absolute value is always non-negative` | absolute_value_inequality_generator.py |
| `ABS_INEQ_PART` | 2 | `ABS_INEQ_PART\|Part 1\|2x + 1 > 15 -> x > 7` | absolute_value_inequality_generator.py |
| `ABS_INEQ_SETUP` | 1 | `ABS_INEQ_SETUP\|abs(2x + 1) > 15` | absolute_value_inequality_generator.py |
| `ABS_INEQ_SPECIAL` | 2 | `ABS_INEQ_SPECIAL\|c = 0\|Check logic for >=` | absolute_value_inequality_generator.py |
| `ABS_INEQ_SPLIT` | 2 | `ABS_INEQ_SPLIT\|OR case\|2x + 1 > 15 or 2x + 1 < -15` | absolute_value_inequality_generator.py |
| `ABS_SETUP` | 1 | `ABS_SETUP\|abs(2x + 1) = 11` | absolute_value_equation_generator.py |
| `ABS_SPLIT` | 2, 3 | `ABS_SPLIT\|Two cases\|2x + 1 = 11\|2x + 1 = -11` | absolute_value_equation_generator.py |
| `ABS_VAL` | 2 | `ABS_VAL\|(-10)\|10` | taxicab_geometry_generator.py |
| `AB_ADD` | 3 | `AB_ADD\|+4000\|5230\|9230` | abacus_addition_generator.py |
| `AB_SET` | 1 | `AB_SET\|5230` | abacus_addition_generator.py |
| `ACCEPT` | 1, 2 | `ACCEPT\|x = −10` | conditional_forms_generator.py, counterexample_search_generator.py, factor_trinomial_generator.py, knights_knaves_generator.py, log_conversion_generator.py, log_equation_generator.py, optimization_generator.py, polynomial_inequality_generator.py, radical_equation_generator.py, rational_equation_generator.py, rational_root_generator.py, set_builder_roster_generator.py |
| `ACT_DERIV` | 3 | `ACT_DERIV\|sigmoid\|0\|1/4` | activation_generator.py |
| `ACT_SETUP` | 3 | `ACT_SETUP\|activation=sigmoid\|x=5\|w1=5,b1=-25,w2=-5,b2=1` | activation_generator.py |
| `ACT_VALUE` | 3 | `ACT_VALUE\|sigmoid\|0\|1/2` | activation_generator.py |
| `AC_COMPLEX` | 3 | `AC_COMPLEX\|Z\|21\|0j` | ac_circuit_generator.py |
| `AC_FORMULA` | 1 | `AC_FORMULA\|omega0^2=1/(L*C)` | ac_circuit_generator.py |
| `AC_PRODUCT` | 2 | `AC_PRODUCT\|3 × 20\|60` | factor_trinomial_generator.py |
| `AC_SETUP` | 3 | `AC_SETUP\|resonance\|R=21, L=8\|C=1/32` | ac_circuit_generator.py |
| `ADAM_SETUP` | 3 | `ADAM_SETUP\|theta=8,g=-5\|beta1=9/10,beta2=99/100\|lr=1/10,epsilon=0` | adam_step_generator.py |
| `ADAM_UPDATE` | 2 | `ADAM_UPDATE\|theta_new\|81/10` | adam_step_generator.py |
| `ADD_COL` | 3 | `ADD_COL\|col_1\|0+0+0\|->0 (carry 0)` | multi_digit_addition_generator.py |
| `ADD_FORMULA` | 1 | `ADD_FORMULA\|P(A ∩ B) = P(A) + P(B) - P(A ∪ B)` | probability_addition_rule_generator.py |
| `ADD_PARTIALS` | 2 | `ADD_PARTIALS\|410370 + 3419750 + 61555500 + 68395000\|133780620` | decimal_mult_generator.py, multi_digit_multiplication_generator.py |
| `ADD_SETUP` | 2 | `ADD_SETUP\|P(A) = 6/10, P(B) = 7/10, P(A ∪ B) = 9/10\|P(A ∩ B)` | probability_addition_rule_generator.py |
| `ADJOINT` | 1 | `ADJOINT\|U^dagger=[[5/13,12/13],[-12/13,5/13]]` | hermitian_check_generator.py |
| `ADJ_LIST` | 2 | `ADJ_LIST\|A\|B, D, E` | euler_circuit_generator.py, graph_traversal_generator.py |
| `ALG_SETUP` | 3 | `ALG_SETUP\|merge sort\|merges 4\|values 16, 2, 19, 15, 28, 36` | algorithm_trace_generator.py |
| `ALIGN_NUM` | 2 | `ALIGN_NUM\|046.36\|177.07` | number_comparison_generator.py |
| `ALPHA` | 2 | `ALPHA\|alpha1\|1/5` | kernel_ridge_generator.py |
| `ALPHA_RENAME` | 2 | `ALPHA_RENAME\|lambda k. ((k m) t)\|lambda z. ((z m) t)` | lambda_reduction_generator.py |
| `AMORT_ROW` | 3 | `AMORT_ROW\|1\|interest=$3432.00\|principal=$264.00,balance=$6600.00` | annuity_generator.py |
| `AMPLITUDE` | 2 | `AMPLITUDE\|abs(2)\|2` | sinusoid_features_generator.py |
| `ANALOGY_SETUP` | 3 | `ANALOGY_SETUP\|man=(-2,3)\|woman=(-2,1)\|king=(1,3)` | embedding_similarity_generator.py |
| `ANALOGY_VECTOR` | 2 | `ANALOGY_VECTOR\|king-man+woman\|(1,1)` | embedding_similarity_generator.py |
| `ANGLE` | 2 | `ANGLE\|theta\|5pi/6` | positional_encoding_generator.py |
| `ANGLE_DEFECT_SETUP` | 2 | `ANGLE_DEFECT_SETUP\|R=2\|angles=60,60,15` | angle_defect_generator.py |
| `ANGLE_EVAL` | 2 | `ANGLE_EVAL\|theta=0..2*pi\|2*pi` | triple_integral_generator.py |
| `ANGLE_FORMULA` | 1 | `ANGLE_FORMULA\|quadrant I: reference = θ` | angle_measure_generator.py |
| `ANGLE_RELATION` | 1 | `ANGLE_RELATION\|6x + 10 = 3x + 58` | angle_relationships_generator.py |
| `ANGLE_SETUP` | 2 | `ANGLE_SETUP\|vertical\|Vertical angles are equal` | angle_relationships_generator.py |
| `ANGLE_SOLVE` | 2 | `ANGLE_SOLVE\|3x = 48\|x = 16` | angle_relationships_generator.py |
| `ANGLE_WRAP` | 2 | `ANGLE_WRAP\|340 deg\|-20 deg` | complex_log_generator.py |
| `ANNUITY_FORMULA` | 1 | `ANNUITY_FORMULA\|interest=balance*r; principal=payment-interest` | annuity_generator.py |
| `ANNUITY_SETUP` | 2, 3 | `ANNUITY_SETUP\|amortization schedule\|balance=6864,payment=3696,r=50%\|periods=5` | annuity_generator.py |
| `ANTICHAIN` | 2 | `ANTICHAIN\|{2, 7, 42}\|size 3` | partial_order_generator.py |
| `ANTICOMM_ENTRY` | 3 | `ANTICOMM_ENTRY\|(1,1)\|8i - 8i\|0` | pauli_algebra_generator.py |
| `ANTIDERIV` | 2 | `ANTIDERIV\|-2x\|-x^2` | antiderivative_generator.py, arc_length_generator.py, area_between_curves_generator.py, definite_integral_generator.py, improper_integral_generator.py, integrating_factor_generator.py, integration_by_parts_generator.py, ode_substitution_generator.py, parametric_calculus_generator.py, partial_fractions_generator.py, separable_ode_generator.py, solid_revolution_generator.py, u_substitution_generator.py, variation_parameters_generator.py |
| `ANTIDERIVATIVE` | 1 | `ANTIDERIVATIVE\|-A*cos(nx)/n` | fourier_series_generator.py |
| `ANTISYM_CHECK` | 3 | `ANTISYM_CHECK\|(3, 1)\|reverse (1, 3)\|ok` | relation_check_generator.py |
| `APPLY_GATE` | 3 | `APPLY_GATE\|Y\|e^(i402π/269)·ket0\|i·e^(i402π/269)·ket1` | quantum_gate_generator.py |
| `APPLY_OPERATOR` | 2 | `APPLY_OPERATOR\|L[Ae^(4x)]\|A(16 + 16 + 3)e^(4x)` | commutator_generator.py, undetermined_coeff_generator.py |
| `APPLY_PAULI` | 2 | `APPLY_PAULI\|sigma_z ket1\|-ket1` | spin_half_generator.py |
| `APPLY_SUBST` | 1 | *(not observed in sampling)* | unification_generator.py |
| `APPROX` | 2 | `APPROX\|12*d^2*L\|302579712` | param_count_generator.py |
| `APPROX_ENTRY` | 2 | `APPROX_ENTRY\|(1,1)\|0` | low_rank_approx_generator.py |
| `APPROX_SETUP` | 2 | `APPROX_SETUP\|estimate √99\|linearize f(x) = √x at a = 100` | linear_approx_generator.py |
| `ARCCOS` | 2 | `ARCCOS\|cos(c)=1/2\|c=pi/3` | great_circle_generator.py |
| `ARCLEN_FORMULA` | 1 | `ARCLEN_FORMULA\|L = ∫ √((dx/dt)^2 + (dy/dt)^2) dt` | arc_length_generator.py, parametric_calculus_generator.py |
| `ARC_FORMULA` | 1 | `ARC_FORMULA\|L = rθ` | arc_sector_generator.py |
| `ARC_LENGTH` | 3 | `ARC_LENGTH\|int_0^T speed dt\|17*4\|68` | curve_geometry_generator.py |
| `ARC_SETUP` | 2 | `ARC_SETUP\|circle r = 6, central angle 10π/9 rad\|sector area` | arc_sector_generator.py |
| `AREA` | 1 | `AREA\|66` | geometry_area_perimeter_generator.py |
| `AREA_INT` | 3 | `AREA_INT\|A = int y dx\|7*3^3/3\|63` | centroid_generator.py |
| `AREA_INTEGRAL` | 2 | `AREA_INTEGRAL\|sqrt(EG-F^2)=R\|area = R*theta*h` | fundamental_form_generator.py |
| `AREA_SCALE` | 3 | `AREA_SCALE\|uv rectangle area\|9*7\|63` | jacobian_generator.py |
| `AREA_SETUP` | 2 | `AREA_SETUP\|y = x^2 - 2x - 3 and y = 5\|area between the curves` | area_between_curves_generator.py |
| `ARGUMENT` | 2 | `ARGUMENT\|(-9,0)\|180 deg` | complex_log_generator.py, euler_formula_generator.py |
| `ARG_SETUP` | 2 | `ARG_SETUP\|¬(q ∧ q)\|¬(q ∧ q) ∨ (¬r ∨ ¬s)` | argument_form_generator.py |
| `ARITH_INTERVAL` | 1 | `ARITH_INTERVAL\|[3/4,1)` | arithmetic_coding_generator.py |
| `ARITH_SETUP` | 2 | `ARITH_SETUP\|A=1/8, B=3/8, C=1/4, D=1/4\|message=DDBCD` | arithmetic_coding_generator.py |
| `ARITH_SYMBOL` | 2 | `ARITH_SYMBOL\|D\|cum=[3/4,1)` | arithmetic_coding_generator.py |
| `ARRAY_STATE` | 2 | `ARRAY_STATE\|pass 1\|3, 7, 10, 35, 11, 23, 39` | algorithm_trace_generator.py |
| `ASSIGN` | 2 | `ASSIGN\|P1\|C1` | kmeans_step_generator.py |
| `ASSUME` | 1 | `ASSUME\|assume w is even or k is even` | direct_proof_algebra_generator.py |
| `ASYMPTOTE` | 1 | `ASYMPTOTE\|y = 3 ± (1/5)x` | hyperbola_features_generator.py |
| `ATA` | 2 | `ATA\|A^T A\|[[2500, 1344], [1344, 2500]]` | svd_generator.py |
| `ATOM_CHECK` | 3 | `ATOM_CHECK\|Al\|left=4\|right=4` | stoichiometry_generator.py |
| `ATTN_OUTPUT` | 2 | `ATTN_OUTPUT\|1\|[[-13/2,15/2]]` | attention_generator.py |
| `ATTN_SCORE` | 2 | `ATTN_SCORE\|1,1\|0` | attention_generator.py |
| `ATTN_SETUP` | 1, 3 | `ATTN_SETUP\|tokens=2,d=2\|Q=[[0,0], [0,0]]\|K=[[0,0], [0,0]]` | attention_generator.py |
| `ATTR_CHECK` | 3 | `ATTR_CHECK\|4\|A: odd\|no` | attribute_sorting_generator.py |
| `AV_VECTOR` | 2 | `AV_VECTOR\|A*v1\|[62/√2, 62/√2]` | svd_generator.py |
| `B` | 1, 3 | `B\|38\|1\|381` | decimal_div_generator.py, long_division_generator.py, percent_problem_generator.py, polynomial_long_division_generator.py |
| `BABY_STEP` | 2 | `BABY_STEP\|j=0\|1` | baby_step_giant_step_generator.py |
| `BACKPROP_DELTA` | 2 | `BACKPROP_DELTA\|h1\|delta=8` | backprop_generator.py |
| `BACKPROP_GRAD` | 2 | `BACKPROP_GRAD\|dL/dy_hat\|-4` | backprop_generator.py |
| `BACKPROP_SETUP` | 3 | `BACKPROP_SETUP\|x=(-1,-2)\|y=2\|eta=1/8` | backprop_generator.py |
| `BACK_SUB` | 2 | `BACK_SUB\|v = y/x\|y/x = 2 ln(x) + C` | ode_substitution_generator.py |
| `BACK_SUB_ROW` | 3 | `BACK_SUB_ROW\|r=177\|x=1\|y=0` | extended_euclid_generator.py, modular_inverse_generator.py, rsa_generator.py |
| `BALANCED_EQ` | 1 | `BALANCED_EQ\|4 Al + 3 O2 -> 2 Al2O3` | stoichiometry_generator.py |
| `BALANCE_COEFFS` | 2 | `BALANCE_COEFFS\|reactants=4,3\|products=2` | stoichiometry_generator.py |
| `BASE` | 2 | `BASE\|h(0)\|-15` | recursive_definition_unfold_generator.py |
| `BASE_ADD_COL` | 3 | `BASE_ADD_COL\|col 0\|2 + 4 + carry 0\|6 -> digit 6, carry 0` | base_arithmetic_generator.py |
| `BASE_ARITH_SETUP` | 2 | `BASE_ARITH_SETUP\|base 8\|2422 + 764` | base_arithmetic_generator.py |
| `BASE_CARRY` | 2 | `BASE_CARRY\|carry 5\|digit 5, carry 0` | base_arithmetic_generator.py |
| `BASE_MUL_COL` | 3 | `BASE_MUL_COL\|col 0\|C * 4 + carry 0\|48 -> digit 0, carry 3` | base_arithmetic_generator.py |
| `BASE_SETUP` | 2 | `BASE_SETUP\|244_16\|decimal` | base_conversion_generator.py |
| `BAYES_CELL` | 3 | `BAYES_CELL\|true positive\|44 * 3/4\|33` | conditional_probability_generator.py |
| `BAYES_FORMULA` | 1 | `BAYES_FORMULA\|P(disease=no given negative) = TN/(TN + FN)` | conditional_probability_generator.py |
| `BAYES_SETUP` | 3 | `BAYES_SETUP\|disease=yes 44, disease=no 70\|sensitivity 3/4, specificity 4/5\|P(disease=no given test negative)` | conditional_probability_generator.py |
| `BAYES_UPDATE_SETUP` | 2, 3 | `BAYES_UPDATE_SETUP\|beta_binomial\|prior=Beta(5,7)\|successes=0, trials=20` | bayesian_update_generator.py |
| `BCH_FORM` | 2 | `BCH_FORM\|A+B+1/2[A,B]\|[[0, 0, 0], [-3, 0, -3], [-2, 0, 0]]` | bch_generator.py |
| `BCH_SETUP` | 3 | `BCH_SETUP\|A=-2E31\|B=-3E23\|order=2` | bch_generator.py |
| `BEC_FORMULA` | 1 | `BEC_FORMULA\|C=1-epsilon` | bec_channel_generator.py |
| `BEC_SETUP` | 1 | `BEC_SETUP\|epsilon=1/4` | bec_channel_generator.py |
| `BELL_ROW` | 3 | `BELL_ROW\|n=1\|1\|1` | set_counting_generator.py |
| `BEREZIN_RULE` | 2 | `BEREZIN_RULE\|int dtheta 1\|0` | grassmann_generator.py |
| `BETA` | 1 | `BETA\|(lambda d. (lambda c. c)) applied to (lambda t. k)` | lambda_reduction_generator.py |
| `BEZOUT_CHECK` | 2 | `BEZOUT_CHECK\|177*19 + 120*-28\|3` | extended_euclid_generator.py |
| `BIAS_CORRECT` | 2 | `BIAS_CORRECT\|m_hat\|-5` | adam_step_generator.py |
| `BINARY_EXPONENT` | 2 | `BINARY_EXPONENT\|50\|110010` | mod_exp_generator.py, quadratic_residue_generator.py |
| `BINOM_FORMULA` | 1 | `BINOM_FORMULA\|P(X ≤ k) = Σ C(n,i)·p^i·(1-p)^(n-i)` | binomial_probability_generator.py |
| `BINOM_SETUP` | 2 | `BINOM_SETUP\|n = 4, p = 2/5\|P(X ≤ 1)` | binomial_probability_generator.py |
| `BISECTION_SETUP` | 3 | `BISECTION_SETUP\|f(x)=x^2-122\|interval=[11, 12]\|iterations=5` | bisection_generator.py |
| `BISECT_UPDATE` | 3 | `BISECT_UPDATE\|1\|product < 0\|[11, 23/2]` | bisection_generator.py |
| `BIT` | 1, 2 | `BIT\|h\|A=1\|B=1` | characteristic_vector_generator.py |
| `BITWISE` | 1 | `BITWISE\|∧\|1101001\|1100110\|1100000` | characteristic_vector_generator.py |
| `BIT_ROW` | 2, 3 | `BIT_ROW\|0 XOR 0\|0` | bitwise_ops_generator.py |
| `BIT_RULE` | 2 | `BIT_RULE\|XOR\|1 when exactly one bit is 1` | bitwise_ops_generator.py |
| `BIT_SETUP` | 2 | `BIT_SETUP\|truth table for XOR\|all 2-bit inputs` | bitwise_ops_generator.py |
| `BLACKBODY_FORMULA` | 1 | `BLACKBODY_FORMULA\|P=sigma*A*T^4` | blackbody_generator.py |
| `BLACKBODY_SETUP` | 3 | `BLACKBODY_SETUP\|stefan_power\|sigma=12, A=14\|T=19` | blackbody_generator.py |
| `BOND_FORMULA` | 1 | `BOND_FORMULA\|price=sum coupon/(1+y)^t + face/(1+y)^n` | bond_pricing_generator.py |
| `BOND_PRICE` | 1 | `BOND_PRICE\|$3168.00` | bond_pricing_generator.py |
| `BOND_SETUP` | 2 | `BOND_SETUP\|face=3600\|coupon=10%,ytm=25%,years=1` | bond_pricing_generator.py |
| `BOOL_SETUP` | 2 | `BOOL_SETUP\|variables Q, R, S\|CNF from g=0 rows` | boolean_algebra_generator.py |
| `BORROW` | 3 | `BORROW\|col_1\|from_left\|1` | multi_digit_subtraction_generator.py |
| `BOX_FORMULA` | 1 | `BOX_FORMULA\|lambda=8*m*L^2*c/((n_high^2-n_low^2)*h)` | particle_in_box_generator.py |
| `BOX_SETUP` | 1, 3 | `BOX_SETUP\|transition_wavelength\|n_low=4, n_high=6\|h=8, c=7` | particle_in_box_generator.py |
| `BRAKET_FORMULA` | 1 | `BRAKET_FORMULA\|inner(phi,psi)=sum conj(phi_k)*psi_k` | braket_generator.py |
| `BRAKET_SETUP` | 3 | `BRAKET_SETUP\|inner_product\|phi=[2-i,-1+i,-1]\|psi=[-1,1-i,0]` | braket_generator.py |
| `BRANCH_TEST` | 2 | `BRANCH_TEST\|2 <= 2\|yes` | piecewise_evaluation_generator.py |
| `BRANCH_USE` | 1 | `BRANCH_USE\|$5.50` | piecewise_evaluation_generator.py |
| `BRING_DOWN` | 2 | `BRING_DOWN\|group 35\|current = 35` | composite_arithmetic_generator.py, manual_square_root_generator.py |
| `BSC_FORMULA` | 1 | `BSC_FORMULA\|H_b=p*(-log2 p)+(1-p)*(-log2(1-p))` | channel_capacity_generator.py |
| `BSC_SETUP` | 3 | `BSC_SETUP\|p=9/50\|-log2(p)=2.474\|-log2(1-p)=0.286` | channel_capacity_generator.py |
| `BSGS_MATCH` | 3 | `BSGS_MATCH\|i=1\|j=4\|x=10` | baby_step_giant_step_generator.py |
| `BSGS_SETUP` | 4 | `BSGS_SETUP\|p=31\|g=3\|h=25\|m=6` | baby_step_giant_step_generator.py |
| `BS_FORMULA` | 2 | `BS_FORMULA\|C=S*N(d1)-K*df*N(d2)\|P=K*df*N(-d2)-S*N(-d1)` | black_scholes_generator.py |
| `BS_RESULT` | 2 | `BS_RESULT\|call=5.85\|put=4.85` | black_scholes_generator.py |
| `BS_SETUP` | 3 | `BS_SETUP\|S=100,K=110\|df=0.9\|N_d1=0.9,N_d2=0.85` | black_scholes_generator.py |
| `C` | 3 | `C\|1/3\|21\|7/21` | fraction_comparison_generator.py, fraction_op_generator.py, mixed_number_operation_generator.py, rational_expr_add_sub_generator.py |
| `CALC` | 1 | `CALC\|x = -10` | systems_elimination_generator.py, systems_substitution_generator.py |
| `CAL_DIVMOD` | 3 | `CAL_DIVMOD\|33\|7\|4 R5` | calendar_arithmetic_generator.py |
| `CAL_FORMULA` | 1 | `CAL_FORMULA\|warm ice: q1=m*c_ice*(0-Ti)` | calorimetry_generator.py |
| `CAL_SETUP` | 3 | `CAL_SETUP\|start 2028-07-29\|end 2028-12-10\|days between` | calendar_arithmetic_generator.py, calorimetry_generator.py |
| `CANCEL` | 2 | `CANCEL\|(n - 8)\|(n - 1)/(n - 3)` | derivative_limit_def_generator.py, derivative_transcendental_generator.py, limit_evaluation_generator.py, power_series_generator.py, rational_expr_mult_div_generator.py, rational_expr_simplify_generator.py, rational_function_features_generator.py, series_convergence_generator.py, trig_identity_verify_generator.py |
| `CANDIDATES` | 1 | `CANDIDATES\|±1/2, ±1, ±5/2, ±5` | rational_root_generator.py |
| `CANONICAL_ORDER` | 1 | `CANONICAL_ORDER\|B=2, D=2, A=3, C=3, E=3, G=4, F=5, H=5` | kraft_inequality_generator.py |
| `CANONICAL_SHIFT` | 3 | `CANONICAL_SHIFT\|code=0\|left=2\|0` | kraft_inequality_generator.py |
| `CARRY_FINAL` | 1 | `CARRY_FINAL\|1` | multi_digit_addition_generator.py |
| `CARTESIAN_RESULT` | 1 | `CARTESIAN_RESULT\|{(p, 19)}` | set_operations_generator.py |
| `CART_PAIR` | 3 | `CART_PAIR\|p\|19\|(p, 19)` | set_operations_generator.py |
| `CASE` | 1 | `CASE\|Bea=knight, Oona=knight` | knights_knaves_generator.py |
| `CASHFLOW_PV` | 2 | `CASHFLOW_PV\|coupon_t1\|288` | bond_pricing_generator.py |
| `CASIMIR_FORCE_SETUP` | 2 | `CASIMIR_FORCE_SETUP\|F/A=-π^2*hbar*c/(240*d^4)\|hbar=14,c=17,d=8` | casimir_force_generator.py |
| `CASIMIR_SETUP` | 3 | `CASIMIR_SETUP\|spin=6\|hbar=35/12\|J^2=j(j+1)hbar^2` | casimir_generator.py |
| `CAYLEY_HEADER` | 1 | `CAYLEY_HEADER\|0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10` | cayley_table_generator.py |
| `CAYLEY_ROW` | 2 | `CAYLEY_ROW\|row 0\|0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10` | cayley_table_generator.py |
| `CBRT` | 2 | `CBRT\|125s^3\|5s` | factor_special_forms_generator.py, inverse_function_generator.py, rational_exponent_generator.py |
| `CDF_EVENT` | 3 | `CDF_EVENT\|Y<=y\|X^2<=y\|X<=sqrt(y)` | rv_transform_generator.py |
| `CDF_FORMULA` | 2 | `CDF_FORMULA\|F_Y(y)=sqrt(y)/18\|0<=y<=324` | rv_transform_generator.py |
| `CEIL` | 2 | `CEIL\|2626.5625\|2627` | confidence_interval_generator.py |
| `CENTER` | 1, 2 | `CENTER\|(0, -2)` | circle_equation_generator.py, ellipse_features_generator.py, hyperbola_features_generator.py, pca_generator.py |
| `CENTROID_COORD` | 3 | `CENTROID_COORD\|xbar = M_y/A\|(567/4)/(63)\|9/4` | centroid_generator.py |
| `CENTROID_SETUP` | 3 | `CENTROID_SETUP\|0 <= y <= 7*x^2\|0 <= x <= 3\|centroid` | centroid_generator.py |
| `CENTROID_UPDATE` | 2 | `CENTROID_UPDATE\|C1\|(3,4)` | kmeans_step_generator.py |
| `CF_PARTIAL` | 2 | `CF_PARTIAL\|a_0\|4` | continued_fraction_generator.py |
| `CF_RESULT` | 1 | `CF_RESULT\|[4; 1, 1, 1, 1, 31]` | continued_fraction_generator.py |
| `CF_SETUP` | 1 | `CF_SETUP\|727/158` | continued_fraction_generator.py |
| `CG_COEFF` | 2 | `CG_COEFF\|ket(+,+)\|0` | clebsch_gordan_generator.py |
| `CG_SETUP` | 3 | `CG_SETUP\|j1=1/2\|j2=1/2\|phase=-` | clebsch_gordan_generator.py |
| `CG_STATE` | 2 | `CG_STATE\|J=0, M=0\|-1/sqrt2*ket(+,-) + 1/sqrt2*ket(-,+)` | clebsch_gordan_generator.py |
| `CHAIN` | 2 | `CHAIN\|{2, 22, 34, 58}\|length 4` | partial_order_generator.py |
| `CHAIN_DERIV` | 2 | `CHAIN_DERIV\|dy/dx\|-25/4` | activation_generator.py |
| `CHAIN_RATE` | 2 | `CHAIN_RATE\|x_s\|-4` | multivar_chain_rule_generator.py |
| `CHAIN_SUM` | 3 | `CHAIN_SUM\|f_x*x_s + f_y*y_s\|(-18)*(-4) + 68*2\|208` | multivar_chain_rule_generator.py |
| `CHAIN_VALUE` | 3 | `CHAIN_VALUE\|x(1,-2)\|(-4)*1 + 3*(-2) + 5\|-5` | multivar_chain_rule_generator.py |
| `CHANGE_BASE` | 1 | `CHANGE_BASE\|log_64(8) = log_2(8)/log_2(64)` | log_conversion_generator.py |
| `CHAR_DIAG` | 2 | `CHAR_DIAG\|diagonal of λI - A\|λ, (λ + 5)` | eigenvalue_generator.py |
| `CHAR_EQ` | 2 | `CHAR_EQ\|assume y=e^(rx)\|r^2 - 9 = 0` | ode_system_generator.py, second_order_ode_generator.py, undetermined_coeff_generator.py, variation_parameters_generator.py |
| `CHAR_POLY` | 2 | `CHAR_POLY\|p(λ) = λ^2 + 5λ\|(λ + 5)*λ` | diagonalization_generator.py, eigenvalue_generator.py, recurrence_generator.py |
| `CHAR_ROOTS` | 2 | `CHAR_ROOTS\|r1 = -3, r2 = 3\|distinct real` | recurrence_generator.py, second_order_ode_generator.py, undetermined_coeff_generator.py, variation_parameters_generator.py |
| `CHAR_SETUP` | 2 | `CHAR_SETUP\|p(λ) = det(λI - A)\|triangular determinant` | eigenvalue_generator.py |
| `CHECK` | 2, 3 | `CHECK\|multiply_back\|23×98+45=2299\|2299` | annuity_generator.py, area_between_curves_generator.py, arithmetic_sequence_generator.py, baby_step_giant_step_generator.py, base_arithmetic_generator.py, bch_generator.py, bitwise_ops_generator.py, boolean_algebra_generator.py, casimir_generator.py, cauchy_riemann_generator.py, characteristic_vector_generator.py, chi_square_generator.py, cholesky_generator.py, clebsch_gordan_generator.py, commutator_generator.py, completing_square_generator.py, conditional_probability_generator.py, convolutional_code_viterbi_generator.py, coset_generator.py, cramers_rule_generator.py, cyclic_group_generator.py, cyk_parser_generator.py, dfa_minimization_generator.py, dfa_simulation_generator.py, diagonalization_generator.py, diffie_hellman_generator.py, ecdh_generator.py, ecdsa_generator.py, eigenvalue_generator.py, elliptic_curve_finite_field_generator.py, embedding_similarity_generator.py, equilibrium_ice_generator.py, error_spotting_generator.py, euler_circuit_generator.py, exact_ode_generator.py, expected_value_generator.py, extended_euclid_generator.py, factor_gcf_generator.py, factor_grouping_generator.py, factor_special_forms_generator.py, factor_trinomial_generator.py, feature_map_generator.py, fill_in_step_generator.py, five_number_summary_generator.py, function_inner_product_generator.py, game_theory_generator.py, gamma_matrix_generator.py, gauss_bonnet_generator.py, gaussian_curvature_generator.py, geometric_mean_generator.py, geometric_probability_generator.py, geometric_sequence_generator.py, gradient_generator.py, gram_schmidt_generator.py, graph_counting_generator.py, hamming_code_generator.py, hermitian_check_generator.py, hessian_classify_generator.py, horner_evaluation_generator.py, hyperbolic_function_generator.py, hypothesis_test_generator.py, index_gymnastics_generator.py, induction_verify_generator.py, information_gain_generator.py, inverse_function_generator.py, kernel_perceptron_generator.py, kernel_validity_generator.py, kmeans_step_generator.py, knights_knaves_generator.py, knn_generator.py, ladder_operator_generator.py, lagrange_multiplier_generator.py, least_squares_generator.py, legendre_construction_generator.py, lhopital_generator.py, lie_exponential_generator.py, limit_evaluation_generator.py, line_integral_generator.py, linear_fractional_generator.py, lll_reduction_generator.py, log_equation_generator.py, logic_grid_puzzle_generator.py, logical_equivalence_laws_generator.py, long_division_generator.py, low_rank_approx_generator.py, lp_corner_generator.py, lu_decomposition_generator.py, lz_compression_generator.py, manual_square_root_generator.py, markov_chain_generator.py, matrix_exponential_generator.py, matrix_group_check_generator.py, matrix_inverse_generator.py, mean_value_theorem_generator.py, method_of_moments_generator.py, mle_generator.py, mobius_transform_generator.py, modular_arithmetic_generator.py, modular_inverse_generator.py, naive_bayes_generator.py, nfa_simulation_generator.py, ode_system_generator.py, operation_properties_generator.py, or_formula_generator.py, partial_derivative_generator.py, partial_order_generator.py, partial_trace_generator.py, pauli_algebra_generator.py, pca_generator.py, pda_simulation_generator.py, perceptron_generator.py, pollard_factorization_generator.py, polynomial_inequality_generator.py, positive_definite_generator.py, power_series_generator.py, prime_factorization_generator.py, projector_generator.py, qr_decomposition_generator.py, quadratic_factoring_generator.py, quadratic_square_root_generator.py, quaternion_generator.py, radical_variable_simplify_generator.py, ratio_table_generator.py, recursive_explicit_generator.py, regex_to_automaton_generator.py, relation_closure_generator.py, resolution_proof_generator.py, riemann_tensor_generator.py, rotational_dynamics_generator.py, routh_hurwitz_generator.py, rsa_generator.py, running_coupling_generator.py, rv_transform_generator.py, series_convergence_generator.py, set_algebra_laws_generator.py, shm_generator.py, signal_arithmetic_generator.py, similar_triangles_generator.py, simplex_generator.py, special_solution_equation_generator.py, statics_generator.py, stereographic_generator.py, structure_constant_generator.py, svd_generator.py, svm_margin_generator.py, syllogism_generator.py, systems_elimination_generator.py, taylor_series_generator.py, tip_bill_split_generator.py, tonelli_shanks_generator.py, totient_generator.py, transportation_generator.py, turing_machine_trace_generator.py, two_sample_test_generator.py, two_step_equation_generator.py, uncertainty_generator.py, venn_region_count_generator.py, young_tableaux_generator.py, z_score_generator.py |
| `CHECK_POINT` | 3 | `CHECK_POINT\|x=0\|17·0 + 12 = 12\|17·0 + 12 = 12` | special_solution_equation_generator.py |
| `CHINCHILLA` | 2 | `CHINCHILLA\|20N\|900000000` | scaling_law_generator.py |
| `CHI_FORMULA` | 1 | `CHI_FORMULA\|χ² = Σ (O - E)^2/E` | chi_square_generator.py |
| `CHI_SETUP` | 2 | `CHI_SETUP\|observed: 53, 50, 46, 57, 44; expected: 50 each\|goodness of fit; df = 4, critical value = 9.488` | chi_square_generator.py |
| `CHI_TERM` | 3 | `CHI_TERM\|53 - 50 = 3\|3^2 = 9\|9/50 = 0.18` | chi_square_generator.py |
| `CHOLESKY_ENTRY` | 2 | `CHOLESKY_ENTRY\|l11\|2` | cholesky_generator.py |
| `CHOL_SETUP` | 2 | `CHOL_SETUP\|A = [[4, -4, 6], [-4, 5, -5], [6, -5, 11]]\|A = L L^T` | cholesky_generator.py |
| `CHRISTOFFEL_FORMULA` | 1 | `CHRISTOFFEL_FORMULA\|Gamma^i_jk = 1/2 g^im(d_j g_mk + d_k g_mj - d_m g_jk)` | christoffel_generator.py |
| `CHRISTOFFEL_SETUP` | 3 | `CHRISTOFFEL_SETUP\|polar\|g_rr=1, g_thetatheta=r^2\|r=45` | christoffel_generator.py |
| `CHRISTOFFEL_VALUE` | 2 | `CHRISTOFFEL_VALUE\|Gamma^phi_thetatheta\|-60/169` | riemann_tensor_generator.py |
| `CIRCLE_ANGLE_SETUP` | 2 | `CIRCLE_ANGLE_SETUP\|triangle inscribed in a circle with one side a diameter; one acute angle is 47°\|the other acute angle` | circle_angle_generator.py |
| `CIRCLE_CALCULATE` | 2 | `CIRCLE_CALCULATE\|radius = diameter / 2 = 46 / 2\|23` | circle_generator.py |
| `CIRCLE_EQ` | 1 | `CIRCLE_EQ\|(x + 1)^2 + (y + 1)^2 = 16` | complex_locus_generator.py |
| `CIRCLE_FORMULA` | 1 | `CIRCLE_FORMULA\|A = πr²` | circle_generator.py |
| `CIRCLE_SETUP` | 2 | `CIRCLE_SETUP\|46\|diameter` | circle_equation_generator.py, circle_generator.py |
| `CIRCLE_SUBSTITUTE` | 1 | `CIRCLE_SUBSTITUTE\|A = π × 23²` | circle_generator.py |
| `CIRCULATION_SUM` | 2 | `CIRCULATION_SUM\|(7 - 0)*45\|315` | vector_theorem_generator.py |
| `CI_FORMULA` | 1 | `CI_FORMULA\|x̄ ± E` | confidence_interval_generator.py |
| `CI_SETUP` | 2 | `CI_SETUP\|σ = 15, n = 25, z* = 1.28\|confidence interval for μ` | confidence_interval_generator.py |
| `CLASS` | 2 | `CLASS\|remainder 1\|{11, 13, 15, 17, 19, 21, 23, 25}` | equivalence_relation_generator.py |
| `CLASSIFY` | 2 | `CLASSIFY\|contingency\|T at 3 of 8 rows` | truth_table_generator.py |
| `CLAUSE` | 2 | `CLAUSE\|C1\|(P75705 OR P2441)` | resolution_proof_generator.py |
| `CLIFFORD_EXPECT` | 3 | `CLIFFORD_EXPECT\|2*eta=0\|I_entry=0\|0` | gamma_matrix_generator.py |
| `CLOSURE_ADD` | 2 | `CLOSURE_ADD\|(6, 6)\|reflexive` | relation_closure_generator.py |
| `CLUE_APPLY` | 3 | `CLUE_APPLY\|clue 1\|Iris's item comes before Finn's item in the listed order\|6 → 3 candidates` | logic_grid_puzzle_generator.py |
| `CLUSTER_MEMBERS` | 2 | `CLUSTER_MEMBERS\|C1\|P1` | kmeans_step_generator.py |
| `CMP` | 3 | `CMP\|44\|9\|>` | fraction_comparison_generator.py, graph_interpret_generator.py, logical_connective_eval_generator.py, set_builder_roster_generator.py |
| `CMP_DIGIT` | 4 | `CMP_DIGIT\|pos_0\|0\|1\|<` | number_comparison_generator.py |
| `CMP_NUM` | 3 | `CMP_NUM\|46.36\|177.07\|<` | number_comparison_generator.py |
| `CNF_FORM` | 1 | `CNF_FORM\|(Q OR R OR NOT S) AND (Q OR NOT R OR S) AND (Q OR NOT R OR NOT S) AND (NOT Q OR NOT R OR NOT S)` | boolean_algebra_generator.py |
| `CODEWORD` | 1, 3 | `CODEWORD\|1110000` | hamming_code_generator.py, kraft_inequality_generator.py |
| `CODE_LENGTH` | 2 | `CODE_LENGTH\|A\|l=4` | huffman_coding_generator.py |
| `COEFF` | 2 | `COEFF\|a_1\|-47760` | laurent_series_generator.py, series_solution_generator.py |
| `COEFFS` | 1, 2 | `COEFFS\|2, 12, 14, -2` | horner_evaluation_generator.py, polynomial_zeros_generator.py, synthetic_division_generator.py |
| `COEFF_MATCH` | 2 | `COEFF_MATCH\|x^n\|(n+1)a_(n+1) = -2a_n` | series_solution_generator.py |
| `COEFF_PAIR` | 3 | `COEFF_PAIR\|i=3, j=1\|3i + 4j = 13\|accepted` | generating_function_generator.py |
| `COFACTOR` | 2 | `COFACTOR\|(1,1) sign +\|minor [[2, 0], [1, -1]]` | determinant_generator.py |
| `COLLIDER_SETUP` | 3 | `COLLIDER_SETUP\|luminosity\|N=85 events\|sigma=15 fb` | cross_section_generator.py |
| `COLLISION` | 1 | `COLLISION\|f(g) = f(h) = 4` | function_properties_generator.py |
| `COLLISION_SETUP` | 3 | `COLLISION_SETUP\|elastic_1d\|m1=4, u1=13\|m2=13, u2=-2` | collision_generator.py |
| `COL_BASIS` | 2 | `COL_BASIS\|original columns 1, 2\|[[3, 1, 0], [2, 1, 2]]` | subspace_basis_generator.py |
| `COMB` | 2 | `COMB\|C(6,1)\|6` | bec_channel_generator.py |
| `COMBO` | 2 | `COMBO\|x = -61*v1 + 11*v2\|[-6, -5]` | diagonalization_generator.py |
| `COMB_CONST` | 3 | `COMB_CONST\|-5\|-2\|-7` | derivative_product_quotient_generator.py, equation_from_two_points_generator.py, linear_complex_generator.py, rational_expr_add_sub_generator.py, simplify_expression_generator.py, special_solution_equation_generator.py |
| `COMB_FORMULA` | 1 | `COMB_FORMULA\|C(n, r) = P(n, r)/r!` | permutation_combination_generator.py |
| `COMB_SETUP` | 2 | `COMB_SETUP\|C(11, 8)\|n!/(r!·(n-r)!)` | counting_classics_generator.py, permutation_combination_generator.py, stars_and_bars_generator.py |
| `COMB_X` | 3 | `COMB_X\|4x\|+4x\|8x` | derivative_product_quotient_generator.py, linear_complex_generator.py, rational_expr_add_sub_generator.py, simplify_expression_generator.py, special_solution_equation_generator.py |
| `COMMON_DIFF` | 2 | `COMMON_DIFF\|10 - 7\|3` | arithmetic_sequence_generator.py, recursive_explicit_generator.py |
| `COMMON_RATIO` | 2 | `COMMON_RATIO\|-60/(-30)\|2` | geometric_sequence_generator.py, recursive_explicit_generator.py |
| `COMMUTATOR` | 2 | `COMMUTATOR\|[A,B]\|[[55i/2, 0], [0, -55i/2]]` | structure_constant_generator.py |
| `COMM_ENTRY` | 3 | `COMM_ENTRY\|(1,1)\|55i/4 - -55i/4\|55i/2` | structure_constant_generator.py |
| `COMM_FORMULA` | 1 | `COMM_FORMULA\|[A,B]f=A(Bf)-B(Af)` | commutator_generator.py |
| `COMM_RESULT` | 2 | `COMM_RESULT\|[D,x^2]f\|2*x^21` | commutator_generator.py |
| `COMM_SETUP` | 3 | `COMM_SETUP\|[D,x^2]f\|f=x^20\|D=d/dx` | commutator_generator.py |
| `COMPARE` | 2, 3 | `COMPARE\|2 = 2\|log_b(a) = k` | algorithm_trace_generator.py, equilibrium_ice_generator.py, fixed_point_generator.py, master_theorem_generator.py |
| `COMPLEMENT` | 2 | `COMPLEMENT\|at least one fixed\|9! - D_9` | derangement_generator.py |
| `COMPLETE_SQUARE` | 2 | `COMPLETE_SQUARE\|half of -4 = -2\|(-2)^2 = 4` | completing_square_generator.py, conic_standard_form_generator.py, polar_parametric_generator.py |
| `COMPOSE` | 3 | `COMPOSE\|j\|f(j) = 15\|g(15) = L` | function_properties_generator.py |
| `COMPOSE_PAIR` | 3 | `COMPOSE_PAIR\|(b, 7)\|(7, R)\|(b, R)` | relation_operations_generator.py |
| `COMPOSITE_FACTOR` | 2 | `COMPOSITE_FACTOR\|5\|73` | divisibility_classification_generator.py |
| `COMPOSITE_SETUP` | 2 | `COMPOSITE_SETUP\|area = length × width with mixed numbers\|convert, multiply, simplify` | composite_arithmetic_generator.py |
| `COMP_INEQ_PART` | 2 | `COMP_INEQ_PART\|Part 1\|4x + 10 < -10 -> x < -5` | compound_inequality_generator.py |
| `COMP_INEQ_SETUP` | 1 | `COMP_INEQ_SETUP\|4x + 10 < -10 or 4x + 10 > -3` | compound_inequality_generator.py |
| `CONCLUDE` | 1 | `CONCLUDE\|s ∣ j` | direct_proof_algebra_generator.py |
| `CONCLUSION_AT` | 2 | `CONCLUSION_AT\|q=F, r=T, s=T\|T` | argument_form_generator.py |
| `CONCLUSION_CHECK` | 1 | `CONCLUSION_CHECK\|not forced` | syllogism_generator.py |
| `COND_COUNT` | 2 | `COND_COUNT\|club=no and commute=bus\|24` | conditional_probability_generator.py |
| `COND_ENTROPY` | 1 | `COND_ENTROPY\|H(Y given X)=H(X,Y)-H(X)` | mutual_information_generator.py |
| `COND_FORMULA` | 1 | `COND_FORMULA\|P(A given B) = count(A and B)/count(B)` | conditional_probability_generator.py, joint_distribution_generator.py |
| `COND_PARTS` | 2 | `COND_PARTS\|n divisible by 24\|n divisible by 2` | conditional_forms_generator.py |
| `COND_SETUP` | 2 | `COND_SETUP\|yes/bike 17, no/bike 15, yes/bus 17, no/bus 24\|P(commute=bus given club=no)` | conditional_probability_generator.py |
| `COND_TOTAL` | 2 | `COND_TOTAL\|club=no total\|15 + 24 = 39` | conditional_probability_generator.py |
| `CONGRUENCE_REDUCE` | 2 | `CONGRUENCE_REDUCE\|27x congruent to 4\|mod 11` | modular_inverse_generator.py |
| `CONGRUENCE_SOLUTIONS` | 3 | `CONGRUENCE_SOLUTIONS\|base 3\|step 11\|3, 14, 25` | modular_inverse_generator.py |
| `CONIC_SETUP` | 2 | `CONIC_SETUP\|(x - 6)^2 = -20(y + 6)\|vertex, focus, directrix` | conic_standard_form_generator.py, ellipse_features_generator.py, hyperbola_features_generator.py, parabola_features_generator.py |
| `CONJ` | 2 | `CONJ\|phi_1=2-i\|2+i` | braket_generator.py |
| `CONJUGATE` | 2 | `CONJUGATE\|6 - 5i\|6 + 5i` | complex_division_generator.py, quaternion_generator.py |
| `CONNECTIVE` | 2 | `CONNECTIVE\|¬q\|T` | logical_connective_eval_generator.py |
| `CONSERVATION_SETUP` | 2 | `CONSERVATION_SETUP\|e- + e+ -> gamma + gamma + pi0\|check=Q,B,Le,Lmu` | conservation_law_generator.py |
| `CONSERVE_CHECK` | 3 | `CONSERVE_CHECK\|Q\|left=0,right=0\|conserved` | conservation_law_generator.py |
| `CONSTRAINT_SUBST` | 3 | `CONSTRAINT_SUBST\|x + y = 15\|x = 15/3\|5` | lagrange_multiplier_generator.py |
| `CONST_SOLVE` | 2 | `CONST_SOLVE\|C1 = -1\|C2 = -1` | recurrence_generator.py |
| `CONTOUR_SETUP` | 3 | `CONTOUR_SETUP\|abs(z)=6\|positive orientation\|f=-4/(z-2) + 1/(z+6) + 6/(z-7)` | contour_integral_generator.py |
| `CONT_DIST_SETUP` | 3 | `CONT_DIST_SETUP\|f(x)=k*x\|support=[0,6]\|interval=(3,4)` | continuous_distribution_generator.py |
| `CONVERGENT` | 2 | `CONVERGENT\|i=0\|4/1` | continued_fraction_generator.py |
| `CONVERGE_CHECK` | 2 | `CONVERGE_CHECK\|abs(r) = 4/7 < 1\|converges` | geometric_sequence_generator.py, series_convergence_generator.py |
| `CONV_ENCODE_STEP` | 3 | `CONV_ENCODE_STEP\|i=1\|prev=0,u=0\|00` | convolutional_code_viterbi_generator.py |
| `CONV_FACTOR` | 2 | `CONV_FACTOR\|1 hr\|60 min` | cross_section_generator.py, dimensional_analysis_generator.py, multi_step_unit_conversion_generator.py, rate_conversion_generator.py, unit_conversion_generator.py |
| `CONV_INIT` | 2 | `CONV_INIT\|h_-2=0,h_-1=1\|k_-2=1,k_-1=0` | continued_fraction_generator.py |
| `CONV_RECEIVED` | 2 | `CONV_RECEIVED\|011101\|flipped position 2` | convolutional_code_viterbi_generator.py |
| `CONV_RESULT` | 2 | `CONV_RESULT\|41 hr\|2460 min` | dimensional_analysis_generator.py, multi_step_unit_conversion_generator.py, rate_conversion_generator.py, temperature_conversion_generator.py, unit_conversion_generator.py |
| `CONV_SETUP` | 2, 3 | `CONV_SETUP\|x=[1,5,4]\|h=[6,7,4,2]` | convolution_generator.py, convolutional_code_viterbi_generator.py |
| `CONV_STEP` | 3 | `CONV_STEP\|i=0\|h=4\|k=1` | continued_fraction_generator.py |
| `CONV_SUM` | 2 | `CONV_SUM\|n=0\|6` | convolution_generator.py |
| `CONV_WINDOW` | 2 | `CONV_WINDOW\|n=0\|x0*h0` | convolution_generator.py |
| `COORDS` | 2 | `COORDS\|c = P^-1 x\|[-61, 11]` | diagonalization_generator.py |
| `CORRECT_BIT` | 3 | `CORRECT_BIT\|position=6\|1->0\|corrected=0111100` | hamming_code_generator.py |
| `CORR_FORMULA` | 1 | `CORR_FORMULA\|r = Sxy/√(Sxx·Syy)` | joint_distribution_generator.py, regression_generator.py |
| `COS` | 2 | `COS\|5pi/6\|-sqrt(3)/2` | positional_encoding_generator.py |
| `COSET` | 2 | `COSET\|0+H\|{0, 6, 4, 2}` | coset_generator.py |
| `COSET_ELEM` | 2 | `COSET_ELEM\|0+H\|0` | coset_generator.py |
| `COSET_SKIP` | 2 | `COSET_SKIP\|2\|already listed` | coset_generator.py |
| `COSET_START` | 2 | `COSET_START\|rep 0\|0+H` | coset_generator.py |
| `COSINE` | 2 | `COSINE\|A,A\|1` | embedding_similarity_generator.py, lr_schedule_generator.py |
| `COST` | 1 | `COST\|initial` | transportation_generator.py |
| `COUNT` | 2 | `COUNT\|neither\|5` | attribute_sorting_generator.py, bayesian_update_generator.py, equivalence_relation_generator.py, logical_connective_eval_generator.py, method_of_moments_generator.py, mle_generator.py, one_to_one_correspondence_generator.py, probability_addition_rule_generator.py, set_builder_roster_generator.py, set_membership_subset_generator.py, set_operations_generator.py |
| `COUNTEREXAMPLE` | 2, 3 | `COUNTEREXAMPLE\|set pair\|A = ∅; B = {27}; left = ∅; right = {27}` | argument_form_generator.py, conditional_forms_generator.py, counterexample_search_generator.py, truth_table_generator.py |
| `COUNTERMODEL` | 1 | `COUNTERMODEL\|kayakers=TFF, pilots=FFF, travelers=TFF` | syllogism_generator.py |
| `COUNT_DP` | 3 | `COUNT_DP\|1\|1\|2` | decimal_mult_generator.py |
| `COUNT_RULE` | 2 | `COUNT_RULE\|symmetric relations\|2^(card(A)(card(A)+1)/2)` | function_properties_generator.py, set_counting_generator.py |
| `COUNT_SETUP` | 1, 2 | `COUNT_SETUP\|45 boxes\|force 26 in one box` | counting_classics_generator.py |
| `COUPON` | 1 | `COUPON\|360` | bond_pricing_generator.py |
| `COVER` | 3 | `COVER\|24\|55\|no c strictly between` | partial_order_generator.py |
| `COV_ENTRY` | 2 | `COV_ENTRY\|xx\|8` | pca_generator.py |
| `COV_FORMULA` | 1 | `COV_FORMULA\|Cov=E[XY]-E[X]E[Y]` | joint_distribution_generator.py |
| `CRC_CHECK` | 3 | `CRC_CHECK\|codeword=10101100\|remainder=0000\|valid` | crc_generator.py |
| `CRC_REMAINDER` | 1 | `CRC_REMAINDER\|1100` | crc_generator.py |
| `CRC_SETUP` | 3 | `CRC_SETUP\|data=1010\|poly=11001\|augmented=10100000` | crc_generator.py |
| `CRC_SKIP` | 2 | `CRC_SKIP\|i=2\|leading bit 0` | crc_generator.py |
| `CRC_XOR` | 3 | `CRC_XOR\|i=0\|10100 xor 11001\|01101` | crc_generator.py |
| `CRIT_EQS` | 2 | `CRIT_EQS\|f_x = 0\|8*x + 3*y - 44 = 0` | hessian_classify_generator.py |
| `CRIT_SOLVE` | 3 | `CRIT_SOLVE\|det\|8*4 - 3^2\|23` | hessian_classify_generator.py |
| `CROSS_ENTROPY` | 2 | `CROSS_ENTROPY\|target=3\|ln(9/2)` | perplexity_generator.py, softmax_gradient_generator.py |
| `CROSS_MULT` | 1 | `CROSS_MULT\|40·BC = 16·25` | similar_triangles_generator.py, triangle_solve_generator.py |
| `CROSS_RATIO` | 1 | `CROSS_RATIO\|4/3` | mobius_transform_generator.py |
| `CROSS_RATIO_SETUP` | 4 | `CROSS_RATIO_SETUP\|z1=-8\|z2=-6\|z3=-3\|z4=2` | mobius_transform_generator.py |
| `CRT_CHECK` | 3 | `CRT_CHECK\|i=1\|0\|0` | crt_generator.py |
| `CRT_CONGRUENCE` | 3 | `CRT_CONGRUENCE\|i=1\|x=0\|mod 5` | crt_generator.py |
| `CRT_FACTOR` | 3 | `CRT_FACTOR\|i=1\|M_i=77\|mod 5` | crt_generator.py |
| `CRT_SETUP` | 1 | `CRT_SETUP\|3 congruences` | crt_generator.py |
| `CRT_TERM` | 2 | `CRT_TERM\|i=1\|0` | crt_generator.py |
| `CRT_TOTAL_MODULUS` | 2 | `CRT_TOTAL_MODULUS\|5, 7, 11\|385` | crt_generator.py |
| `CR_SETUP` | 2 | `CR_SETUP\|u=4x^2 - 4y^2 + 4x\|v=8xy + 3y` | cauchy_riemann_generator.py |
| `CUM_INTERVAL` | 2 | `CUM_INTERVAL\|A\|[0,1/8)` | arithmetic_coding_generator.py |
| `CURL_COMPONENT` | 3 | `CURL_COMPONENT\|i\|-5 - 5\|-10` | div_curl_generator.py |
| `CURRENT_YIELD` | 1 | `CURRENT_YIELD\|5/44` | bond_pricing_generator.py |
| `CURVATURE_FORMULA` | 2 | `CURVATURE_FORMULA\|circle\|kappa = 1/R` | curve_geometry_generator.py |
| `CURVE_GEOM_SETUP` | 3 | `CURVE_GEOM_SETUP\|r(t) = <17*cos(t), 17*sin(t)>\|at t = 0\|curvature, T, N` | curve_geometry_generator.py |
| `CURVE_SETUP` | 2 | `CURVE_SETUP\|f(x) = x^3 - 3x^2 - 45x + 3\|critical points and their nature` | curve_analysis_generator.py |
| `CX_A` | 3 | `CX_A\|0\|-28/53\|-28/53` | braket_generator.py, spin_half_generator.py |
| `CX_M` | 3 | `CX_M\|0\|-45/53\|0` | braket_generator.py, spin_half_generator.py |
| `CX_SETUP` | 2 | `CX_SETUP\|(-2 + 7i) - (-9 - 3i)\|subtract` | complex_division_generator.py, complex_number_ops_generator.py |
| `CYCLE` | 1 | `CYCLE\|(1 3 4 2 5)` | permutation_group_generator.py |
| `CYCLE_LENGTHS` | 1 | `CYCLE_LENGTHS\|5` | permutation_group_generator.py |
| `CYCLE_REJECT` | 2 | `CYCLE_REJECT\|BC\|endpoints already connected` | mst_generator.py |
| `CYCLE_TRACE` | 2 | `CYCLE_TRACE\|start 1\|1->3->4->2->5->1` | permutation_group_generator.py |
| `CYCLIC_START` | 2 | `CYCLIC_START\|3\|identity 1` | cyclic_group_generator.py |
| `CYCLIC_SUBGROUP` | 2 | `CYCLIC_SUBGROUP\|{1, 3, 9, 7}\|4` | cyclic_group_generator.py |
| `CYK_CELL` | 2 | `CYK_CELL\|1,2\|{S}` | cyk_parser_generator.py |
| `CYK_COMBINE` | 3 | `CYK_COMBINE\|T T\|{S}\|cell 1,2` | cyk_parser_generator.py |
| `CYK_RULE` | 2 | `CYK_RULE\|S\|T T` | cyk_parser_generator.py |
| `CYK_SETUP` | 2 | `CYK_SETUP\|string aeee\|length 4` | cyk_parser_generator.py |
| `CYK_SPAN` | 1 | `CYK_SPAN\|2` | cyk_parser_generator.py |
| `CYK_SPLIT` | 3 | `CYK_SPLIT\|cell 1,2\|1,1 x 2,2\|{T} x {T,X}` | cyk_parser_generator.py |
| `CYK_TERMINAL` | 3 | `CYK_TERMINAL\|cell 1,1\|a\|{T}` | cyk_parser_generator.py |
| `CYL_BOUNDS` | 2 | `CYL_BOUNDS\|z\|0..3` | triple_integral_generator.py |
| `CYL_CONVERT` | 2 | `CYL_CONVERT\|2*z dV\|2*z*r dz dr dtheta` | triple_integral_generator.py |
| `D` | 3 | `D\|632\|99\|6` | ac_circuit_generator.py, activation_generator.py, adam_step_generator.py, angle_defect_generator.py, annuity_generator.py, antiderivative_generator.py, arithmetic_coding_generator.py, arithmetic_sequence_generator.py, attention_generator.py, backprop_generator.py, bayesian_update_generator.py, bisection_generator.py, blackbody_generator.py, bond_pricing_generator.py, branching_ratio_generator.py, casimir_force_generator.py, cholesky_generator.py, christoffel_generator.py, circle_angle_generator.py, circle_equation_generator.py, classifier_metrics_generator.py, collision_generator.py, complex_number_ops_generator.py, composite_arithmetic_generator.py, confidence_interval_generator.py, conic_standard_form_generator.py, continuous_distribution_generator.py, coset_generator.py, counting_classics_generator.py, cramers_rule_generator.py, cross_section_generator.py, crt_generator.py, curve_analysis_generator.py, de_moivre_generator.py, decimal_div_generator.py, definite_integral_generator.py, dimensional_analysis_generator.py, doppler_generator.py, einstein_summation_generator.py, electrostatics_generator.py, embedding_similarity_generator.py, energy_conservation_generator.py, entropy_change_generator.py, entropy_generator.py, equilibrium_ice_generator.py, error_spotting_generator.py, exact_ode_generator.py, exponential_equation_generator.py, exponential_model_generator.py, fill_in_step_generator.py, finite_difference_generator.py, flops_memory_generator.py, fourier_series_generator.py, function_inner_product_generator.py, function_operations_generator.py, game_theory_generator.py, gas_law_generator.py, gas_stoichiometry_generator.py, gauss_bonnet_generator.py, gauss_law_generator.py, gaussian_curvature_generator.py, generating_function_generator.py, geometric_distribution_generator.py, geometric_mean_generator.py, geometric_sequence_generator.py, geometry_area_perimeter_generator.py, gradient_descent_generator.py, gradient_step_generator.py, hamiltonian_generator.py, hawking_generator.py, heat_engine_generator.py, huffman_coding_generator.py, hydrogen_atom_generator.py, hyperbolic_distance_generator.py, hyperbolic_function_generator.py, hypothesis_test_generator.py, information_gain_generator.py, integrating_factor_generator.py, interference_generator.py, interpolation_generator.py, invariant_mass_generator.py, jacobi_symbol_generator.py, joint_distribution_generator.py, kernel_ridge_generator.py, kinematics_generator.py, kl_divergence_generator.py, kmeans_step_generator.py, kraft_inequality_generator.py, ladder_operator_generator.py, lagrangian_generator.py, laplace_ivp_generator.py, laurent_series_generator.py, layer_norm_generator.py, lcm_generator.py, least_squares_generator.py, legendre_construction_generator.py, limit_evaluation_generator.py, linear_simple_generator.py, log_conversion_generator.py, logistic_growth_generator.py, long_division_generator.py, lr_schedule_generator.py, magnetism_generator.py, manual_square_root_generator.py, markov_chain_generator.py, matrix_inverse_generator.py, matrix_norm_generator.py, mean_value_theorem_generator.py, method_of_moments_generator.py, midpoint_generator.py, mle_generator.py, modular_inverse_generator.py, multi_step_unit_conversion_generator.py, naive_bayes_generator.py, named_distribution_generator.py, natural_units_generator.py, nets_surface_area_generator.py, newton_raphson_generator.py, newtons_laws_generator.py, npv_irr_generator.py, ode_substitution_generator.py, optics_generator.py, optimization_generator.py, or_formula_generator.py, orbital_mechanics_generator.py, order_of_operations_generator.py, order_statistics_generator.py, parabola_features_generator.py, param_count_generator.py, parametric_calculus_generator.py, particle_in_box_generator.py, partition_function_generator.py, pca_generator.py, percent_problem_generator.py, permutation_combination_generator.py, perplexity_generator.py, physics_formula_generator.py, planck_units_generator.py, polar_parametric_generator.py, primality_test_generator.py, projectile_motion_generator.py, proportion_word_problem_generator.py, proportional_relationship_generator.py, quadratic_residue_generator.py, quantization_generator.py, quantum_formula_generator.py, radical_rationalize_generator.py, rate_conversion_generator.py, ratio_table_generator.py, recurrence_generator.py, regression_generator.py, regular_polygon_area_generator.py, relativistic_energy_generator.py, repeating_decimal_generator.py, riemann_sum_generator.py, riemann_tensor_generator.py, right_triangle_trig_generator.py, rotational_dynamics_generator.py, round_solids_generator.py, routh_hurwitz_generator.py, runge_kutta_generator.py, running_coupling_generator.py, rv_transform_generator.py, scaling_law_generator.py, schwarzschild_generator.py, second_order_ode_generator.py, segment_partition_generator.py, separable_pde_generator.py, series_convergence_generator.py, series_solution_generator.py, set_counting_generator.py, shm_generator.py, similar_triangles_generator.py, simplex_generator.py, sinusoid_features_generator.py, slope_two_points_generator.py, softmax_gradient_generator.py, solution_chem_generator.py, special_relativity_generator.py, special_right_triangle_generator.py, spherical_excess_generator.py, spherical_triangle_generator.py, spin_half_generator.py, standard_deviation_generator.py, standing_wave_generator.py, stars_and_bars_generator.py, statics_generator.py, stereographic_generator.py, stoichiometry_generator.py, svm_margin_generator.py, taylor_series_generator.py, telescoping_generator.py, temperature_conversion_generator.py, tip_bill_split_generator.py, totient_generator.py, transient_circuit_generator.py, triangle_area_sas_generator.py, triangle_solve_generator.py, trig_identity_eval_generator.py, trig_six_functions_generator.py, two_sample_test_generator.py, u_substitution_generator.py, undetermined_coeff_generator.py, unit_conversion_generator.py, variation_parameters_generator.py, vector_ops_generator.py, wavefunction_generator.py, young_tableaux_generator.py, z_score_generator.py |
| `DALEMBERT` | 1 | `DALEMBERT\|u=(f(x-ct)+f(x+ct))/2` | separable_pde_generator.py |
| `DATA_PRECISION` | 1 | `DATA_PRECISION\|n/sigma^2` | bayesian_update_generator.py |
| `DATE_ORDINAL` | 2 | `DATE_ORDINAL\|2028-07-29\|740557` | calendar_arithmetic_generator.py |
| `DB_FORMULA` | 1 | `DB_FORMULA\|G_dB=10*log10(P2/P1)` | signal_arithmetic_generator.py |
| `DECISION` | 2 | `DECISION\|f(x)\|-3` | kernel_perceptron_generator.py, svm_margin_generator.py |
| `DECODE` | 2 | `DECODE\|1100000\|{h, j}` | characteristic_vector_generator.py |
| `DEC_ADD_COL` | 3 | `DEC_ADD_COL\|frac_0\|0+1+0\|->1 (carry 0)` | decimal_add_sub_generator.py |
| `DEC_ALIGN` | 2 | `DEC_ALIGN\|55.60\|69.81` | decimal_add_sub_generator.py |
| `DEC_CARRY_FINAL` | 1 | `DEC_CARRY_FINAL\|1` | decimal_add_sub_generator.py |
| `DEC_SHIFT` | 3 | `DEC_SHIFT\|33.0/0.2\|330/2\|1` | decimal_div_generator.py, percent_problem_generator.py |
| `DEC_SUB_COL` | 3 | `DEC_SUB_COL\|frac_0\|1-0 (borrow_in 0)\|->1 (borrow_out 0)` | decimal_add_sub_generator.py |
| `DEC_TO_FRAC` | 2 | `DEC_TO_FRAC\|4.17\|417/100` | fraction_decimal_percent_converter.py |
| `DEC_TO_PERCENT` | 2 | `DEC_TO_PERCENT\|1.075\|107.5%` | fraction_decimal_percent_converter.py, percent_problem_generator.py, tip_bill_split_generator.py |
| `DEC_TYPE` | 2 | `DEC_TYPE\|151/228\|repeating` | repeating_decimal_generator.py |
| `DEC_VALUE` | 2 | `DEC_VALUE\|151/228\|0.66(228070175438596491)` | repeating_decimal_generator.py |
| `DEDUCE` | 3 | `DEDUCE\|Finn\|item = map\|only solution left` | logic_grid_puzzle_generator.py |
| `DEDUP` | 2 | `DEDUP\|A raw [24, 57, 66, 52, 63, 66]\|{24, 52, 57, 63, 66}` | set_membership_subset_generator.py |
| `DEGREE` | 2, 3 | `DEGREE\|A\|C\|1` | euler_circuit_generator.py, graph_counting_generator.py |
| `DEGREE_COMPARE` | 2 | `DEGREE_COMPARE\|deg num = deg den = 2\|y = 1/1` | limit_evaluation_generator.py, rational_function_features_generator.py, series_convergence_generator.py |
| `DEGREE_SEQUENCE` | 1 | `DEGREE_SEQUENCE\|3, 2, 1, 1, 1` | graph_counting_generator.py |
| `DELTA_VALUE` | 2 | `DELTA_VALUE\|delta_31\|0` | index_gymnastics_generator.py |
| `DEMOIVRE_POWER` | 1 | `DEMOIVRE_POWER\|3125 cis(210 deg)` | de_moivre_generator.py |
| `DEMOIVRE_SETUP` | 2, 4 | `DEMOIVRE_SETUP\|power\|r=5\|theta=330 deg\|n=5` | de_moivre_generator.py |
| `DENSITY` | 2 | `DENSITY\|f_X(x)\|1/18` | rv_transform_generator.py |
| `DENSITY_MATRIX` | 1 | `DENSITY_MATRIX\|rho=[[1/13,0],[0,12/13]]` | density_matrix_generator.py |
| `DENSITY_SETUP` | 2, 3 | `DENSITY_SETUP\|state=plus_phase_0\|psi=(ket00 + e^(i195π/112)ket10)/sqrt(2)` | density_matrix_generator.py, partial_trace_generator.py |
| `DEPTH` | 1, 2 | `DEPTH\|3` | wff_parsing_generator.py |
| `DEQUANT_VALUE` | 2 | `DEQUANT_VALUE\|1\|4/5` | quantization_generator.py |
| `DERANGE_PROB` | 2 | `DERANGE_PROB\|D_4/4!\|9/24` | derangement_generator.py |
| `DERANGE_SETUP` | 2 | `DERANGE_SETUP\|n = 13\|no item fixed` | derangement_generator.py |
| `DERANGE_VALUE` | 2 | `DERANGE_VALUE\|D_2\|1` | derangement_generator.py |
| `DERIV` | 2, 3 | `DERIV\|d_r g_thetatheta = 2r\|at r=45\|90` | christoffel_generator.py, gaussian_curvature_generator.py, riemann_tensor_generator.py |
| `DERIVATIVE` | 1, 2 | `DERIVATIVE\|g'(x)\|4/5` | fixed_point_generator.py, mgf_generator.py, mle_generator.py |
| `DERIVED` | 2 | `DERIVED\|C5\|(P75705)` | resolution_proof_generator.py |
| `DERIV_FORM` | 2 | `DERIV_FORM\|y'\|-3C1e^(-3x) + 3C2e^(3x)` | second_order_ode_generator.py, undetermined_coeff_generator.py, variation_parameters_generator.py |
| `DERIV_RULE` | 2 | `DERIV_RULE\|power rule\|d/dx of c·x^n = c·n·x^(n-1)` | chain_rule_generator.py, derivative_power_rule_generator.py, derivative_product_quotient_generator.py, derivative_transcendental_generator.py, lhopital_generator.py, linear_approx_generator.py, log_diff_higher_order_generator.py, multivar_chain_rule_generator.py |
| `DERIV_SERIES` | 2 | `DERIV_SERIES\|y'\|sum (n+1)a_(n+1)x^n` | series_solution_generator.py |
| `DERIV_SETUP` | 2 | `DERIV_SETUP\|f(x) = 4x^5 - 4x^3 + x\|f'(x)` | chain_rule_generator.py, derivative_power_rule_generator.py, derivative_product_quotient_generator.py, derivative_transcendental_generator.py, log_diff_higher_order_generator.py, tangent_line_generator.py |
| `DESIGN_MATRIX` | 2 | `DESIGN_MATRIX\|X = [[1, -3], [1, -1], [1, 1], [1, 3]]\|y = [1, 9, 11, 7]` | least_squares_generator.py |
| `DET` | 2 | `DET\|K\|3` | kernel_ridge_generator.py, kernel_validity_generator.py |
| `DET2` | 2 | `DET2\|ad - bc\|4` | ode_system_generator.py |
| `DET_FORMULA` | 1 | `DET_FORMULA\|det = ad - bc` | cramers_rule_generator.py, determinant_generator.py, matrix_inverse_generator.py |
| `DEV_ROW` | 3 | `DEV_ROW\|4\|-6\|36` | standard_deviation_generator.py |
| `DFA_ACCEPT` | 1 | `DFA_ACCEPT\|q2` | dfa_minimization_generator.py, dfa_simulation_generator.py |
| `DFA_INPUT` | 1 | `DFA_INPUT\|0010100` | dfa_simulation_generator.py |
| `DFA_MIN_SETUP` | 3 | `DFA_MIN_SETUP\|states A, B, C, D\|alphabet 0, 1\|start A` | dfa_minimization_generator.py |
| `DFA_MIN_TRANSITION` | 3 | `DFA_MIN_TRANSITION\|A\|0\|C` | dfa_minimization_generator.py |
| `DFA_READ` | 2 | `DFA_READ\|pos 1\|0` | dfa_simulation_generator.py |
| `DFA_SETUP` | 3 | `DFA_SETUP\|states q0, q1, q2\|alphabet 0, 1\|start q0` | dfa_simulation_generator.py |
| `DFA_STATE` | 2 | `DFA_STATE\|start\|q0` | dfa_simulation_generator.py |
| `DFA_STEP` | 3 | `DFA_STEP\|q0\|0\|q0` | dfa_simulation_generator.py |
| `DFA_TRANSITION` | 3 | `DFA_TRANSITION\|q0\|0\|q0` | dfa_simulation_generator.py |
| `DFS_EDGE` | 2 | `DFS_EDGE\|A->B\|tree` | graph_traversal_generator.py |
| `DFT_BIN` | 1 | `DFT_BIN\|X0=x0+x1` | dft_generator.py |
| `DFT_SETUP` | 2 | `DFT_SETUP\|N=2\|x=[3,1]` | dft_generator.py |
| `DH_PUBLIC` | 2 | `DH_PUBLIC\|Alice\|11` | diffie_hellman_generator.py |
| `DH_SECRET` | 2 | `DH_SECRET\|Alice\|19` | diffie_hellman_generator.py |
| `DH_SETUP` | 2 | `DH_SETUP\|p=29\|g=26` | diffie_hellman_generator.py |
| `DH_SHARED` | 2 | `DH_SHARED\|Alice\|26` | diffie_hellman_generator.py |
| `DIAG_FORM` | 3 | `DIAG_FORM\|P = [[1, 5], [-1, -6]]\|D = [[-7, 0], [0, -4]]\|P^-1 = [[6, 5], [-1, -1]]` | diagonalization_generator.py, matrix_exponential_generator.py |
| `DIFF_ROW` | 2 | `DIFF_ROW\|Delta y\|[-6, 2, 10]` | finite_difference_generator.py |
| `DIFF_SETUP` | 3 | `DIFF_SETUP\|f(x,y) = 3*x^2 + y^2 - 3*x*y + x + 5*y\|point (3, -3)\|dx=1/2, dy=-1/2` | multivar_chain_rule_generator.py |
| `DIFF_SUM` | 3 | `DIFF_SUM\|f_x*dx + f_y*dy\|28*1/2 + (-10)*(-1/2)\|19` | multivar_chain_rule_generator.py |
| `DIJKSTRA_INIT` | 2 | `DIJKSTRA_INIT\|start A\|A=0, B=inf, C=inf, D=inf, E=inf, F=inf` | dijkstra_generator.py |
| `DIM` | 2 | `DIM\|2*6+1\|13` | casimir_generator.py |
| `DIRECTRIX` | 1 | `DIRECTRIX\|y = -1` | parabola_features_generator.py |
| `DISC` | 2, 3 | `DISC\|13689\|0\|13689` | complex_quadratic_generator.py, discriminant_generator.py, polynomial_zeros_generator.py, quadratic_generator.py |
| `DISC_CLASSIFY` | 2 | `DISC_CLASSIFY\|121 > 0\|two real solutions` | complex_quadratic_generator.py, discriminant_generator.py, polynomial_zeros_generator.py |
| `DIST` | 3 | `DIST\|2\|-5x+4\|-10x+8` | derivative_limit_def_generator.py, derivative_product_quotient_generator.py, equation_from_two_points_generator.py, function_composition_generator.py, parallel_perpendicular_line_generator.py, point_slope_generator.py, polar_parametric_generator.py, radical_multiply_generator.py, radical_rationalize_generator.py, rational_expr_add_sub_generator.py, recursive_explicit_generator.py, simplify_expression_generator.py, solid_revolution_generator.py, special_solution_equation_generator.py, tangent_line_generator.py |
| `DIST2` | 2, 3 | `DIST2\|P1\|C1\|49` | embedding_similarity_generator.py, kernel_evaluation_generator.py, kmeans_step_generator.py |
| `DIST_COMBINE` | 1 | `DIST_COMBINE\|-y - 33 = -32` | systems_substitution_generator.py |
| `DIST_FORMULA` | 1 | `DIST_FORMULA\|d = √((x2 - x1)^2 + (y2 - y1)^2)` | complex_locus_generator.py, distance_formula_generator.py, hypercube_counting_generator.py |
| `DIST_SETUP` | 3 | `DIST_SETUP\|exponential\|target=P(X<t)\|e^(-lambda*t)=1/19` | named_distribution_generator.py |
| `DIST_TABLE` | 2 | `DIST_TABLE\|visited A\|A=0, B=3, C=inf, D=9, E=inf, F=inf` | dijkstra_generator.py |
| `DIST_TERM` | 2 | `DIST_TERM\|-4x\|8x^3 - 8x^2 - 20x` | multiplying_polynomials_generator.py |
| `DIVIDE_EQ` | 2 | `DIVIDE_EQ\|divide by y^2\|y^(-2)dy/dx + 3y^(-1) = 3` | ode_substitution_generator.py |
| `DIVMOD` | 3, 4 | `DIVMOD\|210\|2\|105\|r=0` | base_conversion_generator.py, recursive_definition_unfold_generator.py |
| `DIV_CHECK` | 3 | `DIV_CHECK\|6\|2\|remainder 0` | conditional_forms_generator.py, counterexample_search_generator.py, divisibility_classification_generator.py, logical_connective_eval_generator.py, set_builder_roster_generator.py |
| `DIV_COEFF` | 3 | `DIV_COEFF\|-7\|8\|x=-7/8` | linear_complex_generator.py |
| `DIV_SETUP` | 2 | `DIV_SETUP\|330\|2` | decimal_div_generator.py, percent_problem_generator.py |
| `DIV_SUM` | 3 | `DIV_SUM\|P_x + Q_y + R_z\|1 + 1 + 6\|8` | div_curl_generator.py |
| `DIV_TERM` | 3 | `DIV_TERM\|6x^5\|6x^2\|x^3` | factor_gcf_generator.py, finite_field_generator.py, polynomial_long_division_generator.py |
| `DNF_FORM` | 1 | `DNF_FORM\|(NOT V AND NOT W AND X) OR (V AND NOT W AND X) OR (V AND W AND NOT X) OR (V AND W AND X)` | boolean_algebra_generator.py |
| `DOMAIN` | 1, 2 | `DOMAIN\|x = −45..−35\|{−45, −44, −43, −42, −41, −40, −39, −38, −37, −36, −35}` | relation_operations_generator.py, set_builder_roster_generator.py |
| `DOMAIN_COND` | 2 | `DOMAIN_COND\|denominator ≠ 0\|x + 8 ≠ 0` | domain_range_generator.py |
| `DOMAIN_NOTE` | 2 | `DOMAIN_NOTE\|x ≠ 0\|denominator cannot be zero` | domain_range_generator.py, log_equation_generator.py, logistic_growth_generator.py, probability_addition_rule_generator.py, rational_equation_generator.py, unit_circle_generator.py |
| `DOPPLER_FORMULA` | 1 | `DOPPLER_FORMULA\|f_obs=f*(v+v_observer)/(v-v_source)` | doppler_generator.py |
| `DOPPLER_SETUP` | 3 | `DOPPLER_SETUP\|acoustic_toward\|f=919, v=52\|v_observer=7, v_source=14` | doppler_generator.py |
| `DOT` | 2, 3 | `DOT\|(18, 3) · (0, 1)\|18*0 + 3*1\|3` | embedding_similarity_generator.py, feature_map_generator.py, fundamental_form_generator.py, gradient_generator.py, gram_schmidt_generator.py, kernel_evaluation_generator.py, line_integral_generator.py, lll_reduction_generator.py, qr_decomposition_generator.py |
| `DOT4` | 4 | `DOT4\|gamma1gamma0\|(1,1)\|0*-1 + -1*0 + 0*0 + 0*0\|0` | gamma_matrix_generator.py |
| `DOT_FORMULA` | 1 | `DOT_FORMULA\|cos θ = (u·v)/(‖u‖ · ‖v‖)` | dot_product_generator.py |
| `DOUBLE_SETUP` | 2, 3 | `DOUBLE_SETUP\|integrand 2*x + 4*y + 1\|x:2..7\|y:0..4` | double_integral_generator.py |
| `DPLL_BACKTRACK` | 2 | `DPLL_BACKTRACK\|A\|True` | dpll_trace_generator.py |
| `DPLL_BRANCH` | 3 | `DPLL_BRANCH\|depth 0\|A\|True` | dpll_trace_generator.py |
| `DPLL_CONFLICT` | 1 | `DPLL_CONFLICT\|A=True, B=True` | dpll_trace_generator.py |
| `DPLL_SAT` | 1 | `DPLL_SAT\|A=True, B=True, C=True` | dpll_trace_generator.py |
| `DPLL_SETUP` | 3 | `DPLL_SETUP\|(A OR B) AND (A OR not B) AND (not A OR B) AND (not A OR not B)\|variables A, B\|True first` | dpll_trace_generator.py |
| `DPLL_SIMPLIFY` | 2 | `DPLL_SIMPLIFY\|A=True, B=True\|conflict` | dpll_trace_generator.py |
| `DPLL_STATE` | 3 | `DPLL_STATE\|depth 0\|none\|4 clauses left` | dpll_trace_generator.py |
| `DPLL_UNIT` | 2 | `DPLL_UNIT\|(B)\|B=True` | dpll_trace_generator.py |
| `DP_CELL` | 3 | `DP_CELL\|i=1,amount=0\|base empty set\|1` | dp_table_generator.py |
| `DP_COINS` | 1 | `DP_COINS\|1, 2, 3` | dp_table_generator.py |
| `DP_ITEMS` | 1 | `DP_ITEMS\|1:(w=4,v=4); 2:(w=3,v=3); 3:(w=3,v=3)` | dp_table_generator.py |
| `DP_ROW` | 2 | `DP_ROW\|i=0\|1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0` | dp_table_generator.py |
| `DP_SETUP` | 2, 3 | `DP_SETUP\|coin change\|target 10` | dp_table_generator.py |
| `D_POWER` | 2 | `D_POWER\|D^3\|[[-216, 0], [0, -125]]` | diagonalization_generator.py |
| `E` | 3 | `E\|2\|2\|4` | ac_circuit_generator.py, adam_step_generator.py, angle_defect_generator.py, annuity_generator.py, arc_sector_generator.py, backprop_generator.py, bec_channel_generator.py, blackbody_generator.py, bond_pricing_generator.py, casimir_force_generator.py, casimir_generator.py, christoffel_generator.py, circle_equation_generator.py, complex_division_generator.py, complex_locus_generator.py, confidence_interval_generator.py, conic_standard_form_generator.py, continuous_distribution_generator.py, de_moivre_generator.py, definite_integral_generator.py, density_matrix_generator.py, derivative_limit_def_generator.py, diagonalization_generator.py, distance_formula_generator.py, doppler_generator.py, electrostatics_generator.py, ellipse_features_generator.py, embedding_similarity_generator.py, energy_conservation_generator.py, euler_formula_generator.py, exponential_equation_generator.py, exponential_model_generator.py, factor_special_forms_generator.py, feature_map_generator.py, finance_generator.py, four_vector_generator.py, fractal_iteration_generator.py, function_composition_generator.py, function_evaluation_generator.py, function_operations_generator.py, function_table_generator.py, fundamental_form_generator.py, gauss_bonnet_generator.py, gauss_law_generator.py, gaussian_curvature_generator.py, geometric_mean_generator.py, geometric_sequence_generator.py, gradient_descent_generator.py, gradient_step_generator.py, hamiltonian_generator.py, hawking_generator.py, hermitian_check_generator.py, huffman_coding_generator.py, hydrogen_atom_generator.py, hyperbola_features_generator.py, hyperbolic_function_generator.py, hypercube_counting_generator.py, invariant_mass_generator.py, kernel_evaluation_generator.py, kmeans_step_generator.py, knn_generator.py, kraft_inequality_generator.py, lagrangian_generator.py, laurent_series_generator.py, layer_norm_generator.py, limit_evaluation_generator.py, log_conversion_generator.py, log_equation_generator.py, log_properties_generator.py, low_rank_approx_generator.py, matrix_group_check_generator.py, matrix_norm_generator.py, mean_value_theorem_generator.py, metric_arc_length_generator.py, mgf_generator.py, minkowski_interval_generator.py, mobius_transform_generator.py, named_distribution_generator.py, natural_units_generator.py, npv_irr_generator.py, optimization_generator.py, or_formula_generator.py, orbital_mechanics_generator.py, order_statistics_generator.py, particle_in_box_generator.py, pca_generator.py, piecewise_evaluation_generator.py, planck_units_generator.py, polar_parametric_generator.py, portfolio_generator.py, projectile_motion_generator.py, pythag_hyp_generator.py, radical_equation_generator.py, radical_multiply_generator.py, radical_rationalize_generator.py, rational_exponent_generator.py, recursive_explicit_generator.py, regression_generator.py, related_rates_generator.py, relativistic_energy_generator.py, remainder_factor_theorem_generator.py, riemann_tensor_generator.py, rotational_dynamics_generator.py, round_solids_generator.py, rv_transform_generator.py, schwarzschild_generator.py, set_counting_generator.py, set_operations_generator.py, shm_generator.py, spherical_excess_generator.py, spin_half_generator.py, stereographic_generator.py, svm_margin_generator.py, tangent_line_generator.py, taylor_series_generator.py, triangle_solve_generator.py, trig_identity_eval_generator.py, trig_six_functions_generator.py, uncertainty_generator.py, vector_ops_generator.py, wavefunction_generator.py, z_transform_generator.py |
| `ECDH_SETUP` | 2 | `ECDH_SETUP\|E:y^2=x^3+2x+2 over F_17\|G=(5,1)` | ecdh_generator.py |
| `ECDSA_NONCE` | 2 | `ECDSA_NONCE\|kG=(10,6)\|r=10` | ecdsa_generator.py |
| `ECDSA_PUBLIC` | 1 | `ECDSA_PUBLIC\|Q=dG=(7,6)` | ecdsa_generator.py |
| `ECDSA_SETUP` | 4 | `ECDSA_SETUP\|E/F_17, G=(5,1), n=19\|d=9\|z=8\|k=3` | ecdsa_generator.py |
| `ECDSA_SIGN` | 2 | `ECDSA_SIGN\|s=k^-1(z+rd) mod n\|s=1` | ecdsa_generator.py |
| `ECDSA_VERIFY` | 2 | `ECDSA_VERIFY\|u1=8\|u2=10` | ecdsa_generator.py |
| `EC_ACCUM` | 2 | `EC_ACCUM\|1P\|(7,3)` | elliptic_curve_finite_field_generator.py |
| `EC_ADD` | 1 | `EC_ADD\|(10,6)` | ecdsa_generator.py |
| `EC_IDENTITY` | 2 | `EC_IDENTITY\|O + Q\|(7,3)` | elliptic_curve_finite_field_generator.py |
| `EC_INVERSE` | 3 | `EC_INVERSE\|(2,7)\|(2,12)\|O` | elliptic_curve_finite_field_generator.py |
| `EC_POINT_CHECK` | 3 | `EC_POINT_CHECK\|P\|y^2 mod p = 2\|x^3+ax+b mod p = 2` | elliptic_curve_finite_field_generator.py |
| `EC_PUBLIC` | 2 | `EC_PUBLIC\|A=(16,13)\|B=(10,6)` | ecdh_generator.py |
| `EC_SCALAR` | 2 | `EC_SCALAR\|a=6\|aG=(16,13)` | ecdh_generator.py, ecdsa_generator.py |
| `EC_SCALAR_SETUP` | 2 | `EC_SCALAR_SETUP\|k=6\|P=(7,3)` | elliptic_curve_finite_field_generator.py |
| `EC_SETUP` | 3 | `EC_SETUP\|p=23\|a=1\|b=4` | elliptic_curve_finite_field_generator.py |
| `EC_SHARED` | 2 | `EC_SHARED\|aB=(5,16)\|bA=(5,16)` | ecdh_generator.py |
| `EC_SLOPE` | 2 | `EC_SLOPE\|P+Q\|16` | elliptic_curve_finite_field_generator.py |
| `EC_SLOPE_FORMULA` | 2 | `EC_SLOPE_FORMULA\|P+Q\|(y2-y1)/(x2-x1)` | elliptic_curve_finite_field_generator.py |
| `EC_X3` | 2 | `EC_X3\|P+Q\|9` | elliptic_curve_finite_field_generator.py |
| `EC_Y3` | 2 | `EC_Y3\|P+Q\|11` | elliptic_curve_finite_field_generator.py |
| `EDGE_CHOOSE` | 3 | `EDGE_CHOOSE\|AB\|weight 2\|add B` | mst_generator.py |
| `EDGE_CONSIDER` | 2 | `EDGE_CONSIDER\|BD\|weight 7` | mst_generator.py |
| `EDGE_COUNT` | 2 | `EDGE_COUNT\|m\|4` | euler_circuit_generator.py, graph_counting_generator.py |
| `EDGE_LIST` | 1 | `EDGE_LIST\|AB, AC, BC, CD` | euler_circuit_generator.py |
| `EDGE_WEIGHT` | 2 | `EDGE_WEIGHT\|AB\|3` | dijkstra_generator.py, mst_generator.py |
| `EIGENPAIR` | 2 | `EIGENPAIR\|lambda = 1\|[2, 1]` | ode_system_generator.py |
| `EIGENVALUE` | 1, 2 | `EIGENVALUE\|λ = -5\|p(-5) = 0` | diagonalization_generator.py, eigenvalue_generator.py, matrix_exponential_generator.py, separable_pde_generator.py, svd_generator.py |
| `EIGENVALUES` | 2 | `EIGENVALUES\|A^T A\|36,49` | low_rank_approx_generator.py, matrix_norm_generator.py, pca_generator.py |
| `EIGENVECTOR` | 2 | `EIGENVECTOR\|A + 5I times v = 0\|[4, -5]` | diagonalization_generator.py, eigenvalue_generator.py, matrix_exponential_generator.py, svd_generator.py |
| `EIGEN_CHECK` | 3 | `EIGEN_CHECK\|sigma_z psi\|-1*psi\|lambda=-1` | spin_half_generator.py |
| `EIGEN_MATRIX` | 2 | `EIGEN_MATRIX\|A + 5I\|[[5, 4], [0, 0]]` | eigenvalue_generator.py |
| `EINSTEIN_SETUP` | 2, 3 | `EINSTEIN_SETUP\|trace\|T_ij=[[-6, 5, 6], [2, -2, 1], [-6, 1, 0]]` | einstein_summation_generator.py |
| `ELEC_FORMULA` | 1 | `ELEC_FORMULA\|left charge: E1=q1/r1^2` | electrostatics_generator.py |
| `ELEC_SETUP` | 2, 3 | `ELEC_SETUP\|field_axis\|q1=9, x1=-7\|q2=2, x2=1` | electrostatics_generator.py |
| `ELEMENT_ORDER` | 2 | `ELEMENT_ORDER\|7\|11` | cayley_table_generator.py |
| `ELEMENT_SCAN` | 3 | `ELEMENT_SCAN\|30\|A\|found` | set_expression_generator.py, set_membership_subset_generator.py, set_operations_generator.py |
| `ELIMINATE` | 1, 3 | `ELIMINATE\|clue 1\|Finn: flute; Iris: kite; Ravi: map\|violates clue` | logic_grid_puzzle_generator.py, newtons_laws_generator.py |
| `ELIMINATE_LAMBDA` | 2 | `ELIMINATE_LAMBDA\|f_x = f_y\|y = 2*x` | lagrange_multiplier_generator.py |
| `EL_EQUATION` | 1 | `EL_EQUATION\|mL^2*thetaddot+mgL*sin(theta)=0` | lagrangian_generator.py |
| `EL_SOLVE` | 2 | `EL_SOLVE\|thetaddot\|-(10/9)*sin(theta)` | lagrangian_generator.py |
| `EMBED_SETUP` | 1 | `EMBED_SETUP\|A=(7,24), B=(-5,12), C=(3,4)` | embedding_similarity_generator.py |
| `ENERGY_FORMULA` | 1 | `ENERGY_FORMULA\|mgh=1/2*m*v^2` | energy_conservation_generator.py |
| `ENERGY_LEVEL` | 2 | `ENERGY_LEVEL\|E_28=hbar*omega*(n+1/2)\|2280` | ladder_operator_generator.py |
| `ENERGY_SETUP` | 3 | `ENERGY_SETUP\|gravity_drop\|m=3\|h=605, g=10` | energy_conservation_generator.py |
| `ENERGY_TERM` | 1 | `ENERGY_TERM\|T=1/2*m*L^2*thetadot^2` | lagrangian_generator.py |
| `ENGINE_FORMULA` | 1 | `ENGINE_FORMULA\|W=Qh-Qc` | heat_engine_generator.py |
| `ENGINE_SETUP` | 3 | `ENGINE_SETUP\|engine_efficiency\|Qh=25\|Qc=10` | heat_engine_generator.py |
| `ENQUEUE` | 3 | `ENQUEUE\|B\|from A\|B` | graph_traversal_generator.py |
| `ENTER` | 2 | `ENTER\|x\|most negative reduced cost -4` | simplex_generator.py |
| `ENTROPY_FORMULA` | 1 | `ENTROPY_FORMULA\|DeltaS=nCv*ln(T2/T1)` | entropy_change_generator.py |
| `ENTROPY_SETUP` | 2, 3 | `ENTROPY_SETUP\|eigenvalues=[1/32,1/16,1/16,1/32,1/16,1/8,1/4,1/32,1/4,1/16,1/32]\|S=-sum lambda log2(lambda)` | entropy_change_generator.py, entropy_generator.py, huffman_coding_generator.py, information_gain_generator.py, mutual_information_generator.py, von_neumann_entropy_generator.py |
| `ENTROPY_SKIP` | 2 | `ENTROPY_SKIP\|H(X,Y)\|p=0` | mutual_information_generator.py |
| `ENTROPY_TERM` | 4 | `ENTROPY_TERM\|row 0\|p=3/4\|I=0.415\|249/800` | entropy_rate_markov_generator.py |
| `ENTROPY_VALUE` | 2 | `ENTROPY_VALUE\|parent\|0.9888125` | information_gain_generator.py |
| `ENTROPY_ZERO` | 2 | `ENTROPY_ZERO\|color_left\|count=0` | information_gain_generator.py |
| `EPSILON_VALUE` | 2 | `EPSILON_VALUE\|eps_132\|-1` | index_gymnastics_generator.py |
| `EPS_CLOSURE` | 2 | `EPS_CLOSURE\|{s1}\|{s1}` | nfa_simulation_generator.py |
| `EQUATE_EXP` | 1 | `EQUATE_EXP\|2x - 3 = 1` | exponential_equation_generator.py |
| `EQUILIBRIA` | 2 | `EQUILIBRIA\|f(y) = 0\|y=-6, y=-2, y=10` | stability_generator.py |
| `EQ_2PT_SETUP` | 2 | `EQ_2PT_SETUP\|(3, -6)\|(5, -5)` | equation_from_two_points_generator.py |
| `EQ_OP_BOTH` | 3, 4 | `EQ_OP_BOTH\|multiply\|5\|x\|-25` | absolute_value_equation_generator.py, area_between_curves_generator.py, completing_square_generator.py, curve_analysis_generator.py, error_spotting_generator.py, exponential_equation_generator.py, fill_in_step_generator.py, implicit_diff_generator.py, inverse_function_generator.py, linear_fractional_generator.py, log_diff_higher_order_generator.py, log_equation_generator.py, mean_value_theorem_generator.py, one_step_equation_generator.py, optimization_generator.py, partial_fractions_generator.py, polar_parametric_generator.py, quadratic_factoring_generator.py, quadratic_square_root_generator.py, radical_equation_generator.py, rational_equation_generator.py, related_rates_generator.py, remainder_factor_theorem_generator.py, separable_ode_generator.py, special_solution_equation_generator.py, systems_elimination_generator.py, systems_substitution_generator.py, trig_equation_generator.py, two_step_equation_generator.py |
| `EQ_OP_NOTE` | 3 | `EQ_OP_NOTE\|add\|p\|to both sides` | equation_from_two_points_generator.py, literal_equation_generator.py, parallel_perpendicular_line_generator.py, point_slope_generator.py, standard_form_conversion_generator.py |
| `EQ_RESULT` | 2 | `EQ_RESULT\|x\|-25` | completing_square_generator.py, error_spotting_generator.py, fill_in_step_generator.py, linear_fractional_generator.py, linear_simple_generator.py, one_step_equation_generator.py, quadratic_factoring_generator.py, quadratic_square_root_generator.py, radical_equation_generator.py, rational_equation_generator.py, special_solution_equation_generator.py, two_step_equation_generator.py |
| `EQ_SETUP` | 1, 2 | `EQ_SETUP\|x = 6/2` | area_between_curves_generator.py, completing_square_generator.py, complex_quadratic_generator.py, cramers_rule_generator.py, discriminant_generator.py, error_spotting_generator.py, exponential_equation_generator.py, fill_in_step_generator.py, linear_fractional_generator.py, literal_equation_generator.py, log_equation_generator.py, one_step_equation_generator.py, polynomial_zeros_generator.py, proportion_word_problem_generator.py, proportional_relationship_generator.py, quadratic_factoring_generator.py, quadratic_generator.py, quadratic_square_root_generator.py, radical_equation_generator.py, rational_equation_generator.py, remainder_factor_theorem_generator.py, special_solution_equation_generator.py, standard_form_conversion_generator.py, trig_equation_generator.py, two_step_equation_generator.py |
| `EQ_SIMPLIFY` | 1 | `EQ_SIMPLIFY\|x/4 = -2` | error_spotting_generator.py, fill_in_step_generator.py, linear_fractional_generator.py, two_step_equation_generator.py |
| `ESCAPE_CHECK` | 3 | `ESCAPE_CHECK\|n=1\|norm2=109/16\|escaped` | fractal_iteration_generator.py |
| `ESTIMATE` | 2 | `ESTIMATE\|97702 × 14594 ≈ 100000 × 10000\|1000000000` | long_division_generator.py, multi_digit_multiplication_generator.py |
| `ESTIMATE_CHECK` | 3 | `ESTIMATE_CHECK\|4.5 × 10^6\|4500000\|rounded estimate` | fermi_estimation_generator.py, long_division_generator.py, multi_digit_multiplication_generator.py |
| `EUCLID_DIV` | 4 | `EUCLID_DIV\|177\|120\|1\|57` | continued_fraction_generator.py, extended_euclid_generator.py, modular_inverse_generator.py, rsa_generator.py |
| `EULER_BACKTRACK` | 3 | `EULER_BACKTRACK\|D\|route suffix D\|stack C-A-B-C` | euler_circuit_generator.py |
| `EULER_CRITERION` | 2 | `EULER_CRITERION\|41^18 mod 37\|1` | quadratic_residue_generator.py |
| `EULER_FORMULA` | 1 | `EULER_FORMULA\|χ = V - E + F` | euler_characteristic_generator.py, euler_formula_generator.py |
| `EULER_NOTE` | 2 | `EULER_NOTE\|2\|sphere-family polyhedron: χ is always 2` | euler_characteristic_generator.py |
| `EULER_ROUTE` | 2 | `EULER_ROUTE\|C-A-B-C-D\|uses 4 edges` | euler_circuit_generator.py |
| `EULER_SETUP` | 2, 3 | `EULER_SETUP\|octahedron: V = 6, E = 12, F = 8\|V - E + F` | euler_characteristic_generator.py, euler_formula_generator.py |
| `EULER_STACK` | 2 | `EULER_STACK\|initial\|C` | euler_circuit_generator.py |
| `EULER_START` | 2 | `EULER_START\|C\|alphabetically first odd vertex` | euler_circuit_generator.py |
| `EULER_TRAVERSE` | 3 | `EULER_TRAVERSE\|C->A\|AC\|stack C-A` | euler_circuit_generator.py |
| `EVAL` | 1, 2, 3 | `EVAL\|g(6)\|-35` | arc_length_generator.py, area_between_curves_generator.py, circle_equation_generator.py, complex_division_generator.py, composite_arithmetic_generator.py, conic_standard_form_generator.py, cramers_rule_generator.py, definite_integral_generator.py, derivative_limit_def_generator.py, determinant_generator.py, dot_product_generator.py, ellipse_features_generator.py, euler_method_generator.py, exact_ode_generator.py, five_number_summary_generator.py, function_composition_generator.py, function_operations_generator.py, horner_evaluation_generator.py, hyperbola_features_generator.py, improper_integral_generator.py, lagrange_multiplier_generator.py, legendre_construction_generator.py, limit_evaluation_generator.py, line_integral_generator.py, linear_approx_generator.py, log_conversion_generator.py, log_properties_generator.py, matrix_inverse_generator.py, mean_value_theorem_generator.py, ode_substitution_generator.py, parabola_features_generator.py, parametric_calculus_generator.py, partial_fractions_generator.py, power_series_generator.py, recursive_explicit_generator.py, regular_polygon_area_generator.py, related_rates_generator.py, remainder_factor_theorem_generator.py, riemann_sum_generator.py, row_reduction_generator.py, runge_kutta_generator.py, solid_revolution_generator.py, standard_deviation_generator.py, tangent_line_generator.py, taylor_series_generator.py, triangle_solve_generator.py, trig_equation_generator.py, trig_identity_eval_generator.py, trig_six_functions_generator.py, vector_ops_generator.py |
| `EVAL_AT_ZERO` | 2 | `EVAL_AT_ZERO\|e^0=1\|e^(2*0)=1` | mgf_generator.py |
| `EVAL_PARTIAL` | 3 | `EVAL_PARTIAL\|f_x\|10*2 + 3 + 4\|27` | gradient_generator.py, multivar_chain_rule_generator.py |
| `EVAL_SUB` | 3 | `EVAL_SUB\|p=T, q=T, r=T\|formula: ¬r\|F` | set_identity_membership_table_generator.py, truth_table_generator.py |
| `EV_FORMULA` | 1 | `EV_FORMULA\|E = Σ (payoff)·P` | expected_value_generator.py |
| `EV_SETUP` | 2 | `EV_SETUP\|P($4) = 3/5; P($-8) = 1/5; P($6) = 1/5\|expected value of the game` | expected_value_generator.py |
| `EXACT_MATCH` | 2 | `EXACT_MATCH\|F_y = N\|-4*x + g'(y) = -4*x + 4*y - 1` | exact_ode_generator.py |
| `EXPAND` | 1, 2 | `EXPAND\|j = vz\|j = (sm)z` | complex_locus_generator.py, direct_proof_algebra_generator.py, mobius_transform_generator.py |
| `EXPECTATION` | 3 | `EXPECTATION\|E[X]=11/37\|E[Y]=11/37\|E[XY]=264/1369` | joint_distribution_generator.py |
| `EXPECTED_PAYOFF` | 1 | `EXPECTED_PAYOFF\|row1 against q` | game_theory_generator.py |
| `EXP_APPLY` | 2 | `EXP_APPLY\|x(t) = e^(At)x(0)\|x(0) = [-1, -6]` | matrix_exponential_generator.py |
| `EXP_CELL` | 2 | `EXP_CELL\|(40·40)/200\|8` | chi_square_generator.py |
| `EXP_DIAG` | 2 | `EXP_DIAG\|e^(Dt)\|[[e^(-6t), 0], [0, e^(-5t)]]` | matrix_exponential_generator.py |
| `EXP_ENTRY` | 3 | `EXP_ENTRY\|(1,1)\|-6*e^(-6t) + 7*e^(-5t)\|-6*e^(-6t) + 7*e^(-5t)` | matrix_exponential_generator.py |
| `EXP_EXPAND` | 1 | `EXP_EXPAND\|(-0.3) × (-0.3)` | exponent_generator.py |
| `EXP_FORM` | 1 | `EXP_FORM\|e^(At) = P*e^(Dt)*P^-1` | euler_formula_generator.py, matrix_exponential_generator.py |
| `EXP_PARTIAL` | 3 | `EXP_PARTIAL\|-0.3\|-0.3\|0.09` | exponent_generator.py |
| `EXP_RULE_APPLY` | 3, 4 | `EXP_RULE_APPLY\|add\|26\|18\|44` | exponent_generator.py, exponent_mixed_rules_generator.py |
| `EXP_RULE_IDENTIFY` | 2 | `EXP_RULE_IDENTIFY\|product_rule\|x^a · x^b = x^(a+b)` | exponent_generator.py, exponent_mixed_rules_generator.py, rational_exponent_generator.py |
| `EXP_RULE_SETUP` | 1 | `EXP_RULE_SETUP\|p^26 · p^18` | exponent_generator.py, exponent_mixed_rules_generator.py, rational_exponent_generator.py |
| `EXP_RULE_SIMPLIFY` | 1 | `EXP_RULE_SIMPLIFY\|p^44` | exponent_generator.py, exponent_mixed_rules_generator.py |
| `EXP_SETUP` | 2 | `EXP_SETUP\|-0.3\|2` | exponent_generator.py |
| `EXP_SUB` | 3 | `EXP_SUB\|t/tau\|3\|e^-3` | transient_circuit_generator.py |
| `EXP_VALUE` | 2 | `EXP_VALUE\|exp(-z)\|1` | activation_generator.py |
| `EXT_GCD_SETUP` | 2 | `EXT_GCD_SETUP\|177\|120` | extended_euclid_generator.py, modular_inverse_generator.py, rsa_generator.py |
| `F` | 2, 3 | `F\|4/6\|2/3` | composite_arithmetic_generator.py, derangement_generator.py, fraction_decimal_percent_converter.py, fraction_op_generator.py, mixed_number_operation_generator.py, mobius_transform_generator.py, order_of_operations_generator.py, quaternion_generator.py, radical_rationalize_generator.py, rational_exponent_generator.py, rational_expr_add_sub_generator.py, repeating_decimal_generator.py, simple_probability_generator.py, slope_two_points_generator.py |
| `FACT` | 2 | `FACT\|9\|362880` | derangement_generator.py, named_distribution_generator.py, order_statistics_generator.py, young_tableaux_generator.py |
| `FACTOR` | 1, 2 | `FACTOR\|j = s(mz)` | direct_proof_algebra_generator.py, polynomial_inequality_generator.py, second_order_ode_generator.py, transfer_function_generator.py, undetermined_coeff_generator.py, variation_parameters_generator.py |
| `FACTOR_FORM` | 2 | `FACTOR_FORM\|42\|2 * 3 * 7` | totient_generator.py |
| `FACTOR_FOUND` | 2 | `FACTOR_FOUND\|2\|1` | totient_generator.py |
| `FACTOR_GROUP` | 3 | `FACTOR_GROUP\|3y^2 - 12y\|3y\|(y - 4)` | conic_standard_form_generator.py, curve_analysis_generator.py, derivative_limit_def_generator.py, factor_grouping_generator.py, factor_trinomial_generator.py |
| `FACTOR_PAIR_GOAL` | 2 | `FACTOR_PAIR_GOAL\|m·n = -5\|m + n = 4` | factor_trinomial_generator.py |
| `FACTOR_SETUP` | 1 | `FACTOR_SETUP\|42` | totient_generator.py |
| `FACT_CHECK` | 3 | `FACT_CHECK\|375\|1\|0` | factors_generator.py |
| `FACT_FORMULA` | 1 | `FACT_FORMULA\|10! = 1·2·3·4·5·6·7·8·9·10` | derangement_generator.py, permutation_combination_generator.py |
| `FACT_PAIR` | 2 | `FACT_PAIR\|1\|375` | factors_generator.py |
| `FACT_SETUP` | 2 | `FACT_SETUP\|10!\|expand the factorial` | permutation_combination_generator.py |
| `FACT_VALUE` | 2 | `FACT_VALUE\|10!\|3628800` | stars_and_bars_generator.py |
| `FEATURE_MAP_SETUP` | 3 | `FEATURE_MAP_SETUP\|K(x,z)=(xz+2)^2\|phi(t)=(t^2,2t,2)\|x=-1,z=-13` | feature_map_generator.py |
| `FEATURE_VECTOR` | 2 | `FEATURE_VECTOR\|phi(x)\|(1,-2,2)` | feature_map_generator.py |
| `FEEDBACK` | 1 | `FEEDBACK\|T=G/(1+G)` | transfer_function_generator.py |
| `FERMAT_SETUP` | 3 | `FERMAT_SETUP\|prime 23\|base 64\|exponent 114` | totient_generator.py |
| `FERMI_FACTOR` | 2 | `FERMI_FACTOR\|people\|36000` | fermi_estimation_generator.py |
| `FERMI_SETUP` | 2 | `FERMI_SETUP\|town daily water use\|gallons/day` | fermi_estimation_generator.py |
| `FIELD_SETUP` | 2 | `FIELD_SETUP\|Z_5[x]\|mod 5` | finite_field_generator.py |
| `FIND_SLOPE` | 2 | `FIND_SLOPE\|Given slope (m1)\|-3/2` | parallel_perpendicular_line_generator.py |
| `FINITE_DIFF_SETUP` | 3 | `FINITE_DIFF_SETUP\|forward_derivative\|x0=1,h=1\|f0=2,f1=-7` | finite_difference_generator.py |
| `FIN_FORMULA` | 1 | `FIN_FORMULA\|interest = balance*monthly rate; principal = payment - interest` | finance_generator.py |
| `FIN_SETUP` | 3 | `FIN_SETUP\|loan balance = 1900\|payment = 188, annual rate = 24%\|one-payment breakdown` | finance_generator.py |
| `FIRSTLAW_FORMULA` | 1 | `FIRSTLAW_FORMULA\|W=P*(V2-V1)` | first_law_generator.py |
| `FIRSTLAW_SETUP` | 3 | `FIRSTLAW_SETUP\|isobaric\|P=13, V1=6, V2=2\|Q=116` | first_law_generator.py |
| `FIXED_CHECK` | 3 | `FIXED_CHECK\|i\|f(i) = y\|not fixed` | function_properties_generator.py |
| `FIXED_EQ` | 1 | `FIXED_EQ\|z=(az+b)/(cz+d)` | mobius_transform_generator.py |
| `FIXED_POINT` | 1 | `FIXED_POINT\|-4` | mobius_transform_generator.py |
| `FIXED_POINT_SETUP` | 3 | `FIXED_POINT_SETUP\|g(x)=4/5*x-7/3\|x0=0\|iterations=4` | fixed_point_generator.py |
| `FIXED_POINT_UPDATE` | 3 | `FIXED_POINT_UPDATE\|1\|x_0=0\|x_1=-7/3` | fixed_point_generator.py |
| `FLAG` | 2 | `FLAG\|4\|54 ÷ 9 = 6, not 8` | error_spotting_generator.py |
| `FLOOR_DIV` | 3 | `FLOOR_DIV\|7\|2\|3` | algorithm_trace_generator.py |
| `FLOPS_SETUP` | 2 | `FLOPS_SETUP\|rule=2mnk\|m=32,d=512,h=2048,o=128` | flops_memory_generator.py |
| `FLUX_SUM` | 2 | `FLUX_SUM\|(-2 + 2 + 5)*32\|160` | vector_theorem_generator.py |
| `FOCUS` | 1 | `FOCUS\|(6, -11)` | ellipse_features_generator.py, hyperbola_features_generator.py, parabola_features_generator.py |
| `FOIL_F` | 2 | `FOIL_F\|First: 8 * (-2)\|-16` | complex_division_generator.py, complex_number_ops_generator.py, multiplying_binomials_generator.py |
| `FOIL_I` | 2 | `FOIL_I\|Inner: (-3i) * (-2)\|6i` | complex_division_generator.py, complex_number_ops_generator.py, multiplying_binomials_generator.py |
| `FOIL_L` | 2 | `FOIL_L\|Last: (-3i) * 8i\|-24i^2` | complex_division_generator.py, complex_number_ops_generator.py, multiplying_binomials_generator.py |
| `FOIL_O` | 2 | `FOIL_O\|Outer: 8 * 8i\|64i` | complex_division_generator.py, complex_number_ops_generator.py, multiplying_binomials_generator.py |
| `FOIL_SETUP` | 1 | `FOIL_SETUP\|(1 + √2)(5 + √2)` | complex_division_generator.py, complex_number_ops_generator.py, multiplying_binomials_generator.py, radical_multiply_generator.py, trig_identity_verify_generator.py |
| `FOLD` | 2 | `FOLD\|h(1)\|16` | recursive_definition_unfold_generator.py |
| `FORCE_COMPONENT` | 1 | `FORCE_COMPONENT\|parallel=m*g*sin` | newtons_laws_generator.py |
| `FORCE_EQ` | 1 | `FORCE_EQ\|T-m1*g=m1*a` | newtons_laws_generator.py |
| `FORM` | 2 | `FORM\|converse\|If n is divisible by 2, then n is divisible by 24.` | conditional_forms_generator.py |
| `FORMULA` | 1, 2 | `FORMULA\|sinh x = (e^x - e^(-x))/2` | collision_generator.py, gaussian_curvature_generator.py, hyperbolic_distance_generator.py, hyperbolic_function_generator.py, or_formula_generator.py, projectile_motion_generator.py, stereographic_generator.py, uncertainty_generator.py |
| `FORM_IDENTIFY` | 2 | `FORM_IDENTIFY\|difference_of_squares\|a^2 - b^2 = (a - b)(a + b)` | completing_square_generator.py, conic_standard_form_generator.py, ellipse_features_generator.py, factor_special_forms_generator.py, hyperbola_features_generator.py, parabola_features_generator.py, radical_multiply_generator.py, radical_rationalize_generator.py, rational_equation_generator.py, rational_exponent_generator.py, rational_expr_add_sub_generator.py, rational_expr_mult_div_generator.py |
| `FOURIER_COEF` | 1 | `FOURIER_COEF\|b_11=(16/11)/pi` | fourier_series_generator.py |
| `FOURIER_SETUP` | 3 | `FOURIER_SETUP\|square\|A=4\|n=11` | fourier_series_generator.py |
| `FOUR_VECTOR_SETUP` | 3 | `FOUR_VECTOR_SETUP\|mass_shell\|c=1\|p=12, m=35` | four_vector_generator.py |
| `FRACTAL_SETUP` | 4 | `FRACTAL_SETUP\|julia\|z0=(-1,-3/2)\|c=(1/2,-1/2)\|N=5` | fractal_iteration_generator.py |
| `FRAC_BUILD` | 2 | `FRAC_BUILD\|144/360\|0.4` | conditional_probability_generator.py, geometric_probability_generator.py |
| `FRAC_REDUCE` | 2 | `FRAC_REDUCE\|5/-7\|-5/7` | angle_measure_generator.py, arc_length_generator.py, arc_sector_generator.py, complex_division_generator.py, frequency_table_generator.py, function_operations_generator.py, hyperbola_features_generator.py, implicit_diff_generator.py, improper_integral_generator.py, probability_addition_rule_generator.py, related_rates_generator.py, right_triangle_trig_generator.py |
| `FRAC_TO_DEC` | 2 | `FRAC_TO_DEC\|43/40\|1.075` | fraction_decimal_percent_converter.py |
| `FREQ_SETUP` | 2 | `FREQ_SETUP\|histogram — 50-59: 14, 60-69: 5, 70-79: 2, 80-89: 15\|cumulative count up to 60-69` | frequency_table_generator.py |
| `FUNC_OP` | 2 | `FUNC_OP\|(g · h)(6)\|g(6) · h(6)` | function_composition_generator.py, function_operations_generator.py |
| `FUNC_SETUP` | 2 | `FUNC_SETUP\|f(t) = -2t + 4\|f(1)` | domain_range_generator.py, function_composition_generator.py, function_evaluation_generator.py, function_operations_generator.py, function_table_generator.py, inverse_function_generator.py, piecewise_evaluation_generator.py, rational_function_features_generator.py |
| `FUNDAMENTAL_FORM_SETUP` | 3 | `FUNDAMENTAL_FORM_SETUP\|cylinder\|R=12\|u in [0,2pi/3], v in [0,3]` | fundamental_form_generator.py |
| `GAME_SETUP` | 2 | `GAME_SETUP\|payoffs=(19,12;1,15)\|row player maximizes, column player minimizes` | game_theory_generator.py |
| `GAMMA_SETUP` | 3 | `GAMMA_SETUP\|trace\|gamma1,gamma0\|Tr(product)` | gamma_matrix_generator.py |
| `GAS_FORMULA` | 1 | `GAS_FORMULA\|P1*V1/T1=P2*V2/T2` | gas_law_generator.py, gas_stoichiometry_generator.py |
| `GAS_SETUP` | 3 | `GAS_SETUP\|combined_pressure\|P1=12, V1=18, T1=4\|V2=6, T2=29` | gas_law_generator.py |
| `GAS_STOICH_SETUP` | 3 | `GAS_STOICH_SETUP\|mass_to_gas_pressure\|CaCO3 -> CaO + CO2\|given=600 g CaCO3, gas=CO2` | gas_stoichiometry_generator.py |
| `GATE_MATRIX` | 2 | `GATE_MATRIX\|Y\|[[0,-i],[i,0]]` | quantum_gate_generator.py |
| `GAUSSIAN_CURVATURE_SETUP` | 2, 3 | `GAUSSIAN_CURVATURE_SETUP\|sphere\|R=48` | gaussian_curvature_generator.py |
| `GAUSS_BONNET_SETUP` | 3 | `GAUSS_BONNET_SETUP\|flat_torus\|width=13, height=38\|chi=0` | gauss_bonnet_generator.py |
| `GAUSS_FORMULA` | 1 | `GAUSS_FORMULA\|2*E*A=sigma*A` | gauss_law_generator.py |
| `GAUSS_SETUP` | 3 | `GAUSS_SETUP\|sheet_charge\|sigma=35\|A=13` | gauss_law_generator.py |
| `GCD` | 2 | `GCD\|gcd(9,24)\|3` | derangement_generator.py, pollard_factorization_generator.py |
| `GCD_RESULT` | 1, 2 | `GCD_RESULT\|1` | lcm_generator.py, modular_inverse_generator.py, permutation_group_generator.py, rsa_generator.py, totient_generator.py |
| `GCD_START` | 2 | `GCD_START\|45\|118` | gcf_generator.py, lcm_generator.py |
| `GCD_STEP` | 3 | `GCD_STEP\|45\|118\|45` | gcf_generator.py, lcm_generator.py |
| `GCF_COEFF` | 2 | `GCF_COEFF\|6, 24, 24\|6` | factor_gcf_generator.py, quadratic_factoring_generator.py, rational_expr_simplify_generator.py |
| `GCF_RESULT` | 1 | `GCF_RESULT\|6x^2` | factor_gcf_generator.py, quadratic_factoring_generator.py, rational_expr_simplify_generator.py |
| `GCF_VAR` | 2 | `GCF_VAR\|x^5, x^4, x^2\|x^2` | factor_gcf_generator.py, quadratic_factoring_generator.py, rational_expr_simplify_generator.py |
| `GD_SETUP` | 3 | `GD_SETUP\|f(x,y)=1/2*(3x^2+1y^2)\|start=(10,-3)\|eta=1/8` | gradient_descent_generator.py |
| `GD_UPDATE` | 3 | `GD_UPDATE\|w_old=(-2,-2)\|eta=1/5\|w_new=(2/3,28/15)` | gradient_step_generator.py |
| `GELLMANN_IDENTITY` | 3 | `GELLMANN_IDENTITY\|Tr(lambda_6 lambda_3)\|2 delta_ab\|0` | pauli_algebra_generator.py |
| `GELLMANN_SETUP` | 3 | `GELLMANN_SETUP\|trace\|A=2lambda_6\|B=-4lambda_3` | pauli_algebra_generator.py |
| `GENERAL` | 2 | `GENERAL\|a_n\|C1(-2)^n + C2(-3)^n` | recurrence_generator.py |
| `GEOMETRIC_FORMULA` | 2 | `GEOMETRIC_FORMULA\|c_n = A*(-1)^n/d^(n+1)\|A=-4, d=4` | laurent_series_generator.py |
| `GEOM_FORMULA` | 1 | `GEOM_FORMULA\|E[X] = 1/p` | geometric_distribution_generator.py |
| `GEOM_SETUP` | 2 | `GEOM_SETUP\|p = 2/5\|E[X]` | geometric_distribution_generator.py |
| `GEO_PROB_FORMULA` | 1 | `GEO_PROB_FORMULA\|probability = sector angle / 360` | geometric_probability_generator.py |
| `GEO_PROB_SETUP` | 2 | `GEO_PROB_SETUP\|full circle\|sector angle 144°` | geometric_probability_generator.py |
| `GEO_SETUP` | 2 | `GEO_SETUP\|right triangle, altitude to hypotenuse; segments p = 5 (adjacent to the leg) and q = 71\|the leg adjacent to p` | geometric_mean_generator.py |
| `GF2_XOR` | 3 | `GF2_XOR\|quotient x^3\|0 xor 1\|1` | finite_field_generator.py |
| `GF_DIV_CHECK` | 3 | `GF_DIV_CHECK\|13 / 4\|not integer\|reject` | generating_function_generator.py |
| `GF_EXPAND` | 2 | `GF_EXPAND\|1/(1 - x^3)\|sum x^(3i), i >= 0` | generating_function_generator.py |
| `GF_SETUP` | 2 | `GF_SETUP\|[x^13]\|1/((1 - x^3)(1 - x^4))` | generating_function_generator.py |
| `GIANT_FACTOR` | 2 | `GIANT_FACTOR\|g^-m mod p\|2` | baby_step_giant_step_generator.py |
| `GIANT_STEP` | 2 | `GIANT_STEP\|i=0\|25` | baby_step_giant_step_generator.py |
| `GLB` | 1 | `GLB\|2` | partial_order_generator.py |
| `GOAL` | 1 | `GOAL\|show wk is even` | direct_proof_algebra_generator.py, point_slope_generator.py, standard_form_conversion_generator.py |
| `GRAD` | 2 | `GRAD\|1\|1/3` | softmax_gradient_generator.py |
| `GRADIENT_FORMULA` | 1 | `GRADIENT_FORMULA\|grad=(3x,1y)` | gradient_descent_generator.py, matrix_calculus_generator.py |
| `GRAD_ENTRY` | 2 | `GRAD_ENTRY\|g1\|-8` | matrix_calculus_generator.py |
| `GRAD_RESULT` | 2 | `GRAD_RESULT\|grad g\|(1, 1)` | lagrange_multiplier_generator.py |
| `GRAD_SETUP` | 3 | `GRAD_SETUP\|f(x,y) = 5*x^2 + y^2 + x*y + 4*x - y\|point (2, 3)\|gradient` | gradient_generator.py |
| `GRAPH_CHANGE` | 3 | `GRAPH_CHANGE\|9am\|10am\|4` | graph_interpret_generator.py |
| `GRAPH_DATA` | 2 | `GRAPH_DATA\|bar_chart\|Art:10,Music:42,Science:30,Math:23` | graph_interpret_generator.py |
| `GRAPH_MAX` | 2 | `GRAPH_MAX\|Music\|42` | graph_interpret_generator.py |
| `GRAPH_MAX_CHANGE` | 3 | `GRAPH_MAX_CHANGE\|10am\|11am\|7` | graph_interpret_generator.py |
| `GRAPH_MIN` | 2 | `GRAPH_MIN\|Soccer\|11` | graph_interpret_generator.py |
| `GRAPH_READ` | 2 | `GRAPH_READ\|Art\|10` | graph_interpret_generator.py |
| `GRAPH_SETUP` | 2 | `GRAPH_SETUP\|vertices A, B, C, D, E\|edges AC, BC, CD, DE` | dijkstra_generator.py, euler_circuit_generator.py, graph_counting_generator.py, graph_traversal_generator.py |
| `GRASSMANN_RESULT` | 3 | `GRASSMANN_RESULT\|constant=24\|theta=34\|24 + 34theta` | grassmann_generator.py |
| `GRASSMANN_SETUP` | 3 | `GRASSMANN_SETUP\|multiply_integrate\|x=6 + theta\|y=4 + 5theta` | grassmann_generator.py |
| `GREATEST` | 1 | `GREATEST\|none` | partial_order_generator.py |
| `GREAT_CIRCLE_SETUP` | 3 | `GREAT_CIRCLE_SETUP\|R=4\|A=(0,0)\|B=(0,60)` | great_circle_generator.py |
| `GROUP` | 2 | `GROUP\|(3y^2 - 12y)\|(-5y + 20)` | factor_grouping_generator.py, factor_trinomial_generator.py |
| `GROUP_MULT` | 3 | `GROUP_MULT\|e\|e\|e` | coset_generator.py |
| `GROUP_SETUP` | 2, 3 | `GROUP_SETUP\|Z_11\|addition mod n` | cayley_table_generator.py, coset_generator.py, cyclic_group_generator.py |
| `GS_SETUP` | 2 | `GS_SETUP\|vectors [[2, 0, 2], [-4, 0, -8], [0, 2, -8]]\|orthogonal basis, not normalized` | gram_schmidt_generator.py |
| `GS_SUBTRACT` | 2 | `GS_SUBTRACT\|remove projection on u1\|[2, 0, -2]` | gram_schmidt_generator.py, qr_decomposition_generator.py |
| `GS_VECTOR` | 2 | `GS_VECTOR\|u1 = v1\|[2, 0, 2]` | gram_schmidt_generator.py |
| `HA` | 1 | `HA\|y = 1` | rational_function_features_generator.py |
| `HAMILTON` | 2 | `HAMILTON\|i*i\|-1` | quaternion_generator.py |
| `HAMILTONIAN` | 1 | `HAMILTONIAN\|H=p_x^2/(2m)+1/2*k*x^2` | hamiltonian_generator.py |
| `HAMMING_PLACE` | 2 | `HAMMING_PLACE\|positions 1,2,3,4,5,6,7\|p1,p2,d1,p4,d2,d3,d4` | hamming_code_generator.py |
| `HAMMING_RECEIVED` | 1 | `HAMMING_RECEIVED\|r=0101110` | hamming_code_generator.py |
| `HAMMING_SETUP` | 2 | `HAMMING_SETUP\|data=1000\|even parity` | hamming_code_generator.py |
| `HAM_EQ` | 2 | `HAM_EQ\|xdot=dH/dp_x\|xdot=p_x/4` | hamiltonian_generator.py |
| `HAM_SETUP` | 3 | `HAM_SETUP\|mass_spring\|m=4, k=51\|q=x, p=p_x` | hamiltonian_generator.py |
| `HARMONIC_SETUP` | 1 | `HARMONIC_SETUP\|u=4x^2 - 4y^2 + 3x - 2y` | cauchy_riemann_generator.py |
| `HAWKING_SETUP` | 3 | `HAWKING_SETUP\|temperature\|T_H=hbar*c^3/(8π*G*M*k_B)\|hbar=9,c=3,G=3,M=7,k_B=6` | hawking_generator.py |
| `HESSIAN_DET` | 3 | `HESSIAN_DET\|D = f_xx*f_yy - f_xy^2\|8*4 - 3^2\|23` | hessian_classify_generator.py |
| `HESSIAN_SETUP` | 2 | `HESSIAN_SETUP\|f(x,y) = 4*x^2 + 2*y^2 + 3*x*y - 44*x - 28*y\|find and classify the critical point` | hessian_classify_generator.py |
| `HESSIAN_TEST` | 3 | `HESSIAN_TEST\|D = 23\|f_xx = 8\|local minimum` | hessian_classify_generator.py |
| `HIDDEN_PRE` | 2 | `HIDDEN_PRE\|h1\|z=2` | backprop_generator.py |
| `HIT_EQ` | 2 | `HIT_EQ\|t0=1+p00*t0+p01*t1\|t1=1+p10*t0+p11*t1` | markov_chain_generator.py |
| `HMM_SETUP` | 2 | `HMM_SETUP\|states H,L\|observations BAA` | viterbi_generator.py |
| `HMM_START` | 1 | `HMM_START\|H=1/2, L=1/2` | viterbi_generator.py |
| `HOLE` | 1 | `HOLE\|x = 3` | rational_function_features_generator.py |
| `HOM_SOL` | 2 | `HOM_SOL\|y_h\|y_h = C1e^(-3x) + C2e^(-x)` | undetermined_coeff_generator.py, variation_parameters_generator.py |
| `HOOK` | 4 | `HOOK\|(1,1)\|right=3\|below=2\|hook=6` | young_tableaux_generator.py |
| `HORNER_SETUP` | 2 | `HORNER_SETUP\|3x^4 + x^3 + 2x^2 - x - 1\|x = 4` | horner_evaluation_generator.py |
| `HT_SETUP` | 2 | `HT_SETUP\|H0: p = 0.5; Ha: p ≠ 0.5\|n = 25, 15 successes, critical value = 1.96` | hypothesis_test_generator.py, two_sample_test_generator.py |
| `HUFFMAN_FORMULA` | 1 | `HUFFMAN_FORMULA\|L=sum p_i*l_i` | huffman_coding_generator.py |
| `HUFFMAN_MERGE` | 2 | `HUFFMAN_MERGE\|A:1/16 + D:1/16\|AD:1/8` | huffman_coding_generator.py |
| `HUFFMAN_SETUP` | 1 | `HUFFMAN_SETUP\|A=1/16, B=1/4, C=1/4, D=1/16, E=1/8, F=1/8, G=1/8` | huffman_coding_generator.py |
| `HYDROGEN_FORMULA` | 1 | `HYDROGEN_FORMULA\|E_ion=R_E/n^2` | hydrogen_atom_generator.py |
| `HYDROGEN_SETUP` | 3 | `HYDROGEN_SETUP\|ionization_energy\|n=11\|R_E=31 eV` | hydrogen_atom_generator.py |
| `HYPERBOLIC_DISTANCE_SETUP` | 3 | `HYPERBOLIC_DISTANCE_SETUP\|half-plane\|P=(4,14)\|Q=(4,19)` | hyperbolic_distance_generator.py |
| `HYPERBOLIC_SETUP` | 2 | `HYPERBOLIC_SETUP\|e^x=26/19\|e^(-x)=19/26` | hyperbolic_function_generator.py |
| `HYPERCUBE_FORMULA` | 1 | `HYPERCUBE_FORMULA\|k-faces of the n-cube: C(n,k) · 2^(n-k)` | hypercube_counting_generator.py |
| `HYPERCUBE_SETUP` | 2 | `HYPERCUBE_SETUP\|6-cube\|number of vertices (k = 0)` | hypercube_counting_generator.py |
| `I` | 2 | `I\|7/2\|2/7` | fraction_op_generator.py, mixed_number_operation_generator.py, rational_expr_mult_div_generator.py |
| `ICE_ROW` | 2 | `ICE_ROW\|initial\|[A]=9, [B]=0` | equilibrium_ice_generator.py |
| `IDENTIFY` | 2 | `IDENTIFY\|order matters\|use P(n, r)` | permutation_combination_generator.py |
| `IDENTITY` | 2 | `IDENTITY\|hockey-stick\|Σ i=14..80 C(i,14) = C(81,15)` | counting_classics_generator.py, function_inner_product_generator.py, index_gymnastics_generator.py |
| `IDENTITY_SETUP` | 2 | `IDENTITY_SETUP\|verify: 2/sin^2 x = 1/(1 - cos x) + 1/(1 + cos x)\|transform the right side` | trig_identity_verify_generator.py |
| `IDENT_MATCH` | 1 | `IDENT_MATCH\|2/sin^2 x = 2/sin^2 x` | trig_identity_verify_generator.py |
| `IDENT_SUB` | 1, 2 | `IDENT_SUB\|1 - cos^2 x = sin^2 x` | parametric_calculus_generator.py, trig_identity_verify_generator.py |
| `IE_FORMULA` | 2 | `IE_FORMULA\|n(A union B union C)\|n(A)+n(B)+n(C) - n(AB)-n(AC)-n(BC) + n(ABC)` | inclusion_exclusion_generator.py |
| `IE_SETUP` | 2 | `IE_SETUP\|n(A)=28, n(B)=23, n(C)=35\|n(AB)=13, n(AC)=7, n(BC)=10, n(ABC)=3` | inclusion_exclusion_generator.py |
| `IFACTOR` | 2 | `IFACTOR\|mu = e^(∫ 3 dx)\|e^(3x)` | integrating_factor_generator.py, ode_substitution_generator.py |
| `IG_SETUP` | 3 | `IG_SETUP\|parent pos=7, neg=9\|total=16\|splits=shape,texture` | information_gain_generator.py |
| `IMAGE` | 2 | `IMAGE\|e\|26` | function_properties_generator.py, mobius_transform_generator.py |
| `IMPLICIT_DIFF` | 2 | `IMPLICIT_DIFF\|d/dx of xy\|y + x·y' (product rule)` | implicit_diff_generator.py, log_diff_higher_order_generator.py, related_rates_generator.py |
| `IMPLICIT_SETUP` | 2 | `IMPLICIT_SETUP\|xy = 8\|dy/dx` | implicit_diff_generator.py |
| `IMPROPER_TO_MIX` | 2 | `IMPROPER_TO_MIX\|477/55\|8 37/55` | composite_arithmetic_generator.py, mixed_number_operation_generator.py, order_of_operations_generator.py |
| `INDEGREE` | 2 | `INDEGREE\|A\|0` | graph_traversal_generator.py |
| `INDEGREE_UPDATE` | 2 | `INDEGREE_UPDATE\|B\|0` | graph_traversal_generator.py |
| `INDEP_CHECK` | 3 | `INDEP_CHECK\|P11=264/1369\|product=121/1369\|no` | joint_distribution_generator.py |
| `INDEP_FORMULA` | 1 | `INDEP_FORMULA\|independent iff P11=P(X=1)P(Y=1)` | joint_distribution_generator.py |
| `INDEX` | 3 | `INDEX\|G size 8\|H size 4\|2` | coset_generator.py |
| `INDEX_METRIC` | 3 | `INDEX_METRIC\|raise\|Minkowski\|g^ii=[-1,1,1,1]` | index_raising_generator.py |
| `INDEX_SETUP` | 3 | `INDEX_SETUP\|c=-1\|j=3, k=2\|l=1, m=2` | index_gymnastics_generator.py |
| `INDUCT_ASSUME` | 1 | `INDUCT_ASSUME\|1+...+k = k(k+1)/2` | induction_verify_generator.py |
| `INDUCT_BASE` | 2 | `INDUCT_BASE\|n=1\|1 = 1(2)/2` | induction_verify_generator.py |
| `INDUCT_STEP` | 1, 2 | `INDUCT_STEP\|add k+1\|k(k+1)/2 + (k+1)` | induction_verify_generator.py |
| `INEQ_FLIP` | 1 | `INEQ_FLIP\|Dividing by negative number reverses inequality` | domain_range_generator.py, linear_fractional_generator.py, one_step_inequality_generator.py, two_step_inequality_generator.py |
| `INEQ_OP_ALL` | 3 | `INEQ_OP_ALL\|subtract\|1\|-7 < 2x < 5` | absolute_value_inequality_generator.py, compound_inequality_generator.py |
| `INEQ_OP_BOTH` | 4 | `INEQ_OP_BOTH\|multiply\|3\|x\|-21` | domain_range_generator.py, linear_fractional_generator.py, one_step_inequality_generator.py, two_step_inequality_generator.py |
| `INEQ_RESULT` | 3 | `INEQ_RESULT\|x\|≤\|-21` | domain_range_generator.py, linear_fractional_generator.py, one_step_inequality_generator.py, two_step_inequality_generator.py |
| `INEQ_SETUP` | 1 | `INEQ_SETUP\|x/3 ≤ -7` | linear_fractional_generator.py, one_step_inequality_generator.py, polynomial_inequality_generator.py, two_step_inequality_generator.py |
| `INEQ_SIMPLIFY` | 1 | `INEQ_SIMPLIFY\|x + 5 ≥ 13` | domain_range_generator.py, linear_fractional_generator.py, two_step_inequality_generator.py |
| `INEX_TERM` | 3 | `INEX_TERM\|0\|1×2^3\|8` | function_properties_generator.py |
| `INFO_GAIN` | 2 | `INFO_GAIN\|shape\|0.011625` | information_gain_generator.py |
| `INFO_SETUP` | 2 | `INFO_SETUP\|p=1/32768\|I=-log2(p)` | entropy_generator.py |
| `INFO_TABLE` | 1 | `INFO_TABLE\|1/4=2, 3/8=1.415, 7/16=1.193, 1/2=1, 9/16=0.83, 5/8=0.678, 3/4=0.415` | information_gain_generator.py |
| `INFO_VALUE` | 2 | `INFO_VALUE\|p=7/16\|I=1.193` | information_gain_generator.py |
| `INITIAL` | 2 | `INITIAL\|D_0 = 1\|D_1 = 0` | derangement_generator.py |
| `INITIAL_COEFF` | 2 | `INITIAL_COEFF\|a_0\|23880` | series_solution_generator.py |
| `INITIAL_EQ` | 2 | `INITIAL_EQ\|C1 + C2\|-2` | recurrence_generator.py |
| `INITIAL_SYSTEM` | 2 | `INITIAL_SYSTEM\|C1[2, 1] + C2[1, 0]\|[-10, -3]` | ode_system_generator.py |
| `INNER_ANTIDERIV` | 2 | `INNER_ANTIDERIV\|dy\|2*x*y + 2*y^2 + y` | double_integral_generator.py, triple_integral_generator.py |
| `INNER_EVAL` | 2, 3 | `INNER_EVAL\|y=0..4\|8*x + 36` | double_integral_generator.py, triple_integral_generator.py |
| `INNER_PRODUCT` | 2 | `INNER_PRODUCT\|inner(phi,psi)\|-4-i` | braket_generator.py |
| `INNER_PRODUCT_SETUP` | 3 | `INNER_PRODUCT_SETUP\|interval=[0,2pi]\|f=sin(11x)\|g=cos(13x)` | function_inner_product_generator.py |
| `INSERT_KEY` | 3 | `INSERT_KEY\|pass 1\|7\|index 1` | algorithm_trace_generator.py |
| `INSERT_PLACE` | 2 | `INSERT_PLACE\|index 1\|3, 7, 10, 35, 11, 23, 39` | algorithm_trace_generator.py |
| `INTEGRAL` | 1, 2 | `INTEGRAL\|integral sin(24x) on [0,2pi]\|0` | fourier_series_generator.py, function_inner_product_generator.py, legendre_construction_generator.py |
| `INTEGRAL_SETUP` | 1 | `INTEGRAL_SETUP\|L = integral from r0 to r1 of 1 dr` | metric_arc_length_generator.py |
| `INTEGRATE` | 2 | `INTEGRATE\|v_y = u_x\|v=8xy + 2x + 3y + phi(x)` | cauchy_riemann_generator.py |
| `INTEGRATION_BY_PARTS` | 2 | `INTEGRATION_BY_PARTS\|u=x\|dv=sin(nx)dx` | fourier_series_generator.py |
| `INTEG_RULE` | 2 | `INTEG_RULE\|power rule\|∫ x^n dx = x^(n+1)/(n+1) + C` | antiderivative_generator.py, definite_integral_generator.py, ode_substitution_generator.py, partial_fractions_generator.py, separable_ode_generator.py, solid_revolution_generator.py, u_substitution_generator.py |
| `INTEG_SETUP` | 2 | `INTEG_SETUP\|∫ (-2x - 2) dx\|antiderivative` | antiderivative_generator.py, arc_length_generator.py, definite_integral_generator.py, improper_integral_generator.py, integration_by_parts_generator.py, parametric_calculus_generator.py, partial_fractions_generator.py, u_substitution_generator.py |
| `INTERCEPT_FORMULA` | 1 | `INTERCEPT_FORMULA\|a = ȳ - b·x̄` | regression_generator.py |
| `INTERFERENCE_FORMULA` | 1 | `INTERFERENCE_FORMULA\|y=m*lambda*L/d` | interference_generator.py |
| `INTERFERENCE_SETUP` | 3 | `INTERFERENCE_SETUP\|double_slit\|m=3, lambda=9\|L=11, d=24` | interference_generator.py |
| `INTERP_SETUP` | 3 | `INTERP_SETUP\|lagrange\|points=(-5,47), (4,11), (5,17)\|x=-2` | interpolation_generator.py |
| `INTERVAL_CLASS` | 2 | `INTERVAL_CLASS\|s2=-440\|spacelike` | minkowski_interval_generator.py |
| `INT_ABS` | 2 | `INT_ABS\|-7\|7` | integer_operations_generator.py |
| `INT_ALIGN` | 2 | `INT_ALIGN\|82320\|65750` | multi_digit_addition_generator.py, multi_digit_subtraction_generator.py |
| `INT_APPLY_SIGN` | 3 | `INT_APPLY_SIGN\|6\|negative\|-6` | integer_operations_generator.py |
| `INT_OP` | 4 | `INT_OP\|-\|7\|1\|6` | integer_operations_generator.py |
| `INT_REWRITE` | 2 | `INT_REWRITE\|-7 - (-1)\|-7 + 1` | integer_operations_generator.py |
| `INT_SIGN_RULE` | 2 | `INT_SIGN_RULE\|subtract_rule\|Subtracting is adding the opposite` | integer_operations_generator.py |
| `INVERSE_LAPLACE` | 2 | `INVERSE_LAPLACE\|1/(s + 1)\|e^(-t)` | laplace_ivp_generator.py |
| `INVERSE_MAP` | 2 | `INVERSE_MAP\|x=(u+v)/2\|y=(u-v)/2` | rv_transform_generator.py |
| `INVERSE_METRIC` | 2 | `INVERSE_METRIC\|g^rr=1\|g^thetatheta=1/r^2` | christoffel_generator.py, riemann_tensor_generator.py |
| `INVERSE_PAIR` | 2 | `INVERSE_PAIR\|(e, 3)\|(3, e)` | function_properties_generator.py, relation_operations_generator.py |
| `INV_FORMULA` | 1 | `INV_FORMULA\|A⁻¹ = (1/det)·[[d, -b], [-c, a]]` | matrix_inverse_generator.py |
| `IRR_SETUP` | 2 | `IRR_SETUP\|c0=-2600,c1=3900\|r0=1/10,iterations=2` | npv_irr_generator.py |
| `IRR_VALUE` | 2 | `IRR_VALUE\|f1\|10400/11` | npv_irr_generator.py |
| `ITERATE` | 2 | `ITERATE\|n=1\|z=(-3/4,5/2)` | fractal_iteration_generator.py, gradient_descent_generator.py |
| `IVT_SETUP` | 2 | `IVT_SETUP\|f(x) = x^3 - x + 1 on [1, 3]\|does the IVT guarantee a root?` | mean_value_theorem_generator.py |
| `I_CYCLE` | 2 | `I_CYCLE\|i^2\|-1` | complex_number_ops_generator.py |
| `I_SQUARE` | 2 | `I_SQUARE\|-24i^2\|24` | complex_division_generator.py, complex_log_generator.py, complex_number_ops_generator.py |
| `JACOBIAN` | 2 | `JACOBIAN\|dA\|r dr dtheta` | double_integral_generator.py |
| `JACOBI_END` | 2 | `JACOBI_END\|a=1\|sign -1` | jacobi_symbol_generator.py |
| `JACOBI_RECIPROCITY` | 3 | `JACOBI_RECIPROCITY\|a mod 4 = 3\|n mod 4 = 3\|flip sign` | jacobi_symbol_generator.py |
| `JACOBI_SETUP` | 3 | `JACOBI_SETUP\|a=12\|n=91\|n odd` | jacobi_symbol_generator.py |
| `JACOBI_SWAP` | 3 | `JACOBI_SWAP\|a=91\|n=3\|sign -1` | jacobi_symbol_generator.py |
| `JACOBI_TWO_RULE` | 3 | `JACOBI_TWO_RULE\|n mod 8 = 3\|flip sign\|sign -1` | jacobi_symbol_generator.py |
| `JAC_DET` | 3 | `JAC_DET\|x_u*y_v - x_v*y_u\|(-2)*(-1) - (-1)*0\|2` | jacobian_generator.py |
| `JAC_MATRIX` | 2 | `JAC_MATRIX\|[[x_u, x_v], [y_u, y_v]]\|[[-2, -1], [0, -1]]` | jacobian_generator.py, rv_transform_generator.py |
| `JAC_SETUP` | 3 | `JAC_SETUP\|x = -2*u - v\|y = -v\|d(x,y)/d(u,v)` | jacobian_generator.py |
| `JOINT_SETUP` | 3 | `JOINT_SETUP\|X,Y in {0,1}\|p00=819/1369, p01=143/1369\|p10=143/1369, p11=264/1369` | joint_distribution_generator.py |
| `KERNEL_BASE` | 3 | `KERNEL_BASE\|A,A\|dot+c=10+2\|12` | feature_map_generator.py, kernel_evaluation_generator.py |
| `KERNEL_EXPONENT` | 2 | `KERNEL_EXPONENT\|A,A\|0` | kernel_evaluation_generator.py |
| `KERNEL_SETUP` | 3 | `KERNEL_SETUP\|type=rbf\|points=A=(-1,0), B=(-3,0), C=(-1,2)\|gamma=2` | kernel_evaluation_generator.py |
| `KERNEL_VALIDITY` | 1 | `KERNEL_VALIDITY\|psd=true` | kernel_validity_generator.py |
| `KERNEL_VALUE` | 2 | `KERNEL_VALUE\|A,A\|1` | feature_map_generator.py, kernel_evaluation_generator.py, kernel_perceptron_generator.py, kernel_ridge_generator.py |
| `KIN_FORMULA` | 1 | `KIN_FORMULA\|t = d/v` | invariant_mass_generator.py, kinematics_generator.py |
| `KIN_SETUP` | 3, 4 | `KIN_SETUP\|d = 216 feet\|v = 24 ft/s\|time` | invariant_mass_generator.py, kinematics_generator.py |
| `KL_FORMULA` | 1 | `KL_FORMULA\|D=sum source_i*log2(source_i/target_i)` | kl_divergence_generator.py |
| `KL_SETUP` | 3 | `KL_SETUP\|P=[10/21,1/2,1/42]\|Q=[5/42,1/2,8/21]\|direction=Q to P` | kl_divergence_generator.py |
| `KMAP_GROUP` | 2 | `KMAP_GROUP\|1100, 1101, 1110, 1111\|U AND V` | boolean_algebra_generator.py |
| `KMAP_ROW` | 2 | `KMAP_ROW\|UV=00\|0, 1, 0, 0` | boolean_algebra_generator.py |
| `KMAP_SETUP` | 2 | `KMAP_SETUP\|rows UV=00,UV=01,UV=11,UV=10\|columns WX=00,WX=01,WX=11,WX=10` | boolean_algebra_generator.py |
| `KMAP_SIMPLIFY` | 1 | `KMAP_SIMPLIFY\|(U AND V) OR (U AND NOT X) OR (V AND NOT X) OR (NOT U AND NOT V AND NOT W AND X)` | boolean_algebra_generator.py |
| `KMEANS_SETUP` | 2 | `KMEANS_SETUP\|points=P1=(3,4), P2=(-1,-5), P3=(3,-3), P4=(-4,-1)\|centroids=C1=(-4,4), C2=(-3,-1)` | kmeans_step_generator.py |
| `KNN_DISTANCE` | 3 | `KNN_DISTANCE\|P1\|label=A\|d2=20` | knn_generator.py |
| `KNN_NEIGHBORS` | 1 | `KNN_NEIGHBORS\|P1:20:A,P2:34:B,P4:45:B` | knn_generator.py |
| `KNN_SETUP` | 3 | `KNN_SETUP\|q=(-3,1)\|k=3\|training=P1=(1,3,A), P2=(0,-4,B), P3=(4,3,A), P4=(3,4,B), P5=(5,0,A)` | knn_generator.py |
| `KNN_SORT` | 1 | `KNN_SORT\|P1:20:A,P2:34:B,P4:45:B,P3:53:A,P5:65:A` | knn_generator.py |
| `KP_EXAMPLE` | 3 | `KP_EXAMPLE\|1\|x=-7,y=-1\|alpha=(0,0,0)` | kernel_perceptron_generator.py |
| `KP_SETUP` | 3 | `KP_SETUP\|kernel=linear\|data=[(-7,-1), (7,-1), (3,1)]\|alpha0=(0,0,0)` | kernel_perceptron_generator.py |
| `KP_TERM` | 2 | `KP_TERM\|j=1\|0` | kernel_perceptron_generator.py |
| `KRAFT_CHECK` | 2, 3 | `KRAFT_CHECK\|sum=1\|complete` | huffman_coding_generator.py, kraft_inequality_generator.py |
| `KRAFT_CLASSIFY` | 2 | `KRAFT_CLASSIFY\|slack=0\|complete` | kraft_inequality_generator.py |
| `KRAFT_FORMULA` | 1 | `KRAFT_FORMULA\|sum 2^-l_i` | huffman_coding_generator.py, kraft_inequality_generator.py |
| `KRAFT_SETUP` | 2 | `KRAFT_SETUP\|A=3, B=2, C=3, D=2, E=3, F=5, G=4, H=5\|binary prefix code` | kraft_inequality_generator.py |
| `KRAFT_TERM` | 3 | `KRAFT_TERM\|A\|l=3\|1/8` | kraft_inequality_generator.py |
| `KRR_SETUP` | 3 | `KRR_SETUP\|kernel=linear\|data=[(3,-3), (-2,4)]\|lambda=2,x*=-4` | kernel_ridge_generator.py |
| `KV_CACHE` | 2 | `KV_CACHE\|values\|1048576` | flops_memory_generator.py |
| `K_EXPR` | 1, 2 | `K_EXPR\|K = [B]^2/[A]\|48 = (2x)^2/(9-x)` | equilibrium_ice_generator.py |
| `L` | 3 | `L\|3\|7\|21` | fraction_comparison_generator.py, fraction_op_generator.py, linear_fractional_generator.py, mixed_number_operation_generator.py, rational_expr_add_sub_generator.py |
| `LABEL_COUNT` | 2 | `LABEL_COUNT\|A\|1` | knn_generator.py |
| `LADDER_APPLY` | 2 | `LADDER_APPLY\|a ket29\|sqrt(29) ket28` | ladder_operator_generator.py |
| `LADDER_COMM` | 2 | `LADDER_COMM\|[a,adag] ketn\|ket27` | ladder_operator_generator.py |
| `LADDER_RULE` | 2 | `LADDER_RULE\|J_- = J1_- + J2_-\|lower from highest weights` | clebsch_gordan_generator.py, ladder_operator_generator.py |
| `LADDER_SETUP` | 3 | `LADDER_SETUP\|single_step_energy\|state=ket29\|hbar=10, omega=8` | ladder_operator_generator.py |
| `LAGRANGE_EQ` | 2 | `LAGRANGE_EQ\|f_x = lambda\|y^2` | lagrange_multiplier_generator.py |
| `LAGRANGE_FACTOR` | 3 | `LAGRANGE_FACTOR\|L_0\|j=1\|2/3` | interpolation_generator.py |
| `LAGRANGE_SETUP` | 3 | `LAGRANGE_SETUP\|f(x,y) = x*y^2\|constraint x + y = 15\|maximize` | lagrange_multiplier_generator.py |
| `LAGRANGIAN` | 1, 2 | `LAGRANGIAN\|L=T-V` | lagrangian_generator.py |
| `LAG_SETUP` | 3 | `LAG_SETUP\|pendulum\|m=11, L=9\|g=10, q=theta` | lagrangian_generator.py |
| `LAMBDA_SETUP` | 2 | `LAMBDA_SETUP\|((lambda d. (lambda c. c)) (lambda t. k))\|leftmost-outermost` | lambda_reduction_generator.py |
| `LAPLACE` | 2 | `LAPLACE\|L[y' + y]\|(sY + 3) + Y` | laplace_ivp_generator.py, transfer_function_generator.py |
| `LAPLACE_TABLE` | 1 | `LAPLACE_TABLE\|L{y'} = sY - y(0); L{e^(kt)} = 1/(s-k); L^-1{1/(s-k)} = e^(kt)` | laplace_ivp_generator.py |
| `LATTICE_PAIR` | 3 | `LATTICE_PAIR\|(4, 4)\|lub 4\|glb 4` | partial_order_generator.py |
| `LAURENT_SETUP` | 3 | `LAURENT_SETUP\|center a=1\|w=(z-1)\|f=(-5 + 5(z-1) - 4(z-1)^2 + 2(z-1)^3 + 4(z-1)^4 - 2(z-1)^5 + 3(z-1)^6)/(z-1)^3` | laurent_series_generator.py |
| `LAURENT_TERM` | 1 | `LAURENT_TERM\|1(z+4)^-1` | residue_generator.py |
| `LAW` | 3 | `LAW\|distributive ∨ over ∧\|q ∨ (¬u ∧ ¬p)\|(q ∨ ¬u) ∧ (q ∨ ¬p)` | logical_equivalence_laws_generator.py, set_algebra_laws_generator.py |
| `LAYERNORM_SETUP` | 3 | `LAYERNORM_SETUP\|x=(-12,4)\|gamma=(4,1)\|beta=(-2,3)` | layer_norm_generator.py |
| `LB` | 2 | `LB\|{2, 24}\|{2}` | partial_order_generator.py |
| `LCM_FROM_GCD` | 3 | `LCM_FROM_GCD\|90*53\|1\|4770` | lcm_generator.py |
| `LCM_STEP` | 3 | `LCM_STEP\|1\|2\|2` | permutation_group_generator.py, pollard_factorization_generator.py |
| `LEADING_MINOR` | 2 | `LEADING_MINOR\|Delta1\|4` | positive_definite_generator.py |
| `LEAST` | 1 | `LEAST\|none` | partial_order_generator.py |
| `LEGENDRE_RESULT` | 3 | `LEGENDRE_RESULT\|1\|1\|quadratic residue` | quadratic_residue_generator.py |
| `LEGENDRE_SETUP` | 2 | `LEGENDRE_SETUP\|a=41\|p=37` | legendre_construction_generator.py, quadratic_residue_generator.py |
| `LIE_EXP_FORM` | 2 | `LIE_EXP_FORM\|e^(theta J)\|cos(theta)I + sin(theta)J` | lie_exponential_generator.py |
| `LIE_EXP_SETUP` | 4 | `LIE_EXP_SETUP\|SO2\|theta=-330 deg\|J=[[0, -1], [1, 0]]\|goal=e^(theta J)` | lie_exponential_generator.py |
| `LIMITING_REAGENT` | 2 | `LIMITING_REAGENT\|H2\|NH3=26/3 mol` | stoichiometry_generator.py |
| `LIMIT_CHECK` | 2 | `LIMIT_CHECK\|NH3 from N2=58 mol\|NH3 from H2=26/3 mol` | stoichiometry_generator.py |
| `LIMIT_SETUP` | 1, 2 | `LIMIT_SETUP\|lim x→6 of (x^2 - 10x + 24)/(x - 6)\|0/0: factor and cancel` | derivative_limit_def_generator.py, improper_integral_generator.py, lhopital_generator.py, limit_evaluation_generator.py, power_series_generator.py, series_convergence_generator.py |
| `LINEAR_SYSTEM` | 2 | `LINEAR_SYSTEM\|a=9/14, b=-1/14\|c=-3/13, d=11/13` | markov_chain_generator.py |
| `LINE_EQ` | 1 | `LINE_EQ\|2x - 12y - 29 = 0` | complex_locus_generator.py |
| `LINE_INTEGRAL` | 3 | `LINE_INTEGRAL\|int_0^1 dot dt\|9/2 - 9\|-9/2` | line_integral_generator.py |
| `LINE_RELATION_SETUP` | 3 | `LINE_RELATION_SETUP\|parallel\|y = -3/2x\|(-1, -3)` | parallel_perpendicular_line_generator.py |
| `LINE_SETUP` | 2 | `LINE_SETUP\|F(x,y) = <4*x + 4*y - 1, 4*y + 4*x - 3>\|from (-3, 0) to (-1, 4)` | line_integral_generator.py |
| `LLL_DONE` | 1 | `LLL_DONE\|[(6,-2),(6,9)]` | lll_reduction_generator.py |
| `LLL_SETUP` | 1 | `LLL_SETUP\|[(-6,13),(0,11)]` | lll_reduction_generator.py |
| `LOCUS_SETUP` | 3 | `LOCUS_SETUP\|z=x+iy\|p=(2,1)\|q=(3,-5)` | complex_locus_generator.py |
| `LOG2` | 2 | `LOG2\|1/32\|-5` | entropy_generator.py, huffman_coding_generator.py, mutual_information_generator.py, von_neumann_entropy_generator.py |
| `LOG2_RATIO` | 3 | `LOG2_RATIO\|i=0\|ratio=1/4\|log=-2` | kl_divergence_generator.py |
| `LOG_BOTH_SIDES` | 1 | `LOG_BOTH_SIDES\|log_3(3^x) = log_3(59)` | exponential_equation_generator.py, log_diff_higher_order_generator.py, separable_ode_generator.py |
| `LOG_EVAL` | 2 | `LOG_EVAL\|19/14\|ln(19/14)` | hyperbolic_distance_generator.py |
| `LOG_EXACT` | 2 | `LOG_EXACT\|log_12(144)\|2` | master_theorem_generator.py |
| `LOG_FORM` | 1 | `LOG_FORM\|log_7(49) = y ⟺ 7^y = 49` | log_conversion_generator.py, log_equation_generator.py |
| `LOG_FORMULA` | 1 | `LOG_FORMULA\|log z = ln r + i(arg + 2pi*k)` | complex_log_generator.py |
| `LOG_IDENT` | 2 | `LOG_IDENT\|ln(1) = 0\|0` | exponential_equation_generator.py, log_conversion_generator.py |
| `LOG_LIKELIHOOD` | 1 | `LOG_LIKELIHOOD\|ell(mu)=-(1/(2*4))*sum((x_i-mu)^2)+C` | mle_generator.py |
| `LOG_ONE_TO_ONE` | 1 | `LOG_ONE_TO_ONE\|2x - 6 = x + 5` | log_equation_generator.py |
| `LOG_POWER` | 2 | `LOG_POWER\|log_10(x^2)\|2log_10(x)` | derivative_transcendental_generator.py, log_diff_higher_order_generator.py, log_properties_generator.py, ph_calculation_generator.py |
| `LOG_PRODUCT` | 1, 2 | `LOG_PRODUCT\|log_10(1000x^2y^3)\|log_10(1000x^2) + log_10(y^3)` | log_equation_generator.py, log_properties_generator.py, ph_calculation_generator.py |
| `LOG_QUOTIENT` | 2 | `LOG_QUOTIENT\|log_3(x^3y^3) - log_3(z)\|log_3(x^3y^3/z)` | log_properties_generator.py |
| `LOG_SETUP` | 1, 2 | `LOG_SETUP\|log_10(1000x^2y^3)\|expand` | complex_log_generator.py, log_properties_generator.py |
| `LOG_SOFTMAX` | 2 | `LOG_SOFTMAX\|1\|ln(1/3)` | softmax_gradient_generator.py |
| `LOG_SUPPLIED` | 2 | `LOG_SUPPLIED\|log10(1)\|0` | signal_arithmetic_generator.py |
| `LOG_TERM` | 3 | `LOG_TERM\|96\|ln(7)\|96*ln(7)` | entropy_change_generator.py |
| `LOOKUP_SUPPLIED` | 2 | `LOOKUP_SUPPLIED\|e^(-lambda*t)\|1/19` | named_distribution_generator.py |
| `LORA_COUNT` | 2 | `LORA_COUNT\|r*(d_in+d_out)\|100800` | param_count_generator.py |
| `LOWRANK_SETUP` | 2 | `LOWRANK_SETUP\|A=[[5,0], [0,9]]\|rank=1` | low_rank_approx_generator.py |
| `LP_CORNER_SETUP` | 3 | `LP_CORNER_SETUP\|max z=4x+14y\|0<=x<=11, 0<=y<=6\|x+y<=14` | lp_corner_generator.py |
| `LR_PHASE` | 1 | `LR_PHASE\|decay` | lr_schedule_generator.py |
| `LR_SETUP` | 3 | `LR_SETUP\|base=3/100\|min=0\|warmup=10,total=210,t=110` | lr_schedule_generator.py |
| `LR_VALUE` | 1 | `LR_VALUE\|3/200` | lr_schedule_generator.py |
| `LS_LINE` | 2 | `LS_LINE\|a = 7, b = 1\|ŷ = 7 + x` | least_squares_generator.py |
| `LS_SETUP` | 2 | `LS_SETUP\|points [(-3, 1), (-1, 9), (1, 11), (3, 7)]\|model y = a + bx` | least_squares_generator.py |
| `LUB` | 1 | `LUB\|24` | partial_order_generator.py |
| `LUHN_DIGIT` | 3 | `LUHN_DIGIT\|digit 2\|keep\|2 -> 2` | modular_arithmetic_generator.py |
| `LU_ENTRY` | 3 | `LU_ENTRY\|u11\|a11 = 2\|2` | lu_decomposition_generator.py |
| `LU_RESULT` | 2 | `LU_RESULT\|L\|[[1, 0, 0], [-4, 1, 0], [2, 4, 1]]` | lu_decomposition_generator.py |
| `LU_SETUP` | 2 | `LU_SETUP\|A = [[2, 3, 3], [-8, -9, -13], [4, 18, 1]]\|unit lower L` | lu_decomposition_generator.py |
| `LZ77_EMIT` | 1 | `LZ77_EMIT\|(0,0,t)` | lz_compression_generator.py |
| `LZ77_EXPAND` | 4 | `LZ77_EXPAND\|(0,0,h)\|no copy\|then add h\|out = h` | lz_compression_generator.py |
| `LZ77_MATCH` | 4 | `LZ77_MATCH\|pos 0\|literal\|offset 0, len 0\|next t` | lz_compression_generator.py |
| `LZ77_SEARCH` | 3 | `LZ77_SEARCH\|pos 1\|start 0\|len 0` | lz_compression_generator.py |
| `LZ78_APPEND` | 2 | `LZ78_APPEND\|empty + y\|out = y` | lz_compression_generator.py |
| `LZ78_DICT` | 2 | `LZ78_DICT\|0\|empty` | lz_compression_generator.py |
| `LZ78_EMIT` | 1 | `LZ78_EMIT\|(0,y)` | lz_compression_generator.py |
| `LZ78_LOOKUP` | 2 | `LZ78_LOOKUP\|index 0\|phrase empty` | lz_compression_generator.py |
| `LZ78_MATCH` | 4 | `LZ78_MATCH\|pos 0\|phrase empty\|index 0\|next y` | lz_compression_generator.py |
| `LZ_SETUP` | 2 | `LZ_SETUP\|LZ78 decode\|(0,y), (0,d), (1,d), (0,b), (2,y), (2,$)` | lz_compression_generator.py |
| `M` | 3 | `M\|6\|99\|594` | ac_circuit_generator.py, activation_generator.py, adam_step_generator.py, angle_defect_generator.py, angle_measure_generator.py, annuity_generator.py, arc_length_generator.py, arc_sector_generator.py, arithmetic_coding_generator.py, arithmetic_sequence_generator.py, attention_generator.py, backprop_generator.py, bec_channel_generator.py, binomial_probability_generator.py, bisection_generator.py, black_scholes_generator.py, blackbody_generator.py, bond_pricing_generator.py, calorimetry_generator.py, casimir_force_generator.py, casimir_generator.py, cayley_table_generator.py, chain_rule_generator.py, channel_capacity_generator.py, christoffel_generator.py, circle_angle_generator.py, classifier_metrics_generator.py, collision_generator.py, commutator_generator.py, complex_locus_generator.py, complex_log_generator.py, composite_arithmetic_generator.py, confidence_interval_generator.py, conic_standard_form_generator.py, continued_fraction_generator.py, continuous_distribution_generator.py, contour_integral_generator.py, convolution_generator.py, coset_generator.py, counterexample_search_generator.py, counting_classics_generator.py, cramers_rule_generator.py, cross_section_generator.py, crt_generator.py, curve_analysis_generator.py, cyclic_group_generator.py, de_moivre_generator.py, decimal_div_generator.py, definite_integral_generator.py, density_matrix_generator.py, derangement_generator.py, derivative_limit_def_generator.py, derivative_power_rule_generator.py, derivative_transcendental_generator.py, determinant_generator.py, dimensional_analysis_generator.py, doppler_generator.py, dot_product_generator.py, einstein_summation_generator.py, electrostatics_generator.py, elliptic_curve_finite_field_generator.py, embedding_similarity_generator.py, energy_conservation_generator.py, entropy_change_generator.py, entropy_generator.py, entropy_rate_markov_generator.py, equilibrium_ice_generator.py, equivalence_relation_generator.py, error_spotting_generator.py, euler_method_generator.py, evaluate_expression_generator.py, expected_value_generator.py, exponential_model_generator.py, extended_euclid_generator.py, factor_special_forms_generator.py, feature_map_generator.py, fermi_estimation_generator.py, fill_in_step_generator.py, finance_generator.py, finite_difference_generator.py, finite_field_generator.py, first_law_generator.py, five_number_summary_generator.py, fixed_point_generator.py, flops_memory_generator.py, four_vector_generator.py, fourier_series_generator.py, fractal_iteration_generator.py, fraction_op_generator.py, function_composition_generator.py, function_evaluation_generator.py, function_operations_generator.py, function_properties_generator.py, function_table_generator.py, fundamental_form_generator.py, game_theory_generator.py, gas_law_generator.py, gas_stoichiometry_generator.py, gauss_bonnet_generator.py, gauss_law_generator.py, gaussian_curvature_generator.py, generating_function_generator.py, geometric_distribution_generator.py, geometric_mean_generator.py, geometric_sequence_generator.py, geometry_area_perimeter_generator.py, gradient_descent_generator.py, gradient_step_generator.py, graph_counting_generator.py, graph_interpret_generator.py, grassmann_generator.py, great_circle_generator.py, hamiltonian_generator.py, hawking_generator.py, hermitian_check_generator.py, horner_evaluation_generator.py, huffman_coding_generator.py, hydrogen_atom_generator.py, hypercube_counting_generator.py, hypothesis_test_generator.py, index_gymnastics_generator.py, index_raising_generator.py, information_gain_generator.py, interference_generator.py, interpolation_generator.py, invariant_mass_generator.py, joint_distribution_generator.py, kernel_evaluation_generator.py, kernel_perceptron_generator.py, kernel_ridge_generator.py, kernel_validity_generator.py, kinematics_generator.py, kl_divergence_generator.py, ladder_operator_generator.py, lagrangian_generator.py, laplace_ivp_generator.py, laurent_series_generator.py, layer_norm_generator.py, lcm_generator.py, legendre_construction_generator.py, lhopital_generator.py, limit_evaluation_generator.py, linear_approx_generator.py, log_conversion_generator.py, log_diff_higher_order_generator.py, logistic_growth_generator.py, long_division_generator.py, lp_corner_generator.py, lr_schedule_generator.py, magnetism_generator.py, markov_chain_generator.py, matrix_calculus_generator.py, matrix_group_check_generator.py, matrix_inverse_generator.py, matrix_ops_generator.py, mean_value_theorem_generator.py, method_of_moments_generator.py, metric_arc_length_generator.py, mgf_generator.py, midpoint_generator.py, mixed_number_operation_generator.py, mobius_transform_generator.py, mod_exp_generator.py, modular_inverse_generator.py, multi_step_unit_conversion_generator.py, mutual_information_generator.py, naive_bayes_generator.py, named_distribution_generator.py, natural_units_generator.py, nets_surface_area_generator.py, newton_raphson_generator.py, newtons_laws_generator.py, npv_irr_generator.py, ode_system_generator.py, operation_properties_generator.py, optics_generator.py, optimization_generator.py, or_formula_generator.py, orbital_mechanics_generator.py, order_of_operations_generator.py, order_statistics_generator.py, param_count_generator.py, parametric_calculus_generator.py, particle_in_box_generator.py, partition_function_generator.py, pca_generator.py, percent_problem_generator.py, percent_word_problem_generator.py, perceptron_generator.py, permutation_combination_generator.py, physics_formula_generator.py, piecewise_evaluation_generator.py, planck_units_generator.py, polar_parametric_generator.py, polynomial_zeros_generator.py, portfolio_generator.py, positive_definite_generator.py, primality_test_generator.py, projectile_motion_generator.py, proportion_word_problem_generator.py, proportional_relationship_generator.py, quadratic_residue_generator.py, quantization_generator.py, quantum_formula_generator.py, quark_composition_generator.py, quaternion_generator.py, radical_multiply_generator.py, radical_rationalize_generator.py, rate_conversion_generator.py, ratio_table_generator.py, rational_equation_generator.py, rational_exponent_generator.py, recurrence_generator.py, recursive_definition_unfold_generator.py, recursive_explicit_generator.py, reed_solomon_generator.py, regression_generator.py, regular_polygon_area_generator.py, related_rates_generator.py, relativistic_energy_generator.py, remainder_factor_theorem_generator.py, riemann_sum_generator.py, riemann_tensor_generator.py, right_triangle_trig_generator.py, rotational_dynamics_generator.py, round_solids_generator.py, routh_hurwitz_generator.py, row_reduction_generator.py, rsa_generator.py, runge_kutta_generator.py, running_coupling_generator.py, rv_transform_generator.py, scaling_law_generator.py, schwarzschild_generator.py, second_order_ode_generator.py, segment_partition_generator.py, separable_pde_generator.py, series_solution_generator.py, set_builder_roster_generator.py, set_counting_generator.py, set_operations_generator.py, shm_generator.py, signal_arithmetic_generator.py, similar_triangles_generator.py, simplex_generator.py, solid_revolution_generator.py, solution_chem_generator.py, special_relativity_generator.py, special_right_triangle_generator.py, spherical_excess_generator.py, spherical_triangle_generator.py, standing_wave_generator.py, stars_and_bars_generator.py, statics_generator.py, stereographic_generator.py, stoichiometry_generator.py, svm_margin_generator.py, synthetic_division_generator.py, tangent_line_generator.py, taxicab_geometry_generator.py, taylor_series_generator.py, temperature_conversion_generator.py, tensor_product_generator.py, tip_bill_split_generator.py, totient_generator.py, transfer_function_generator.py, transformation_generator.py, transient_circuit_generator.py, transportation_generator.py, triangle_area_sas_generator.py, triangle_solve_generator.py, trig_identity_eval_generator.py, two_sample_test_generator.py, uncertainty_generator.py, undetermined_coeff_generator.py, unit_circle_generator.py, unit_conversion_generator.py, vector_ops_generator.py, volume_rect_prism_generator.py, von_neumann_entropy_generator.py, wavefunction_generator.py, young_tableaux_generator.py, z_score_generator.py, z_transform_generator.py |
| `MAG_FORMULA` | 1 | `MAG_FORMULA\|magnitude = √(x^2 + y^2 + z^2)` | magnetism_generator.py, vector_ops_generator.py |
| `MAG_SETUP` | 3 | `MAG_SETUP\|force\|q=10, v=6\|B=7, sin=7/25` | magnetism_generator.py |
| `MAIN_CONNECTIVE` | 1 | `MAIN_CONNECTIVE\|∨` | wff_parsing_generator.py |
| `MAP` | 2 | `MAP\|e\|f(e) = 3` | function_properties_generator.py |
| `MARGIN` | 2 | `MARGIN\|2/norm(w)\|2/5` | svm_margin_generator.py |
| `MARGINAL` | 1 | `MARGINAL\|P(X=0)=p00+p01` | joint_distribution_generator.py, mutual_information_generator.py |
| `MARKOV_SETUP` | 2, 3 | `MARKOV_SETUP\|two_state\|P00=4/7, P01=3/7\|P10=3/13, P11=10/13` | entropy_rate_markov_generator.py, markov_chain_generator.py |
| `MASTER_CASE` | 2 | `MASTER_CASE\|case 2\|Θ(n^2 log n)` | master_theorem_generator.py |
| `MATMUL_FLOPS` | 2 | `MATMUL_FLOPS\|XW1\|67108864` | flops_memory_generator.py |
| `MATRIX_ADD` | 2 | `MATRIX_ADD\|P0+P1\|[[1,0],[0,1]]` | bch_generator.py, casimir_generator.py, projector_generator.py |
| `MATRIX_ENTRY` | 1 | `MATRIX_ENTRY\|P2_01=P00*P01 + P01*P11` | markov_chain_generator.py |
| `MATRIX_ENTRY_SUM` | 3 | `MATRIX_ENTRY_SUM\|(1,2)\|-1 + 1\|0` | gamma_matrix_generator.py |
| `MATRIX_EXP` | 3 | `MATRIX_EXP\|e^A\|I + A\|[[1, 0, 0], [0, 1, 0], [-2, 0, 1]]` | bch_generator.py |
| `MATRIX_GROUP_SETUP` | 2 | `MATRIX_GROUP_SETUP\|O2\|M=[[-264/265,-23/265],[-23/265,264/265]]` | matrix_group_check_generator.py |
| `MATRIX_MULT` | 2, 3 | `MATRIX_MULT\|row1 dot col1\|256/4225*256/4225+1008/4225*1008/4225\|256/4225` | projector_generator.py |
| `MATRIX_POWER` | 2 | `MATRIX_POWER\|J^2\|-I` | lie_exponential_generator.py |
| `MATRIX_PRODUCT` | 2 | `MATRIX_PRODUCT\|AB\|[[55i/4, 0], [0, -55i/4]]` | bch_generator.py, casimir_generator.py, gamma_matrix_generator.py, pauli_algebra_generator.py, structure_constant_generator.py |
| `MATRIX_ROW` | 2 | `MATRIX_ROW\|d\|1 0 0` | graph_counting_generator.py, relation_operations_generator.py |
| `MATRIX_SCALE` | 2 | `MATRIX_SCALE\|1/2 ladder sum\|[[3267/98, 0, 0, 0], [0, 1089/14, 0, 0], [0, 0, 1089/14, 0], [0, 0, 0, 3267/98]]` | bch_generator.py, casimir_generator.py |
| `MATRIX_SETUP` | 2 | `MATRIX_SETUP\|unitary\|U=[[5/13,-12/13],[12/13,5/13]]` | hermitian_check_generator.py |
| `MATRIX_SUB` | 2 | `MATRIX_SUB\|AB - BA\|[[0, 0, 0], [-6, 0, 0], [0, 0, 0]]` | bch_generator.py |
| `MATRIX_SUM` | 1 | `MATRIX_SUM\|B=A+A^T` | matrix_calculus_generator.py |
| `MATRIX_VALUE` | 2 | `MATRIX_VALUE\|A\|[[0, 5i/2], [-5i/2, 0]]` | pauli_algebra_generator.py, structure_constant_generator.py |
| `MAT_ENTRY` | 2, 3 | `MAT_ENTRY\|(1,1)\|-3` | lie_exponential_generator.py, matrix_calculus_generator.py, matrix_ops_generator.py |
| `MAT_SETUP` | 2 | `MAT_SETUP\|A = [[3, -2], [-1, -6]], B = [[-6, -5], [1, 0]]\|A + B` | determinant_generator.py, diagonalization_generator.py, eigenvalue_generator.py, matrix_exponential_generator.py, matrix_inverse_generator.py, matrix_ops_generator.py, row_reduction_generator.py, subspace_basis_generator.py, svd_generator.py |
| `MAX` | 2, 3 | `MAX\|10, 7\|10` | dp_table_generator.py, matrix_norm_generator.py, taxicab_geometry_generator.py |
| `MAXIMAL` | 1 | `MAXIMAL\|{55, 58}` | partial_order_generator.py |
| `MAXTERM` | 2 | `MAXTERM\|001\|Q OR R OR NOT S` | boolean_algebra_generator.py |
| `MC_SETUP` | 3 | `MC_SETUP\|expression=x^T A x\|A=[[-1,3], [-2,2]]\|x=(4,0)` | matrix_calculus_generator.py |
| `MEAN` | 1 | `MEAN\|-4` | layer_norm_generator.py |
| `MEAN_DIV` | 3 | `MEAN_DIV\|63\|9\|7` | composite_arithmetic_generator.py, five_number_summary_generator.py, regression_generator.py, simple_stats_generator.py, standard_deviation_generator.py |
| `MEASURE_BASIS` | 3 | `MEASURE_BASIS\|z\|ket+z=ket0\|ket-z=ket1` | spin_half_generator.py |
| `MEASURE_FAVORABLE` | 2 | `MEASURE_FAVORABLE\|sector angle\|144` | geometric_probability_generator.py |
| `MEASURE_PROB` | 3 | `MEASURE_PROB\|computational basis\|P(0)=0\|P(1)=1` | quantum_gate_generator.py |
| `MEASURE_TOTAL` | 2 | `MEASURE_TOTAL\|full circle angle\|360` | geometric_probability_generator.py |
| `MEDIAN_PAIR` | 2 | `MEDIAN_PAIR\|7\|8` | five_number_summary_generator.py, simple_stats_generator.py |
| `MEDIAN_PICK` | 1, 2 | `MEDIAN_PICK\|9` | five_number_summary_generator.py, simple_stats_generator.py |
| `MEMBER_ROW` | 1 | `MEMBER_ROW\|x∈B, x∈M, x∈T` | set_identity_membership_table_generator.py |
| `MEMORY_SETUP` | 3 | `MEMORY_SETUP\|kv_cache\|L=4,h=16,d_k=64\|seq=128,precision_bytes=2` | flops_memory_generator.py |
| `MEMORY_UNIT` | 2 | `MEMORY_UNIT\|MiB\|2` | flops_memory_generator.py |
| `MERGE_BEGIN` | 3 | `MERGE_BEGIN\|merge 1\|lo=1,mid=2,hi=3\|left 2; right 19` | algorithm_trace_generator.py |
| `MERGE_COMPARE` | 3 | `MERGE_COMPARE\|2\|19\|take left` | algorithm_trace_generator.py |
| `MERGE_DONE` | 3 | `MERGE_DONE\|merge 1\|range 1-2\|array 16, 2, 19, 15, 28, 36` | algorithm_trace_generator.py |
| `MERGE_TAKE` | 2 | `MERGE_TAKE\|2\|merged 2` | algorithm_trace_generator.py |
| `METRIC` | 2 | `METRIC\|Chebyshev\|d = max(abs(x2 - x1), abs(y2 - y1))` | taxicab_geometry_generator.py |
| `METRICS_SETUP` | 1 | `METRICS_SETUP\|TP=39, FP=10, FN=21, TN=47` | classifier_metrics_generator.py |
| `METRIC_ARC_SETUP` | 3 | `METRIC_ARC_SETUP\|polar metric\|ds^2=dr^2+r^2 dtheta^2\|theta=60 deg, r:5->31` | metric_arc_length_generator.py |
| `METRIC_FORMULA` | 1 | `METRIC_FORMULA\|precision=TP/(TP+FP)` | classifier_metrics_generator.py |
| `METRIC_RESTRICT` | 2 | `METRIC_RESTRICT\|dtheta=0\|ds^2=dr^2` | metric_arc_length_generator.py |
| `MGF_SETUP` | 3 | `MGF_SETUP\|P(X=0)=19/24\|P(X=1)=1/6\|P(X=2)=1/24` | mgf_generator.py |
| `MGF_TERM` | 3 | `MGF_TERM\|x=0\|p0*e^(0t)\|19/24` | mgf_generator.py |
| `MIDDLE_EVAL` | 3 | `MIDDLE_EVAL\|phi=0..pi\|int sin(phi) dphi = 2\|2` | triple_integral_generator.py |
| `MIDLINE` | 1 | `MIDLINE\|y = 3` | sinusoid_features_generator.py |
| `MIDPOINT` | 2 | `MIDPOINT\|iter 1\|3` | algorithm_trace_generator.py |
| `MID_FORMULA` | 1 | `MID_FORMULA\|M = ((x1 + x2)/2, (y1 + y2)/2)` | circle_equation_generator.py, midpoint_generator.py |
| `MIN` | 2 | `MIN\|36,49\|36` | matrix_norm_generator.py |
| `MIN3` | 4 | `MIN3\|2\|2\|1\|1` | dp_table_generator.py |
| `MINIMAL` | 1 | `MINIMAL\|{2, 3, 33}` | partial_order_generator.py |
| `MINKOWSKI_FORMULA` | 1 | `MINKOWSKI_FORMULA\|eta_total=eta1+eta2` | minkowski_interval_generator.py |
| `MINKOWSKI_SETUP` | 3 | `MINKOWSKI_SETUP\|rapidity_addition\|eta1=3/2\|eta2=1/3` | minkowski_interval_generator.py |
| `MINTERM` | 2 | `MINTERM\|001\|NOT V AND NOT W AND X` | boolean_algebra_generator.py |
| `MIN_INITIAL` | 3 | `MIN_INITIAL\|nonaccept A, C\|accept B, D\|{A,C}, {B,D}` | dfa_minimization_generator.py |
| `MIN_REFINE` | 2 | `MIN_REFINE\|round 1\|{A,C}, {B,D}` | dfa_minimization_generator.py |
| `MIN_SIGNATURE` | 3 | `MIN_SIGNATURE\|round 1\|A\|0->B0,1->B1` | dfa_minimization_generator.py |
| `MIN_STABLE` | 1 | `MIN_STABLE\|{A,C}, {B,D}` | dfa_minimization_generator.py |
| `MIN_TRANSITION` | 3 | `MIN_TRANSITION\|{A,C}\|0\|{A,C}` | dfa_minimization_generator.py |
| `MISSED` | 1 | `MISSED\|16` | function_properties_generator.py |
| `MIX_FORMULA` | 2 | `MIX_FORMULA\|q=(d-b)/(a-b-c+d)\|p=(d-c)/(a-b-c+d)` | game_theory_generator.py |
| `MIX_IMPROPER` | 2 | `MIX_IMPROPER\|2 2/7\|16/7` | composite_arithmetic_generator.py, mixed_number_operation_generator.py, order_of_operations_generator.py |
| `MI_FORMULA` | 1 | `MI_FORMULA\|I=H(X)+H(Y)-H(X,Y)` | mutual_information_generator.py |
| `MI_SETUP` | 2 | `MI_SETUP\|rows=[[1/2,0];[0,1/2]]\|task=H(X,Y), H(Y given X), and I(X;Y)` | mutual_information_generator.py |
| `MLE_SETUP` | 2, 3 | `MLE_SETUP\|normal_mu\|parameter=mu\|sigma^2=4` | mle_generator.py |
| `MOBIUS_SETUP` | 2 | `MOBIUS_SETUP\|T(z)=(3z - 1)/(4z + 1)\|z0=-3` | mobius_transform_generator.py |
| `MODE` | 2 | `MODE\|2\|10, 13` | frequency_table_generator.py, simple_stats_generator.py |
| `MODEL` | 1 | `MODEL\|A = P(1 + r)^t` | exponential_model_generator.py |
| `MODEL_APPLY` | 1 | `MODEL_APPLY\|A = 4500 · (1 + 0.18)^2` | exponential_model_generator.py |
| `MODEL_OUTPUT` | 1 | `MODEL_OUTPUT\|-3/2` | activation_generator.py |
| `MODEXP_MULTIPLY` | 2 | `MODEXP_MULTIPLY\|bit 1=1\|26` | mod_exp_generator.py, quadratic_residue_generator.py |
| `MODEXP_SETUP` | 3 | `MODEXP_SETUP\|base 26\|exponent 50\|modulus 37` | mod_exp_generator.py |
| `MODEXP_SQUARE` | 2 | `MODEXP_SQUARE\|bit 1=1\|1` | mod_exp_generator.py, quadratic_residue_generator.py |
| `MODEXP_STATE` | 2 | `MODEXP_STATE\|after bit 1\|26` | mod_exp_generator.py, quadratic_residue_generator.py |
| `MODE_COUNT` | 2 | `MODE_COUNT\|1\|1` | simple_stats_generator.py |
| `MOD_INVERSE` | 2 | `MOD_INVERSE\|77 mod 59\|23` | crt_generator.py, ecdsa_generator.py, elliptic_curve_finite_field_generator.py, modular_inverse_generator.py, rsa_generator.py |
| `MOD_NORMALIZE` | 3 | `MOD_NORMALIZE\|23\|mod 59\|23` | modular_inverse_generator.py, rsa_generator.py |
| `MOD_POWER` | 3 | `MOD_POWER\|41^1\|mod 42\|41` | diffie_hellman_generator.py, pollard_factorization_generator.py, primality_test_generator.py, rsa_generator.py, tonelli_shanks_generator.py, totient_generator.py |
| `MOD_REDUCE` | 3 | `MOD_REDUCE\|25\|mod 12\|1` | calendar_arithmetic_generator.py, cayley_table_generator.py, coset_generator.py, crt_generator.py, cyclic_group_generator.py, de_moivre_generator.py, elliptic_curve_finite_field_generator.py, finite_field_generator.py, jacobi_symbol_generator.py, lie_exponential_generator.py, mod_exp_generator.py, modular_arithmetic_generator.py, modular_inverse_generator.py, primality_test_generator.py, quadratic_residue_generator.py, reed_solomon_generator.py, rsa_generator.py, totient_generator.py |
| `MOD_SETUP` | 2, 3, 4 | `MOD_SETUP\|12-hour clock\|12 + 13 hours` | modular_arithmetic_generator.py, modular_inverse_generator.py |
| `MOD_SOLVE` | 2 | `MOD_SOLVE\|0 means 12 on a clock\|1 o'clock` | modular_arithmetic_generator.py |
| `MOD_TERM` | 2 | `MOD_TERM\|10 * 6\|60` | modular_arithmetic_generator.py |
| `MOE_FORMULA` | 1 | `MOE_FORMULA\|E = z*·σ/√n` | confidence_interval_generator.py |
| `MOLAR_MASS` | 2 | `MOLAR_MASS\|CO\|28 g/mol` | gas_stoichiometry_generator.py, stoichiometry_generator.py |
| `MOLAR_VOLUME` | 2 | `MOLAR_VOLUME\|1 mol gas\|24 L` | stoichiometry_generator.py |
| `MOMENT` | 2 | `MOMENT\|m1\|-1/2` | adam_step_generator.py |
| `MOMENTUM` | 1 | `MOMENTUM\|x components` | collision_generator.py |
| `MOMENT_X` | 3 | `MOMENT_X\|M_x = 1/2 int y^2 dx\|7^2*3^5/10\|11907/10` | centroid_generator.py |
| `MOMENT_Y` | 3 | `MOMENT_Y\|M_y = int x*y dx\|7*3^4/4\|567/4` | centroid_generator.py |
| `MOM_EQUATION` | 2 | `MOM_EQUATION\|E[X]=1/lambda\|xbar=1/lambda` | method_of_moments_generator.py |
| `MOM_SETUP` | 3 | `MOM_SETUP\|exponential\|parameter=lambda\|data=[10,3,5,2,9,4]` | method_of_moments_generator.py |
| `MONO_ADD_EXP` | 2 | `MONO_ADD_EXP\|x^1 * x^5 = x^(1+5)\|x^6` | monomial_mult_div_generator.py |
| `MONO_DIV_COEFF` | 2 | `MONO_DIV_COEFF\|-28 / 7\|-4` | monomial_mult_div_generator.py |
| `MONO_MULT_COEFF` | 2 | `MONO_MULT_COEFF\|-9 * 3\|-27` | monomial_mult_div_generator.py |
| `MONO_SETUP` | 1 | `MONO_SETUP\|(-28x^8) / (7x^4)` | monomial_mult_div_generator.py |
| `MONO_SUB_EXP` | 2 | `MONO_SUB_EXP\|x^8 / x^4 = x^(8-4)\|x^4` | monomial_mult_div_generator.py |
| `MOOD` | 2 | `MOOD\|OOO\|figure 2` | syllogism_generator.py |
| `MOVE_TERM` | 2, 3 | `MOVE_TERM\|-4x\|left\|4x+2+4x = -5` | area_between_curves_generator.py, completing_square_generator.py, conic_standard_form_generator.py, linear_complex_generator.py, polar_parametric_generator.py, quadratic_factoring_generator.py, quadratic_square_root_generator.py, radical_equation_generator.py, special_solution_equation_generator.py, standard_form_conversion_generator.py |
| `MR_DECOMPOSE` | 2 | `MR_DECOMPOSE\|76\|2^2 * 19` | primality_test_generator.py |
| `MR_SETUP` | 2 | `MR_SETUP\|n=77\|witnesses 10, 19` | primality_test_generator.py |
| `MR_SQUARE` | 2 | `MR_SQUARE\|r=1\|23` | primality_test_generator.py |
| `MR_WITNESS` | 1 | `MR_WITNESS\|10` | primality_test_generator.py |
| `MR_WITNESS_RESULT` | 2 | `MR_WITNESS_RESULT\|10\|composite` | primality_test_generator.py |
| `MSE_FORMULA` | 2 | `MSE_FORMULA\|L=(1/n) sum r_i^2\|grad=(2/n) sum r_i*[1,x_i]` | gradient_step_generator.py |
| `MSE_GRADIENT` | 2 | `MSE_GRADIENT\|g0=-40/3\|g1=-58/3` | gradient_step_generator.py |
| `MSE_SAMPLE` | 3 | `MSE_SAMPLE\|i=1\|pred=-4\|r=-7` | gradient_step_generator.py |
| `MSE_SETUP` | 3 | `MSE_SETUP\|model y_hat=w0+w1*x\|samples=[(1,3), (0,0), (2,5)]\|w=(-2,-2), eta=1/5` | gradient_step_generator.py |
| `MST_ADD` | 2 | `MST_ADD\|AB\|total 2` | mst_generator.py |
| `MST_SET` | 1 | `MST_SET\|AB` | mst_generator.py |
| `MST_SETUP` | 2 | `MST_SETUP\|weighted undirected graph\|vertices A, B, C, D, E, F` | mst_generator.py |
| `MU` | 2 | `MU\|143/205\|round=1` | lll_reduction_generator.py |
| `MULTIPLY_IF` | 2 | `MULTIPLY_IF\|e^(3x)y' + 3e^(3x)y\|28e^(7x)` | integrating_factor_generator.py, ode_substitution_generator.py |
| `MULTIVALUED_LOG` | 2 | `MULTIVALUED_LOG\|ln(36/7) + i*(-pi/9 + 2pi*k)\|k in Z` | complex_log_generator.py |
| `MULTI_FORMULA` | 2 | `MULTI_FORMULA\|n!/(a!b!c!...)\|10! / repeats` | stars_and_bars_generator.py |
| `MULTI_SETUP` | 2 | `MULTI_SETUP\|2 H's, 4 L's, 4 T's\|total 10` | stars_and_bars_generator.py |
| `MUL_PARTIAL` | 3 | `MUL_PARTIAL\|6\|68395\|410370` | decimal_mult_generator.py, multi_digit_multiplication_generator.py |
| `MUL_SETUP` | 2 | `MUL_SETUP\|68395\|1956` | decimal_mult_generator.py, multi_digit_multiplication_generator.py |
| `MUL_TERM` | 3 | `MUL_TERM\|20\|(-1/5)x\|-4x` | linear_fractional_generator.py, polynomial_long_division_generator.py, rational_equation_generator.py |
| `MVT_SETUP` | 2 | `MVT_SETUP\|f(x) = x^2 - 4x - 5 on [2, 4]\|find the c guaranteed by the MVT` | mean_value_theorem_generator.py |
| `MV_CHAIN_SETUP` | 3 | `MV_CHAIN_SETUP\|z = f(x,y) = x^2 + 4*y^2 - 2*x*y + 6*x + 2*y\|x = -4*s + 3*t + 5, y = 2*s - 2*t + 1\|(s,t) = (1, -2)` | multivar_chain_rule_generator.py |
| `NATURAL_SETUP` | 3 | `NATURAL_SETUP\|mass\|hbar=1,c=1\|m=61/5 TeV` | natural_units_generator.py |
| `NB_FEATURE_COUNT` | 3 | `NB_FEATURE_COUNT\|Spam\|known=1\|count=9` | naive_bayes_generator.py |
| `NB_LIKELIHOOD` | 3 | `NB_LIKELIHOOD\|Spam\|known=1\|5/7` | naive_bayes_generator.py |
| `NB_PRIOR` | 2 | `NB_PRIOR\|Spam\|12/31` | naive_bayes_generator.py |
| `NB_SCORE` | 2 | `NB_SCORE\|Spam\|start=12/31` | naive_bayes_generator.py |
| `NB_SETUP` | 3 | `NB_SETUP\|query=known=1, money=0, offer=0\|alpha=1\|classes=Spam,Ham` | naive_bayes_generator.py |
| `NCR` | 2 | `NCR\|C(6,0)\|1` | binomial_probability_generator.py, derangement_generator.py, generating_function_generator.py, hypercube_counting_generator.py |
| `NEAREST` | 2 | `NEAREST\|queen\|(1,1)` | embedding_similarity_generator.py |
| `NEED` | 2 | `NEED\|line 2 gives the base ratio 8:11\|line 4 multiplies 8 by 2` | fill_in_step_generator.py |
| `NEG_LOG` | 2 | `NEG_LOG\|p=1/64\|ln(64)` | perplexity_generator.py |
| `NET_SETUP` | 2 | `NET_SETUP\|2 right triangles with legs 9 and 12; rectangles 9 by 3, 12 by 3, and 15 by 3\|total surface area` | nets_surface_area_generator.py |
| `NEWTON_DD` | 2 | `NEWTON_DD\|f[x0,x1]\|2` | interpolation_generator.py |
| `NEWTON_SETUP` | 2, 3 | `NEWTON_SETUP\|f(x)=x^2-42\|f'(x)=2x\|x0=7,iterations=2` | newton_raphson_generator.py, newtons_laws_generator.py |
| `NEWTON_STEP` | 2 | `NEWTON_STEP\|1\|59/150` | npv_irr_generator.py |
| `NEWTON_UPDATE` | 3 | `NEWTON_UPDATE\|1\|x_0=7\|x_1=13/2` | newton_raphson_generator.py |
| `NEW_SLOPE` | 2 | `NEW_SLOPE\|New slope (m2) = -3/2\|Parallel lines have the same slope` | parallel_perpendicular_line_generator.py |
| `NFA_ACCEPT` | 1 | `NFA_ACCEPT\|s3` | nfa_simulation_generator.py |
| `NFA_ACTIVE` | 2 | `NFA_ACTIVE\|start\|{s1}` | nfa_simulation_generator.py |
| `NFA_EPSILON` | 2 | `NFA_EPSILON\|q2\|{q3}` | nfa_simulation_generator.py |
| `NFA_INPUT` | 1 | `NFA_INPUT\|acbabb` | nfa_simulation_generator.py |
| `NFA_MOVE` | 4 | `NFA_MOVE\|{s1}\|a\|s1->{s1,s2}\|{s1,s2}` | nfa_simulation_generator.py |
| `NFA_READ` | 2 | `NFA_READ\|pos 1\|a` | nfa_simulation_generator.py |
| `NFA_SETUP` | 3 | `NFA_SETUP\|states s1, s2, s3\|alphabet a, b, c\|start s1` | nfa_simulation_generator.py |
| `NFA_TRANSITION` | 3 | `NFA_TRANSITION\|s1\|a\|{s1,s2}` | nfa_simulation_generator.py |
| `NILPOTENT` | 3 | `NILPOTENT\|theta^2=0\|5theta^2\|0` | grassmann_generator.py |
| `NLL` | 2 | `NLL\|125 tokens\|125*ln(64)` | perplexity_generator.py |
| `NORM2` | 2 | `NORM2\|b1\|205` | lll_reduction_generator.py |
| `NORMALIZE` | 2 | `NORMALIZE\|1/2 + 1/2\|1` | clebsch_gordan_generator.py, layer_norm_generator.py |
| `NORMALIZE_SIGN` | 2 | `NORMALIZE_SIGN\|(-6,-4)\|(6,4)` | lll_reduction_generator.py |
| `NORMAL_EQ` | 2 | `NORMAL_EQ\|X^T X\|[[4, 0], [0, 20]]` | least_squares_generator.py |
| `NORMAL_SLOPE` | 2 | `NORMAL_SLOPE\|-1/(-2)\|1/2` | tangent_line_generator.py |
| `NORMAL_SYMMETRY` | 2 | `NORMAL_SYMMETRY\|N_neg_d1=0.1\|N_neg_d2=0.15` | black_scholes_generator.py |
| `NORM_CHECK` | 2 | `NORM_CHECK\|P(+z)+P(-z)\|1` | spin_half_generator.py |
| `NORM_SETUP` | 2 | `NORM_SETUP\|X ~ N(90, 8)\|is x = 112 unusual?` | matrix_norm_generator.py, normal_table_generator.py, z_score_generator.py |
| `NORM_SQUARED` | 2 | `NORM_SQUARED\|q\|1` | quaternion_generator.py |
| `NO_COLLISION` | 1 | `NO_COLLISION\|all outputs distinct` | function_properties_generator.py |
| `NO_MISSED` | 1 | `NO_MISSED\|all codomain values hit` | function_properties_generator.py |
| `NO_REDEX` | 2 | `NO_REDEX\|lambda c. c\|no beta redex remains` | lambda_reduction_generator.py |
| `NPV_SETUP` | 2 | `NPV_SETUP\|c0=-2100,c1=2000,c2=1750,c3=650\|rate=25%` | npv_irr_generator.py |
| `NPV_TERM` | 2 | `NPV_TERM\|t=0\|-2100` | npv_irr_generator.py |
| `NULL_REL` | 2 | `NULL_REL\|x1 + 3*x3 - 3*x4 = 0\|x1 = -3*x3 + 3*x4` | subspace_basis_generator.py |
| `NULL_VECTOR` | 2 | `NULL_VECTOR\|x3=1, x4=0\|[-3, -4, 1, 0]` | subspace_basis_generator.py |
| `NUMBER_OPERATOR` | 2 | `NUMBER_OPERATOR\|N ket28\|28 ket28` | ladder_operator_generator.py |
| `NW_ALLOC` | 1, 3 | `NW_ALLOC\|cell x11\|min(16,14)\|14` | transportation_generator.py |
| `NYQUIST` | 1 | `NYQUIST\|required rate = 2*f_max` | signal_arithmetic_generator.py |
| `OBJECTIVE` | 1 | `OBJECTIVE\|at (0,0)` | lp_corner_generator.py |
| `OCCURS_CHECK` | 3 | `OCCURS_CHECK\|X\|f(X)\|fail` | unification_generator.py |
| `ODD_VERTICES` | 2 | `ODD_VERTICES\|C, D\|2` | euler_circuit_generator.py |
| `ODE_SETUP` | 2, 3 | `ODE_SETUP\|dy/dt = ky; y doubles every 132 hours\|find k exactly` | euler_method_generator.py, exact_ode_generator.py, integrating_factor_generator.py, laplace_ivp_generator.py, logistic_growth_generator.py, ode_substitution_generator.py, ode_system_generator.py, runge_kutta_generator.py, second_order_ode_generator.py, separable_ode_generator.py, series_solution_generator.py, stability_generator.py, undetermined_coeff_generator.py, variation_parameters_generator.py |
| `OPTICS_FORMULA` | 1 | `OPTICS_FORMULA\|1/f=1/d_o+1/d_i` | optics_generator.py |
| `OPTICS_SETUP` | 3 | `OPTICS_SETUP\|mirror_magnification\|f=17, d_o=68\|h_o=17` | optics_generator.py |
| `OPT_SETUP` | 2 | `OPT_SETUP\|square sheet 3534 by 3534; cut corners x and fold\|maximize volume` | optimization_generator.py |
| `ORBIT_FORMULA` | 1 | `ORBIT_FORMULA\|F=G*m1*m2/r^2` | orbital_mechanics_generator.py |
| `ORBIT_SETUP` | 3 | `ORBIT_SETUP\|gravity_force\|m1=57, m2=20\|r=24, G=1` | orbital_mechanics_generator.py |
| `ORDER_PAIR` | 2 | `ORDER_PAIR\|24 ≤ 55\|reachable in H` | partial_order_generator.py |
| `ORDER_PDF` | 1 | `ORDER_PDF\|f_{3:9}(x)=252*x^2*(1-x)^6` | order_statistics_generator.py |
| `ORDER_SETUP` | 3 | `ORDER_SETUP\|n=9\|k=3\|q=11/13` | order_statistics_generator.py |
| `ORDER_START` | 2 | `ORDER_START\|7\|identity 0` | cayley_table_generator.py |
| `ORDER_STEP` | 2 | `ORDER_STEP\|k=1\|7` | cayley_table_generator.py |
| `ORTHOGONALITY` | 2 | `ORTHOGONALITY\|lower multiplet\|orthogonal to higher J` | clebsch_gordan_generator.py |
| `OR_SETUP` | 3 | `OR_SETUP\|M/M/1\|lambda=15\|mu=28` | or_formula_generator.py |
| `OUTER_ANTIDERIV` | 2 | `OUTER_ANTIDERIV\|dx\|4*x^2 + 36*x` | double_integral_generator.py |
| `OUTER_EVAL` | 3 | `OUTER_EVAL\|x=2..7\|4*(7^2 - 2^2) + 36*(7 - 2)\|360` | double_integral_generator.py |
| `OUTER_PRODUCT` | 1 | `OUTER_PRODUCT\|rho=1/2(ket00bra00+e^(-i195π/112)ket00bra10+e^(i195π/112)ket10bra00+ket10bra10)` | partial_trace_generator.py |
| `OUTPUT` | 1 | `OUTPUT\|y_hat=-2` | backprop_generator.py |
| `PAIR` | 2 | `PAIR\|apricot\|badger` | one_to_one_correspondence_generator.py |
| `PARALLEL_RELATION` | 1 | `PARALLEL_RELATION\|5x + 38 = 6x + 20` | angle_relationships_generator.py |
| `PARALLEL_SETUP` | 2 | `PARALLEL_SETUP\|alternate_interior\|Alternate interior angles are equal` | angle_relationships_generator.py |
| `PARALLEL_SOLVE` | 2 | `PARALLEL_SOLVE\|-1x = -18\|x = 18` | angle_relationships_generator.py |
| `PARAMS` | 3 | `PARAMS\|W1=[[0,0], [1,2]]\|b1=(2,2)\|v=(-2,-1), c=2` | backprop_generator.py |
| `PARAM_PART` | 2 | `PARAM_PART\|attention_per_layer\|5308416` | param_count_generator.py |
| `PARAM_PATH` | 3 | `PARAM_PATH\|r(t)\|(-2, -3*t + 3)\|0 <= t <= 1` | line_integral_generator.py |
| `PARAM_SETUP` | 2, 3 | `PARAM_SETUP\|x = 33cos t - 11, y = 33sin t + 9\|eliminate t` | param_count_generator.py, parametric_calculus_generator.py, polar_parametric_generator.py |
| `PARITY` | 1, 2 | `PARITY\|transpositions 4\|even` | fourier_series_generator.py, permutation_group_generator.py |
| `PARITY_CALC` | 2 | `PARITY_CALC\|p1=d1 xor d2 xor d4\|1 xor 0 xor 0=1` | hamming_code_generator.py |
| `PARSE` | 2, 3 | `PARSE\|p\|atom` | wff_parsing_generator.py |
| `PARTFRAC_SETUP` | 1 | `PARTFRAC_SETUP\|(4x + 13)/(x + 3)^2 = A/(x + 3) + B/(x + 3)^2` | partial_fractions_generator.py, telescoping_generator.py |
| `PARTIAL` | 2 | `PARTIAL\|u_x\|8x + 3` | cauchy_riemann_generator.py, fundamental_form_generator.py, hamiltonian_generator.py, lagrangian_generator.py |
| `PARTIAL_FRAC` | 2 | `PARTIAL_FRAC\|Y(s)\|1/(s + 1) - 4/(s - 4)` | laplace_ivp_generator.py |
| `PARTIAL_RESULT` | 2 | `PARTIAL_RESULT\|f_x\|32*x^3*y^3 + 12*x^2*y^2` | div_curl_generator.py, exact_ode_generator.py, gradient_generator.py, hessian_classify_generator.py, jacobian_generator.py, lagrange_multiplier_generator.py, line_integral_generator.py, multivar_chain_rule_generator.py, partial_derivative_generator.py, vector_theorem_generator.py |
| `PARTIAL_RULE` | 3 | `PARTIAL_RULE\|8*x^4*y^3\|d/dx\|32*x^3*y^3` | partial_derivative_generator.py |
| `PARTIAL_SETUP` | 2 | `PARTIAL_SETUP\|f(x,y) = 8*x^4*y^3 + 4*x^3*y^2\|f_xx` | partial_derivative_generator.py |
| `PARTIAL_TRACE` | 2 | `PARTIAL_TRACE\|ket00bra00\|ket0bra0` | partial_trace_generator.py |
| `PARTICLE_TABLE` | 1 | `PARTICLE_TABLE\|e-(Q=-1,B=0,Le=1,Lmu=0); e+(Q=1,B=0,Le=-1,Lmu=0); gamma(Q=0,B=0,Le=0,Lmu=0); pi0(Q=0,B=0,Le=0,Lmu=0)` | conservation_law_generator.py |
| `PARTICULAR` | 2 | `PARTICULAR\|y_p\|-e^(4x)` | undetermined_coeff_generator.py, variation_parameters_generator.py |
| `PARTICULAR_CHECK` | 2 | `PARTICULAR_CHECK\|K = 1\|-5K - 6K + 12 = K` | recurrence_generator.py |
| `PARTICULAR_TRY` | 2 | `PARTICULAR_TRY\|a_n = K\|constant forcing` | recurrence_generator.py |
| `PARTITION` | 1 | `PARTITION\|{{11, 13, 15, 17, 19, 21, 23, 25}, {12, 14, 16, 18, 20, 22, 24, 26}}` | equivalence_relation_generator.py |
| `PARTITION_FORMULA` | 1 | `PARTITION_FORMULA\|Z=g0+g1*b` | partition_function_generator.py |
| `PARTITION_SETUP` | 3 | `PARTITION_SETUP\|degenerate_two_level\|g0=1, g1=5\|epsilon=15, b=1/4` | partition_function_generator.py |
| `PARTS_CHOOSE` | 2 | `PARTS_CHOOSE\|u = 67x, dv = sin(x) dx\|du = 67 dx, v = -cos(x)` | integration_by_parts_generator.py |
| `PARTS_FORMULA` | 1 | `PARTS_FORMULA\|∫ u dv = uv - ∫ v du` | integration_by_parts_generator.py |
| `PASCAL_ROW` | 2 | `PASCAL_ROW\|0\|1` | pascal_triangle_generator.py |
| `PASCAL_SETUP` | 1 | `PASCAL_SETUP\|18C7` | pascal_triangle_generator.py |
| `PATH` | 2 | `PATH\|8→26→9\|add (8, 9)` | relation_closure_generator.py |
| `PATH_DERIV` | 2 | `PATH_DERIV\|r'(t)\|(0, -3)` | curve_geometry_generator.py, line_integral_generator.py |
| `PAULI_IDENTITY` | 3 | `PAULI_IDENTITY\|Tr(sigma_z sigma_z)\|2 delta_ij\|8` | pauli_algebra_generator.py |
| `PAULI_MATRIX` | 2 | `PAULI_MATRIX\|sigma_z\|[[1,0],[0,-1]]` | spin_half_generator.py |
| `PAULI_SETUP` | 3 | `PAULI_SETUP\|trace\|A=-4sigma_z\|B=-sigma_z` | pauli_algebra_generator.py |
| `PCA_SETUP` | 2 | `PCA_SETUP\|points=[(2,-1), (-6,-1), (-2,7), (-2,-9)]\|population covariance` | pca_generator.py |
| `PC_VECTOR` | 2 | `PC_VECTOR\|e2\|(0,1)` | pca_generator.py |
| `PDA_POP` | 2 | `PDA_POP\|A\|stack=$AA` | pda_simulation_generator.py |
| `PDA_PUSH` | 2 | `PDA_PUSH\|A\|stack=$A` | pda_simulation_generator.py |
| `PDA_READ` | 1 | `PDA_READ\|a` | pda_simulation_generator.py |
| `PDA_REJECT` | 1 | `PDA_REJECT\|pop from bottom` | pda_simulation_generator.py |
| `PDA_SETUP` | 2 | `PDA_SETUP\|a^n b^n\|stack=$` | pda_simulation_generator.py |
| `PDA_STATE` | 3 | `PDA_STATE\|pos 1\|push\|stack=$` | pda_simulation_generator.py |
| `PDE_SETUP` | 2 | `PDE_SETUP\|u_t = 11u_xx on [0,8]\|u(x,0)=14sin(10πx/8)` | separable_pde_generator.py |
| `PDF_FORMULA` | 1 | `PDF_FORMULA\|f_Y(y)=1/(36*sqrt(y))` | rv_transform_generator.py |
| `PD_SETUP` | 2 | `PD_SETUP\|A=[[4,6], [6,18]]\|Sylvester criterion` | positive_definite_generator.py |
| `PERCENT_CALC_PART` | 3 | `PERCENT_CALC_PART\|1.845\|485\|894.825` | percent_problem_generator.py |
| `PERCENT_TO_DEC` | 2 | `PERCENT_TO_DEC\|87%\|0.87` | annuity_generator.py, bond_pricing_generator.py, composite_arithmetic_generator.py, exponential_model_generator.py, fill_in_step_generator.py, finance_generator.py, fraction_decimal_percent_converter.py, npv_irr_generator.py, percent_problem_generator.py, percent_word_problem_generator.py, piecewise_evaluation_generator.py, portfolio_generator.py, tip_bill_split_generator.py |
| `PERCEPTRON_RULE` | 2 | `PERCEPTRON_RULE\|score=w0+w1*x1+w2*x2\|if y*score <= 0 update` | perceptron_generator.py |
| `PERCEPTRON_SAMPLE` | 3 | `PERCEPTRON_SAMPLE\|i=1\|x=(-2,2)\|y=1` | perceptron_generator.py |
| `PERCEPTRON_SCORE` | 2 | `PERCEPTRON_SCORE\|i=1\|score=-5` | perceptron_generator.py |
| `PERCEPTRON_SETUP` | 3 | `PERCEPTRON_SETUP\|eta=2\|w=(1,2,-1)\|samples=[(-2,2,1), (0,2,1), (-3,3,1)]` | perceptron_generator.py |
| `PERCEPTRON_UPDATE` | 2, 3 | `PERCEPTRON_UPDATE\|i=1\|w=(3,-2,3)` | perceptron_generator.py |
| `PERIM` | 1 | `PERIM\|42` | geometry_area_perimeter_generator.py, polygon_perimeter_generator.py |
| `PERIOD` | 1 | `PERIOD\|90°` | sinusoid_features_generator.py |
| `PERM_COMPOSE` | 3 | `PERM_COMPOSE\|i=1\|tau(i)=4\|sigma(tau(i))=3` | permutation_group_generator.py |
| `PERM_FORMULA` | 1 | `PERM_FORMULA\|P(n, r) = n·(n-1)···(n-r+1), 3 factors` | permutation_combination_generator.py |
| `PERM_RESULT` | 1 | `PERM_RESULT\|[3, 5, 4, 2, 1]` | permutation_group_generator.py |
| `PERM_SETUP` | 2, 3 | `PERM_SETUP\|arrange 3 of 4\|order matters` | permutation_combination_generator.py, permutation_group_generator.py |
| `PERPLEXITY` | 2 | `PERPLEXITY\|exp(CE)\|64` | perplexity_generator.py |
| `PERPLEXITY_SETUP` | 2 | `PERPLEXITY_SETUP\|tokens=125\|p=1/64` | perplexity_generator.py |
| `PE_ENTRY` | 2 | `PE_ENTRY\|0\|1/2` | positional_encoding_generator.py |
| `PE_SETUP` | 3 | `PE_SETUP\|position=216\|d=2\|theta=5pi/6` | positional_encoding_generator.py |
| `PF_PRIME` | 1 | `PF_PRIME\|347` | prime_factorization_generator.py, repeating_decimal_generator.py |
| `PF_STEP` | 3 | `PF_STEP\|1041\|3\|347` | prime_factorization_generator.py, repeating_decimal_generator.py |
| `PHASE_SHIFT` | 1 | `PHASE_SHIFT\|30° left` | sinusoid_features_generator.py |
| `PHI_STEP` | 2 | `PHI_STEP\|p=2\|21` | totient_generator.py |
| `PHYS_FORMULA` | 1 | `PHYS_FORMULA\|W = F*d` | physics_formula_generator.py |
| `PHYS_SETUP` | 3 | `PHYS_SETUP\|F = 58 newtons\|d = 18 meters\|work` | physics_formula_generator.py |
| `PH_FORMULA` | 1 | `PH_FORMULA\|pOH=-log10([OH-]), pH=14-pOH` | ph_calculation_generator.py |
| `PH_SETUP` | 2, 3 | `PH_SETUP\|hydroxide_with_log\|[OH-]=7*10^-6\|log10(7)=0.85` | ph_calculation_generator.py |
| `PI2_NUM` | 3 | `PI2_NUM\|-119/491520\|π^2\|-119π^2/491520` | casimir_force_generator.py |
| `PICTO_COUNT` | 2 | `PICTO_COUNT\|Giraffes\|1` | graph_interpret_generator.py |
| `PICTO_KEY` | 2 | `PICTO_KEY\|♦\|5` | graph_interpret_generator.py |
| `PIVOT` | 3 | `PIVOT\|row=s1\|column=x\|pivot=1` | simplex_generator.py |
| `PIVOT_COLS` | 2 | `PIVOT_COLS\|columns 1, 2\|rank = 2` | subspace_basis_generator.py |
| `PI_COEFF` | 2 | `PI_COEFF\|10π/9\|10/9` | arc_sector_generator.py |
| `PI_DEN` | 3 | `PI_DEN\|27/112\|π\|27/(112π)` | gauss_law_generator.py, hawking_generator.py, magnetism_generator.py |
| `PI_MULT` | 3 | `PI_MULT\|2\|π\|2π` | shm_generator.py |
| `PLACE_DP` | 3 | `PLACE_DP\|2262\|2\|22.62` | decimal_mult_generator.py |
| `PLACE_DP_Q` | 3 | `PLACE_DP_Q\|165\|3\|165` | decimal_div_generator.py, percent_problem_generator.py |
| `PLACE_VALUE` | 2 | `PLACE_VALUE\|4 * 16^0\|4` | base_conversion_generator.py |
| `PLANCK_SETUP` | 4 | `PLANCK_SETUP\|time\|hbar=121\|G=1\|c=25` | planck_units_generator.py |
| `PLUS_MINUS` | 2 | `PLUS_MINUS\|y - 6 = ±5\|y - 6 = 5 or y - 6 = -5` | completing_square_generator.py, quadratic_square_root_generator.py, rational_equation_generator.py |
| `POINT_FROM_LAMBDA` | 3 | `POINT_FROM_LAMBDA\|x\|80/4\|20` | lagrange_multiplier_generator.py |
| `POINT_SLOPE_SETUP` | 1 | `POINT_SLOPE_SETUP\|y + 6 = 1/2(x - 3)` | equation_from_two_points_generator.py, parallel_perpendicular_line_generator.py, point_slope_generator.py |
| `POLAR_AREA_FORMULA` | 1 | `POLAR_AREA_FORMULA\|A = (1/2) ∫ r^2 dθ` | parametric_calculus_generator.py |
| `POLAR_BOUNDS` | 2 | `POLAR_BOUNDS\|r\|0..2` | double_integral_generator.py |
| `POLAR_CONVERT` | 2 | `POLAR_CONVERT\|x^2 + y^2\|r^2` | double_integral_generator.py |
| `POLAR_EVAL` | 3 | `POLAR_EVAL\|theta range * radial integral\|pi/2 * 4\|2*pi` | double_integral_generator.py |
| `POLAR_FORM` | 1 | `POLAR_FORM\|9 cis(180 deg)` | euler_formula_generator.py |
| `POLAR_FORMULA` | 1 | `POLAR_FORMULA\|x = r cos θ, y = r sin θ` | polar_parametric_generator.py |
| `POLAR_SETUP` | 2, 3 | `POLAR_SETUP\|r = 47\|pole=(-8, -19)\|rectangular equation` | parametric_calculus_generator.py, polar_parametric_generator.py |
| `POLES` | 1 | `POLES\|s=-2, -8` | transfer_function_generator.py |
| `POLE_ORDER` | 1 | `POLE_ORDER\|1` | residue_generator.py |
| `POLE_TEST` | 3 | `POLE_TEST\|pole 2\|abs(2) < 6\|inside` | contour_integral_generator.py |
| `POLISH` | 1 | `POLISH\|ACpKrpArAqq` | wff_parsing_generator.py |
| `POLLARD_FACTOR` | 2 | `POLLARD_FACTOR\|31\|19` | pollard_factorization_generator.py |
| `POLLARD_PM1_SETUP` | 3 | `POLLARD_PM1_SETUP\|n=589\|base=2\|B=6` | pollard_factorization_generator.py |
| `POLLARD_RHO_SETUP` | 3 | `POLLARD_RHO_SETUP\|n=391\|c=5\|x0=4` | pollard_factorization_generator.py |
| `POLYDIV_SETUP` | 2 | `POLYDIV_SETUP\|x^3 + 5x^2 + 8x - 4\|x + 1` | finite_field_generator.py, polynomial_long_division_generator.py |
| `POLY_ACCUM` | 2 | `POLY_ACCUM\|x^0\|1` | finite_field_generator.py |
| `POLY_ADD_START` | 1 | `POLY_ADD_START\|max degree 2` | finite_field_generator.py |
| `POLY_COEFF` | 3 | `POLY_COEFF\|sum\|x^0\|2` | finite_field_generator.py |
| `POLY_COMBINE` | 1 | `POLY_COMBINE\|x^3 + 9x^2 - 7x + 1` | multiplying_binomials_generator.py, polynomial_add_sub_generator.py |
| `POLY_DIST_NEG` | 1 | `POLY_DIST_NEG\|Distribute negative sign to second polynomial` | polynomial_add_sub_generator.py |
| `POLY_DIV_SETUP` | 1 | `POLY_DIV_SETUP\|(x^5 + x^4 + 5x^3) / (x^2)` | polynomial_div_monomial_generator.py |
| `POLY_DIV_SPLIT` | 1 | `POLY_DIV_SPLIT\|(x^5) / (x^2) + (x^4) / (x^2) + (5x^3) / (x^2)` | polynomial_div_monomial_generator.py |
| `POLY_FORMULA` | 1 | `POLY_FORMULA\|A = (1/2)·a·P` | regular_polygon_area_generator.py |
| `POLY_GROUP_LIKE` | 1 | `POLY_GROUP_LIKE\|(-3x^3 +4x^3) + (x^2 +8x^2) + (-7x) + (1)` | multiplying_polynomials_generator.py, polynomial_add_sub_generator.py |
| `POLY_INPUT` | 2 | `POLY_INPUT\|f(x)\|x^2 + 4x + 1` | finite_field_generator.py |
| `POLY_MULT_SETUP` | 1 | `POLY_MULT_SETUP\|(-4x - 3)(-2x^2 + 2x + 5)` | multiplying_polynomials_generator.py |
| `POLY_MUL_START` | 2 | `POLY_MUL_START\|degree 2\|degree 2` | finite_field_generator.py |
| `POLY_REMAINDER` | 1 | `POLY_REMAINDER\|x^4 + x^2 + x + 1` | finite_field_generator.py |
| `POLY_SCALE` | 3 | `POLY_SCALE\|x^3 - 3x/5\|5/2\|(5x^3 - 3x)/2` | legendre_construction_generator.py |
| `POLY_SETUP` | 1, 2 | `POLY_SETUP\|(-3x^3 + x^2) - (-4x^3 - 8x^2 + 7x - 1)` | factor_gcf_generator.py, factor_grouping_generator.py, factor_special_forms_generator.py, factor_trinomial_generator.py, polynomial_add_sub_generator.py, rational_expr_add_sub_generator.py, rational_expr_mult_div_generator.py, rational_expr_simplify_generator.py, regular_polygon_area_generator.py |
| `POLY_SUB` | 2, 3 | `POLY_SUB\|(x^3 + 5x^2) - (x^3 + x^2)\|4x^2` | legendre_construction_generator.py, polynomial_long_division_generator.py |
| `PORT_FORMULA` | 2 | `PORT_FORMULA\|E=wA*rA+wB*rB\|Var=wA^2*varA+wB^2*varB+2*wA*wB*cov` | portfolio_generator.py |
| `PORT_RESULT` | 2 | `PORT_RESULT\|expected_return=0.125\|variance=0.0225` | portfolio_generator.py |
| `PORT_SETUP` | 3 | `PORT_SETUP\|wA=0.25,wB=0.75\|rA=8%,rB=14%\|varA=0.09,varB=0.0225,cov=0.01125` | portfolio_generator.py |
| `POSTERIOR_PARAM` | 1 | `POSTERIOR_PARAM\|alpha' = alpha + successes` | bayesian_update_generator.py |
| `POST_PRECISION` | 1 | `POST_PRECISION\|prior precision + data precision` | bayesian_update_generator.py |
| `POTENTIAL_BUILD` | 3 | `POTENTIAL_BUILD\|integrate P dx\|2*x^2 + 4*x*y - x + g(y)\|g'(y) remains` | exact_ode_generator.py, line_integral_generator.py |
| `POTENTIAL_RESULT` | 2 | `POTENTIAL_RESULT\|phi(x,y)\|2*x^2 + 2*y^2 + 4*x*y - x - 3*y` | exact_ode_generator.py, line_integral_generator.py |
| `POW` | 2 | `POW\|(7/10)^3\|0.343` | binomial_probability_generator.py, geometric_distribution_generator.py, recurrence_generator.py |
| `POWER_ENTRY` | 3 | `POWER_ENTRY\|(1,1)\|(-216)\|-216` | diagonalization_generator.py |
| `POWER_FORM` | 1 | `POWER_FORM\|A^3 = P*D^3*P^-1` | diagonalization_generator.py |
| `POWER_INTEGRAL` | 2 | `POWER_INTEGRAL\|int_0^a x dx\|a^2/2` | continuous_distribution_generator.py, wavefunction_generator.py |
| `POWER_REDUCE` | 2 | `POWER_REDUCE\|41^181\|41^1 mod 42` | totient_generator.py |
| `POWER_RULE` | 2 | `POWER_RULE\|4x^5\|20x^4` | chain_rule_generator.py, commutator_generator.py, curve_analysis_generator.py, derivative_power_rule_generator.py, derivative_product_quotient_generator.py, derivative_transcendental_generator.py, lhopital_generator.py, linear_approx_generator.py, log_diff_higher_order_generator.py, mean_value_theorem_generator.py, optimization_generator.py, tangent_line_generator.py |
| `POWER_SETUP` | 2 | `POWER_SETUP\|(cos 241 deg + i sin 241 deg)^(6i)\|principal logarithm` | complex_log_generator.py |
| `POWER_SET_RESULT` | 1 | `POWER_SET_RESULT\|{∅, {a}, {k}, {a, k}}` | set_operations_generator.py |
| `POWER_SHIFT` | 3 | `POWER_SHIFT\|k=0\|0-3\|-3` | laurent_series_generator.py |
| `PREDICT` | 2 | `PREDICT\|x*\|68/15` | kernel_ridge_generator.py |
| `PREIMAGE` | 2 | `PREIMAGE\|16\|∅` | function_properties_generator.py |
| `PREMISES_ALL_T` | 2 | `PREMISES_ALL_T\|q=T, r=T, s=T\|no` | argument_form_generator.py |
| `PRIME` | 1 | `PRIME\|41` | divisibility_classification_generator.py |
| `PRIM_CANDIDATES` | 2 | `PRIM_CANDIDATES\|visited A\|AB=2, AD=5, AC=12, AF=23` | mst_generator.py |
| `PRIM_START` | 1 | `PRIM_START\|A` | mst_generator.py |
| `PRINCIPAL_LOG` | 1 | `PRINCIPAL_LOG\|ln(36/7) - i*pi/9` | complex_log_generator.py |
| `PRINCIPAL_MINOR` | 2 | `PRINCIPAL_MINOR\|K11\|3` | kernel_validity_generator.py |
| `PRIOR_PRECISION` | 1 | `PRIOR_PRECISION\|1/tau^2` | bayesian_update_generator.py |
| `PROBABILITY` | 2 | `PROBABILITY\|P(+z)\|225/12769` | spin_half_generator.py |
| `PROB_CONDITIONAL` | 2 | `PROB_CONDITIONAL\|P(blue given first was blue)\|6/15` | compound_probability_generator.py |
| `PROB_DEPENDENT` | 1 | `PROB_DEPENDENT\|Drawing without replacement means dependent events` | compound_probability_generator.py |
| `PROB_DESCRIBE` | 1 | `PROB_DESCRIBE\|Coin and d12: tails, then 3` | compound_probability_generator.py |
| `PROB_IDENTIFY` | 2 | `PROB_IDENTIFY\|P(tails)\|1/2` | compound_probability_generator.py |
| `PROB_INDEPENDENT` | 1 | `PROB_INDEPENDENT\|The coin flip and die roll are independent events` | compound_probability_generator.py |
| `PROB_MULTIPLY` | 3 | `PROB_MULTIPLY\|1/2\|1/12\|1/24` | compound_probability_generator.py |
| `PROB_SETUP` | 2 | `PROB_SETUP\|5\|128` | simple_probability_generator.py |
| `PROB_SIMPLIFY` | 2 | `PROB_SIMPLIFY\|42/240\|7/40` | compound_probability_generator.py |
| `PROB_WEIGHT` | 2 | `PROB_WEIGHT\|0^2\|0` | clebsch_gordan_generator.py |
| `PRODUCT` | 2 | `PRODUCT\|Delta x^2 * Delta p^2\|16900pi^2/12 - 1/2` | uncertainty_generator.py |
| `PROJECT` | 2 | `PROJECT\|P1\|0` | pca_generator.py |
| `PROJECTILE_SETUP` | 3 | `PROJECTILE_SETUP\|vx=15\|vy=20\|g=10` | projectile_motion_generator.py |
| `PROJECTION` | 2 | `PROJECTION\|X*beta\|[4, 6, 8, 10]` | least_squares_generator.py, legendre_construction_generator.py |
| `PROJECTOR_SETUP` | 2 | `PROJECTOR_SETUP\|v=(16/65, 63/65)\|P=vv^T=[[256/4225,1008/4225],[1008/4225,3969/4225]]` | projector_generator.py |
| `PROJ_COEFF` | 3 | `PROJ_COEFF\|v2 on u1\|-24/8\|-3` | gram_schmidt_generator.py |
| `PROJ_VECTOR` | 2 | `PROJ_VECTOR\|-3*u1\|[-6, 0, -6]` | gram_schmidt_generator.py |
| `PROPERTY_MATCH` | 3 | `PROPERTY_MATCH\|multiplicative identity property\|a × 1 = a\|5771 × 1` | operation_properties_generator.py |
| `PROPERTY_RESULT` | 2 | `PROPERTY_RESULT\|reflexive\|yes` | relation_check_generator.py |
| `PROP_SETUP` | 1 | `PROP_SETUP\|2/2 = x/3` | proportion_word_problem_generator.py, proportional_relationship_generator.py, similar_triangles_generator.py, triangle_solve_generator.py |
| `PSD_SETUP` | 2 | `PSD_SETUP\|K=[[3,0], [0,1]]\|criterion=all principal minors >= 0` | kernel_validity_generator.py |
| `PURITY` | 1 | `PURITY\|Tr(rho^2)=145/169` | density_matrix_generator.py |
| `PYTHAG_CALCULATE` | 2 | `PYTHAG_CALCULATE\|h² = 13456 - 6400 = 7056\|7056` | pythag_leg_generator.py |
| `PYTHAG_CONTEXT` | 3 | `PYTHAG_CONTEXT\|ladder\|ladder=116ft, given=80ft\|diagram=WTH` | pythag_leg_generator.py |
| `PYTHAG_FORMULA` | 1 | `PYTHAG_FORMULA\|a² + b² = c²` | pythag_hyp_generator.py, pythag_leg_generator.py |
| `PYTHAG_MODEL` | 3 | `PYTHAG_MODEL\|ground=80\|wall=?\|ladder=116` | pythag_leg_generator.py |
| `PYTHAG_ROOT` | 2 | `PYTHAG_ROOT\|705600\|840` | pythag_leg_generator.py |
| `PYTHAG_SETUP` | 2, 3 | `PYTHAG_SETUP\|legs=336,385\|hypotenuse QS=?` | pythag_hyp_generator.py, pythag_leg_generator.py |
| `PYTHAG_SOLVE` | 2 | `PYTHAG_SOLVE\|b² = 1758276 - 1052676\|705600` | pythag_leg_generator.py |
| `PYTHAG_SQUARE` | 2 | `PYTHAG_SQUARE\|1026\|1052676` | pythag_leg_generator.py |
| `PYTHAG_SUBSTITUTE` | 1 | `PYTHAG_SUBSTITUTE\|1026² + b² = 1326²` | pythag_leg_generator.py |
| `Q1` | 4 | `Q1\|-117\|117\|26\|0` | complex_quadratic_generator.py, polynomial_zeros_generator.py, quadratic_generator.py |
| `Q2` | 4 | `Q2\|-117\|117\|26\|-9` | complex_quadratic_generator.py, polynomial_zeros_generator.py, quadratic_generator.py |
| `QN_ADD` | 4 | `QN_ADD\|Q\|left\|0 + e-(-1)\|-1` | conservation_law_generator.py |
| `QR_ENTRY` | 2 | `QR_ENTRY\|q1\|[1, 0, 0]` | qr_decomposition_generator.py |
| `QR_SETUP` | 2 | `QR_SETUP\|A = [[2, -5, 2], [0, 5, -4], [0, 0, 1]]\|Gram-Schmidt columns` | qr_decomposition_generator.py |
| `QUADRANT` | 2 | `QUADRANT\|7°\|quadrant I` | angle_measure_generator.py, polar_parametric_generator.py, unit_circle_generator.py |
| `QUADRATIC` | 3 | `QUADRATIC\|3\|18\|24` | mobius_transform_generator.py |
| `QUANTUM_FORMULA` | 1 | `QUANTUM_FORMULA\|Delta_lambda=h/(m*c)*(1-cos(theta))` | quantum_formula_generator.py |
| `QUANTUM_SETUP` | 2, 3 | `QUANTUM_SETUP\|gate=Y\|input=e^(i402π/269)·ket0` | quantum_formula_generator.py, quantum_gate_generator.py |
| `QUANT_SETUP` | 3 | `QUANT_SETUP\|x=(4/5,29/100,-81/100)\|scale=1/20\|zero_point=-7` | quantization_generator.py |
| `QUANT_VALUE` | 2 | `QUANT_VALUE\|1\|9` | quantization_generator.py |
| `QUARK_CHARGE` | 2 | `QUARK_CHARGE\|anti_u\|-2/3` | quark_composition_generator.py |
| `QUARK_SETUP` | 3 | `QUARK_SETUP\|antibaryon,count=801\|anti_u anti_b anti_d\|u=2/3,d=-1/3,s=-1/3,c=2/3,b=-1/3; anti=-charge` | quark_composition_generator.py |
| `QUARTILE` | 3 | `QUARTILE\|Q1\|5,8,12,12,13\|12` | five_number_summary_generator.py |
| `QUAT_COMPONENT` | 3 | `QUAT_COMPONENT\|q*v\|real\|-2` | quaternion_generator.py |
| `QUAT_INVERSE` | 2 | `QUAT_INVERSE\|q\|(0,-1,0,0)` | quaternion_generator.py |
| `QUAT_MUL_START` | 3 | `QUAT_MUL_START\|q*v\|q\|v` | quaternion_generator.py |
| `QUAT_RESULT` | 2 | `QUAT_RESULT\|q*v\|(-2,0,-1,1)` | quaternion_generator.py |
| `QUAT_SETUP` | 2 | `QUAT_SETUP\|q=(0,1,0,0)\|v=(0,2,1,1)` | quaternion_generator.py |
| `QUEUE_STATE` | 2 | `QUEUE_STATE\|initial\|A` | graph_traversal_generator.py |
| `QUOTIENT` | 1 | `QUOTIENT\|x^3 + x^2` | finite_field_generator.py |
| `Q_EXPR` | 1 | `Q_EXPR\|Q = [B]/[A]` | equilibrium_ice_generator.py |
| `R` | 1 | `R\|21` | complex_number_ops_generator.py, finite_field_generator.py, long_division_generator.py, polynomial_long_division_generator.py, polynomial_zeros_generator.py, synthetic_division_generator.py |
| `RANGE` | 1 | `RANGE\|{10, 11, 19, 25}` | relation_operations_generator.py |
| `RAPIDITY_SUM` | 2 | `RAPIDITY_SUM\|collinear boosts\|11/6` | minkowski_interval_generator.py |
| `RATE_MONTHLY` | 2 | `RATE_MONTHLY\|24% / 12\|0.02` | finance_generator.py |
| `RATE_SETUP` | 2 | `RATE_SETUP\|circle: dr/dt = 4 m/s; r = 35 m\|dA/dt` | related_rates_generator.py |
| `RATIO` | 2, 3 | `RATIO\|y = 2*x\|y = 2*x` | lagrange_multiplier_generator.py, simplex_generator.py |
| `RATIONALIZE` | 1 | `RATIONALIZE\|(17 - √53)/(17 - √53)` | dot_product_generator.py, limit_evaluation_generator.py, radical_rationalize_generator.py, special_right_triangle_generator.py |
| `RATIO_BASE` | 3 | `RATIO_BASE\|7:4\|1\|7:4` | error_spotting_generator.py, fill_in_step_generator.py, ratio_table_generator.py |
| `RATIO_TABLE` | 2 | `RATIO_TABLE\|Distance (miles): 7, 14, 56, 77\|Time (hours): 4, 8, 32, ?` | error_spotting_generator.py, fill_in_step_generator.py, ratio_table_generator.py |
| `RAW_FORMULA` | 1 | `RAW_FORMULA\|x = μ + z·σ` | z_score_generator.py |
| `REARRANGE_EQ` | 1 | `REARRANGE_EQ\|whole = 2408 / 1.505` | percent_problem_generator.py |
| `RECIPROCAL` | 2 | `RECIPROCAL\|csc θ = 1/sin θ\|25/24` | trig_six_functions_generator.py |
| `RECOVER_DATA` | 2 | `RECOVER_DATA\|positions 3,5,6,7\|1100` | hamming_code_generator.py |
| `RECT_FORM` | 1 | `RECT_FORM\|20` | de_moivre_generator.py, euler_formula_generator.py |
| `RECUR` | 3 | `RECUR\|6P_6 = 11x P_5 - 5P_4\|P_5 = (63x^5 - 70x^3 + 15x)/8\|P_4 = (35x^4 - 30x^2 + 3)/8` | legendre_construction_generator.py |
| `RECURRENCE` | 2 | `RECURRENCE\|a_(n+1)\|-2a_n/(n+1)` | derangement_generator.py, series_solution_generator.py |
| `REC_SETUP` | 1, 2 | `REC_SETUP\|a_n = -5 a_(n-1) - 6 a_(n-2)\|a_0 = -2, a_1 = 5` | master_theorem_generator.py, recurrence_generator.py |
| `REDUCED_DENSITY` | 1 | `REDUCED_DENSITY\|rho_A=[[1/2,e^(-i195π/112)/2],[e^(i195π/112)/2,1/2]]` | partial_trace_generator.py |
| `REFLEXIVE_CHECK` | 2 | `REFLEXIVE_CHECK\|(19, 19)\|present` | equivalence_relation_generator.py, relation_check_generator.py |
| `REGEX_ACCEPT` | 1 | `REGEX_ACCEPT\|q20210_3, q20210_4` | regex_to_automaton_generator.py |
| `REGEX_SETUP` | 3 | `REGEX_SETUP\|(a or b)*(ab or ba)\|alphabet a,b\|canonical progress DFA` | regex_to_automaton_generator.py |
| `REGEX_STATE` | 2 | `REGEX_STATE\|q20210_0\|start` | regex_to_automaton_generator.py |
| `REGEX_TRANSITION` | 3 | `REGEX_TRANSITION\|q20210_0\|a\|q20210_1` | regex_to_automaton_generator.py |
| `REGION` | 2 | `REGION\|both\|{17, 19, 25}` | attribute_sorting_generator.py, venn_region_count_generator.py |
| `REGION_EQ` | 2 | `REGION_EQ\|A ∩ B ∩ C\|1` | venn_region_count_generator.py |
| `REGION_MEASURE` | 3 | `REGION_MEASURE\|area\|5*9\|45` | vector_theorem_generator.py |
| `REGION_REWRITE` | 2 | `REGION_REWRITE\|0 <= y <= 40\|y/5 <= x <= 8` | double_integral_generator.py |
| `REG_ROW` | 3 | `REG_ROW\|x-x̄=-2\|y-ȳ=0\|product=0` | regression_generator.py |
| `REG_SETUP` | 2 | `REG_SETUP\|points: (1, 73), (2, 74), (3, 75), (4, 72), (5, 71)\|correlation coefficient r` | regression_generator.py |
| `REJECT` | 1, 2 | `REJECT\|x = −45` | conditional_forms_generator.py, counterexample_search_generator.py, factor_trinomial_generator.py, knights_knaves_generator.py, log_conversion_generator.py, log_equation_generator.py, optimization_generator.py, polynomial_inequality_generator.py, radical_equation_generator.py, rational_equation_generator.py, rational_root_generator.py, set_builder_roster_generator.py |
| `RELAX` | 3 | `RELAX\|A->B\|update inf to 3\|via weight 3` | dijkstra_generator.py |
| `RELU` | 3 | `RELU\|z=2\|h=2\|deriv=1` | backprop_generator.py |
| `REL_ENERGY_FORMULA` | 1 | `REL_ENERGY_FORMULA\|E=sqrt(p^2+m^2)` | relativistic_energy_generator.py |
| `REL_ENERGY_SETUP` | 3 | `REL_ENERGY_SETUP\|energy_momentum\|c=1\|p=15, m=8` | relativistic_energy_generator.py |
| `REL_FORMULA` | 1 | `REL_FORMULA\|ct_prime=gamma*(ct-beta*x), x_prime=gamma*(x-beta*ct)` | special_relativity_generator.py |
| `REL_PAIR` | 2 | `REL_PAIR\|(2, 2)\|same block` | equivalence_relation_generator.py |
| `REL_SETUP` | 2, 3 | `REL_SETUP\|A = {19, 28, 37}\|R = {(19, 19), (28, 28), (37, 37)}` | equivalence_relation_generator.py, relation_check_generator.py, relation_closure_generator.py, relation_operations_generator.py, special_relativity_generator.py |
| `REPEAT_DETECT` | 2 | `REPEAT_DETECT\|remainder 52 repeats\|repetend 228070175438596491` | repeating_decimal_generator.py |
| `REPRESENT` | 2 | `REPRESENT\|s ∣ v\|v = sm` | direct_proof_algebra_generator.py |
| `REP_DIM` | 2 | `REP_DIM\|6bar\|6` | young_tableaux_generator.py |
| `RESIDUAL` | 2 | `RESIDUAL\|y - X*beta\|[-3, 3, 3, -3]` | least_squares_generator.py |
| `RESIDUE` | 1, 3 | `RESIDUE\|1` | contour_integral_generator.py, residue_generator.py |
| `RESIDUE_SETUP` | 2 | `RESIDUE_SETUP\|a=-4\|f=1/(z+4) + 3 + (z+4)` | residue_generator.py |
| `RESIDUE_SUM` | 1 | `RESIDUE_SUM\|-4` | contour_integral_generator.py |
| `RESID_SETUP` | 2 | `RESID_SETUP\|point (5, 30), line ŷ = 31.3 - 0.1x\|residual = observed − predicted` | regression_generator.py |
| `RESOLVE` | 3 | `RESOLVE\|C1\|C2\|P2441` | resolution_proof_generator.py |
| `RESTRICT_CHECK` | 3 | `RESTRICT_CHECK\|(m, 5)\|m in D=yes\|keep` | relation_operations_generator.py |
| `RES_EMPTY` | 1 | `RES_EMPTY\|C7` | resolution_proof_generator.py |
| `RES_SETUP` | 1 | `RES_SETUP\|C1=(P75705 OR P2441), C2=(not P2441), C3=(not P75705), C4=(P22733 OR P49061 OR P46599)` | resolution_proof_generator.py |
| `RES_SKIP` | 3 | `RES_SKIP\|C1\|C2\|(P75705)` | resolution_proof_generator.py |
| `REVERSE` | 2 | `REVERSE\|0,1,0,0,1,0,1,1\|11010010` | base_arithmetic_generator.py, base_conversion_generator.py, bitwise_ops_generator.py |
| `REWRITE` | 1, 2 | `REWRITE\|5771 × 1\|5771` | antiderivative_generator.py, arc_length_generator.py, area_between_curves_generator.py, chain_rule_generator.py, circle_equation_generator.py, completing_square_generator.py, complex_division_generator.py, complex_log_generator.py, complex_number_ops_generator.py, complex_quadratic_generator.py, confidence_interval_generator.py, conic_standard_form_generator.py, cramers_rule_generator.py, curve_analysis_generator.py, definite_integral_generator.py, derivative_limit_def_generator.py, derivative_power_rule_generator.py, derivative_product_quotient_generator.py, derivative_transcendental_generator.py, domain_range_generator.py, dot_product_generator.py, euler_formula_generator.py, evaluate_expression_generator.py, exponent_generator.py, exponent_mixed_rules_generator.py, exponential_equation_generator.py, factor_gcf_generator.py, factor_grouping_generator.py, factor_special_forms_generator.py, factor_trinomial_generator.py, frequency_table_generator.py, function_composition_generator.py, function_operations_generator.py, horner_evaluation_generator.py, implicit_diff_generator.py, improper_integral_generator.py, induction_verify_generator.py, integrating_factor_generator.py, integration_by_parts_generator.py, inverse_function_generator.py, lambda_reduction_generator.py, laurent_series_generator.py, lhopital_generator.py, limit_evaluation_generator.py, linear_approx_generator.py, linear_complex_generator.py, linear_fractional_generator.py, literal_equation_generator.py, log_conversion_generator.py, log_diff_higher_order_generator.py, log_equation_generator.py, log_properties_generator.py, logical_equivalence_laws_generator.py, logistic_growth_generator.py, master_theorem_generator.py, matrix_inverse_generator.py, method_of_moments_generator.py, mgf_generator.py, midpoint_generator.py, mle_generator.py, normal_table_generator.py, ode_substitution_generator.py, operation_properties_generator.py, optimization_generator.py, order_of_operations_generator.py, parametric_calculus_generator.py, partial_fractions_generator.py, permutation_combination_generator.py, polar_parametric_generator.py, polynomial_zeros_generator.py, power_series_generator.py, quadratic_factoring_generator.py, radical_add_sub_generator.py, radical_equation_generator.py, radical_multiply_generator.py, radical_rationalize_generator.py, radical_variable_simplify_generator.py, rational_equation_generator.py, rational_exponent_generator.py, rational_expr_add_sub_generator.py, rational_expr_mult_div_generator.py, rational_expr_simplify_generator.py, rational_function_features_generator.py, recursive_explicit_generator.py, regression_generator.py, related_rates_generator.py, right_triangle_trig_generator.py, row_reduction_generator.py, separable_ode_generator.py, separable_pde_generator.py, series_convergence_generator.py, series_solution_generator.py, set_algebra_laws_generator.py, set_expression_generator.py, set_operations_generator.py, simplify_expression_generator.py, sinusoid_features_generator.py, solid_revolution_generator.py, special_right_triangle_generator.py, special_solution_equation_generator.py, spin_half_generator.py, standard_form_conversion_generator.py, stars_and_bars_generator.py, synthetic_division_generator.py, tangent_line_generator.py, taxicab_geometry_generator.py, taylor_series_generator.py, trig_equation_generator.py, trig_identity_eval_generator.py, trig_identity_verify_generator.py, trig_six_functions_generator.py, u_substitution_generator.py, vector_ops_generator.py, z_transform_generator.py |
| `RG_SETUP` | 3 | `RG_SETUP\|one_loop\|alpha0=1/12\|beta=4/3,L=4` | running_coupling_generator.py |
| `RHO_ITER` | 4 | `RHO_ITER\|1\|x=21, y=55\|abs(r)=34\|gcd=17` | pollard_factorization_generator.py |
| `RICCI_ENTRY` | 2 | `RICCI_ENTRY\|R_phiphi\|1` | riemann_tensor_generator.py |
| `RIDGE_ENTRY` | 2 | `RIDGE_ENTRY\|K\|[[9,-6], [-6,4]]` | kernel_ridge_generator.py |
| `RIEMANN_ENTRY` | 2 | `RIEMANN_ENTRY\|R^phi_theta phi theta\|144/169` | riemann_tensor_generator.py |
| `RIEMANN_SETUP` | 2, 3 | `RIEMANN_SETUP\|f(x) = x^2 on [-1, 7], n = 4\|midpoint Riemann sum` | riemann_sum_generator.py, riemann_tensor_generator.py |
| `RK_COMBINE` | 2 | `RK_COMBINE\|k1+2k2+2k3+k4\|-727/32` | runge_kutta_generator.py |
| `RK_STAGE` | 3 | `RK_STAGE\|k1\|x=1\|u=2` | runge_kutta_generator.py |
| `RODRIGUES_FORM` | 2 | `RODRIGUES_FORM\|e^(theta K)\|I + sin(theta)K + (1-cos(theta))K^2` | lie_exponential_generator.py |
| `ROOT` | 1, 2, 3 | `ROOT\|1521\|39` | ac_circuit_generator.py, adam_step_generator.py, cholesky_generator.py, completing_square_generator.py, confidence_interval_generator.py, de_moivre_generator.py, doppler_generator.py, embedding_similarity_generator.py, energy_conservation_generator.py, factor_special_forms_generator.py, four_vector_generator.py, fundamental_form_generator.py, hypothesis_test_generator.py, invariant_mass_generator.py, joint_distribution_generator.py, ladder_operator_generator.py, layer_norm_generator.py, low_rank_approx_generator.py, matrix_norm_generator.py, metric_arc_length_generator.py, or_formula_generator.py, orbital_mechanics_generator.py, planck_units_generator.py, pythag_hyp_generator.py, qr_decomposition_generator.py, quadratic_generator.py, quadratic_square_root_generator.py, radical_add_sub_generator.py, radical_multiply_generator.py, radical_rationalize_generator.py, radical_variable_simplify_generator.py, rational_equation_generator.py, rational_exponent_generator.py, regression_generator.py, relativistic_energy_generator.py, round_solids_generator.py, rv_transform_generator.py, schwarzschild_generator.py, shm_generator.py, svd_generator.py, svm_margin_generator.py, two_sample_test_generator.py |
| `ROOT_ANGLE` | 2 | `ROOT_ANGLE\|k=0\|60 deg` | de_moivre_generator.py |
| `ROOT_EXTRACT` | 2 | `ROOT_EXTRACT\|4\|√22` | exponent_generator.py |
| `ROOT_IDENTIFY` | 3 | `ROOT_IDENTIFY\|352\|16\|22` | exponent_generator.py |
| `ROOT_SETUP` | 1 | `ROOT_SETUP\|√352` | exponent_generator.py, radical_add_sub_generator.py, radical_multiply_generator.py, radical_rationalize_generator.py, radical_variable_simplify_generator.py |
| `ROOT_SIMPLIFY` | 1, 2 | `ROOT_SIMPLIFY\|4√22` | complex_quadratic_generator.py, distance_formula_generator.py, dot_product_generator.py, euler_formula_generator.py, exponent_generator.py, geometric_mean_generator.py, hypercube_counting_generator.py, polar_parametric_generator.py, vector_ops_generator.py |
| `ROSTER` | 2 | `ROSTER\|S\|∅` | set_builder_roster_generator.py |
| `ROTATED_VECTOR` | 1 | `ROTATED_VECTOR\|(2,-1,-1)` | quaternion_generator.py |
| `ROT_FORMULA` | 1 | `ROT_FORMULA\|I=I_cm+m*d^2` | rotational_dynamics_generator.py |
| `ROT_SETUP` | 3 | `ROT_SETUP\|parallel_axis\|I_cm=4, m=9\|d=1` | rotational_dynamics_generator.py |
| `ROUND` | 2 | `ROUND\|9\|9` | quantization_generator.py |
| `ROUNDTRIP_ERROR` | 2 | `ROUNDTRIP_ERROR\|sum_abs\|1/50` | quantization_generator.py |
| `ROUND_CHECK` | 3 | `ROUND_CHECK\|4\|8\|>=5` | place_value_rounding_generator.py |
| `ROUND_RESULT` | 2 | `ROUND_RESULT\|19148\|19150` | place_value_rounding_generator.py |
| `ROUTH_ROW` | 2 | `ROUTH_ROW\|s^3\|1, 9` | routh_hurwitz_generator.py |
| `ROUTH_SETUP` | 1 | `ROUTH_SETUP\|p(s)=s^3+17s^2+9s+22` | routh_hurwitz_generator.py |
| `ROW_ENTROPY` | 2 | `ROW_ENTROPY\|H0\|649/800` | entropy_rate_markov_generator.py |
| `ROW_OP` | 1, 2 | `ROW_OP\|R2 → R2 - 3·R1\|[0, 1, 0, 4]` | row_reduction_generator.py, simplex_generator.py, subspace_basis_generator.py |
| `RREF_RESULT` | 2 | `RREF_RESULT\|RREF(A)\|[[1, 0, 3, -3], [0, 1, 4, -1], [0, 0, 0, 0]]` | subspace_basis_generator.py |
| `RSA_DECRYPT` | 2 | `RSA_DECRYPT\|2\|63` | rsa_generator.py |
| `RSA_ENCRYPT` | 2 | `RSA_ENCRYPT\|63\|2` | rsa_generator.py |
| `RSA_PRIVATE_KEY` | 1 | `RSA_PRIVATE_KEY\|d=43` | rsa_generator.py |
| `RSA_PUBLIC_KEY` | 2 | `RSA_PUBLIC_KEY\|n=65\|e=19` | rsa_generator.py |
| `RSA_SETUP` | 3 | `RSA_SETUP\|p=5\|q=13\|message=63` | rsa_generator.py |
| `RSQ_FORMULA` | 1 | `RSQ_FORMULA\|r^2 = Sxy^2/(Sxx·Syy)` | regression_generator.py |
| `RS_CORRECT` | 2 | `RS_CORRECT\|position=3\|[19,68,14,2]` | reed_solomon_generator.py |
| `RS_EVAL` | 2 | `RS_EVAL\|x=10\|22` | reed_solomon_generator.py |
| `RS_LINE` | 3 | `RS_LINE\|m0=40\|m1=69\|agree=3` | reed_solomon_generator.py |
| `RS_PAIR` | 2 | `RS_PAIR\|x=10,13\|y=19,68` | reed_solomon_generator.py |
| `RS_RECEIVED` | 1 | `RS_RECEIVED\|[19,68,71,2]` | reed_solomon_generator.py |
| `RS_SETUP` | 3 | `RS_SETUP\|F_59\|m(x)=29+17x\|points 10,21,48,58` | reed_solomon_generator.py |
| `RUNNING_TOTAL` | 3 | `RUNNING_TOTAL\|0\|8\|8` | function_properties_generator.py |
| `S` | 3 | `S\|632\|594\|38` | ac_circuit_generator.py, activation_generator.py, adam_step_generator.py, angle_defect_generator.py, angle_measure_generator.py, annuity_generator.py, arc_length_generator.py, area_between_curves_generator.py, arithmetic_coding_generator.py, arithmetic_sequence_generator.py, backprop_generator.py, bayesian_update_generator.py, bec_channel_generator.py, binomial_probability_generator.py, bisection_generator.py, black_scholes_generator.py, calendar_arithmetic_generator.py, calorimetry_generator.py, casimir_force_generator.py, casimir_generator.py, channel_capacity_generator.py, cholesky_generator.py, circle_angle_generator.py, circle_equation_generator.py, collision_generator.py, commutator_generator.py, complex_locus_generator.py, complex_log_generator.py, complex_number_ops_generator.py, complex_quadratic_generator.py, composite_arithmetic_generator.py, confidence_interval_generator.py, continued_fraction_generator.py, continuous_distribution_generator.py, counting_classics_generator.py, cramers_rule_generator.py, decimal_div_generator.py, definite_integral_generator.py, density_matrix_generator.py, derangement_generator.py, determinant_generator.py, dft_generator.py, distance_formula_generator.py, doppler_generator.py, ellipse_features_generator.py, elliptic_curve_finite_field_generator.py, embedding_similarity_generator.py, entropy_generator.py, equilibrium_ice_generator.py, euler_characteristic_generator.py, euler_circuit_generator.py, euler_method_generator.py, expected_value_generator.py, exponential_model_generator.py, extended_euclid_generator.py, finance_generator.py, finite_difference_generator.py, first_law_generator.py, five_number_summary_generator.py, four_vector_generator.py, fourier_series_generator.py, fractal_iteration_generator.py, fraction_op_generator.py, function_inner_product_generator.py, function_operations_generator.py, fundamental_form_generator.py, game_theory_generator.py, gaussian_curvature_generator.py, generating_function_generator.py, geometric_distribution_generator.py, geometric_sequence_generator.py, gradient_descent_generator.py, gradient_step_generator.py, graph_interpret_generator.py, graph_traversal_generator.py, hamiltonian_generator.py, heat_engine_generator.py, hermitian_check_generator.py, hydrogen_atom_generator.py, hyperbola_features_generator.py, hyperbolic_distance_generator.py, hyperbolic_function_generator.py, hypercube_counting_generator.py, hypothesis_test_generator.py, inclusion_exclusion_generator.py, index_gymnastics_generator.py, information_gain_generator.py, integrating_factor_generator.py, interpolation_generator.py, invariant_mass_generator.py, joint_distribution_generator.py, kernel_evaluation_generator.py, kernel_ridge_generator.py, kernel_validity_generator.py, kinematics_generator.py, kmeans_step_generator.py, knn_generator.py, kraft_inequality_generator.py, ladder_operator_generator.py, lagrangian_generator.py, layer_norm_generator.py, legendre_construction_generator.py, linear_simple_generator.py, logistic_growth_generator.py, long_division_generator.py, low_rank_approx_generator.py, lp_corner_generator.py, lr_schedule_generator.py, manual_square_root_generator.py, markov_chain_generator.py, matrix_group_check_generator.py, matrix_inverse_generator.py, matrix_ops_generator.py, mean_value_theorem_generator.py, metric_arc_length_generator.py, mgf_generator.py, midpoint_generator.py, minkowski_interval_generator.py, mixed_number_operation_generator.py, mle_generator.py, mobius_transform_generator.py, modular_inverse_generator.py, mutual_information_generator.py, naive_bayes_generator.py, named_distribution_generator.py, newton_raphson_generator.py, newtons_laws_generator.py, normal_table_generator.py, npv_irr_generator.py, ode_substitution_generator.py, ode_system_generator.py, optics_generator.py, optimization_generator.py, or_formula_generator.py, order_of_operations_generator.py, order_statistics_generator.py, parabola_features_generator.py, parametric_calculus_generator.py, particle_in_box_generator.py, pca_generator.py, percent_problem_generator.py, percent_word_problem_generator.py, permutation_group_generator.py, ph_calculation_generator.py, piecewise_evaluation_generator.py, polar_parametric_generator.py, pollard_factorization_generator.py, positive_definite_generator.py, probability_addition_rule_generator.py, quadratic_residue_generator.py, quantization_generator.py, quantum_formula_generator.py, quaternion_generator.py, radical_add_sub_generator.py, radical_rationalize_generator.py, rational_expr_add_sub_generator.py, recurrence_generator.py, regression_generator.py, related_rates_generator.py, riemann_sum_generator.py, riemann_tensor_generator.py, rotational_dynamics_generator.py, routh_hurwitz_generator.py, row_reduction_generator.py, rsa_generator.py, runge_kutta_generator.py, rv_transform_generator.py, schwarzschild_generator.py, second_order_ode_generator.py, segment_partition_generator.py, separable_pde_generator.py, series_convergence_generator.py, set_counting_generator.py, shm_generator.py, signal_arithmetic_generator.py, slope_two_points_generator.py, softmax_gradient_generator.py, solid_revolution_generator.py, special_relativity_generator.py, spherical_excess_generator.py, spin_half_generator.py, standing_wave_generator.py, stars_and_bars_generator.py, statics_generator.py, stereographic_generator.py, taxicab_geometry_generator.py, taylor_series_generator.py, telescoping_generator.py, temperature_conversion_generator.py, tip_bill_split_generator.py, totient_generator.py, transformation_generator.py, transportation_generator.py, triangle_solve_generator.py, trig_identity_eval_generator.py, trig_six_functions_generator.py, two_sample_test_generator.py, undetermined_coeff_generator.py, unit_circle_generator.py, vector_ops_generator.py, venn_region_count_generator.py, z_score_generator.py |
| `SAMPLE_MOMENT` | 2 | `SAMPLE_MOMENT\|xbar\|11/2` | method_of_moments_generator.py |
| `SAMPLE_SIZE_FORMULA` | 1 | `SAMPLE_SIZE_FORMULA\|n = (z*/E)^2·p̂(1-p̂)` | confidence_interval_generator.py |
| `SA_BASES` | 2 | `SA_BASES\|2π(33)² = 2π × 1089\|2178π` | volume_3d_generator.py |
| `SA_FACES` | 3 | `SA_FACES\|top/bottom\|9 × 11\|99` | volume_3d_generator.py |
| `SA_FORMULA` | 1 | `SA_FORMULA\|SA = 2(lw + lh + wh)` | round_solids_generator.py, volume_3d_generator.py |
| `SA_LATERAL` | 2 | `SA_LATERAL\|2π × 33 × 60\|3960π` | volume_3d_generator.py |
| `SA_SETUP` | 2 | `SA_SETUP\|rectangular_prism\|l=9, w=11, h=7` | volume_3d_generator.py |
| `SA_TOTAL` | 2 | `SA_TOTAL\|SA = 2(99 + 63 + 77)\|478` | round_solids_generator.py, volume_3d_generator.py |
| `SB_FORMULA` | 1 | `SB_FORMULA\|C(n-1, k-1)` | stars_and_bars_generator.py |
| `SB_SETUP` | 2 | `SB_SETUP\|x1+...+x4 = 31\|xi >= 1` | stars_and_bars_generator.py |
| `SCALE_DIV` | 3 | `SCALE_DIV\|1344\|28\|48` | scaling_generator.py |
| `SCALE_EXACT` | 2 | `SCALE_EXACT\|20*cos\|20` | de_moivre_generator.py, euler_formula_generator.py |
| `SCALE_IDENTIFY` | 2 | `SCALE_IDENTIFY\|9 inches\|actual_dimension` | scaling_generator.py |
| `SCALE_MODE` | 3 | `SCALE_MODE\|λ = -7\|(-343)*(-61)\|20923` | diagonalization_generator.py |
| `SCALE_MULT` | 3 | `SCALE_MULT\|9\|99\|891` | scaling_generator.py |
| `SCALE_SETUP` | 3 | `SCALE_SETUP\|1 inch\|99 feet\|99` | scaling_generator.py |
| `SCALE_SHIFT` | 2 | `SCALE_SHIFT\|1\|-6` | layer_norm_generator.py |
| `SCALING_COMPUTE` | 2 | `SCALING_COMPUTE\|6ND\|20790000000000000000` | scaling_law_generator.py |
| `SCALING_SETUP` | 3 | `SCALING_SETUP\|N=45000000\|D=77000000000\|F=38000000000000000` | scaling_law_generator.py |
| `SCAN` | 2 | `SCAN\|(\|parenthesis depth 1` | wff_parsing_generator.py |
| `SCHWARZSCHILD_SETUP` | 3, 4 | `SCHWARZSCHILD_SETUP\|radius\|G=4\|M=52\|c=2` | schwarzschild_generator.py |
| `SCI_IDENTIFY` | 2 | `SCI_IDENTIFY\|2.57\|7` | exponent_generator.py |
| `SCI_MOVE_DECIMAL` | 2 | `SCI_MOVE_DECIMAL\|left\|7` | exponent_generator.py |
| `SCI_OPERATION` | 4 | `SCI_OPERATION\|multiply_coefficients\|7.4\|9\|66.6` | exponent_generator.py |
| `SCI_SETUP` | 1 | `SCI_SETUP\|25700000` | exponent_generator.py |
| `SCORE_EQ` | 1 | `SCORE_EQ\|29-9*mu=0` | mle_generator.py |
| `SEARCH_BOUNDS` | 3 | `SEARCH_BOUNDS\|iter 1\|lo=0\|hi=7` | algorithm_trace_generator.py |
| `SEARCH_STATE` | 2 | `SEARCH_STATE\|lo=4\|hi=7` | algorithm_trace_generator.py |
| `SECOND_DERIV_TEST` | 2 | `SECOND_DERIV_TEST\|f''(-3) = -24 < 0\|local maximum at x = -3` | curve_analysis_generator.py, optimization_generator.py |
| `SECOND_PARTIAL` | 2 | `SECOND_PARTIAL\|f_xx\|8` | hessian_classify_generator.py |
| `SECTION_FORMULA` | 1 | `SECTION_FORMULA\|P = (x1 + m/(m+n)·(x2 - x1), y1 + m/(m+n)·(y2 - y1))` | segment_partition_generator.py |
| `SECTION_SETUP` | 2 | `SECTION_SETUP\|A(3, 5), B(21, 17); ratio 4:2 from A\|point P` | segment_partition_generator.py |
| `SECTOR_FORMULA` | 1 | `SECTOR_FORMULA\|A = (1/2)r^2θ` | arc_sector_generator.py |
| `SELECT_MIN` | 2 | `SELECT_MIN\|A\|0` | dijkstra_generator.py |
| `SELECT_RELEVANT` | 2 | `SELECT_RELEVANT\|base = 47, rate = 15%\|ignore 44 (irrelevant)` | percent_word_problem_generator.py, proportion_word_problem_generator.py |
| `SEPARATE` | 1, 2 | `SEPARATE\|y^2 dy = x^2 dx` | ode_substitution_generator.py, separable_ode_generator.py, separable_pde_generator.py |
| `SEQ_APPLY` | 1 | `SEQ_APPLY\|55 = 7 + (n - 1)·3` | arithmetic_sequence_generator.py, geometric_sequence_generator.py, recursive_explicit_generator.py |
| `SEQ_FORMULA` | 1 | `SEQ_FORMULA\|a_n = a_1 + (n - 1)d` | arithmetic_sequence_generator.py, geometric_sequence_generator.py, recursive_explicit_generator.py |
| `SEQ_SETUP` | 2 | `SEQ_SETUP\|7, 10, 13, 16, ...\|which term equals 55` | arithmetic_sequence_generator.py, geometric_sequence_generator.py, recursive_explicit_generator.py |
| `SERIES` | 1 | `SERIES\|G=G1*G2` | transfer_function_generator.py |
| `SERIES_ASSUME` | 2 | `SERIES_ASSUME\|y\|sum a_n x^n` | series_solution_generator.py |
| `SERIES_GROUP` | 2 | `SERIES_GROUP\|even powers\|cos(theta)I` | lie_exponential_generator.py |
| `SERIES_SETUP` | 2 | `SERIES_SETUP\|Σ 1/n^(17/5), n ≥ 1\|converge or diverge?` | legendre_construction_generator.py, power_series_generator.py, series_convergence_generator.py |
| `SERIES_TERM` | 3 | `SERIES_TERM\|n=0\|1\|1` | grassmann_generator.py |
| `SETUP` | 1 | `SETUP\|assume w is even or k is even; show wk is even` | direct_proof_algebra_generator.py |
| `SETUP_PERCENT_EQ` | 1 | `SETUP_PERCENT_EQ\|part = 1.845 * 485` | percent_problem_generator.py |
| `SET_SETUP` | 2, 3, 4 | `SET_SETUP\|A = {5, 6, 23, 26}\|B = {3, 17, 18}\|C = {7, 13, 24, 28, 31, 40}` | set_expression_generator.py, set_operations_generator.py |
| `SET_SIDE` | 2 | `SET_SIDE\|left\|∅` | counterexample_search_generator.py |
| `SHIFT` | 1, 2 | `SHIFT\|yi = xi - 1\|y1+...+y4 = 27` | algorithm_trace_generator.py, recurrence_generator.py, stars_and_bars_generator.py, z_transform_generator.py |
| `SHM_FORMULA` | 1 | `SHM_FORMULA\|omega^2=g/L` | shm_generator.py |
| `SHM_SETUP` | 3 | `SHM_SETUP\|pendulum_period\|g=10\|L=10` | shm_generator.py |
| `SHORTEST` | 2 | `SHORTEST\|(6,-2)\|norm^2=40` | lll_reduction_generator.py |
| `SIDE` | 2 | `SIDE\|left\|∈` | set_identity_membership_table_generator.py |
| `SIGFIG_ROUND` | 3 | `SIGFIG_ROUND\|4500000\|2 significant figures\|4.5 × 10^6` | fermi_estimation_generator.py |
| `SIGMA_EXPAND` | 1 | `SIGMA_EXPAND\|12 + 48 + 192 + 768` | sigma_notation_generator.py |
| `SIGMA_SETUP` | 2 | `SIGMA_SETUP\|Σ_(k=1)^(4) 3·4^k\|expand and evaluate` | sigma_notation_generator.py |
| `SIGMA_TERM` | 3 | `SIGMA_TERM\|k=1\|3·4^1\|12` | sigma_notation_generator.py |
| `SIGN` | 3 | `SIGN\|left\|-1\|negative` | bisection_generator.py |
| `SIGNAL_SETUP` | 2, 3 | `SIGNAL_SETUP\|sampling\|f_max=1432 Hz\|f_s=4454 Hz` | signal_arithmetic_generator.py |
| `SIGN_CHART` | 2 | `SIGN_CHART\|zeros\|2, 3` | polynomial_inequality_generator.py |
| `SIGN_RULE` | 2 | `SIGN_RULE\|arctan of a negative\|negative angle` | trig_equation_generator.py, trig_identity_eval_generator.py, trig_six_functions_generator.py, unit_circle_generator.py |
| `SIGN_TEST` | 4 | `SIGN_TEST\|(-inf, -6)\|y = -7\|f(y) = -85 (negative)\|down` | stability_generator.py |
| `SIMILAR_APPLY` | 3 | `SIMILAR_APPLY\|8\|0.5\|4` | scaling_generator.py |
| `SIMILAR_SCALE` | 3 | `SIMILAR_SCALE\|15\|5\|3` | scaling_generator.py |
| `SIMILAR_SETUP` | 3 | `SIMILAR_SETUP\|square\|5\|15` | scaling_generator.py |
| `SIMPLEX_SETUP` | 3 | `SIMPLEX_SETUP\|max z=4x+2y\|x<=13\|y<=17` | simplex_generator.py |
| `SIM_SETUP` | 2 | `SIM_SETUP\|△ABC ~ △DEF; DE = 40, AB = 16, EF = 25\|find BC` | similar_triangles_generator.py |
| `SIN` | 2 | `SIN\|5pi/6\|1/2` | positional_encoding_generator.py |
| `SINGULAR_VALUE` | 2 | `SINGULAR_VALUE\|sigma1\|5` | low_rank_approx_generator.py |
| `SINUSOID_SETUP` | 2 | `SINUSOID_SETUP\|y = 2cos(4(x + 30°)) + 3\|amplitude, period, phase shift, midline` | sinusoid_features_generator.py |
| `SIZE_REDUCE` | 2 | `SIZE_REDUCE\|b2=(0, 11)\|b2-1b1=(6, -2)` | lll_reduction_generator.py |
| `SLOPE_CALC` | 2 | *(not observed in sampling)* | equation_from_two_points_generator.py |
| `SLOPE_FORMULA` | 1 | `SLOPE_FORMULA\|m = (y2 - y1) / (x2 - x1)` | equation_from_two_points_generator.py, regression_generator.py, slope_two_points_generator.py |
| `SLOPE_INT_IDENTIFY` | 2 | `SLOPE_INT_IDENTIFY\|Slope (m)\|-61` | slope_intercept_form_generator.py |
| `SLOPE_INT_MATCH` | 2 | `SLOPE_INT_MATCH\|Compare to Slope-Intercept Form\|y = mx + b` | slope_intercept_form_generator.py |
| `SLOPE_INT_SETUP` | 1 | `SLOPE_INT_SETUP\|y = -61x` | slope_intercept_form_generator.py |
| `SLOPE_RESULT` | 1 | `SLOPE_RESULT\|1/2` | equation_from_two_points_generator.py |
| `SLOPE_SETUP` | 2 | `SLOPE_SETUP\|(1, 3)\|(-2, 9)` | slope_two_points_generator.py |
| `SLOPE_SUBST` | 1 | `SLOPE_SUBST\|m = (9 - 3) / (-2 - 1)` | equation_from_two_points_generator.py, slope_two_points_generator.py |
| `SLOPE_UNDEFINED` | 1 | `SLOPE_UNDEFINED\|Division by zero` | slope_two_points_generator.py |
| `SOFTMAX_EXP` | 2 | `SOFTMAX_EXP\|1,1\|1` | attention_generator.py, softmax_gradient_generator.py |
| `SOFTMAX_PROB` | 2 | `SOFTMAX_PROB\|1\|1/3` | softmax_gradient_generator.py |
| `SOFTMAX_SETUP` | 3 | `SOFTMAX_SETUP\|z=(1*ln(6),1*ln(8),1*ln(4))\|T=1\|target=3` | softmax_gradient_generator.py |
| `SOFTMAX_WEIGHT` | 2 | `SOFTMAX_WEIGHT\|1,1\|1/2` | attention_generator.py |
| `SOLUTIONS` | 2 | `SOLUTIONS\|cos x = 1/2\|60°, 300°, 420°, 660°, 780°, 1020°, 1140°, 1380°, 1500°, 1740°, 1860°, 2100°, 2220°, 2460°, 2580°, 2820°, 2940°, 3180°, 3300°, 3540°, 3660°, 3900°, 4020°, 4260°, 4380°, 4620°, 4740°, 4980°, 5100°, 5340°, 5460°, 5700°, 5820°, 6060°, 6180°, 6420°, 6540°, 6780°, 6900°, 7140°, 7260°, 7500°, 7620°, 7860°, 7980°, 8220°, 8340°, 8580°, 8700°, 8940°, 9060°, 9300°, 9420°, 9660°, 9780°, 10020°, 10140°, 10380°, 10500°, 10740°, 10860°, 11100°, 11220°, 11460°, 11580°, 11820°, 11940°, 12180°, 12300°, 12540°, 12660°, 12900°, 13020°, 13260°, 13380°, 13620°, 13740°, 13980°` | trig_equation_generator.py |
| `SOLUTION_FORMULA` | 1 | `SOLUTION_FORMULA\|M1*V1=M2*V2` | solution_chem_generator.py |
| `SOLUTION_SETUP` | 3 | `SOLUTION_SETUP\|dilution_stock_volume\|M1=3\|M2=1/3, V2=345` | solution_chem_generator.py |
| `SOLVE_CONST` | 2 | `SOLVE_CONST\|C1 = 3\|C2 = -1` | ode_system_generator.py, second_order_ode_generator.py, undetermined_coeff_generator.py |
| `SOLVE_U` | 2 | `SOLVE_U\|e^(-3x)u = e^(-3x) + C\|u = 1 + Ce^(3x)` | ode_substitution_generator.py |
| `SOLVE_Y` | 2 | `SOLVE_Y\|e^(3x)y = 4e^(7x) + C\|y = 4e^(4x) + Ce^(-3x)` | integrating_factor_generator.py, laplace_ivp_generator.py, ode_substitution_generator.py |
| `SOL_ENTRY` | 3 | `SOL_ENTRY\|x1(t)\|(-6*e^(-6t) + 7*e^(-5t))*(-1) + (e^(-6t) - e^(-5t))*(-6)\|-e^(-5t)` | matrix_exponential_generator.py |
| `SOL_FORM` | 1, 2 | `SOL_FORM\|y = C1e^(-3x) + C2e^(3x)` | ode_system_generator.py, second_order_ode_generator.py, undetermined_coeff_generator.py, variation_parameters_generator.py |
| `SORT` | 2 | `SORT\|9,15,20,2,1\|1,2,9,15,20` | five_number_summary_generator.py, simple_stats_generator.py |
| `SORT_EDGES` | 1 | `SORT_EDGES\|BD=7, AB=9, AE=10, CD=11, AD=13, BC=16, DE=19` | mst_generator.py |
| `SPECIAL_SOLUTION` | 2 | `SPECIAL_SOLUTION\|12 = 12\|identity: true for every x` | radical_equation_generator.py, special_solution_equation_generator.py |
| `SPEED` | 2, 3 | `SPEED\|norm r'(0)\|17` | curve_geometry_generator.py |
| `SPHERICAL_BOUNDS` | 2 | `SPHERICAL_BOUNDS\|rho\|0..11` | triple_integral_generator.py |
| `SPHERICAL_CONVERT` | 2 | `SPHERICAL_CONVERT\|5 dV\|5*rho^2*sin(phi) drho dphi dtheta` | triple_integral_generator.py |
| `SPHERICAL_COSINES` | 1 | `SPHERICAL_COSINES\|cos(c)=sin(lat1)sin(lat2)+cos(lat1)cos(lat2)cos(dlon)` | great_circle_generator.py |
| `SPHERICAL_COSINE_LAW` | 1 | `SPHERICAL_COSINE_LAW\|cos(a)=cos(b)cos(c)+sin(b)sin(c)cos(A)` | spherical_triangle_generator.py |
| `SPHERICAL_EXCESS_SETUP` | 2 | `SPHERICAL_EXCESS_SETUP\|R=12\|angles=60,135,30` | spherical_excess_generator.py |
| `SPHERICAL_SINE_LAW` | 1 | `SPHERICAL_SINE_LAW\|sin(A)/sin(a)=sin(B)/sin(b)` | spherical_triangle_generator.py |
| `SPHERICAL_TRIANGLE_SETUP` | 2 | `SPHERICAL_TRIANGLE_SETUP\|b=90 deg, c=120 deg, A=120 deg\|find cos(a)` | spherical_triangle_generator.py |
| `SPIN_COMPONENT` | 2 | `SPIN_COMPONENT\|row=1\|-28/53` | spin_half_generator.py |
| `SPIN_SETUP` | 3 | `SPIN_SETUP\|measurement_probability\|axis=z\|psi=[-15/113,-112/113]` | spin_half_generator.py |
| `SPLIT_MIDDLE` | 2 | `SPLIT_MIDDLE\|-17y = -12y - 5y\|3y^2 - 12y - 5y + 20` | factor_trinomial_generator.py |
| `SPLIT_SETUP` | 3 | `SPLIT_SETUP\|shape\|left pos=3, neg=5\|right pos=4, neg=4` | information_gain_generator.py |
| `SQRT_BOTH_SIDES` | 2 | `SQRT_BOTH_SIDES\|(y - 6)^2 = 25\|y - 6 = ±5` | completing_square_generator.py, quadratic_square_root_generator.py, rational_equation_generator.py |
| `SQRT_DIGIT` | 2 | `SQRT_DIGIT\|5\|root = 5` | manual_square_root_generator.py |
| `SQRT_NEG` | 2 | `SQRT_NEG\|√(-48)\|i√48` | complex_quadratic_generator.py, polynomial_zeros_generator.py |
| `SQRT_SETUP` | 2 | `SQRT_SETUP\|N = 355216\|groups 35, 52, 16` | manual_square_root_generator.py |
| `SQRT_TRIAL` | 3 | `SQRT_TRIAL\|x = 5\|(0 + 5)*5 = 25\|fits` | manual_square_root_generator.py |
| `SQUARE_BOTH_SIDES` | 2 | `SQUARE_BOTH_SIDES\|√(3x - 5) = x - 1\|3x - 5 = (x - 1)^2` | radical_equation_generator.py |
| `SQUARE_FACTOR` | 3 | `SQUARE_FACTOR\|95316\|676 × 141\|676` | radical_add_sub_generator.py, radical_multiply_generator.py, radical_rationalize_generator.py, radical_variable_simplify_generator.py |
| `SQUARE_TEST` | 3 | `SQUARE_TEST\|121\|11^2 = 121\|perfect square` | discriminant_generator.py |
| `STABILITY` | 3 | `STABILITY\|y=-6\|left down, right up\|unstable` | stability_generator.py |
| `STANDING_BOUNDARY` | 1 | `STANDING_BOUNDARY\|closed-open pipe uses h=2k-1` | standing_wave_generator.py |
| `STANDING_FORMULA` | 1 | `STANDING_FORMULA\|lambda=4L/h, f=v/lambda` | standing_wave_generator.py |
| `STANDING_SETUP` | 3 | `STANDING_SETUP\|closed_pipe\|k=7\|L=17, v=116` | standing_wave_generator.py |
| `STATEMENT_EVAL` | 3 | `STATEMENT_EVAL\|Bea says Oona is a knight\|T\|consistent` | knights_knaves_generator.py |
| `STATICS_FORMULA` | 1 | `STATICS_FORMULA\|sum_tau_left=0 => RB*L=W*x` | statics_generator.py |
| `STATICS_SETUP` | 3 | `STATICS_SETUP\|supported_beam\|W=123, L=6\|x=3` | statics_generator.py |
| `STATIONARY` | 2 | `STATIONARY\|pi0=2/3\|pi1=1/3` | entropy_rate_markov_generator.py |
| `STAT_ABS_DEV` | 2 | `STAT_ABS_DEV\|-26\|26` | statistics_generator.py |
| `STAT_AVERAGE` | 2 | `STAT_AVERAGE\|(52 + 63) / 2\|57.5` | statistics_generator.py |
| `STAT_COUNT` | 1 | `STAT_COUNT\|7` | statistics_generator.py |
| `STAT_DEVIATION` | 3 | `STAT_DEVIATION\|0\|26\|-26` | statistics_generator.py |
| `STAT_DIVIDE` | 2 | `STAT_DIVIDE\|448 / 7\|64` | statistics_generator.py |
| `STAT_FREQUENCY` | 2 | `STAT_FREQUENCY\|11\|2` | statistics_generator.py |
| `STAT_MAD` | 3 | `STAT_MAD\|60\|5\|12` | statistics_generator.py |
| `STAT_MAX` | 1 | `STAT_MAX\|93` | statistics_generator.py |
| `STAT_MEAN` | 2 | `STAT_MEAN\|130 / 5\|26` | statistics_generator.py |
| `STAT_MIDDLE` | 2 | `STAT_MIDDLE\|positions 5 and 6\|52, 63` | statistics_generator.py |
| `STAT_MIN` | 1 | `STAT_MIN\|17` | statistics_generator.py |
| `STAT_MODE` | 2 | `STAT_MODE\|53\|3` | statistics_generator.py |
| `STAT_ORDER` | 1 | `STAT_ORDER\|12, 19, 38, 39, 52, 63, 74, 77, 78, 88` | statistics_generator.py |
| `STAT_RANGE` | 2 | `STAT_RANGE\|93 - 17\|76` | statistics_generator.py |
| `STAT_SETUP` | 1 | `STAT_SETUP\|65, 37, 74, 59, 82, 80, 51` | statistics_generator.py |
| `STAT_SUM` | 2 | `STAT_SUM\|65 + 37 + 74 + 59 + 82 + 80 + 51\|448` | statistics_generator.py |
| `STD` | 1 | `STD\|8` | layer_norm_generator.py |
| `STEADY_EQUATION` | 2 | `STEADY_EQUATION\|pi0*pi01=pi1*pi10\|pi0+pi1=1` | markov_chain_generator.py |
| `STEPPING_STONE` | 2 | `STEPPING_STONE\|enter x21\|+x21 -x22 +x12 -x11` | transportation_generator.py |
| `STEREO_SETUP` | 3, 4 | `STEREO_SETUP\|sphere_to_plane\|X=-150/167\|Y=45/167\|Z=-58/167` | stereographic_generator.py |
| `STIRLING_CELL` | 3 | `STIRLING_CELL\|S(1,1)\|1×0+1\|1` | set_counting_generator.py |
| `STMT_EVAL` | 3 | `STMT_EVAL\|p\|6 is prime\|F` | logical_connective_eval_generator.py |
| `STOICH_RATIO` | 2 | `STOICH_RATIO\|N2->NH3\|2/1=2` | gas_stoichiometry_generator.py, stoichiometry_generator.py |
| `STOICH_SETUP` | 2, 3 | `STOICH_SETUP\|limiting_reagent\|N2 + 3 H2 -> 2 NH3\|given=N2=29 mol, H2=13 mol` | stoichiometry_generator.py |
| `STRUCTURE_CONSTANT` | 3 | `STRUCTURE_CONSTANT\|epsilon_yxz\|-1\|55iJz` | structure_constant_generator.py |
| `STRUCTURE_SETUP` | 3 | `STRUCTURE_SETUP\|A=-5Jy\|B=11Jx\|epsilon_yxz=-1` | structure_constant_generator.py |
| `SU3_SETUP` | 2 | `SU3_SETUP\|left=3bar\|right=3bar` | young_tableaux_generator.py |
| `SUBEXPR` | 2 | `SUBEXPR\|B − C\|{3, 17, 18}` | set_expression_generator.py, set_operations_generator.py |
| `SUBGROUP` | 2 | `SUBGROUP\|H={0, 6, 4, 2}\|size 4` | coset_generator.py |
| `SUBGROUP_ELEM` | 2 | `SUBGROUP_ELEM\|k=1\|3` | coset_generator.py, cyclic_group_generator.py |
| `SUBGROUP_START` | 2 | `SUBGROUP_START\|H=<6>\|identity 0` | coset_generator.py |
| `SUBSET_CHECK` | 3 | `SUBSET_CHECK\|{26}\|subset of A?\|yes` | set_membership_subset_generator.py |
| `SUBSET_SIZE` | 2 | `SUBSET_SIZE\|0\|∅` | set_operations_generator.py |
| `SUBST` | 2, 3 | `SUBST\|x\|1\|4(1)+y+7` | arc_length_generator.py, chain_rule_generator.py, curve_analysis_generator.py, derivative_limit_def_generator.py, evaluate_expression_generator.py, function_composition_generator.py, function_evaluation_generator.py, function_operations_generator.py, function_table_generator.py, implicit_diff_generator.py, integrating_factor_generator.py, legendre_construction_generator.py, lhopital_generator.py, limit_evaluation_generator.py, line_integral_generator.py, linear_approx_generator.py, log_diff_higher_order_generator.py, logistic_growth_generator.py, mean_value_theorem_generator.py, ode_substitution_generator.py, optimization_generator.py, parametric_calculus_generator.py, partial_fractions_generator.py, piecewise_evaluation_generator.py, polar_parametric_generator.py, power_series_generator.py, recursive_explicit_generator.py, related_rates_generator.py, remainder_factor_theorem_generator.py, second_order_ode_generator.py, separable_ode_generator.py, tangent_line_generator.py, taylor_series_generator.py, trig_equation_generator.py, u_substitution_generator.py, undetermined_coeff_generator.py |
| `SUBSTITUTE` | 2 | `SUBSTITUTE\|d:=(lambda t. k) in lambda c. c\|lambda c. c` | lambda_reduction_generator.py |
| `SUBSTITUTION` | 2 | `SUBSTITUTION\|y = vx\|dy/dx = v + x dv/dx` | ode_substitution_generator.py |
| `SUB_COL` | 3 | `SUB_COL\|col_1\|5-6-borrow0\|->9 (borrow_out 1)` | multi_digit_subtraction_generator.py |
| `SUM` | 2, 3 | `SUM\|73 + 74 + 75 + 72 + 71\|365` | bayesian_update_generator.py, method_of_moments_generator.py, mle_generator.py, regression_generator.py |
| `SUM_ORDER` | 2 | `SUM_ORDER\|Σ i^5\|n^6` | master_theorem_generator.py |
| `SUPPORT` | 2 | `SUPPORT\|0<=x<=18\|0<=y<=324` | rv_transform_generator.py |
| `SUPPORT_TERM` | 2 | `SUPPORT_TERM\|1\|(-3,0)` | svm_margin_generator.py |
| `SVM_SETUP` | 3 | `SVM_SETUP\|x1=(-3,0),y1=1,alpha1=1\|x2=(0,4),y2=-1,alpha2=1\|b=5,x=(4,-1)` | svm_margin_generator.py |
| `SWAP` | 2 | `SWAP\|norm b2=40\|norm b1=205` | lll_reduction_generator.py |
| `SWAP_VARS` | 1 | `SWAP_VARS\|x = -2y + 5` | inverse_function_generator.py |
| `SYMMETRIC_CHECK` | 3 | `SYMMETRIC_CHECK\|(19, 19)\|reverse (19, 19)\|present` | equivalence_relation_generator.py, relation_check_generator.py |
| `SYMMETRY` | 2 | `SYMMETRY\|odd function\|a0=0, a_n=0` | fourier_series_generator.py |
| `SYNDIV_SETUP` | 2 | `SYNDIV_SETUP\|2x^3 + 12x^2 + 14x - 2\|r = -4` | polynomial_zeros_generator.py, synthetic_division_generator.py |
| `SYNDROME_CALC` | 2 | `SYNDROME_CALC\|s1=b1 xor b3 xor b5 xor b7\|0 xor 0 xor 1 xor 0=1` | hamming_code_generator.py |
| `SYNDROME_VALUE` | 2 | `SYNDROME_VALUE\|s1=1, s2=0, s4=1\|position=5` | hamming_code_generator.py |
| `SYN_DROP` | 1 | `SYN_DROP\|2` | horner_evaluation_generator.py, polynomial_zeros_generator.py, synthetic_division_generator.py |
| `SYN_ROW` | 1 | `SYN_ROW\|2, 4, -2, 6` | polynomial_zeros_generator.py, synthetic_division_generator.py |
| `SYS_ADD` | 1 | `SYS_ADD\|Add equations: -11y = -77` | systems_elimination_generator.py |
| `SYS_EQ_NEW` | 1 | `SYS_EQ_NEW\|New equation with y only` | systems_substitution_generator.py |
| `SYS_ISOLATE` | 2 | `SYS_ISOLATE\|Isolate x in Eq 1\|x = -y - 11` | systems_substitution_generator.py |
| `SYS_MULT` | 1 | `SYS_MULT\|Eq1 * -5, Eq2 * 2` | systems_elimination_generator.py |
| `SYS_REWRITE` | 2 | `SYS_REWRITE\|10x - 5y = 25\|-10x - 6y = -102` | systems_elimination_generator.py |
| `SYS_SETUP` | 2 | `SYS_SETUP\|x + y = -11\|3x + 2y = -32` | systems_elimination_generator.py, systems_substitution_generator.py |
| `SYS_SUBST` | 1 | `SYS_SUBST\|Substitute x in Eq 2` | systems_substitution_generator.py |
| `SYS_SUBST_BACK` | 1 | `SYS_SUBST_BACK\|Substitute y=-1 into x = -y - 11` | systems_elimination_generator.py, systems_substitution_generator.py |
| `TABLEAU` | 2, 3 | `TABLEAU\|initial\|s1: x + s1 = 13\|s2: y + s2 = 17` | simplex_generator.py |
| `TABLEAU_RULE` | 3 | `TABLEAU_RULE\|3bar x 3bar\|two antiboxes split into symmetric plus antisymmetric\|6bar + 3` | young_tableaux_generator.py |
| `TABLE_COMPARE` | 1, 2 | `TABLE_COMPARE\|match` | set_identity_membership_table_generator.py |
| `TABLE_ENTRY` | 2 | `TABLE_ENTRY\|f(-3)\|-30` | euler_method_generator.py, function_table_generator.py, taylor_series_generator.py |
| `TABLE_LOOKUP` | 2 | `TABLE_LOOKUP\|g(1)\|3` | de_moivre_generator.py, dot_product_generator.py, euler_formula_generator.py, function_evaluation_generator.py, lie_exponential_generator.py, normal_table_generator.py, pascal_triangle_generator.py, polar_parametric_generator.py, right_triangle_trig_generator.py, triangle_solve_generator.py, trig_equation_generator.py, trig_identity_eval_generator.py, unit_circle_generator.py |
| `TANGENT_PLANE` | 2 | `TANGENT_PLANE\|z = z0 + fx(x-a) + fy(y-b)\|z = 170 + 25*(x - 3) + 58*(y - 4)` | gradient_generator.py |
| `TARGET_STATE` | 2 | `TARGET_STATE\|J=0\|M=0` | clebsch_gordan_generator.py |
| `TAYLOR_FORMULA` | 1 | `TAYLOR_FORMULA\|P_n(x) = Σ f^(k)(a)/k!·(x - a)^k` | taylor_series_generator.py |
| `TAYLOR_SETUP` | 2 | `TAYLOR_SETUP\|f(x) = cos(x), center a = 0\|Maclaurin polynomial of degree 4` | taylor_series_generator.py |
| `TELESCOPE_CANCEL` | 2 | `TELESCOPE_CANCEL\|survive first and last\|1/72 - 1/138` | telescoping_generator.py |
| `TELE_SETUP` | 1 | `TELE_SETUP\|Σ k=72..137 (1/k - 1/(k+1))` | telescoping_generator.py |
| `TEMP_SCALE` | 2 | `TEMP_SCALE\|z1/T\|ln(6)` | softmax_gradient_generator.py |
| `TENSOR_ENTRY` | 2 | `TENSOR_ENTRY\|C_11\|19` | einstein_summation_generator.py, index_raising_generator.py |
| `TENSOR_RULE` | 1 | `TENSOR_RULE\|diag(a,b) tensor diag(c,d)=diag(ac,ad,bc,bd)` | tensor_product_generator.py |
| `TENSOR_SETUP` | 3 | `TENSOR_SETUP\|A=diag(0,4)\|B=diag(-2,2)\|u=[-4,-1], v=[0,1]` | tensor_product_generator.py |
| `TENSOR_STATE` | 2 | `TENSOR_STATE\|u tensor v\|[0,-4,0,-1]` | tensor_product_generator.py |
| `TERM` | 2 | `TERM\|i=0: 1·(2/5)^0·(3/5)^4\|0.1296` | binomial_probability_generator.py |
| `TERMS` | 1 | `TERMS\|x[0..3]=[21,168,1344,10752]` | z_transform_generator.py |
| `TEST_CHOOSE` | 2 | `TEST_CHOOSE\|p-series\|Σ 1/n^p with p = 17/5` | power_series_generator.py, series_convergence_generator.py |
| `TEST_STAT_FORMULA` | 1 | `TEST_STAT_FORMULA\|z = (p̂ - p0)/√(p0(1-p0)/n)` | hypothesis_test_generator.py, two_sample_test_generator.py |
| `TF_SETUP` | 3 | `TF_SETUP\|block_feedback\|G1=5/(s+5), G2=4/(s+4)\|H=1` | transfer_function_generator.py |
| `THEOREM` | 1, 2 | `THEOREM\|quadratic formula\|y = (-b ± √(b^2 - 4ac))/(2a)` | angle_defect_generator.py, circle_angle_generator.py, gauss_bonnet_generator.py, geometric_mean_generator.py, logistic_growth_generator.py, mean_value_theorem_generator.py, parametric_calculus_generator.py, polar_parametric_generator.py, quadratic_generator.py, rational_root_generator.py, remainder_factor_theorem_generator.py, series_convergence_generator.py, special_right_triangle_generator.py, spherical_excess_generator.py, taylor_series_generator.py, triangle_solve_generator.py, trig_identity_eval_generator.py, trig_six_functions_generator.py |
| `THEOREM_REWRITE` | 2 | `THEOREM_REWRITE\|circulation\|double integral of Q_x - P_y` | vector_theorem_generator.py |
| `THEOREM_SETUP` | 3 | `THEOREM_SETUP\|Green\|F=<0, 7*x>\|rectangle 5 by 9` | vector_theorem_generator.py |
| `THETA` | 2 | `THETA\|min(15,14)\|14` | transportation_generator.py |
| `THROUGHPUT` | 2 | `THROUGHPUT\|tokens_per_second\|3800000000/27` | scaling_law_generator.py |
| `TIME_COMPONENT` | 2 | `TIME_COMPONENT\|k=1\|2-i` | braket_generator.py |
| `TIME_DERIV` | 2 | `TIME_DERIV\|d/dt(m*L^2*thetadot)\|m*L^2*thetaddot` | lagrangian_generator.py |
| `TIME_EVOLVE` | 2 | `TIME_EVOLVE\|U psi\|[2-i,-1+2i,1]` | braket_generator.py |
| `TM_CONFIG` | 4 | `TM_CONFIG\|step 0\|state=q0\|head=0\|tape=0` | turing_machine_trace_generator.py |
| `TM_HALT` | 2 | `TM_HALT\|step 2\|halted` | turing_machine_trace_generator.py |
| `TM_MOVE` | 3 | `TM_MOVE\|0\|R\|1` | turing_machine_trace_generator.py |
| `TM_READ` | 2 | `TM_READ\|head=0\|0` | turing_machine_trace_generator.py |
| `TM_RULE` | 2 | `TM_RULE\|q0,0\|q0,1,R` | turing_machine_trace_generator.py |
| `TM_SETUP` | 3 | `TM_SETUP\|binary_flip\|input=0\|limit=4` | turing_machine_trace_generator.py |
| `TM_WRITE` | 2 | `TM_WRITE\|head=0\|1` | turing_machine_trace_generator.py |
| `TOPO_AVAILABLE` | 1 | `TOPO_AVAILABLE\|A` | graph_traversal_generator.py |
| `TOPO_PICK` | 2 | `TOPO_PICK\|available {3, 11}\|pick 3` | partial_order_generator.py |
| `TOPO_READY` | 1 | `TOPO_READY\|B` | graph_traversal_generator.py |
| `TOPO_SELECT` | 2 | `TOPO_SELECT\|A\|A` | graph_traversal_generator.py |
| `TOTIENT_RESULT` | 2 | `TOTIENT_RESULT\|phi(42)\|12` | totient_generator.py |
| `TRACE` | 2 | `TRACE\|4 + 1\|5` | ode_system_generator.py |
| `TRACE_ADD` | 4 | `TRACE_ADD\|gamma1gamma0\|(1,1)\|0 + 0\|0` | gamma_matrix_generator.py |
| `TRACE_ENTRY` | 2 | `TRACE_ENTRY\|(1,1)\|4` | einstein_summation_generator.py, pauli_algebra_generator.py |
| `TRACE_EXPECT` | 1, 3 | `TRACE_EXPECT\|Tr(rho A)=p0*a+p1*b` | density_matrix_generator.py, gamma_matrix_generator.py |
| `TRACE_SUM` | 2 | `TRACE_SUM\|4 + 4\|8` | pauli_algebra_generator.py |
| `TRANSFER` | 1 | `TRANSFER\|G(s)=20/(s^2+9s+20)` | transfer_function_generator.py |
| `TRANSFORM_APPLY` | 2 | `TRANSFORM_APPLY\|(-(-4), (8))\|(4, 8)` | transformation_generator.py |
| `TRANSFORM_RULE` | 1 | `TRANSFORM_RULE\|(x, y) → (-y, x)` | transformation_generator.py |
| `TRANSFORM_SETUP` | 2, 3 | `TRANSFORM_SETUP\|P(8, -4)\|rotation 90° counterclockwise about the origin` | rv_transform_generator.py, transformation_generator.py |
| `TRANSIENT_FORMULA` | 1 | `TRANSIENT_FORMULA\|tau=L/R` | transient_circuit_generator.py |
| `TRANSIENT_SETUP` | 3 | `TRANSIENT_SETUP\|rl_rise\|R=4, L=16\|V=34, t=12` | transient_circuit_generator.py |
| `TRANSITIVE_CHECK` | 3 | `TRANSITIVE_CHECK\|(19, 19) and (19, 19)\|need (19, 19)\|present` | equivalence_relation_generator.py, relation_check_generator.py |
| `TRANSPORT_SETUP` | 3 | `TRANSPORT_SETUP\|supply=(16,15)\|demand=(14,17)\|costs=(10,9;2,4)` | transportation_generator.py |
| `TRIG_RATIO` | 2 | `TRIG_RATIO\|cos\|adjacent/hypotenuse` | right_triangle_trig_generator.py |
| `TRIG_SETUP` | 2 | `TRIG_SETUP\|right triangle: leg opposite A = 60, leg adjacent to A = 25, hypotenuse = 65\|cos A` | right_triangle_trig_generator.py, trig_identity_eval_generator.py, trig_six_functions_generator.py, unit_circle_generator.py |
| `TRIG_VALUE` | 2, 3 | `TRIG_VALUE\|sin(lat1)=0\|sin(lat2)=0\|cos(dlon)=1/2` | christoffel_generator.py, great_circle_generator.py, spherical_triangle_generator.py |
| `TRIPLE_EVAL` | 3 | `TRIPLE_EVAL\|rho_part * phi_part * angle\|5*1331/3*2*2*pi\|26620/3*pi` | triple_integral_generator.py |
| `TRIPLE_SETUP` | 3 | `TRIPLE_SETUP\|integrand 5\|ball radius 11\|spherical` | triple_integral_generator.py |
| `TRI_ANGLE_SETUP` | 3 | `TRI_ANGLE_SETUP\|23\|23\|x` | angle_relationships_generator.py |
| `TRI_ANGLE_SOLVE` | 2 | `TRI_ANGLE_SOLVE\|x = 180 - 23 - 23\|134` | angle_relationships_generator.py |
| `TRI_ANGLE_SUM` | 1 | `TRI_ANGLE_SUM\|23 + 23 + x = 180` | angle_relationships_generator.py |
| `TRI_AREA_FORMULA` | 1 | `TRI_AREA_FORMULA\|Area = (1/2)·a·b·sin C` | triangle_area_sas_generator.py |
| `TRI_SETUP` | 2 | `TRI_SETUP\|45-45-90 triangle, leg = 187\|hypotenuse` | special_right_triangle_generator.py, triangle_area_sas_generator.py, triangle_solve_generator.py |
| `TRUNCATE` | 2 | `TRUNCATE\|rank=1\|discard=5` | low_rank_approx_generator.py |
| `TRUTH_ROW` | 1, 2 | `TRUTH_ROW\|row 1\|p=T, q=T, r=T` | argument_form_generator.py, boolean_algebra_generator.py, truth_table_generator.py |
| `TRY` | 2, 3 | `TRY\|x = −45\|−46 < x ≤ −35 and (x is even and x is perfect square)\|false` | conditional_forms_generator.py, counterexample_search_generator.py, factor_trinomial_generator.py, log_conversion_generator.py, log_equation_generator.py, polynomial_inequality_generator.py, radical_equation_generator.py, rational_equation_generator.py, rational_root_generator.py, set_builder_roster_generator.py |
| `TS_FACTOR` | 3 | `TS_FACTOR\|p-1=72\|q=9\|s=3` | tonelli_shanks_generator.py |
| `TS_INIT` | 4 | `TS_INIT\|m=3\|c=10\|t=72\|r=71` | tonelli_shanks_generator.py |
| `TS_LOOP` | 2 | `TS_LOOP\|i=1\|b=27` | tonelli_shanks_generator.py |
| `TS_NONRESIDUE` | 1 | `TS_NONRESIDUE\|5` | tonelli_shanks_generator.py |
| `TS_SETUP` | 2 | `TS_SETUP\|a=69\|p=73` | tonelli_shanks_generator.py |
| `TT_COLUMN` | 2 | `TT_COLUMN\|formula\|FTFTFTFF` | truth_table_generator.py |
| `TT_SETUP` | 2 | `TT_SETUP\|variables p, q, r\|8` | truth_table_generator.py |
| `TWIDDLE` | 1, 3 | `TWIDDLE\|W2=-1` | dft_generator.py |
| `TWOS_SETUP` | 2 | `TWOS_SETUP\|8-bit two's complement\|offset = 2^8 = 256` | base_conversion_generator.py |
| `UB` | 2 | `UB\|{2, 24}\|{24}` | partial_order_generator.py |
| `UC_GUESS` | 2 | `UC_GUESS\|exponential forcing\|y_p = Ae^(4x)` | undetermined_coeff_generator.py |
| `UC_POINT` | 2 | `UC_POINT\|180°\|(-1, 0)` | unit_circle_generator.py |
| `UNCERTAINTY_SETUP` | 3 | `UNCERTAINTY_SETUP\|particle in a box\|L=1, hbar=1\|n=130` | uncertainty_generator.py |
| `UNFOLD` | 2 | `UNFOLD\|h(21)\|h(20) + 31·21` | recursive_definition_unfold_generator.py |
| `UNIFY_BIND` | 3 | `UNIFY_BIND\|X\|b\|{X=b}` | unification_generator.py |
| `UNIFY_DECOMPOSE` | 2 | `UNIFY_DECOMPOSE\|f\|2 arguments` | unification_generator.py |
| `UNIFY_FAIL` | 1 | `UNIFY_FAIL\|occurs-check X in f(X)` | unification_generator.py |
| `UNIFY_PAIR` | 2 | `UNIFY_PAIR\|f(X,a)\|f(b,Y)` | unification_generator.py |
| `UNIFY_SETUP` | 3 | `UNIFY_SETUP\|f(X,a)\|f(b,Y)\|occurs-check` | unification_generator.py |
| `UNIT_ATTACH` | 3 | `UNIT_ATTACH\|9\|seconds\|9 seconds` | cross_section_generator.py, kinematics_generator.py, physics_formula_generator.py |
| `UNIT_CONVERT` | 2 | `UNIT_CONVERT\|6 minutes\|360 seconds` | physics_formula_generator.py |
| `UNIT_NORMAL` | 2 | `UNIT_NORMAL\|T'(0)/norm T'(0)\|<-1, 0>` | curve_geometry_generator.py |
| `UNIT_RATE_DIV` | 3 | `UNIT_RATE_DIV\|$25.00\|10\|$2.50` | unit_rate_generator.py |
| `UNIT_RATE_PICK` | 2 | `UNIT_RATE_PICK\|2\|4` | unit_rate_generator.py |
| `UNIT_RATE_SETUP` | 3 | `UNIT_RATE_SETUP\|10\|oranges\|$25.00` | unit_rate_generator.py |
| `UNIT_RATE_TABLE` | 2 | `UNIT_RATE_TABLE\|2,4,5,8\|4,8,10,16` | unit_rate_generator.py |
| `UNIT_RULE` | 3 | `UNIT_RULE\|c=1\|E=m\|energy uses TeV` | natural_units_generator.py |
| `UNIT_TANGENT` | 2 | `UNIT_TANGENT\|r'(0)/speed\|<0, 1>` | curve_geometry_generator.py |
| `UNLIKE_RADICALS` | 2 | `UNLIKE_RADICALS\|√2 ≠ √3\|unlike radicands — cannot combine` | radical_add_sub_generator.py |
| `UNPAIRED` | 2 | `UNPAIRED\|neither\|∅` | one_to_one_correspondence_generator.py |
| `UNROLL` | 2 | `UNROLL\|8, 32, 128, 512\|geometric, r = 4` | recursive_explicit_generator.py |
| `UPDATE` | 2 | `UPDATE\|W1_11\|1` | backprop_generator.py, kernel_perceptron_generator.py |
| `U_VECTOR` | 2 | `U_VECTOR\|u1 = A*v1/σ1\|[1/√2, 1/√2]` | svd_generator.py |
| `VA` | 1 | `VA\|x = 5` | rational_function_features_generator.py |
| `VALIDITY` | 2 | `VALIDITY\|valid\|addition` | argument_form_generator.py |
| `VALUE_FORMULA` | 1 | `VALUE_FORMULA\|v=(ad-bc)/(a-b-c+d)` | game_theory_generator.py |
| `VARIANCE` | 1, 2 | `VARIANCE\|Delta x^2\|1/12 - 1/(33800pi^2)` | layer_norm_generator.py, uncertainty_generator.py |
| `VAR_FORMULA` | 1 | `VAR_FORMULA\|Var(X) = Σ P(x)·(x - μ)^2` | expected_value_generator.py |
| `VAR_ROW` | 3 | `VAR_ROW\|8 - 2.8 = 5.2\|(5.2)^2 = 27.04\|1/5·27.04 = 5.408` | expected_value_generator.py |
| `VECTOR_NORM` | 2 | `VECTOR_NORM\|A\|25` | embedding_similarity_generator.py |
| `VECTOR_SETUP` | 2 | `VECTOR_SETUP\|F(x,y,z) = <x - 3*y, x + y + 5*z, -5*x - 5*y + 6*z>\|divergence and curl` | div_curl_generator.py |
| `VEC_ENTRY` | 3 | `VEC_ENTRY\|(1)\|20923 + (-704)*5\|17403` | diagonalization_generator.py |
| `VEC_SETUP` | 2 | `VEC_SETUP\|v = ⟨-7, -5, 1⟩\|magnitude` | dot_product_generator.py, vector_ops_generator.py |
| `VENN_MARK` | 2 | `VENN_MARK\|travelers ∩ ¬pilots\|x1` | syllogism_generator.py |
| `VENN_SHADE` | 2 | `VENN_SHADE\|researchers − historians\|empty` | syllogism_generator.py |
| `VERIFY` | 2 | `VERIFY\|1\|ok` | error_spotting_generator.py |
| `VERTEX` | 1 | `VERTEX\|(6, -6)` | ellipse_features_generator.py, hyperbola_features_generator.py, lp_corner_generator.py, parabola_features_generator.py |
| `VERTEX_SOLVE` | 2 | `VERTEX_SOLVE\|x=0\|y=0` | lp_corner_generator.py |
| `VISIT` | 2 | `VISIT\|A\|A` | graph_traversal_generator.py |
| `VITERBI_BACKTRACE` | 2 | `VITERBI_BACKTRACE\|L->H->H\|27/512` | viterbi_generator.py |
| `VITERBI_CAND` | 3 | `VITERBI_CAND\|t=2,state=H\|from H\|9/128` | convolutional_code_viterbi_generator.py, viterbi_generator.py |
| `VITERBI_INIT` | 3 | `VITERBI_INIT\|H\|obs=B\|1/8` | viterbi_generator.py |
| `VITERBI_PICK` | 2, 3 | `VITERBI_PICK\|t=2,state=H\|from L\|3/32` | convolutional_code_viterbi_generator.py, viterbi_generator.py |
| `VOLUME` | 1 | `VOLUME\|200` | volume_rect_prism_generator.py |
| `VOLUME_SETUP` | 2 | `VOLUME_SETUP\|region under y = 12x on [0, 11], rotated about the x-axis\|disk method` | solid_revolution_generator.py |
| `VOL_BASE_AREA` | 2 | `VOL_BASE_AREA\|Base Area = (1/2) × 4 × 3\|6.0` | round_solids_generator.py, volume_3d_generator.py |
| `VOL_CALCULATE` | 2 | `VOL_CALCULATE\|V = 6.0 × 11\|66.0` | round_solids_generator.py, volume_3d_generator.py |
| `VOL_FORMULA` | 1 | `VOL_FORMULA\|V = Base Area × length` | round_solids_generator.py, solid_revolution_generator.py, volume_3d_generator.py |
| `VOL_SETUP` | 2 | `VOL_SETUP\|triangular_prism\|b=4, h_tri=3, length=11` | volume_3d_generator.py |
| `VOP_FORM` | 2 | `VOP_FORM\|u1' = -y2*g/W\|-288/8 * e^(6x)` | variation_parameters_generator.py |
| `WALK_ENTRY` | 2 | `WALK_ENTRY\|A^2[2,3]\|1` | graph_counting_generator.py |
| `WALK_GOAL` | 2 | `WALK_GOAL\|length 2\|2 to 3` | graph_counting_generator.py |
| `WALK_TERM` | 3 | `WALK_TERM\|via 1\|A[2,1]*A[1,3]\|1` | graph_counting_generator.py |
| `WARSHALL_K` | 2 | `WARSHALL_K\|k=4\|0 0 0 1 0; 1 0 0 1 0; 0 1 1 0 1; 0 1 0 0 0; 0 0 1 1 0` | relation_closure_generator.py |
| `WAVE_FORMULA` | 1 | `WAVE_FORMULA\|1=N^2*integral_0^L (x/L)^(2k) dx` | wavefunction_generator.py |
| `WAVE_SETUP` | 3 | `WAVE_SETUP\|power_interval\|psi=N*(x/L)^3\|0<=x<=24` | wavefunction_generator.py |
| `WEEKDAY_SCAN` | 2, 3 | `WEEKDAY_SCAN\|index 5\|Saturday` | calendar_arithmetic_generator.py |
| `WEIGHT_VECTOR` | 2 | `WEIGHT_VECTOR\|w\|(-3,-4)` | svm_margin_generator.py |
| `WIDTH_SETUP` | 3 | `WIDTH_SETUP\|branching_ratio\|Gamma_a=6, Gamma_b=2, Gamma_c=18\|target=BR_c` | branching_ratio_generator.py |
| `WORK_DIFF` | 3 | `WORK_DIFF\|phi(end) - phi(start)\|7 - 21\|-14` | line_integral_generator.py |
| `WRONSKIAN` | 2 | `WRONSKIAN\|y1*y2' - y1'*y2\|8` | variation_parameters_generator.py |
| `XOR` | 3 | `XOR\|control=1\|target=0\|1` | quantum_gate_generator.py |
| `YOUNG_SETUP` | 3 | `YOUNG_SETUP\|partition=[4,4,3]\|n=11\|group=S_11` | young_tableaux_generator.py |
| `Z` | 1 | `Z\|63 R84` | abacus_addition_generator.py, absolute_value_equation_generator.py, absolute_value_inequality_generator.py, ac_circuit_generator.py, activation_generator.py, adam_step_generator.py, algorithm_trace_generator.py, angle_defect_generator.py, angle_measure_generator.py, angle_relationships_generator.py, annuity_generator.py, antiderivative_generator.py, arc_length_generator.py, arc_sector_generator.py, area_between_curves_generator.py, argument_form_generator.py, arithmetic_coding_generator.py, arithmetic_sequence_generator.py, attention_generator.py, attribute_sorting_generator.py, baby_step_giant_step_generator.py, backprop_generator.py, base_arithmetic_generator.py, base_conversion_generator.py, bayesian_update_generator.py, bch_generator.py, bec_channel_generator.py, binomial_probability_generator.py, bisection_generator.py, bitwise_ops_generator.py, black_scholes_generator.py, blackbody_generator.py, bond_pricing_generator.py, boolean_algebra_generator.py, braket_generator.py, branching_ratio_generator.py, calendar_arithmetic_generator.py, calorimetry_generator.py, casimir_force_generator.py, casimir_generator.py, cauchy_riemann_generator.py, cayley_table_generator.py, centroid_generator.py, chain_rule_generator.py, channel_capacity_generator.py, characteristic_vector_generator.py, chi_square_generator.py, cholesky_generator.py, christoffel_generator.py, circle_angle_generator.py, circle_equation_generator.py, circle_generator.py, classifier_metrics_generator.py, clebsch_gordan_generator.py, collision_generator.py, commutator_generator.py, completing_square_generator.py, complex_division_generator.py, complex_locus_generator.py, complex_log_generator.py, complex_number_ops_generator.py, complex_quadratic_generator.py, composite_arithmetic_generator.py, compound_inequality_generator.py, compound_probability_generator.py, conditional_forms_generator.py, conditional_probability_generator.py, confidence_interval_generator.py, conic_standard_form_generator.py, conservation_law_generator.py, continued_fraction_generator.py, continuous_distribution_generator.py, contour_integral_generator.py, convolution_generator.py, convolutional_code_viterbi_generator.py, coset_generator.py, counterexample_search_generator.py, counting_classics_generator.py, cramers_rule_generator.py, crc_generator.py, cross_section_generator.py, crt_generator.py, curve_analysis_generator.py, curve_geometry_generator.py, cyclic_group_generator.py, cyk_parser_generator.py, de_moivre_generator.py, decimal_add_sub_generator.py, decimal_div_generator.py, decimal_mult_generator.py, definite_integral_generator.py, density_matrix_generator.py, derangement_generator.py, derivative_limit_def_generator.py, derivative_power_rule_generator.py, derivative_product_quotient_generator.py, derivative_transcendental_generator.py, determinant_generator.py, dfa_minimization_generator.py, dfa_simulation_generator.py, dft_generator.py, diagonalization_generator.py, diffie_hellman_generator.py, dijkstra_generator.py, dimensional_analysis_generator.py, direct_proof_algebra_generator.py, discriminant_generator.py, distance_formula_generator.py, div_curl_generator.py, divisibility_classification_generator.py, domain_range_generator.py, doppler_generator.py, dot_product_generator.py, double_integral_generator.py, dp_table_generator.py, dpll_trace_generator.py, ecdh_generator.py, ecdsa_generator.py, eigenvalue_generator.py, einstein_summation_generator.py, electrostatics_generator.py, ellipse_features_generator.py, elliptic_curve_finite_field_generator.py, embedding_similarity_generator.py, energy_conservation_generator.py, entropy_change_generator.py, entropy_generator.py, entropy_rate_markov_generator.py, equation_from_two_points_generator.py, equilibrium_ice_generator.py, equivalence_relation_generator.py, error_spotting_generator.py, euler_characteristic_generator.py, euler_circuit_generator.py, euler_formula_generator.py, euler_method_generator.py, evaluate_expression_generator.py, exact_ode_generator.py, expected_value_generator.py, exponent_generator.py, exponent_mixed_rules_generator.py, exponential_equation_generator.py, exponential_model_generator.py, extended_euclid_generator.py, factor_gcf_generator.py, factor_grouping_generator.py, factor_special_forms_generator.py, factor_trinomial_generator.py, factors_generator.py, feature_map_generator.py, fermi_estimation_generator.py, fill_in_step_generator.py, finance_generator.py, finite_difference_generator.py, finite_field_generator.py, first_law_generator.py, five_number_summary_generator.py, fixed_point_generator.py, flops_memory_generator.py, four_vector_generator.py, fourier_series_generator.py, fractal_iteration_generator.py, fraction_comparison_generator.py, fraction_decimal_percent_converter.py, fraction_op_generator.py, frequency_table_generator.py, function_composition_generator.py, function_evaluation_generator.py, function_inner_product_generator.py, function_operations_generator.py, function_properties_generator.py, function_table_generator.py, fundamental_form_generator.py, game_theory_generator.py, gamma_matrix_generator.py, gas_law_generator.py, gas_stoichiometry_generator.py, gauss_bonnet_generator.py, gauss_law_generator.py, gaussian_curvature_generator.py, gcf_generator.py, generating_function_generator.py, geometric_distribution_generator.py, geometric_mean_generator.py, geometric_probability_generator.py, geometric_sequence_generator.py, geometry_area_perimeter_generator.py, gradient_descent_generator.py, gradient_generator.py, gradient_step_generator.py, gram_schmidt_generator.py, graph_counting_generator.py, graph_interpret_generator.py, graph_traversal_generator.py, grassmann_generator.py, great_circle_generator.py, hamiltonian_generator.py, hamming_code_generator.py, hawking_generator.py, heat_engine_generator.py, hermitian_check_generator.py, hessian_classify_generator.py, horner_evaluation_generator.py, huffman_coding_generator.py, hydrogen_atom_generator.py, hyperbola_features_generator.py, hyperbolic_distance_generator.py, hyperbolic_function_generator.py, hypercube_counting_generator.py, hypothesis_test_generator.py, implicit_diff_generator.py, improper_integral_generator.py, inclusion_exclusion_generator.py, index_gymnastics_generator.py, index_raising_generator.py, induction_verify_generator.py, information_gain_generator.py, integer_operations_generator.py, integrating_factor_generator.py, integration_by_parts_generator.py, interference_generator.py, interpolation_generator.py, invariant_mass_generator.py, inverse_function_generator.py, jacobi_symbol_generator.py, jacobian_generator.py, joint_distribution_generator.py, kernel_evaluation_generator.py, kernel_perceptron_generator.py, kernel_ridge_generator.py, kernel_validity_generator.py, kinematics_generator.py, kl_divergence_generator.py, kmeans_step_generator.py, knights_knaves_generator.py, knn_generator.py, kraft_inequality_generator.py, ladder_operator_generator.py, lagrange_multiplier_generator.py, lagrangian_generator.py, lambda_reduction_generator.py, laplace_ivp_generator.py, laurent_series_generator.py, layer_norm_generator.py, lcm_generator.py, least_squares_generator.py, legendre_construction_generator.py, lhopital_generator.py, lie_exponential_generator.py, limit_evaluation_generator.py, line_integral_generator.py, linear_approx_generator.py, linear_complex_generator.py, linear_fractional_generator.py, linear_simple_generator.py, literal_equation_generator.py, lll_reduction_generator.py, log_conversion_generator.py, log_diff_higher_order_generator.py, log_equation_generator.py, log_properties_generator.py, logic_grid_puzzle_generator.py, logical_connective_eval_generator.py, logical_equivalence_laws_generator.py, logistic_growth_generator.py, long_division_generator.py, low_rank_approx_generator.py, lp_corner_generator.py, lr_schedule_generator.py, lu_decomposition_generator.py, lz_compression_generator.py, magnetism_generator.py, manual_square_root_generator.py, markov_chain_generator.py, master_theorem_generator.py, matrix_calculus_generator.py, matrix_exponential_generator.py, matrix_group_check_generator.py, matrix_inverse_generator.py, matrix_norm_generator.py, matrix_ops_generator.py, mean_value_theorem_generator.py, method_of_moments_generator.py, metric_arc_length_generator.py, mgf_generator.py, midpoint_generator.py, minkowski_interval_generator.py, mixed_number_operation_generator.py, mle_generator.py, mobius_transform_generator.py, mod_exp_generator.py, modular_arithmetic_generator.py, modular_inverse_generator.py, monomial_mult_div_generator.py, mst_generator.py, multi_digit_addition_generator.py, multi_digit_multiplication_generator.py, multi_digit_subtraction_generator.py, multi_step_unit_conversion_generator.py, multiplying_binomials_generator.py, multiplying_polynomials_generator.py, multivar_chain_rule_generator.py, mutual_information_generator.py, naive_bayes_generator.py, named_distribution_generator.py, natural_units_generator.py, nets_surface_area_generator.py, newton_raphson_generator.py, newtons_laws_generator.py, nfa_simulation_generator.py, normal_table_generator.py, npv_irr_generator.py, number_comparison_generator.py, ode_substitution_generator.py, ode_system_generator.py, one_step_equation_generator.py, one_step_inequality_generator.py, one_to_one_correspondence_generator.py, operation_properties_generator.py, optics_generator.py, optimization_generator.py, or_formula_generator.py, orbital_mechanics_generator.py, order_of_operations_generator.py, order_statistics_generator.py, parabola_features_generator.py, parallel_perpendicular_line_generator.py, param_count_generator.py, parametric_calculus_generator.py, partial_derivative_generator.py, partial_fractions_generator.py, partial_order_generator.py, partial_trace_generator.py, particle_in_box_generator.py, partition_function_generator.py, pascal_triangle_generator.py, pauli_algebra_generator.py, pca_generator.py, pda_simulation_generator.py, percent_problem_generator.py, percent_word_problem_generator.py, perceptron_generator.py, permutation_combination_generator.py, permutation_group_generator.py, perplexity_generator.py, ph_calculation_generator.py, physics_formula_generator.py, piecewise_evaluation_generator.py, place_value_rounding_generator.py, planck_units_generator.py, point_slope_generator.py, polar_parametric_generator.py, pollard_factorization_generator.py, polygon_perimeter_generator.py, polynomial_add_sub_generator.py, polynomial_div_monomial_generator.py, polynomial_inequality_generator.py, polynomial_long_division_generator.py, polynomial_zeros_generator.py, portfolio_generator.py, positional_encoding_generator.py, positive_definite_generator.py, power_series_generator.py, primality_test_generator.py, prime_factorization_generator.py, probability_addition_rule_generator.py, projectile_motion_generator.py, projector_generator.py, proportion_word_problem_generator.py, proportional_relationship_generator.py, pythag_hyp_generator.py, pythag_leg_generator.py, qr_decomposition_generator.py, quadratic_factoring_generator.py, quadratic_generator.py, quadratic_residue_generator.py, quadratic_square_root_generator.py, quantization_generator.py, quantum_formula_generator.py, quantum_gate_generator.py, quark_composition_generator.py, quaternion_generator.py, radical_add_sub_generator.py, radical_equation_generator.py, radical_multiply_generator.py, radical_rationalize_generator.py, radical_variable_simplify_generator.py, rate_conversion_generator.py, ratio_table_generator.py, rational_equation_generator.py, rational_exponent_generator.py, rational_expr_add_sub_generator.py, rational_expr_mult_div_generator.py, rational_expr_simplify_generator.py, rational_function_features_generator.py, rational_root_generator.py, recurrence_generator.py, recursive_definition_unfold_generator.py, recursive_explicit_generator.py, reed_solomon_generator.py, regex_to_automaton_generator.py, regression_generator.py, regular_polygon_area_generator.py, related_rates_generator.py, relation_check_generator.py, relation_closure_generator.py, relation_operations_generator.py, relativistic_energy_generator.py, remainder_factor_theorem_generator.py, repeating_decimal_generator.py, residue_generator.py, resolution_proof_generator.py, riemann_sum_generator.py, riemann_tensor_generator.py, right_triangle_trig_generator.py, rotational_dynamics_generator.py, round_solids_generator.py, routh_hurwitz_generator.py, row_reduction_generator.py, rsa_generator.py, runge_kutta_generator.py, running_coupling_generator.py, rv_transform_generator.py, scaling_generator.py, scaling_law_generator.py, schwarzschild_generator.py, second_order_ode_generator.py, segment_partition_generator.py, separable_ode_generator.py, separable_pde_generator.py, series_convergence_generator.py, series_solution_generator.py, set_algebra_laws_generator.py, set_builder_roster_generator.py, set_counting_generator.py, set_expression_generator.py, set_identity_membership_table_generator.py, set_membership_subset_generator.py, set_operations_generator.py, shm_generator.py, sigma_notation_generator.py, signal_arithmetic_generator.py, similar_triangles_generator.py, simple_probability_generator.py, simple_stats_generator.py, simplex_generator.py, simplify_expression_generator.py, sinusoid_features_generator.py, slope_intercept_form_generator.py, slope_two_points_generator.py, softmax_gradient_generator.py, solid_revolution_generator.py, solution_chem_generator.py, special_relativity_generator.py, special_right_triangle_generator.py, special_solution_equation_generator.py, spherical_excess_generator.py, spherical_triangle_generator.py, spin_half_generator.py, stability_generator.py, standard_deviation_generator.py, standard_form_conversion_generator.py, standing_wave_generator.py, stars_and_bars_generator.py, statics_generator.py, statistics_generator.py, stereographic_generator.py, stoichiometry_generator.py, structure_constant_generator.py, subspace_basis_generator.py, svd_generator.py, svm_margin_generator.py, syllogism_generator.py, synthetic_division_generator.py, systems_elimination_generator.py, systems_substitution_generator.py, tangent_line_generator.py, taxicab_geometry_generator.py, taylor_series_generator.py, telescoping_generator.py, temperature_conversion_generator.py, tensor_product_generator.py, tip_bill_split_generator.py, tonelli_shanks_generator.py, totient_generator.py, transfer_function_generator.py, transformation_generator.py, transient_circuit_generator.py, transportation_generator.py, triangle_area_sas_generator.py, triangle_solve_generator.py, trig_equation_generator.py, trig_identity_eval_generator.py, trig_identity_verify_generator.py, trig_six_functions_generator.py, triple_integral_generator.py, truth_table_generator.py, turing_machine_trace_generator.py, two_sample_test_generator.py, two_step_equation_generator.py, two_step_inequality_generator.py, u_substitution_generator.py, uncertainty_generator.py, undetermined_coeff_generator.py, unification_generator.py, unit_circle_generator.py, unit_conversion_generator.py, unit_rate_generator.py, variation_parameters_generator.py, vector_ops_generator.py, vector_theorem_generator.py, venn_region_count_generator.py, viterbi_generator.py, volume_3d_generator.py, volume_rect_prism_generator.py, von_neumann_entropy_generator.py, wavefunction_generator.py, wff_parsing_generator.py, young_tableaux_generator.py, z_score_generator.py, z_transform_generator.py |
| `ZERO` | 1 | `ZERO\|s=-5` | transfer_function_generator.py |
| `ZERO_PRODUCT` | 2 | `ZERO_PRODUCT\|(x - 2)(x - 3)\|x = 2 or x = 3` | area_between_curves_generator.py, curve_analysis_generator.py, domain_range_generator.py, log_equation_generator.py, optimization_generator.py, polynomial_inequality_generator.py, polynomial_zeros_generator.py, quadratic_factoring_generator.py, radical_equation_generator.py, trig_equation_generator.py |
| `ZSCORE` | 2 | `ZSCORE\|(39 - 40)/2\|-0.5` | normal_table_generator.py, z_score_generator.py |
| `ZSCORE_FORMULA` | 1 | `ZSCORE_FORMULA\|z = (x - μ)/σ` | z_score_generator.py |
| `ZT_PAIR` | 1 | `ZT_PAIR\|Z{r^n u[n]}=1/(1-r z^-1)` | z_transform_generator.py |
| `ZT_SETUP` | 2, 3 | `ZT_SETUP\|geometric\|x[n]=21*8^n u[n]` | z_transform_generator.py |
