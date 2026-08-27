# Op-Code Legend

**Generated file — do not hand-edit.** Regenerate with `python tools/gen_opcode_legend.py` (verify freshness with `--check`).

The scratchpad vocabulary belongs to the model and evolves organically: generators may introduce new op-codes freely, and this legend is *descriptive*, not prescriptive. Steps are pipe-delimited strings (`CODE|field|field|...`, at most 4 payload fields) built with `helpers.step()`; the final step of every problem is `Z|<final_answer>`.

1637 distinct op-codes observed.

| Code | Payload fields | Example | Used by |
|---|---|---|---|
| `A` | 3 | `A\|46\|46\|92` | ac_circuit_generator.py, activation_generator.py, adam_step_generator.py, algorithm_trace_generator.py, angle_defect_generator.py, angle_measure_generator.py, annuity_generator.py, arithmetic_coding_generator.py, arithmetic_sequence_generator.py, attention_generator.py, backprop_generator.py, base_conversion_generator.py, bayesian_update_generator.py, binomial_probability_generator.py, bisection_generator.py, bond_pricing_generator.py, branching_ratio_generator.py, calendar_arithmetic_generator.py, calorimetry_generator.py, casimir_generator.py, cayley_table_generator.py, channel_capacity_generator.py, chi_square_generator.py, circle_equation_generator.py, classifier_metrics_generator.py, collision_generator.py, commutator_generator.py, complex_division_generator.py, complex_locus_generator.py, complex_number_ops_generator.py, composite_arithmetic_generator.py, conditional_probability_generator.py, confidence_interval_generator.py, conic_standard_form_generator.py, continued_fraction_generator.py, contour_integral_generator.py, convolution_generator.py, coset_generator.py, counterexample_search_generator.py, counting_classics_generator.py, crt_generator.py, curve_analysis_generator.py, cyclic_group_generator.py, de_moivre_generator.py, definite_integral_generator.py, density_matrix_generator.py, derangement_generator.py, derivative_limit_def_generator.py, determinant_generator.py, dft_generator.py, dijkstra_generator.py, distance_formula_generator.py, doppler_generator.py, dot_product_generator.py, dp_table_generator.py, einstein_summation_generator.py, electrostatics_generator.py, ellipse_features_generator.py, embedding_similarity_generator.py, energy_conservation_generator.py, entropy_change_generator.py, entropy_generator.py, entropy_rate_markov_generator.py, euler_characteristic_generator.py, euler_formula_generator.py, euler_method_generator.py, evaluate_expression_generator.py, expected_value_generator.py, exponential_model_generator.py, extended_euclid_generator.py, feature_map_generator.py, fill_in_step_generator.py, finance_generator.py, finite_field_generator.py, five_number_summary_generator.py, fixed_point_generator.py, flops_memory_generator.py, four_vector_generator.py, fractal_iteration_generator.py, fraction_op_generator.py, frequency_table_generator.py, function_composition_generator.py, function_evaluation_generator.py, function_inner_product_generator.py, function_operations_generator.py, function_table_generator.py, game_theory_generator.py, gaussian_curvature_generator.py, generating_function_generator.py, geometric_mean_generator.py, geometry_area_perimeter_generator.py, gradient_descent_generator.py, gradient_step_generator.py, graph_counting_generator.py, graph_interpret_generator.py, grassmann_generator.py, great_circle_generator.py, hamiltonian_generator.py, heat_engine_generator.py, hermitian_check_generator.py, horner_evaluation_generator.py, huffman_coding_generator.py, hyperbola_features_generator.py, hyperbolic_distance_generator.py, hyperbolic_function_generator.py, hypercube_counting_generator.py, inclusion_exclusion_generator.py, index_gymnastics_generator.py, information_gain_generator.py, integrating_factor_generator.py, interpolation_generator.py, invariant_mass_generator.py, joint_distribution_generator.py, kernel_evaluation_generator.py, kernel_perceptron_generator.py, kernel_ridge_generator.py, kl_divergence_generator.py, kmeans_step_generator.py, knn_generator.py, kraft_inequality_generator.py, ladder_operator_generator.py, lagrangian_generator.py, laplace_ivp_generator.py, layer_norm_generator.py, legendre_construction_generator.py, lhopital_generator.py, limit_evaluation_generator.py, linear_approx_generator.py, low_rank_approx_generator.py, lp_corner_generator.py, lr_schedule_generator.py, manual_square_root_generator.py, markov_chain_generator.py, matrix_calculus_generator.py, matrix_group_check_generator.py, matrix_norm_generator.py, matrix_ops_generator.py, mean_value_theorem_generator.py, mgf_generator.py, midpoint_generator.py, minkowski_interval_generator.py, mixed_number_operation_generator.py, mobius_transform_generator.py, modular_arithmetic_generator.py, mst_generator.py, mutual_information_generator.py, naive_bayes_generator.py, named_distribution_generator.py, nets_surface_area_generator.py, newtons_laws_generator.py, npv_irr_generator.py, operation_properties_generator.py, or_formula_generator.py, order_of_operations_generator.py, order_statistics_generator.py, parabola_features_generator.py, param_count_generator.py, partition_function_generator.py, pascal_triangle_generator.py, pca_generator.py, percent_word_problem_generator.py, perceptron_generator.py, permutation_group_generator.py, piecewise_evaluation_generator.py, polar_parametric_generator.py, polygon_perimeter_generator.py, polynomial_zeros_generator.py, portfolio_generator.py, probability_addition_rule_generator.py, pythag_hyp_generator.py, quantization_generator.py, quark_composition_generator.py, quaternion_generator.py, radical_add_sub_generator.py, radical_multiply_generator.py, rational_expr_add_sub_generator.py, recurrence_generator.py, recursive_explicit_generator.py, reed_solomon_generator.py, regression_generator.py, relativistic_energy_generator.py, remainder_factor_theorem_generator.py, riemann_sum_generator.py, riemann_tensor_generator.py, rotational_dynamics_generator.py, round_solids_generator.py, runge_kutta_generator.py, running_coupling_generator.py, rv_transform_generator.py, segment_partition_generator.py, separable_pde_generator.py, shm_generator.py, sigma_notation_generator.py, simple_stats_generator.py, simplex_generator.py, softmax_gradient_generator.py, solution_chem_generator.py, spherical_excess_generator.py, spherical_triangle_generator.py, spin_half_generator.py, standard_deviation_generator.py, stars_and_bars_generator.py, statics_generator.py, stereographic_generator.py, svm_margin_generator.py, synthetic_division_generator.py, tangent_line_generator.py, taxicab_geometry_generator.py, taylor_series_generator.py, temperature_conversion_generator.py, tip_bill_split_generator.py, transfer_function_generator.py, transformation_generator.py, transportation_generator.py, triangle_solve_generator.py, trig_identity_eval_generator.py, trig_six_functions_generator.py, two_sample_test_generator.py, undetermined_coeff_generator.py, variation_parameters_generator.py, vector_ops_generator.py, venn_region_count_generator.py, von_neumann_entropy_generator.py, wavefunction_generator.py, young_tableaux_generator.py, z_score_generator.py |
| `ABS` | 2 | `ABS\|5/13\|5/13` | fixed_point_generator.py, matrix_norm_generator.py, rv_transform_generator.py |
| `ABSORB_EQ` | 2 | `ABSORB_EQ\|u0=p0A+p00*u0+p01*u1\|u1=p1A+p10*u0+p11*u1` | markov_chain_generator.py |
| `ABS_CASE` | 2 | `ABS_CASE\|Case 1\|x - 6 = 1` | absolute_value_equation_generator.py |
| `ABS_CHECK` | 2 | `ABS_CHECK\|-3 < 0\|Absolute value cannot be negative` | absolute_value_equation_generator.py |
| `ABS_ERROR` | 2 | `ABS_ERROR\|1\|1/50` | quantization_generator.py |
| `ABS_INEQ_CHECK` | 2 | `ABS_INEQ_CHECK\|-1 < 0\|Absolute value is always non-negative` | absolute_value_inequality_generator.py |
| `ABS_INEQ_PART` | 2 | `ABS_INEQ_PART\|Part 1\|4x - 9 ≥ 9 -> x ≥ 9/2` | absolute_value_inequality_generator.py |
| `ABS_INEQ_SETUP` | 1 | `ABS_INEQ_SETUP\|abs(4x - 9) ≥ 9` | absolute_value_inequality_generator.py |
| `ABS_INEQ_SPECIAL` | 2 | `ABS_INEQ_SPECIAL\|c = 0\|Check logic for >=` | absolute_value_inequality_generator.py |
| `ABS_INEQ_SPLIT` | 2 | `ABS_INEQ_SPLIT\|OR case\|4x - 9 ≥ 9 or 4x - 9 ≤ -9` | absolute_value_inequality_generator.py |
| `ABS_SETUP` | 1 | `ABS_SETUP\|abs(x - 6) = 1` | absolute_value_equation_generator.py |
| `ABS_SPLIT` | 2, 3 | `ABS_SPLIT\|Two cases\|x - 6 = 1\|x - 6 = -1` | absolute_value_equation_generator.py |
| `ABS_VAL` | 2 | `ABS_VAL\|(-15)\|15` | taxicab_geometry_generator.py |
| `AB_ADD` | 3 | `AB_ADD\|+4000\|5230\|9230` | abacus_addition_generator.py |
| `AB_SET` | 1 | `AB_SET\|5230` | abacus_addition_generator.py |
| `ACCEPT` | 1, 2 | `ACCEPT\|x = −10` | conditional_forms_generator.py, counterexample_search_generator.py, factor_trinomial_generator.py, knights_knaves_generator.py, log_conversion_generator.py, log_equation_generator.py, optimization_generator.py, polynomial_inequality_generator.py, radical_equation_generator.py, rational_equation_generator.py, rational_root_generator.py, set_builder_roster_generator.py |
| `ACT_DERIV` | 3 | `ACT_DERIV\|relu\|1\|1` | activation_generator.py |
| `ACT_SETUP` | 3 | `ACT_SETUP\|activation=relu\|x=3\|w1=3,b1=-8,w2=-3,b2=5` | activation_generator.py |
| `ACT_VALUE` | 3 | `ACT_VALUE\|relu\|1\|1` | activation_generator.py |
| `AC_COMPLEX` | 3 | `AC_COMPLEX\|Z\|9\|0j` | ac_circuit_generator.py |
| `AC_FORMULA` | 1 | `AC_FORMULA\|omega0^2=1/(L*C)` | ac_circuit_generator.py |
| `AC_PRODUCT` | 2 | `AC_PRODUCT\|3 × (-12)\|-36` | factor_trinomial_generator.py |
| `AC_SETUP` | 3 | `AC_SETUP\|resonance\|R=9, L=2\|C=1/200` | ac_circuit_generator.py |
| `ADAM_SETUP` | 3 | `ADAM_SETUP\|theta=-17,g=3\|beta1=9/10,beta2=99/100\|lr=1/20,epsilon=0` | adam_step_generator.py |
| `ADAM_UPDATE` | 2 | `ADAM_UPDATE\|theta_new\|-341/20` | adam_step_generator.py |
| `ADD_COL` | 3 | `ADD_COL\|col_1\|0+0+0\|->0 (carry 0)` | multi_digit_addition_generator.py |
| `ADD_FORMULA` | 1 | `ADD_FORMULA\|P(A ∪ B) = P(A) + P(B) - P(A ∩ B)` | probability_addition_rule_generator.py |
| `ADD_PARTIALS` | 2 | `ADD_PARTIALS\|410370 + 3419750 + 61555500 + 68395000\|133780620` | decimal_mult_generator.py, multi_digit_multiplication_generator.py |
| `ADD_SETUP` | 2 | `ADD_SETUP\|fair die; A = [5, 6], B = [4, 5, 6]\|P(A ∪ B)` | probability_addition_rule_generator.py |
| `ADJOINT` | 1 | `ADJOINT\|A^dagger=[[17,2],[2,17]]` | hermitian_check_generator.py |
| `ADJ_LIST` | 2 | `ADJ_LIST\|A\|B, D, E` | euler_circuit_generator.py, graph_traversal_generator.py |
| `ALG_SETUP` | 3 | `ALG_SETUP\|insertion sort\|passes 4\|values 25, 13, 12, 32, 10, 15, 35` | algorithm_trace_generator.py |
| `ALIGN_NUM` | 2 | `ALIGN_NUM\|046.36\|177.07` | number_comparison_generator.py |
| `ALPHA` | 2 | `ALPHA\|alpha1\|75/64` | kernel_ridge_generator.py |
| `ALPHA_RENAME` | 2 | `ALPHA_RENAME\|lambda m. (d m)\|lambda z. (d z)` | lambda_reduction_generator.py |
| `AMORT_ROW` | 3 | `AMORT_ROW\|1\|interest=$16440.00\|principal=$3135.00,balance=$79065.00` | annuity_generator.py |
| `AMPLITUDE` | 2 | `AMPLITUDE\|abs(1)\|1` | sinusoid_features_generator.py |
| `ANALOGY_SETUP` | 3 | `ANALOGY_SETUP\|man=(2,-4)\|woman=(2,-2)\|king=(2,-1)` | embedding_similarity_generator.py |
| `ANALOGY_VECTOR` | 2 | `ANALOGY_VECTOR\|king-man+woman\|(2,1)` | embedding_similarity_generator.py |
| `ANGLE` | 2 | `ANGLE\|theta\|pi/2` | positional_encoding_generator.py |
| `ANGLE_DEFECT_SETUP` | 2 | `ANGLE_DEFECT_SETUP\|R=4\|angles=45,45,75` | angle_defect_generator.py |
| `ANGLE_EVAL` | 2 | `ANGLE_EVAL\|theta=0..2*pi\|2*pi` | triple_integral_generator.py |
| `ANGLE_FORMULA` | 1 | `ANGLE_FORMULA\|quadrant I: reference = θ` | angle_measure_generator.py |
| `ANGLE_RELATION` | 1 | `ANGLE_RELATION\|angle1 + angle2 = 90°` | angle_relationships_generator.py |
| `ANGLE_SETUP` | 2 | `ANGLE_SETUP\|complementary\|angle1 = 15°` | angle_relationships_generator.py |
| `ANGLE_SOLVE` | 2 | `ANGLE_SOLVE\|90 - 15\|75` | angle_relationships_generator.py |
| `ANGLE_WRAP` | 2 | `ANGLE_WRAP\|337 deg\|-23 deg` | complex_log_generator.py |
| `ANNUITY_FORMULA` | 1 | `ANNUITY_FORMULA\|PV = PMT*(1 - (1+r)^(-n))/r` | annuity_generator.py |
| `ANNUITY_SETUP` | 2, 3 | `ANNUITY_SETUP\|ordinary annuity present value\|PMT=9740,r=25%,n=3` | annuity_generator.py |
| `ANTICOMM_ENTRY` | 3 | `ANTICOMM_ENTRY\|(1,1)\|0 + 0\|0` | pauli_algebra_generator.py |
| `ANTIDERIV` | 2 | `ANTIDERIV\|2 cos(x)\|2 sin(x)` | antiderivative_generator.py, arc_length_generator.py, area_between_curves_generator.py, definite_integral_generator.py, improper_integral_generator.py, integrating_factor_generator.py, integration_by_parts_generator.py, ode_substitution_generator.py, parametric_calculus_generator.py, partial_fractions_generator.py, separable_ode_generator.py, solid_revolution_generator.py, u_substitution_generator.py, variation_parameters_generator.py |
| `ANTIDERIVATIVE` | 1 | `ANTIDERIVATIVE\|-A*cos(nx)/n` | fourier_series_generator.py |
| `ANTISYM_CHECK` | 3 | `ANTISYM_CHECK\|(2, 4)\|reverse (4, 2)\|violation` | relation_check_generator.py |
| `APPLY_GATE` | 3 | `APPLY_GATE\|X\|e^(i229π/233)·ket0\|e^(i229π/233)·ket1` | quantum_gate_generator.py |
| `APPLY_OPERATOR` | 2 | `APPLY_OPERATOR\|L[Ae^x]\|A(1 + 6 + 8)e^x` | commutator_generator.py, undetermined_coeff_generator.py |
| `APPLY_PAULI` | 2 | `APPLY_PAULI\|sigma_y ket0\|i ket1` | spin_half_generator.py |
| `APPLY_SUBST` | 1 | *(not observed in sampling)* | unification_generator.py |
| `APPROX` | 2 | `APPROX\|12*d^2*L\|2617245696` | param_count_generator.py |
| `APPROX_ENTRY` | 2 | `APPROX_ENTRY\|(1,1)\|0` | low_rank_approx_generator.py |
| `APPROX_SETUP` | 2 | `APPROX_SETUP\|estimate √80\|linearize f(x) = √x at a = 81` | linear_approx_generator.py |
| `ARCCOS` | 2 | `ARCCOS\|cos(c)=-1/2\|c=2pi/3` | great_circle_generator.py |
| `ARCLEN_FORMULA` | 1 | `ARCLEN_FORMULA\|L = ∫ √((dx/dt)^2 + (dy/dt)^2) dt` | arc_length_generator.py, parametric_calculus_generator.py |
| `ARC_FORMULA` | 1 | `ARC_FORMULA\|L = (θ/360)·2πr` | arc_sector_generator.py |
| `ARC_LENGTH` | 3 | `ARC_LENGTH\|int_0^T speed dt\|5*2\|10` | curve_geometry_generator.py |
| `ARC_SETUP` | 2 | `ARC_SETUP\|circle r = 34, central angle 17π/12 rad\|sector area` | arc_sector_generator.py |
| `AREA` | 1 | `AREA\|66` | geometry_area_perimeter_generator.py |
| `AREA_INT` | 3 | `AREA_INT\|A = int y dx\|3*12^3/3\|1728` | centroid_generator.py |
| `AREA_INTEGRAL` | 2 | `AREA_INTEGRAL\|sqrt(EG-F^2)=R^2 sin(phi)\|area = R^2*theta*(cos phi1 - cos phi2)` | fundamental_form_generator.py |
| `AREA_SCALE` | 3 | `AREA_SCALE\|uv rectangle area\|7*9\|63` | jacobian_generator.py |
| `AREA_SETUP` | 2 | `AREA_SETUP\|y = x^2 + 29x + 74 and y = -x^2 + 3x - 6\|area between the curves` | area_between_curves_generator.py |
| `ARGUMENT` | 2 | `ARGUMENT\|(-2,2)\|135 deg` | complex_log_generator.py, euler_formula_generator.py |
| `ARITH_INTERVAL` | 1 | `ARITH_INTERVAL\|[5/8,3/4)` | arithmetic_coding_generator.py |
| `ARITH_SETUP` | 2 | `ARITH_SETUP\|A=1/2, B=1/8, C=1/8, D=1/4\|message=CCCBAD` | arithmetic_coding_generator.py |
| `ARITH_SYMBOL` | 2 | `ARITH_SYMBOL\|C\|cum=[5/8,3/4)` | arithmetic_coding_generator.py |
| `ARRAY_STATE` | 2 | `ARRAY_STATE\|pass 1\|13, 25, 12, 32, 10, 15, 35` | algorithm_trace_generator.py |
| `ASSIGN` | 2 | `ASSIGN\|P1\|C2` | kmeans_step_generator.py |
| `ASYMPTOTE` | 1 | `ASYMPTOTE\|y = -1 ± (12/5)(x + 3)` | hyperbola_features_generator.py |
| `ATA` | 2 | `ATA\|A^T A\|[[421, 420], [420, 421]]` | svd_generator.py |
| `ATOM_CHECK` | 3 | `ATOM_CHECK\|Al\|left=4\|right=4` | stoichiometry_generator.py |
| `ATTN_OUTPUT` | 2 | `ATTN_OUTPUT\|1\|[[-11/2,1/2]]` | attention_generator.py |
| `ATTN_SCORE` | 2 | `ATTN_SCORE\|1,1\|0` | attention_generator.py |
| `ATTN_SETUP` | 1, 3 | `ATTN_SETUP\|tokens=2,d=2\|Q=[[0,0], [0,0]]\|K=[[0,0], [0,0]]` | attention_generator.py |
| `ATTR_CHECK` | 3 | `ATTR_CHECK\|4\|A: odd\|no` | attribute_sorting_generator.py |
| `AV_VECTOR` | 2 | `AV_VECTOR\|A*v1\|[29/√2, 29/√2]` | svd_generator.py |
| `B` | 1, 3 | `B\|38\|1\|381` | decimal_div_generator.py, long_division_generator.py, percent_problem_generator.py, polynomial_long_division_generator.py |
| `BABY_STEP` | 2 | `BABY_STEP\|j=0\|1` | baby_step_giant_step_generator.py |
| `BACKPROP_DELTA` | 2 | `BACKPROP_DELTA\|h1\|delta=4` | backprop_generator.py |
| `BACKPROP_GRAD` | 2 | `BACKPROP_GRAD\|dL/dy_hat\|-4` | backprop_generator.py |
| `BACKPROP_SETUP` | 3 | `BACKPROP_SETUP\|x=(2,2)\|y=2\|eta=1/4` | backprop_generator.py |
| `BACK_SUB` | 2 | `BACK_SUB\|u = 1/y\|y = 1/(5 - e^x)` | ode_substitution_generator.py |
| `BACK_SUB_ROW` | 3 | `BACK_SUB_ROW\|r=511\|x=1\|y=0` | extended_euclid_generator.py, modular_inverse_generator.py, rsa_generator.py |
| `BALANCED_EQ` | 1 | `BALANCED_EQ\|4 Al + 3 O2 -> 2 Al2O3` | stoichiometry_generator.py |
| `BALANCE_COEFFS` | 2 | `BALANCE_COEFFS\|reactants=4,3\|products=2` | stoichiometry_generator.py |
| `BASE_ADD_COL` | 3 | `BASE_ADD_COL\|col 0\|0 + 1 + carry 0\|1 -> digit 1, carry 0` | base_arithmetic_generator.py |
| `BASE_ARITH_SETUP` | 2 | `BASE_ARITH_SETUP\|base 16\|920 * F` | base_arithmetic_generator.py |
| `BASE_CARRY` | 2 | `BASE_CARRY\|carry 8\|digit 8, carry 0` | base_arithmetic_generator.py |
| `BASE_MUL_COL` | 3 | `BASE_MUL_COL\|col 0\|0 * F + carry 0\|0 -> digit 0, carry 0` | base_arithmetic_generator.py |
| `BASE_SETUP` | 2 | `BASE_SETUP\|DCB_16\|decimal` | base_conversion_generator.py |
| `BAYES_CELL` | 3 | `BAYES_CELL\|true positive\|80 * 9/10\|72` | conditional_probability_generator.py |
| `BAYES_FORMULA` | 1 | `BAYES_FORMULA\|P(disease=no given negative) = TN/(TN + FN)` | conditional_probability_generator.py |
| `BAYES_SETUP` | 3 | `BAYES_SETUP\|disease=yes 80, disease=no 280\|sensitivity 9/10, specificity 19/20\|P(disease=no given test negative)` | conditional_probability_generator.py |
| `BAYES_UPDATE_SETUP` | 2, 3 | `BAYES_UPDATE_SETUP\|beta_binomial\|prior=Beta(12,8)\|successes=17, trials=26` | bayesian_update_generator.py |
| `BCH_FORM` | 2 | `BCH_FORM\|A+B+1/2[A,B]\|[[0, 3, 0], [0, 0, 0], [-1, 3/2, 0]]` | bch_generator.py |
| `BCH_SETUP` | 3 | `BCH_SETUP\|A=3E12\|B=-E31\|order=2` | bch_generator.py |
| `BEC_FORMULA` | 1 | `BEC_FORMULA\|P(exactly one)=C(n,1)*epsilon*(1-epsilon)^(n-1)` | bec_channel_generator.py |
| `BEC_SETUP` | 1 | `BEC_SETUP\|epsilon=1/3` | bec_channel_generator.py |
| `BEREZIN_RULE` | 2 | `BEREZIN_RULE\|int dtheta 1\|0` | grassmann_generator.py |
| `BETA` | 1 | `BETA\|(lambda c. d) applied to (lambda c. (lambda p. p))` | lambda_reduction_generator.py |
| `BEZOUT_CHECK` | 2 | `BEZOUT_CHECK\|511*19 + 294*-33\|7` | extended_euclid_generator.py |
| `BIAS_CORRECT` | 2 | `BIAS_CORRECT\|m_hat\|3` | adam_step_generator.py |
| `BINARY_EXPONENT` | 2 | `BINARY_EXPONENT\|42\|101010` | mod_exp_generator.py, quadratic_residue_generator.py |
| `BINOM_FORMULA` | 1 | `BINOM_FORMULA\|P(X ≤ k) = Σ C(n,i)·p^i·(1-p)^(n-i)` | binomial_probability_generator.py |
| `BINOM_SETUP` | 2 | `BINOM_SETUP\|n = 5, p = 3/4\|P(X ≤ 1)` | binomial_probability_generator.py |
| `BISECTION_SETUP` | 3 | `BISECTION_SETUP\|f(x)=x^2-24\|interval=[4, 5]\|iterations=4` | bisection_generator.py |
| `BISECT_UPDATE` | 3 | `BISECT_UPDATE\|1\|product > 0\|[9/2, 5]` | bisection_generator.py |
| `BIT_ROW` | 2, 3 | `BIT_ROW\|bit 0\|0 OR 0\|0` | bitwise_ops_generator.py |
| `BIT_RULE` | 2 | `BIT_RULE\|OR\|1 when at least one bit is 1` | bitwise_ops_generator.py |
| `BIT_SETUP` | 2 | `BIT_SETUP\|0110 OR 1100\|4-bit mask` | bitwise_ops_generator.py |
| `BLACKBODY_FORMULA` | 1 | `BLACKBODY_FORMULA\|P=sigma*A*T^4` | blackbody_generator.py |
| `BLACKBODY_SETUP` | 3 | `BLACKBODY_SETUP\|stefan_power\|sigma=8, A=18\|T=10` | blackbody_generator.py |
| `BOND_FORMULA` | 1 | `BOND_FORMULA\|price=sum coupon/(1+y)^t + face/(1+y)^n` | bond_pricing_generator.py |
| `BOND_PRICE` | 1 | `BOND_PRICE\|$8000.00` | bond_pricing_generator.py |
| `BOND_SETUP` | 2 | `BOND_SETUP\|face=8000\|coupon=10%,ytm=10%,years=5` | bond_pricing_generator.py |
| `BOOL_SETUP` | 2 | `BOOL_SETUP\|variables V, W, X, Y\|CNF from F=0 rows` | boolean_algebra_generator.py |
| `BORROW` | 3 | `BORROW\|col_1\|from_left\|1` | multi_digit_subtraction_generator.py |
| `BOX_FORMULA` | 1 | `BOX_FORMULA\|E_n=n^2*h^2/(8*m*L^2)` | particle_in_box_generator.py |
| `BOX_SETUP` | 1, 3 | `BOX_SETUP\|energy_level\|n=7, h=9\|m=5, L=2` | particle_in_box_generator.py |
| `BRAKET_FORMULA` | 1 | `BRAKET_FORMULA\|U=diag(phases)` | braket_generator.py |
| `BRAKET_SETUP` | 3 | `BRAKET_SETUP\|time_evolution\|psi=[1-i,1+i]\|phases=[i,i]` | braket_generator.py |
| `BRANCH_TEST` | 2 | `BRANCH_TEST\|9.5 <= 2\|no` | piecewise_evaluation_generator.py |
| `BRANCH_USE` | 1 | `BRANCH_USE\|$8.75` | piecewise_evaluation_generator.py |
| `BRING_DOWN` | 2 | `BRING_DOWN\|group 16\|current = 16` | composite_arithmetic_generator.py, manual_square_root_generator.py |
| `BSC_FORMULA` | 1 | `BSC_FORMULA\|H_b=p*(-log2 p)+(1-p)*(-log2(1-p))` | channel_capacity_generator.py |
| `BSC_SETUP` | 3 | `BSC_SETUP\|p=9/100\|-log2(p)=3.474\|-log2(1-p)=0.136` | channel_capacity_generator.py |
| `BSGS_MATCH` | 3 | `BSGS_MATCH\|i=1\|j=1\|x=6` | baby_step_giant_step_generator.py |
| `BSGS_SETUP` | 4 | `BSGS_SETUP\|p=23\|g=5\|h=8\|m=5` | baby_step_giant_step_generator.py |
| `BS_FORMULA` | 2 | `BS_FORMULA\|C=S*N(d1)-K*df*N(d2)\|P=K*df*N(-d2)-S*N(-d1)` | black_scholes_generator.py |
| `BS_RESULT` | 2 | `BS_RESULT\|call=16.2\|put=4.2` | black_scholes_generator.py |
| `BS_SETUP` | 3 | `BS_SETUP\|S=120,K=120\|df=0.9\|N_d1=0.9,N_d2=0.85` | black_scholes_generator.py |
| `C` | 3 | `C\|1/3\|21\|7/21` | fraction_comparison_generator.py, fraction_op_generator.py, mixed_number_operation_generator.py, rational_expr_add_sub_generator.py |
| `CALC` | 1 | `CALC\|y = 8` | systems_elimination_generator.py, systems_substitution_generator.py |
| `CAL_DIVMOD` | 3 | `CAL_DIVMOD\|41\|7\|5 R6` | calendar_arithmetic_generator.py |
| `CAL_FORMULA` | 1 | `CAL_FORMULA\|warm ice: q1=m*c_ice*(0-Ti)` | calorimetry_generator.py |
| `CAL_SETUP` | 3 | `CAL_SETUP\|2026-08-06 through 2026-09-15\|count Sunday\|inclusive` | calendar_arithmetic_generator.py, calorimetry_generator.py |
| `CANCEL` | 2 | `CANCEL\|3n\|4n - 3` | derivative_limit_def_generator.py, derivative_transcendental_generator.py, limit_evaluation_generator.py, power_series_generator.py, rational_expr_mult_div_generator.py, rational_expr_simplify_generator.py, rational_function_features_generator.py, series_convergence_generator.py, trig_identity_verify_generator.py |
| `CANDIDATES` | 1 | `CANDIDATES\|±1, ±2, ±3, ±6, ±9, ±18` | rational_root_generator.py |
| `CANONICAL_ORDER` | 1 | `CANONICAL_ORDER\|C=1, D=2, A=3, B=4, E=4` | kraft_inequality_generator.py |
| `CANONICAL_SHIFT` | 3 | `CANONICAL_SHIFT\|code=0\|left=1\|0` | kraft_inequality_generator.py |
| `CARRY_FINAL` | 1 | `CARRY_FINAL\|1` | multi_digit_addition_generator.py |
| `CARTESIAN_RESULT` | 1 | `CARTESIAN_RESULT\|{(a, 1), (a, 2)}` | set_operations_generator.py |
| `CART_PAIR` | 3 | `CART_PAIR\|a\|1\|(a, 1)` | set_operations_generator.py |
| `CASE` | 1 | `CASE\|Bea=knight, Oona=knight` | knights_knaves_generator.py |
| `CASHFLOW_PV` | 2 | `CASHFLOW_PV\|coupon_t1\|8000/11` | bond_pricing_generator.py |
| `CASIMIR_FORCE_SETUP` | 2 | `CASIMIR_FORCE_SETUP\|F/A=-π^2*hbar*c/(240*d^4)\|hbar=12,c=10,d=5` | casimir_force_generator.py |
| `CASIMIR_SETUP` | 3 | `CASIMIR_SETUP\|spin=1\|hbar=19/11\|J^2=Jz^2+(J+J-+J-J+)/2` | casimir_generator.py |
| `CAYLEY_HEADER` | 1 | `CAYLEY_HEADER\|1, 3, 5, 9, 11, 13, 15, 17, 19, 23, 25, 27` | cayley_table_generator.py |
| `CAYLEY_ROW` | 2 | `CAYLEY_ROW\|row 1\|1, 3, 5, 9, 11, 13, 15, 17, 19, 23, 25, 27` | cayley_table_generator.py |
| `CBRT` | 2 | `CBRT\|125w^3\|5w` | factor_special_forms_generator.py, inverse_function_generator.py, rational_exponent_generator.py |
| `CDF_EVENT` | 3 | `CDF_EVENT\|Y<=y\|X^2<=y\|X<=sqrt(y)` | rv_transform_generator.py |
| `CDF_FORMULA` | 2 | `CDF_FORMULA\|F_Y(y)=sqrt(y)/19\|0<=y<=361` | rv_transform_generator.py |
| `CEIL` | 2 | `CEIL\|870.9456\|871` | confidence_interval_generator.py |
| `CENTER` | 1, 2 | `CENTER\|(-4, 2)` | circle_equation_generator.py, ellipse_features_generator.py, hyperbola_features_generator.py, pca_generator.py |
| `CENTROID_COORD` | 3 | `CENTROID_COORD\|xbar = M_y/A\|(15552)/(1728)\|9` | centroid_generator.py |
| `CENTROID_SETUP` | 3 | `CENTROID_SETUP\|0 <= y <= 3*x^2\|0 <= x <= 12\|centroid` | centroid_generator.py |
| `CENTROID_UPDATE` | 2 | `CENTROID_UPDATE\|C1\|(-1,4)` | kmeans_step_generator.py |
| `CF_PARTIAL` | 2 | `CF_PARTIAL\|a_0\|1` | continued_fraction_generator.py |
| `CF_RESULT` | 1 | `CF_RESULT\|[1; 3, 1, 16, 2]` | continued_fraction_generator.py |
| `CF_SETUP` | 1 | `CF_SETUP\|173/138` | continued_fraction_generator.py |
| `CG_COEFF` | 2 | `CG_COEFF\|ket(+,-)\|-1/sqrt2` | clebsch_gordan_generator.py |
| `CG_SETUP` | 3 | `CG_SETUP\|j1=1/2\|j2=1/2\|phase=-` | clebsch_gordan_generator.py |
| `CG_STATE` | 2 | `CG_STATE\|J=1, M=0\|-1/sqrt2*ket(+,-) - 1/sqrt2*ket(-,+)` | clebsch_gordan_generator.py |
| `CHAIN_DERIV` | 2 | `CHAIN_DERIV\|dy/dx\|-9` | activation_generator.py |
| `CHAIN_RATE` | 2 | `CHAIN_RATE\|dx/dt\|4` | multivar_chain_rule_generator.py |
| `CHAIN_SUM` | 3 | `CHAIN_SUM\|f_x*dx/dt + f_y*dy/dt\|0*4 + (-5)*(-2)\|10` | multivar_chain_rule_generator.py |
| `CHAIN_VALUE` | 3 | `CHAIN_VALUE\|x(-1)\|4*(-1) + (-5)\|-9` | multivar_chain_rule_generator.py |
| `CHANGE_BASE` | 1 | `CHANGE_BASE\|log_32(64) = log_2(64)/log_2(32)` | log_conversion_generator.py |
| `CHAR_DIAG` | 2 | `CHAR_DIAG\|diagonal of λI - A\|(λ + 4), (λ - 3), (λ - 5)` | eigenvalue_generator.py |
| `CHAR_EQ` | 2 | `CHAR_EQ\|assume y=e^(rx)\|r^2 - r - 12 = 0` | ode_system_generator.py, second_order_ode_generator.py, undetermined_coeff_generator.py, variation_parameters_generator.py |
| `CHAR_POLY` | 2 | `CHAR_POLY\|p(λ) = λ^3 - 4λ^2 - 17λ + 60\|(λ + 4)*(λ - 3)*(λ - 5)` | diagonalization_generator.py, eigenvalue_generator.py, recurrence_generator.py |
| `CHAR_ROOTS` | 2 | `CHAR_ROOTS\|r1 = -3, r2 = 4\|distinct real` | recurrence_generator.py, second_order_ode_generator.py, undetermined_coeff_generator.py, variation_parameters_generator.py |
| `CHAR_SETUP` | 2 | `CHAR_SETUP\|p(λ) = det(λI - A)\|triangular determinant` | eigenvalue_generator.py |
| `CHECK` | 2, 3 | `CHECK\|multiply_back\|23×98+45=2299\|2299` | annuity_generator.py, area_between_curves_generator.py, arithmetic_sequence_generator.py, baby_step_giant_step_generator.py, base_arithmetic_generator.py, bch_generator.py, bitwise_ops_generator.py, boolean_algebra_generator.py, casimir_generator.py, cauchy_riemann_generator.py, chi_square_generator.py, cholesky_generator.py, clebsch_gordan_generator.py, commutator_generator.py, completing_square_generator.py, conditional_probability_generator.py, convolutional_code_viterbi_generator.py, coset_generator.py, cramers_rule_generator.py, cyclic_group_generator.py, cyk_parser_generator.py, dfa_minimization_generator.py, dfa_simulation_generator.py, diagonalization_generator.py, diffie_hellman_generator.py, ecdh_generator.py, ecdsa_generator.py, eigenvalue_generator.py, elliptic_curve_finite_field_generator.py, embedding_similarity_generator.py, equilibrium_ice_generator.py, error_spotting_generator.py, euler_circuit_generator.py, exact_ode_generator.py, expected_value_generator.py, extended_euclid_generator.py, factor_gcf_generator.py, factor_grouping_generator.py, factor_special_forms_generator.py, factor_trinomial_generator.py, feature_map_generator.py, fill_in_step_generator.py, five_number_summary_generator.py, function_inner_product_generator.py, game_theory_generator.py, gamma_matrix_generator.py, gauss_bonnet_generator.py, gaussian_curvature_generator.py, geometric_mean_generator.py, geometric_probability_generator.py, geometric_sequence_generator.py, gradient_generator.py, gram_schmidt_generator.py, graph_counting_generator.py, hamming_code_generator.py, hermitian_check_generator.py, hessian_classify_generator.py, horner_evaluation_generator.py, hyperbolic_function_generator.py, hypothesis_test_generator.py, index_gymnastics_generator.py, induction_verify_generator.py, information_gain_generator.py, inverse_function_generator.py, kernel_perceptron_generator.py, kernel_validity_generator.py, kmeans_step_generator.py, knights_knaves_generator.py, knn_generator.py, ladder_operator_generator.py, lagrange_multiplier_generator.py, least_squares_generator.py, legendre_construction_generator.py, lhopital_generator.py, lie_exponential_generator.py, limit_evaluation_generator.py, line_integral_generator.py, linear_fractional_generator.py, lll_reduction_generator.py, log_equation_generator.py, long_division_generator.py, low_rank_approx_generator.py, lp_corner_generator.py, lu_decomposition_generator.py, lz_compression_generator.py, manual_square_root_generator.py, markov_chain_generator.py, matrix_exponential_generator.py, matrix_group_check_generator.py, matrix_inverse_generator.py, mean_value_theorem_generator.py, method_of_moments_generator.py, mle_generator.py, mobius_transform_generator.py, modular_arithmetic_generator.py, modular_inverse_generator.py, naive_bayes_generator.py, nfa_simulation_generator.py, ode_system_generator.py, operation_properties_generator.py, or_formula_generator.py, partial_derivative_generator.py, partial_trace_generator.py, pauli_algebra_generator.py, pca_generator.py, pda_simulation_generator.py, perceptron_generator.py, pollard_factorization_generator.py, polynomial_inequality_generator.py, positive_definite_generator.py, power_series_generator.py, prime_factorization_generator.py, projector_generator.py, qr_decomposition_generator.py, quadratic_factoring_generator.py, quadratic_square_root_generator.py, quaternion_generator.py, radical_variable_simplify_generator.py, ratio_table_generator.py, recursive_explicit_generator.py, regex_to_automaton_generator.py, resolution_proof_generator.py, riemann_tensor_generator.py, rotational_dynamics_generator.py, routh_hurwitz_generator.py, rsa_generator.py, running_coupling_generator.py, rv_transform_generator.py, series_convergence_generator.py, shm_generator.py, signal_arithmetic_generator.py, similar_triangles_generator.py, simplex_generator.py, special_solution_equation_generator.py, statics_generator.py, stereographic_generator.py, structure_constant_generator.py, svd_generator.py, svm_margin_generator.py, systems_elimination_generator.py, taylor_series_generator.py, tip_bill_split_generator.py, tonelli_shanks_generator.py, totient_generator.py, transportation_generator.py, turing_machine_trace_generator.py, two_sample_test_generator.py, two_step_equation_generator.py, uncertainty_generator.py, venn_region_count_generator.py, young_tableaux_generator.py, z_score_generator.py |
| `CHECK_POINT` | 3 | `CHECK_POINT\|x=0\|15·0 + 13 = 13\|15·0 + 13 = 13` | special_solution_equation_generator.py |
| `CHINCHILLA` | 2 | `CHINCHILLA\|20N\|1920000000` | scaling_law_generator.py |
| `CHI_FORMULA` | 1 | `CHI_FORMULA\|E = (row·col)/N; χ² = Σ (O - E)^2/E` | chi_square_generator.py |
| `CHI_SETUP` | 2 | `CHI_SETUP\|row 1: 22, 58; row 2: 58, 62; N = 200\|independence; df = 1, critical value = 3.841` | chi_square_generator.py |
| `CHI_TERM` | 3 | `CHI_TERM\|22 - 32 = -10\|(-10)^2 = 100\|100/32 = 3.125` | chi_square_generator.py |
| `CHOLESKY_ENTRY` | 2 | `CHOLESKY_ENTRY\|l11\|3` | cholesky_generator.py |
| `CHOL_SETUP` | 2 | `CHOL_SETUP\|A = [[9, 3, -3], [3, 10, 11], [-3, 11, 21]]\|A = L L^T` | cholesky_generator.py |
| `CHRISTOFFEL_FORMULA` | 1 | `CHRISTOFFEL_FORMULA\|Gamma^i_jk = 1/2 g^im(d_j g_mk + d_k g_mj - d_m g_jk)` | christoffel_generator.py |
| `CHRISTOFFEL_SETUP` | 3 | `CHRISTOFFEL_SETUP\|polar\|g_rr=1, g_thetatheta=r^2\|r=5` | christoffel_generator.py |
| `CHRISTOFFEL_VALUE` | 2 | `CHRISTOFFEL_VALUE\|Gamma^phi_thetatheta\|-60/169` | riemann_tensor_generator.py |
| `CIRCLE_ANGLE_SETUP` | 2 | `CIRCLE_ANGLE_SETUP\|central angle 70° subtends an arc\|inscribed angle on the same arc` | circle_angle_generator.py |
| `CIRCLE_CALCULATE` | 2 | `CIRCLE_CALCULATE\|radius = diameter / 2 = 34 / 2\|17` | circle_generator.py |
| `CIRCLE_EQ` | 1 | `CIRCLE_EQ\|(x + 2)^2 + (y + 5)^2 = 25` | complex_locus_generator.py |
| `CIRCLE_FORMULA` | 1 | `CIRCLE_FORMULA\|A = πr²` | circle_generator.py |
| `CIRCLE_SETUP` | 2 | `CIRCLE_SETUP\|34\|diameter` | circle_equation_generator.py, circle_generator.py |
| `CIRCLE_SUBSTITUTE` | 1 | `CIRCLE_SUBSTITUTE\|A = π × 17²` | circle_generator.py |
| `CIRCULATION_SUM` | 2 | `CIRCULATION_SUM\|(5 - 0)*28\|140` | vector_theorem_generator.py |
| `CI_FORMULA` | 1 | `CI_FORMULA\|x̄ ± E` | confidence_interval_generator.py |
| `CI_SETUP` | 2 | `CI_SETUP\|σ = 28, n = 25, z* = 1.96\|margin of error` | confidence_interval_generator.py |
| `CLAUSE` | 2 | `CLAUSE\|C1\|(not P77634)` | resolution_proof_generator.py |
| `CLIFFORD_EXPECT` | 3 | `CLIFFORD_EXPECT\|2*eta=0\|I_entry=0\|0` | gamma_matrix_generator.py |
| `CLUSTER_MEMBERS` | 2 | `CLUSTER_MEMBERS\|C1\|P3` | kmeans_step_generator.py |
| `CMP` | 3 | `CMP\|44\|9\|>` | fraction_comparison_generator.py, graph_interpret_generator.py, logical_connective_eval_generator.py, set_builder_roster_generator.py |
| `CMP_DIGIT` | 4 | `CMP_DIGIT\|pos_0\|0\|1\|<` | number_comparison_generator.py |
| `CMP_NUM` | 3 | `CMP_NUM\|46.36\|177.07\|<` | number_comparison_generator.py |
| `CNF_FORM` | 1 | `CNF_FORM\|(V OR NOT W OR NOT X OR Y) AND (NOT V OR NOT W OR X OR Y) AND (NOT V OR NOT W OR NOT X OR NOT Y)` | boolean_algebra_generator.py |
| `CODEWORD` | 1, 3 | `CODEWORD\|0100101` | hamming_code_generator.py, kraft_inequality_generator.py |
| `CODE_LENGTH` | 2 | `CODE_LENGTH\|A\|l=3` | huffman_coding_generator.py |
| `COEFF` | 2 | `COEFF\|a_1\|5280` | laurent_series_generator.py, series_solution_generator.py |
| `COEFFS` | 1, 2 | `COEFFS\|1, 3, -6, 1` | horner_evaluation_generator.py, polynomial_zeros_generator.py, synthetic_division_generator.py |
| `COEFF_MATCH` | 2 | `COEFF_MATCH\|x^n\|(n+1)a_(n+1) = a_n` | series_solution_generator.py |
| `COEFF_PAIR` | 3 | `COEFF_PAIR\|i=2, j=5\|4i + 5j = 33\|accepted` | generating_function_generator.py |
| `COFACTOR` | 2 | `COFACTOR\|(1,1) sign +\|minor [[3, 4], [-3, 3]]` | determinant_generator.py |
| `COLLIDER_SETUP` | 3 | `COLLIDER_SETUP\|events_pb\|L=20 fb^-1\|sigma=16 pb` | cross_section_generator.py |
| `COLLISION_SETUP` | 3 | `COLLISION_SETUP\|inelastic_1d\|m1=2, u1=10\|m2=19, u2=7` | collision_generator.py |
| `COL_BASIS` | 2 | `COL_BASIS\|original columns 1, 2, 3\|[[3, -2, 1], [-1, 1, 0], [-1, 0, 0]]` | subspace_basis_generator.py |
| `COMB` | 2 | `COMB\|C(5,1)\|5` | bec_channel_generator.py |
| `COMBO` | 2 | `COMBO\|x = 5*v1 - 22*v2\|[-7, -5]` | diagonalization_generator.py |
| `COMB_CONST` | 3 | `COMB_CONST\|7\|+9\|16` | derivative_product_quotient_generator.py, equation_from_two_points_generator.py, linear_complex_generator.py, rational_expr_add_sub_generator.py, simplify_expression_generator.py, special_solution_equation_generator.py |
| `COMB_FORMULA` | 1 | `COMB_FORMULA\|C(n, r) = P(n, r)/r!` | permutation_combination_generator.py |
| `COMB_SETUP` | 2 | `COMB_SETUP\|choose 4 of 10\|order does not matter` | counting_classics_generator.py, permutation_combination_generator.py, stars_and_bars_generator.py |
| `COMB_X` | 3 | `COMB_X\|-5x\|-3x\|-8x` | derivative_product_quotient_generator.py, linear_complex_generator.py, rational_expr_add_sub_generator.py, simplify_expression_generator.py, special_solution_equation_generator.py |
| `COMMON_DIFF` | 2 | `COMMON_DIFF\|-13 - (-4)\|-9` | arithmetic_sequence_generator.py, recursive_explicit_generator.py |
| `COMMON_RATIO` | 2 | `COMMON_RATIO\|1160/580\|2` | geometric_sequence_generator.py, recursive_explicit_generator.py |
| `COMMUTATOR` | 2 | `COMMUTATOR\|[A,B]\|[[-105i/2, 0], [0, 105i/2]]` | structure_constant_generator.py |
| `COMM_ENTRY` | 3 | `COMM_ENTRY\|(1,1)\|-105i/4 - 105i/4\|-105i/2` | structure_constant_generator.py |
| `COMM_FORMULA` | 1 | `COMM_FORMULA\|[A,B]f=A(Bf)-B(Af)` | commutator_generator.py |
| `COMM_RESULT` | 2 | `COMM_RESULT\|[x,p]f\|11i*x^19` | commutator_generator.py |
| `COMM_SETUP` | 3 | `COMM_SETUP\|[x,p]f\|f=x^19\|p=-i*hbar*D, hbar=11` | commutator_generator.py |
| `COMPARE` | 2, 3 | `COMPARE\|6 = 6\|log_b(a) = k` | algorithm_trace_generator.py, equilibrium_ice_generator.py, fixed_point_generator.py, master_theorem_generator.py |
| `COMPLEMENT` | 2 | `COMPLEMENT\|at least one fixed\|9! - D_9` | derangement_generator.py |
| `COMPLETE_SQUARE` | 2 | `COMPLETE_SQUARE\|half of 16 = 8\|8^2 = 64` | completing_square_generator.py, conic_standard_form_generator.py, polar_parametric_generator.py |
| `COMPOSITE_FACTOR` | 2 | `COMPOSITE_FACTOR\|5\|73` | divisibility_classification_generator.py |
| `COMPOSITE_SETUP` | 2 | `COMPOSITE_SETUP\|area = length × width with mixed numbers\|convert, multiply, simplify` | composite_arithmetic_generator.py |
| `COMP_INEQ_PART` | 2 | `COMP_INEQ_PART\|Part 1\|x + 8 < 2 -> x < -6` | compound_inequality_generator.py |
| `COMP_INEQ_SETUP` | 1 | `COMP_INEQ_SETUP\|-10 < 4x - 6 < 6` | compound_inequality_generator.py |
| `COND_COUNT` | 2 | `COND_COUNT\|club=no and commute=bus\|4` | conditional_probability_generator.py |
| `COND_ENTROPY` | 1 | `COND_ENTROPY\|H(Y given X)=H(X,Y)-H(X)` | mutual_information_generator.py |
| `COND_FORMULA` | 1 | `COND_FORMULA\|P(A given B) = count(A and B)/count(B)` | conditional_probability_generator.py, joint_distribution_generator.py |
| `COND_PARTS` | 2 | `COND_PARTS\|n divisible by 24\|n divisible by 2` | conditional_forms_generator.py |
| `COND_SETUP` | 2 | `COND_SETUP\|yes/bike 27, no/bike 8, yes/bus 26, no/bus 4\|P(club=no given commute=bus)` | conditional_probability_generator.py |
| `COND_TOTAL` | 2 | `COND_TOTAL\|commute=bus total\|26 + 4 = 30` | conditional_probability_generator.py |
| `CONGRUENCE_REDUCE` | 2 | `CONGRUENCE_REDUCE\|8x congruent to 2\|mod 5` | modular_inverse_generator.py |
| `CONGRUENCE_SOLUTIONS` | 3 | `CONGRUENCE_SOLUTIONS\|base 4\|step 5\|4, 9, 14` | modular_inverse_generator.py |
| `CONIC_SETUP` | 2 | `CONIC_SETUP\|x^2 = -4(y + 5)\|vertex, focus, directrix` | conic_standard_form_generator.py, ellipse_features_generator.py, hyperbola_features_generator.py, parabola_features_generator.py |
| `CONJ` | 2 | `CONJ\|phi_1=0\|0` | braket_generator.py |
| `CONJUGATE` | 2 | `CONJUGATE\|-3 + 4i\|-3 - 4i` | complex_division_generator.py, quaternion_generator.py |
| `CONNECTIVE` | 2 | `CONNECTIVE\|¬q\|T` | logical_connective_eval_generator.py |
| `CONSERVATION_SETUP` | 2 | `CONSERVATION_SETUP\|mu- + pi0 -> nu_e + e- + pi0 + anti_nu_mu\|check=Q,B,Le,Lmu` | conservation_law_generator.py |
| `CONSERVE_CHECK` | 3 | `CONSERVE_CHECK\|Q\|left=-1,right=-1\|conserved` | conservation_law_generator.py |
| `CONSTRAINT_SUBST` | 3 | `CONSTRAINT_SUBST\|x + y = 16\|x = 16/4\|4` | lagrange_multiplier_generator.py |
| `CONST_SOLVE` | 2 | `CONST_SOLVE\|C1 = -1\|C2 = -2` | recurrence_generator.py |
| `CONTOUR_SETUP` | 3 | `CONTOUR_SETUP\|abs(z)=5\|positive orientation\|f=-2/(z-6) - 1/(z-2) - 3/(z-5)` | contour_integral_generator.py |
| `CONT_DIST_SETUP` | 3 | `CONT_DIST_SETUP\|f(x)=k*x\|support=[0,3]\|interval=(0,2)` | continuous_distribution_generator.py |
| `CONVERGENT` | 2 | `CONVERGENT\|i=0\|1/1` | continued_fraction_generator.py |
| `CONVERGE_CHECK` | 2 | `CONVERGE_CHECK\|abs(r) = 9/11 < 1\|converges` | geometric_sequence_generator.py, series_convergence_generator.py |
| `CONV_ENCODE_STEP` | 3 | `CONV_ENCODE_STEP\|i=1\|prev=0,u=1\|11` | convolutional_code_viterbi_generator.py |
| `CONV_FACTOR` | 2 | `CONV_FACTOR\|1 hr\|60 min` | cross_section_generator.py, dimensional_analysis_generator.py, multi_step_unit_conversion_generator.py, rate_conversion_generator.py, unit_conversion_generator.py |
| `CONV_INIT` | 2 | `CONV_INIT\|h_-2=0,h_-1=1\|k_-2=1,k_-1=0` | continued_fraction_generator.py |
| `CONV_RECEIVED` | 2 | `CONV_RECEIVED\|100110\|flipped position 2` | convolutional_code_viterbi_generator.py |
| `CONV_RESULT` | 2 | `CONV_RESULT\|41 hr\|2460 min` | dimensional_analysis_generator.py, multi_step_unit_conversion_generator.py, rate_conversion_generator.py, temperature_conversion_generator.py, unit_conversion_generator.py |
| `CONV_SETUP` | 2, 3 | `CONV_SETUP\|x=[3,2,6,0]\|h=[9,8,2,1]` | convolution_generator.py, convolutional_code_viterbi_generator.py |
| `CONV_STEP` | 3 | `CONV_STEP\|i=0\|h=1\|k=1` | continued_fraction_generator.py |
| `CONV_SUM` | 2 | `CONV_SUM\|n=0\|27` | convolution_generator.py |
| `CONV_WINDOW` | 2 | `CONV_WINDOW\|n=0\|x0*h0` | convolution_generator.py |
| `COORDS` | 2 | `COORDS\|c = P^-1 x\|[5, -22]` | diagonalization_generator.py |
| `CORRECT_BIT` | 3 | `CORRECT_BIT\|position=2\|0->1\|corrected=0101010` | hamming_code_generator.py |
| `CORR_FORMULA` | 1 | `CORR_FORMULA\|r = Sxy/√(Sxx·Syy)` | joint_distribution_generator.py, regression_generator.py |
| `COS` | 2 | `COS\|pi/2\|0` | positional_encoding_generator.py |
| `COSET` | 2 | `COSET\|eH\|{e, r, r2}` | coset_generator.py |
| `COSET_ELEM` | 2 | `COSET_ELEM\|eH\|e` | coset_generator.py |
| `COSET_SKIP` | 2 | `COSET_SKIP\|r\|already listed` | coset_generator.py |
| `COSET_START` | 2 | `COSET_START\|rep e\|eH` | coset_generator.py |
| `COSINE` | 2 | `COSINE\|A,A\|1` | embedding_similarity_generator.py, lr_schedule_generator.py |
| `COST` | 1 | `COST\|initial` | transportation_generator.py |
| `COUNT` | 2 | `COUNT\|neither\|5` | attribute_sorting_generator.py, bayesian_update_generator.py, logical_connective_eval_generator.py, method_of_moments_generator.py, mle_generator.py, one_to_one_correspondence_generator.py, probability_addition_rule_generator.py, set_builder_roster_generator.py, set_membership_subset_generator.py, set_operations_generator.py |
| `COUNTEREXAMPLE` | 2 | `COUNTEREXAMPLE\|set pair\|A = ∅; B = {27}; left = ∅; right = {27}` | conditional_forms_generator.py, counterexample_search_generator.py |
| `COUNT_DP` | 3 | `COUNT_DP\|1\|1\|2` | decimal_mult_generator.py |
| `COUNT_SETUP` | 1, 2 | `COUNT_SETUP\|78 boxes\|force 12 in one box` | counting_classics_generator.py |
| `COUPON` | 1 | `COUPON\|800` | bond_pricing_generator.py |
| `COV_ENTRY` | 2 | `COV_ENTRY\|xx\|8` | pca_generator.py |
| `COV_FORMULA` | 1 | `COV_FORMULA\|Cov=E[XY]-E[X]E[Y]` | joint_distribution_generator.py |
| `CRC_CHECK` | 3 | `CRC_CHECK\|codeword=1011010100\|remainder=0000\|valid` | crc_generator.py |
| `CRC_REMAINDER` | 1 | `CRC_REMAINDER\|0100` | crc_generator.py |
| `CRC_SETUP` | 3 | `CRC_SETUP\|data=101101\|poly=11001\|augmented=1011010000` | crc_generator.py |
| `CRC_SKIP` | 2 | `CRC_SKIP\|i=2\|leading bit 0` | crc_generator.py |
| `CRC_XOR` | 3 | `CRC_XOR\|i=0\|10110 xor 11001\|01111` | crc_generator.py |
| `CRIT_EQS` | 2 | `CRIT_EQS\|f_x = 0\|-2*x + 4*y + 8 = 0` | hessian_classify_generator.py |
| `CRIT_SOLVE` | 3 | `CRIT_SOLVE\|det\|(-2)*(-10) - 4^2\|4` | hessian_classify_generator.py |
| `CROSS_ENTROPY` | 2 | `CROSS_ENTROPY\|target=3\|ln(14)` | perplexity_generator.py, softmax_gradient_generator.py |
| `CROSS_MULT` | 1 | `CROSS_MULT\|8·EF = 20·10` | similar_triangles_generator.py, triangle_solve_generator.py |
| `CROSS_RATIO` | 1 | `CROSS_RATIO\|55/7` | mobius_transform_generator.py |
| `CROSS_RATIO_SETUP` | 4 | `CROSS_RATIO_SETUP\|z1=-1\|z2=3\|z3=4\|z4=-8` | mobius_transform_generator.py |
| `CRT_CHECK` | 3 | `CRT_CHECK\|i=1\|0\|0` | crt_generator.py |
| `CRT_CONGRUENCE` | 3 | `CRT_CONGRUENCE\|i=1\|x=0\|mod 3` | crt_generator.py |
| `CRT_FACTOR` | 3 | `CRT_FACTOR\|i=1\|M_i=28\|mod 3` | crt_generator.py |
| `CRT_SETUP` | 1 | `CRT_SETUP\|3 congruences` | crt_generator.py |
| `CRT_TERM` | 2 | `CRT_TERM\|i=1\|0` | crt_generator.py |
| `CRT_TOTAL_MODULUS` | 2 | `CRT_TOTAL_MODULUS\|3, 4, 7\|84` | crt_generator.py |
| `CR_SETUP` | 2 | `CR_SETUP\|u=4x^2 - 4y^2 - 3x + 2y\|v=8xy - 2x - 3y` | cauchy_riemann_generator.py |
| `CUM_INTERVAL` | 2 | `CUM_INTERVAL\|A\|[0,1/2)` | arithmetic_coding_generator.py |
| `CURL_COMPONENT` | 3 | `CURL_COMPONENT\|Q_x - P_y\|1 + 4\|5` | div_curl_generator.py |
| `CURRENT_YIELD` | 1 | `CURRENT_YIELD\|0.1` | bond_pricing_generator.py |
| `CURVATURE_FORMULA` | 2 | `CURVATURE_FORMULA\|circle\|kappa = 1/R` | curve_geometry_generator.py |
| `CURVE_GEOM_SETUP` | 3 | `CURVE_GEOM_SETUP\|r(t) = <11*cos(t), 11*sin(t)>\|at t = 0\|curvature, T, N` | curve_geometry_generator.py |
| `CURVE_SETUP` | 2 | `CURVE_SETUP\|f(x) = x^3 - 12x^2 + 45x + 2\|inflection point and concavity` | curve_analysis_generator.py |
| `CX_A` | 3 | `CX_A\|0\|-56i/65\|-56i/65` | braket_generator.py, spin_half_generator.py |
| `CX_M` | 3 | `CX_M\|0\|33/65\|0` | braket_generator.py, spin_half_generator.py |
| `CX_SETUP` | 2 | `CX_SETUP\|(6 - 5i) + (-9 - 6i)\|add` | complex_division_generator.py, complex_number_ops_generator.py |
| `CYCLE` | 1 | `CYCLE\|(1 2 4 3 6 5)` | permutation_group_generator.py |
| `CYCLE_LENGTHS` | 1 | `CYCLE_LENGTHS\|6` | permutation_group_generator.py |
| `CYCLE_REJECT` | 2 | `CYCLE_REJECT\|AE\|endpoints already connected` | mst_generator.py |
| `CYCLE_TRACE` | 2 | `CYCLE_TRACE\|start 1\|1->2->4->3->6->5->1` | permutation_group_generator.py |
| `CYCLIC_START` | 2 | `CYCLIC_START\|5\|identity 1` | cyclic_group_generator.py |
| `CYCLIC_SUBGROUP` | 2 | `CYCLIC_SUBGROUP\|{1, 5, 11, 13, 9, 3}\|6` | cyclic_group_generator.py |
| `CYK_CELL` | 2 | `CYK_CELL\|1,2\|{}` | cyk_parser_generator.py |
| `CYK_COMBINE` | 3 | `CYK_COMBINE\|Y B\|{S}\|cell 2,3` | cyk_parser_generator.py |
| `CYK_RULE` | 2 | `CYK_RULE\|S\|T T or V T` | cyk_parser_generator.py |
| `CYK_SETUP` | 2 | `CYK_SETUP\|string daa\|length 3` | cyk_parser_generator.py |
| `CYK_SPAN` | 1 | `CYK_SPAN\|2` | cyk_parser_generator.py |
| `CYK_SPLIT` | 3 | `CYK_SPLIT\|cell 1,2\|1,1 x 2,2\|{T,Z} x {V}` | cyk_parser_generator.py |
| `CYK_TERMINAL` | 3 | `CYK_TERMINAL\|cell 1,1\|d\|{T,Z}` | cyk_parser_generator.py |
| `CYL_BOUNDS` | 2 | `CYL_BOUNDS\|z\|0..10` | triple_integral_generator.py |
| `CYL_CONVERT` | 2 | `CYL_CONVERT\|6*z dV\|6*z*r dz dr dtheta` | triple_integral_generator.py |
| `D` | 3 | `D\|632\|99\|6` | ac_circuit_generator.py, activation_generator.py, adam_step_generator.py, angle_defect_generator.py, annuity_generator.py, antiderivative_generator.py, arithmetic_coding_generator.py, arithmetic_sequence_generator.py, attention_generator.py, backprop_generator.py, bayesian_update_generator.py, bisection_generator.py, blackbody_generator.py, bond_pricing_generator.py, branching_ratio_generator.py, casimir_force_generator.py, cholesky_generator.py, christoffel_generator.py, circle_angle_generator.py, circle_equation_generator.py, classifier_metrics_generator.py, collision_generator.py, complex_number_ops_generator.py, composite_arithmetic_generator.py, confidence_interval_generator.py, conic_standard_form_generator.py, continuous_distribution_generator.py, coset_generator.py, counting_classics_generator.py, cramers_rule_generator.py, cross_section_generator.py, crt_generator.py, curve_analysis_generator.py, de_moivre_generator.py, decimal_div_generator.py, definite_integral_generator.py, dimensional_analysis_generator.py, doppler_generator.py, einstein_summation_generator.py, electrostatics_generator.py, embedding_similarity_generator.py, energy_conservation_generator.py, entropy_change_generator.py, entropy_generator.py, equilibrium_ice_generator.py, error_spotting_generator.py, exact_ode_generator.py, exponential_equation_generator.py, exponential_model_generator.py, fill_in_step_generator.py, finite_difference_generator.py, flops_memory_generator.py, fourier_series_generator.py, function_inner_product_generator.py, function_operations_generator.py, game_theory_generator.py, gas_law_generator.py, gas_stoichiometry_generator.py, gauss_bonnet_generator.py, gauss_law_generator.py, gaussian_curvature_generator.py, generating_function_generator.py, geometric_distribution_generator.py, geometric_mean_generator.py, geometric_sequence_generator.py, geometry_area_perimeter_generator.py, gradient_descent_generator.py, gradient_step_generator.py, hamiltonian_generator.py, hawking_generator.py, heat_engine_generator.py, huffman_coding_generator.py, hydrogen_atom_generator.py, hyperbolic_distance_generator.py, hyperbolic_function_generator.py, hypothesis_test_generator.py, information_gain_generator.py, integrating_factor_generator.py, interference_generator.py, interpolation_generator.py, invariant_mass_generator.py, jacobi_symbol_generator.py, joint_distribution_generator.py, kernel_ridge_generator.py, kinematics_generator.py, kl_divergence_generator.py, kmeans_step_generator.py, kraft_inequality_generator.py, ladder_operator_generator.py, lagrangian_generator.py, laplace_ivp_generator.py, laurent_series_generator.py, layer_norm_generator.py, lcm_generator.py, least_squares_generator.py, legendre_construction_generator.py, limit_evaluation_generator.py, linear_simple_generator.py, log_conversion_generator.py, logistic_growth_generator.py, long_division_generator.py, lr_schedule_generator.py, magnetism_generator.py, manual_square_root_generator.py, markov_chain_generator.py, matrix_inverse_generator.py, matrix_norm_generator.py, mean_value_theorem_generator.py, method_of_moments_generator.py, midpoint_generator.py, mle_generator.py, modular_inverse_generator.py, multi_step_unit_conversion_generator.py, naive_bayes_generator.py, named_distribution_generator.py, natural_units_generator.py, nets_surface_area_generator.py, newton_raphson_generator.py, newtons_laws_generator.py, npv_irr_generator.py, ode_substitution_generator.py, optics_generator.py, optimization_generator.py, or_formula_generator.py, orbital_mechanics_generator.py, order_of_operations_generator.py, order_statistics_generator.py, parabola_features_generator.py, param_count_generator.py, parametric_calculus_generator.py, particle_in_box_generator.py, partition_function_generator.py, pca_generator.py, percent_problem_generator.py, permutation_combination_generator.py, perplexity_generator.py, physics_formula_generator.py, planck_units_generator.py, polar_parametric_generator.py, primality_test_generator.py, projectile_motion_generator.py, proportion_word_problem_generator.py, proportional_relationship_generator.py, quadratic_residue_generator.py, quantization_generator.py, quantum_formula_generator.py, radical_rationalize_generator.py, rate_conversion_generator.py, ratio_table_generator.py, recurrence_generator.py, regression_generator.py, regular_polygon_area_generator.py, relativistic_energy_generator.py, repeating_decimal_generator.py, riemann_sum_generator.py, riemann_tensor_generator.py, right_triangle_trig_generator.py, rotational_dynamics_generator.py, round_solids_generator.py, routh_hurwitz_generator.py, runge_kutta_generator.py, running_coupling_generator.py, rv_transform_generator.py, scaling_law_generator.py, schwarzschild_generator.py, second_order_ode_generator.py, segment_partition_generator.py, separable_pde_generator.py, series_convergence_generator.py, series_solution_generator.py, shm_generator.py, similar_triangles_generator.py, simplex_generator.py, sinusoid_features_generator.py, slope_two_points_generator.py, softmax_gradient_generator.py, solution_chem_generator.py, special_relativity_generator.py, special_right_triangle_generator.py, spherical_excess_generator.py, spherical_triangle_generator.py, spin_half_generator.py, standard_deviation_generator.py, standing_wave_generator.py, stars_and_bars_generator.py, statics_generator.py, stereographic_generator.py, stoichiometry_generator.py, svm_margin_generator.py, taylor_series_generator.py, telescoping_generator.py, temperature_conversion_generator.py, tip_bill_split_generator.py, totient_generator.py, transient_circuit_generator.py, triangle_area_sas_generator.py, triangle_solve_generator.py, trig_identity_eval_generator.py, trig_six_functions_generator.py, two_sample_test_generator.py, u_substitution_generator.py, undetermined_coeff_generator.py, unit_conversion_generator.py, variation_parameters_generator.py, vector_ops_generator.py, wavefunction_generator.py, young_tableaux_generator.py, z_score_generator.py |
| `DALEMBERT` | 1 | `DALEMBERT\|u=(f(x-ct)+f(x+ct))/2` | separable_pde_generator.py |
| `DATA_PRECISION` | 1 | `DATA_PRECISION\|n/sigma^2` | bayesian_update_generator.py |
| `DATE_ORDINAL` | 2 | `DATE_ORDINAL\|2028-09-26\|740616` | calendar_arithmetic_generator.py |
| `DB_FORMULA` | 1 | `DB_FORMULA\|G_dB=10*log10(P2/P1)` | signal_arithmetic_generator.py |
| `DECISION` | 2 | `DECISION\|f(x)\|-22` | kernel_perceptron_generator.py, svm_margin_generator.py |
| `DEC_ADD_COL` | 3 | `DEC_ADD_COL\|frac_0\|0+1+0\|->1 (carry 0)` | decimal_add_sub_generator.py |
| `DEC_ALIGN` | 2 | `DEC_ALIGN\|55.60\|69.81` | decimal_add_sub_generator.py |
| `DEC_CARRY_FINAL` | 1 | `DEC_CARRY_FINAL\|1` | decimal_add_sub_generator.py |
| `DEC_SHIFT` | 3 | `DEC_SHIFT\|33.0/0.2\|330/2\|1` | decimal_div_generator.py, percent_problem_generator.py |
| `DEC_SUB_COL` | 3 | `DEC_SUB_COL\|frac_0\|1-0 (borrow_in 0)\|->1 (borrow_out 0)` | decimal_add_sub_generator.py |
| `DEC_TO_FRAC` | 2 | `DEC_TO_FRAC\|4.17\|417/100` | fraction_decimal_percent_converter.py |
| `DEC_TO_PERCENT` | 2 | `DEC_TO_PERCENT\|1.075\|107.5%` | fraction_decimal_percent_converter.py, percent_problem_generator.py, tip_bill_split_generator.py |
| `DEC_TYPE` | 2 | `DEC_TYPE\|151/228\|repeating` | repeating_decimal_generator.py |
| `DEC_VALUE` | 2 | `DEC_VALUE\|151/228\|0.66(228070175438596491)` | repeating_decimal_generator.py |
| `DEDUP` | 2 | `DEDUP\|A raw [24, 57, 66, 52, 63, 66]\|{24, 52, 57, 63, 66}` | set_membership_subset_generator.py |
| `DEGREE` | 2, 3 | `DEGREE\|A\|B\|1` | euler_circuit_generator.py, graph_counting_generator.py |
| `DEGREE_COMPARE` | 2 | `DEGREE_COMPARE\|deg num = deg den = 2\|y = 3/2` | limit_evaluation_generator.py, rational_function_features_generator.py, series_convergence_generator.py |
| `DEGREE_SEQUENCE` | 1 | `DEGREE_SEQUENCE\|4, 2, 2, 1, 1` | graph_counting_generator.py |
| `DELTA_VALUE` | 2 | `DELTA_VALUE\|delta_22\|1` | index_gymnastics_generator.py |
| `DEMOIVRE_POWER` | 1 | `DEMOIVRE_POWER\|625 cis(120 deg)` | de_moivre_generator.py |
| `DEMOIVRE_SETUP` | 2, 4 | `DEMOIVRE_SETUP\|power\|r=5\|theta=210 deg\|n=4` | de_moivre_generator.py |
| `DENSITY` | 2 | `DENSITY\|f_X(x)\|1/19` | rv_transform_generator.py |
| `DENSITY_MATRIX` | 1 | `DENSITY_MATRIX\|rho=[[2/15,0],[0,13/15]]` | density_matrix_generator.py |
| `DENSITY_SETUP` | 2, 3 | `DENSITY_SETUP\|state=Schmidt\|psi=(sqrt(219)ket00 - sqrt(5)ket11)/sqrt(224)` | density_matrix_generator.py, partial_trace_generator.py |
| `DEQUANT_VALUE` | 2 | `DEQUANT_VALUE\|1\|7/25` | quantization_generator.py |
| `DERANGE_PROB` | 2 | `DERANGE_PROB\|D_7/7!\|1854/5040` | derangement_generator.py |
| `DERANGE_SETUP` | 2 | `DERANGE_SETUP\|n = 8\|exactly 3 fixed` | derangement_generator.py |
| `DERANGE_VALUE` | 2 | `DERANGE_VALUE\|D_2\|1` | derangement_generator.py |
| `DERIV` | 2, 3 | `DERIV\|d_r g_thetatheta = 2r\|at r=5\|10` | christoffel_generator.py, gaussian_curvature_generator.py, riemann_tensor_generator.py |
| `DERIVATIVE` | 1, 2 | `DERIVATIVE\|g'(x)\|5/13` | fixed_point_generator.py, mgf_generator.py, mle_generator.py |
| `DERIVED` | 2 | `DERIVED\|C4\|{}` | resolution_proof_generator.py |
| `DERIV_FORM` | 2 | `DERIV_FORM\|y'\|-3C1e^(-3x) + 4C2e^(4x)` | second_order_ode_generator.py, undetermined_coeff_generator.py, variation_parameters_generator.py |
| `DERIV_RULE` | 2 | `DERIV_RULE\|power rule\|d/dx of c·x^n = c·n·x^(n-1)` | chain_rule_generator.py, derivative_power_rule_generator.py, derivative_product_quotient_generator.py, derivative_transcendental_generator.py, lhopital_generator.py, linear_approx_generator.py, log_diff_higher_order_generator.py, multivar_chain_rule_generator.py |
| `DERIV_SERIES` | 2 | `DERIV_SERIES\|y'\|sum (n+1)a_(n+1)x^n` | series_solution_generator.py |
| `DERIV_SETUP` | 2 | `DERIV_SETUP\|f(x) = 3x^2 + 6x - 7\|f'(x)` | chain_rule_generator.py, derivative_power_rule_generator.py, derivative_product_quotient_generator.py, derivative_transcendental_generator.py, log_diff_higher_order_generator.py, tangent_line_generator.py |
| `DESIGN_MATRIX` | 2 | `DESIGN_MATRIX\|X = [[1, -3], [1, -1], [1, 1], [1, 3]]\|y = [4, 4, 8, 16]` | least_squares_generator.py |
| `DET` | 2 | `DET\|K\|13` | kernel_ridge_generator.py, kernel_validity_generator.py |
| `DET2` | 2 | `DET2\|ad - bc\|6` | ode_system_generator.py |
| `DET_FORMULA` | 1 | `DET_FORMULA\|det = a11·M11 - a12·M12 + a13·M13` | cramers_rule_generator.py, determinant_generator.py, matrix_inverse_generator.py |
| `DEV_ROW` | 3 | `DEV_ROW\|19\|4\|16` | standard_deviation_generator.py |
| `DFA_ACCEPT` | 1 | `DFA_ACCEPT\|q1` | dfa_minimization_generator.py, dfa_simulation_generator.py |
| `DFA_INPUT` | 1 | `DFA_INPUT\|101000` | dfa_simulation_generator.py |
| `DFA_MIN_SETUP` | 3 | `DFA_MIN_SETUP\|states A, B, C, D\|alphabet 0, 1\|start A` | dfa_minimization_generator.py |
| `DFA_MIN_TRANSITION` | 3 | `DFA_MIN_TRANSITION\|A\|0\|C` | dfa_minimization_generator.py |
| `DFA_READ` | 2 | `DFA_READ\|pos 1\|1` | dfa_simulation_generator.py |
| `DFA_SETUP` | 3 | `DFA_SETUP\|states q0, q1\|alphabet 0, 1\|start q0` | dfa_simulation_generator.py |
| `DFA_STATE` | 2 | `DFA_STATE\|start\|q0` | dfa_simulation_generator.py |
| `DFA_STEP` | 3 | `DFA_STEP\|q0\|1\|q1` | dfa_simulation_generator.py |
| `DFA_TRANSITION` | 3 | `DFA_TRANSITION\|q0\|0\|q0` | dfa_simulation_generator.py |
| `DFS_EDGE` | 2 | `DFS_EDGE\|A->B\|tree` | graph_traversal_generator.py |
| `DFT_BIN` | 1 | `DFT_BIN\|X0=x0+x1` | dft_generator.py |
| `DFT_SETUP` | 2 | `DFT_SETUP\|N=2\|x=[6,-2]` | dft_generator.py |
| `DH_PUBLIC` | 2 | `DH_PUBLIC\|Alice\|13` | diffie_hellman_generator.py |
| `DH_SECRET` | 2 | `DH_SECRET\|Alice\|12` | diffie_hellman_generator.py |
| `DH_SETUP` | 2 | `DH_SETUP\|p=17\|g=10` | diffie_hellman_generator.py |
| `DH_SHARED` | 2 | `DH_SHARED\|Alice\|13` | diffie_hellman_generator.py |
| `DIAG_FORM` | 3 | `DIAG_FORM\|P = [[3, 1], [-1, 0]]\|D = [[-3, 0], [0, -2]]\|P^-1 = [[0, -1], [1, 3]]` | diagonalization_generator.py, matrix_exponential_generator.py |
| `DIFF_ROW` | 2 | `DIFF_ROW\|Delta y\|[15, 11, 7]` | finite_difference_generator.py |
| `DIFF_SETUP` | 3 | `DIFF_SETUP\|f(x,y) = 4*x^2 + 4*y^2 - x*y + 2*x + 3*y\|point (-3, 2)\|dx=-2/5, dy=-1/2` | multivar_chain_rule_generator.py |
| `DIFF_SUM` | 3 | `DIFF_SUM\|f_x*dx + f_y*dy\|(-24)*(-2/5) + 22*(-1/2)\|-1.4` | multivar_chain_rule_generator.py |
| `DIJKSTRA_INIT` | 2 | `DIJKSTRA_INIT\|start D\|A=inf, B=inf, C=inf, D=0, E=inf, F=inf` | dijkstra_generator.py |
| `DIM` | 2 | `DIM\|2*3/2+1\|4` | casimir_generator.py |
| `DIRECTRIX` | 1 | `DIRECTRIX\|y = -4` | parabola_features_generator.py |
| `DISC` | 2, 3 | `DISC\|36\|-8064\|8100` | complex_quadratic_generator.py, discriminant_generator.py, polynomial_zeros_generator.py, quadratic_generator.py |
| `DISC_CLASSIFY` | 2 | `DISC_CLASSIFY\|97 > 0\|two real solutions` | complex_quadratic_generator.py, discriminant_generator.py, polynomial_zeros_generator.py |
| `DIST` | 3 | `DIST\|2\|5x+1\|10x+2` | derivative_limit_def_generator.py, derivative_product_quotient_generator.py, equation_from_two_points_generator.py, function_composition_generator.py, parallel_perpendicular_line_generator.py, point_slope_generator.py, polar_parametric_generator.py, radical_multiply_generator.py, radical_rationalize_generator.py, rational_expr_add_sub_generator.py, recursive_explicit_generator.py, simplify_expression_generator.py, solid_revolution_generator.py, special_solution_equation_generator.py, tangent_line_generator.py |
| `DIST2` | 2, 3 | `DIST2\|P1\|C1\|9` | embedding_similarity_generator.py, kernel_evaluation_generator.py, kmeans_step_generator.py |
| `DIST_COMBINE` | 1 | `DIST_COMBINE\|-7x - 45 = -38` | systems_substitution_generator.py |
| `DIST_FORMULA` | 1 | `DIST_FORMULA\|d = √((x2 - x1)^2 + (y2 - y1)^2)` | complex_locus_generator.py, distance_formula_generator.py, hypercube_counting_generator.py |
| `DIST_SETUP` | 3 | `DIST_SETUP\|poisson\|lambda=1\|k=1` | named_distribution_generator.py |
| `DIST_TABLE` | 2 | `DIST_TABLE\|visited D\|A=6, B=inf, C=4, D=0, E=inf, F=9` | dijkstra_generator.py |
| `DIST_TERM` | 2 | `DIST_TERM\|-5x\|10x^3 - 5x^2 - 15x` | multiplying_polynomials_generator.py |
| `DIVIDE_EQ` | 2 | `DIVIDE_EQ\|divide by y^2\|y^(-2)dy/dx + y^(-1) = 5` | ode_substitution_generator.py |
| `DIVMOD` | 4 | `DIVMOD\|188\|2\|94\|r=0` | base_conversion_generator.py |
| `DIV_CHECK` | 3 | `DIV_CHECK\|6\|2\|remainder 0` | conditional_forms_generator.py, counterexample_search_generator.py, divisibility_classification_generator.py, logical_connective_eval_generator.py, set_builder_roster_generator.py |
| `DIV_COEFF` | 3 | `DIV_COEFF\|16\|-8\|x=-2` | linear_complex_generator.py |
| `DIV_SETUP` | 2 | `DIV_SETUP\|330\|2` | decimal_div_generator.py, percent_problem_generator.py |
| `DIV_SUM` | 3 | `DIV_SUM\|P_x + Q_y\|5 - 4\|1` | div_curl_generator.py |
| `DIV_TERM` | 3 | `DIV_TERM\|8n^4\|4n^2\|2n^2` | factor_gcf_generator.py, finite_field_generator.py, polynomial_long_division_generator.py |
| `DNF_FORM` | 1 | `DNF_FORM\|(NOT Q AND NOT R AND NOT S) OR (NOT Q AND NOT R AND S) OR (NOT Q AND R AND NOT S) OR (NOT Q AND R AND S) OR (Q AND NOT R AND NOT S) OR (Q AND NOT R AND S)` | boolean_algebra_generator.py |
| `DOMAIN` | 2 | `DOMAIN\|x = −45..−35\|{−45, −44, −43, −42, −41, −40, −39, −38, −37, −36, −35}` | set_builder_roster_generator.py |
| `DOMAIN_COND` | 2 | `DOMAIN_COND\|denominator ≠ 0\|x^2 - x - 20 ≠ 0` | domain_range_generator.py |
| `DOMAIN_NOTE` | 2 | `DOMAIN_NOTE\|x ≠ 5\|denominator cannot be zero` | domain_range_generator.py, log_equation_generator.py, logistic_growth_generator.py, probability_addition_rule_generator.py, rational_equation_generator.py, unit_circle_generator.py |
| `DOPPLER_FORMULA` | 1 | `DOPPLER_FORMULA\|f_obs=f*sqrt((1+beta)/(1-beta))` | doppler_generator.py |
| `DOPPLER_SETUP` | 3 | `DOPPLER_SETUP\|relativistic_approach\|f=102\|beta=35/37` | doppler_generator.py |
| `DOT` | 2, 3 | `DOT\|(-7, 6) · (3/5, 4/5)\|(-7)*3/5 + 6*4/5\|0.6` | embedding_similarity_generator.py, feature_map_generator.py, fundamental_form_generator.py, gradient_generator.py, gram_schmidt_generator.py, kernel_evaluation_generator.py, line_integral_generator.py, lll_reduction_generator.py, qr_decomposition_generator.py |
| `DOT4` | 4 | `DOT4\|gamma3gamma0\|(1,1)\|0*1 + -1*0 + 0*0 + 0*0\|0` | gamma_matrix_generator.py |
| `DOT_FORMULA` | 1 | `DOT_FORMULA\|cos θ = (u·v)/(‖u‖ · ‖v‖)` | dot_product_generator.py |
| `DOUBLE_SETUP` | 2, 3 | `DOUBLE_SETUP\|integrand 10\|x:0..7\|y:0..2*x` | double_integral_generator.py |
| `DPLL_BACKTRACK` | 2 | `DPLL_BACKTRACK\|A\|True` | dpll_trace_generator.py |
| `DPLL_BRANCH` | 3 | `DPLL_BRANCH\|depth 0\|A\|True` | dpll_trace_generator.py |
| `DPLL_CONFLICT` | 1 | `DPLL_CONFLICT\|A=True, B=True` | dpll_trace_generator.py |
| `DPLL_SAT` | 1 | `DPLL_SAT\|A=True, B=True, C=True` | dpll_trace_generator.py |
| `DPLL_SETUP` | 3 | `DPLL_SETUP\|(A) AND (not A OR B) AND (not B OR C)\|variables A, B, C\|True first` | dpll_trace_generator.py |
| `DPLL_SIMPLIFY` | 2 | `DPLL_SIMPLIFY\|A=True\|2 clauses left` | dpll_trace_generator.py |
| `DPLL_STATE` | 3 | `DPLL_STATE\|depth 0\|none\|3 clauses left` | dpll_trace_generator.py |
| `DPLL_UNIT` | 2 | `DPLL_UNIT\|(A)\|A=True` | dpll_trace_generator.py |
| `DP_CELL` | 3 | `DP_CELL\|i=1,c=0\|base\|0` | dp_table_generator.py |
| `DP_COINS` | 1 | `DP_COINS\|1, 2, 4` | dp_table_generator.py |
| `DP_ITEMS` | 1 | `DP_ITEMS\|1:(w=2,v=10); 2:(w=1,v=4); 3:(w=2,v=6); 4:(w=3,v=2)` | dp_table_generator.py |
| `DP_ROW` | 2 | `DP_ROW\|i=0\|0, 0, 0, 0, 0, 0, 0, 0` | dp_table_generator.py |
| `DP_SETUP` | 2, 3 | `DP_SETUP\|0/1 knapsack\|capacity 7` | dp_table_generator.py |
| `D_POWER` | 2 | `D_POWER\|D^4\|[[81, 0], [0, 16]]` | diagonalization_generator.py |
| `E` | 3 | `E\|26\|3\|17576` | ac_circuit_generator.py, adam_step_generator.py, angle_defect_generator.py, annuity_generator.py, arc_sector_generator.py, backprop_generator.py, bec_channel_generator.py, blackbody_generator.py, bond_pricing_generator.py, casimir_force_generator.py, casimir_generator.py, christoffel_generator.py, circle_equation_generator.py, complex_division_generator.py, complex_locus_generator.py, confidence_interval_generator.py, conic_standard_form_generator.py, continuous_distribution_generator.py, de_moivre_generator.py, definite_integral_generator.py, density_matrix_generator.py, derivative_limit_def_generator.py, diagonalization_generator.py, distance_formula_generator.py, doppler_generator.py, electrostatics_generator.py, ellipse_features_generator.py, embedding_similarity_generator.py, energy_conservation_generator.py, euler_formula_generator.py, exponential_equation_generator.py, exponential_model_generator.py, factor_special_forms_generator.py, feature_map_generator.py, finance_generator.py, four_vector_generator.py, fractal_iteration_generator.py, function_composition_generator.py, function_evaluation_generator.py, function_operations_generator.py, function_table_generator.py, fundamental_form_generator.py, gauss_bonnet_generator.py, gauss_law_generator.py, gaussian_curvature_generator.py, geometric_mean_generator.py, geometric_sequence_generator.py, gradient_descent_generator.py, gradient_step_generator.py, hamiltonian_generator.py, hawking_generator.py, hermitian_check_generator.py, huffman_coding_generator.py, hydrogen_atom_generator.py, hyperbola_features_generator.py, hyperbolic_function_generator.py, hypercube_counting_generator.py, invariant_mass_generator.py, kernel_evaluation_generator.py, kmeans_step_generator.py, knn_generator.py, kraft_inequality_generator.py, lagrangian_generator.py, laurent_series_generator.py, layer_norm_generator.py, limit_evaluation_generator.py, log_conversion_generator.py, log_equation_generator.py, log_properties_generator.py, low_rank_approx_generator.py, matrix_group_check_generator.py, matrix_norm_generator.py, mean_value_theorem_generator.py, metric_arc_length_generator.py, mgf_generator.py, minkowski_interval_generator.py, mobius_transform_generator.py, named_distribution_generator.py, natural_units_generator.py, npv_irr_generator.py, optimization_generator.py, or_formula_generator.py, orbital_mechanics_generator.py, order_statistics_generator.py, particle_in_box_generator.py, pca_generator.py, piecewise_evaluation_generator.py, planck_units_generator.py, polar_parametric_generator.py, portfolio_generator.py, projectile_motion_generator.py, pythag_hyp_generator.py, radical_equation_generator.py, radical_multiply_generator.py, radical_rationalize_generator.py, rational_exponent_generator.py, recursive_explicit_generator.py, regression_generator.py, related_rates_generator.py, relativistic_energy_generator.py, remainder_factor_theorem_generator.py, riemann_tensor_generator.py, rotational_dynamics_generator.py, round_solids_generator.py, rv_transform_generator.py, schwarzschild_generator.py, set_operations_generator.py, shm_generator.py, spherical_excess_generator.py, spin_half_generator.py, stereographic_generator.py, svm_margin_generator.py, tangent_line_generator.py, taylor_series_generator.py, triangle_solve_generator.py, trig_identity_eval_generator.py, trig_six_functions_generator.py, uncertainty_generator.py, vector_ops_generator.py, wavefunction_generator.py, z_transform_generator.py |
| `ECDH_SETUP` | 2 | `ECDH_SETUP\|E:y^2=x^3+2x+2 over F_17\|G=(5,1)` | ecdh_generator.py |
| `ECDSA_NONCE` | 2 | `ECDSA_NONCE\|kG=(13,10)\|r=13` | ecdsa_generator.py |
| `ECDSA_PUBLIC` | 1 | `ECDSA_PUBLIC\|Q=dG=(16,13)` | ecdsa_generator.py |
| `ECDSA_SETUP` | 4 | `ECDSA_SETUP\|E/F_17, G=(5,1), n=19\|d=6\|z=7\|k=11` | ecdsa_generator.py |
| `ECDSA_SIGN` | 2 | `ECDSA_SIGN\|s=k^-1(z+rd) mod n\|s=6` | ecdsa_generator.py |
| `ECDSA_VERIFY` | 2 | `ECDSA_VERIFY\|u1=17\|u2=18` | ecdsa_generator.py |
| `EC_ACCUM` | 2 | `EC_ACCUM\|1P\|(10,6)` | elliptic_curve_finite_field_generator.py |
| `EC_ADD` | 1 | `EC_ADD\|(13,10)` | ecdsa_generator.py |
| `EC_IDENTITY` | 2 | `EC_IDENTITY\|O + Q\|(10,6)` | elliptic_curve_finite_field_generator.py |
| `EC_INVERSE` | 3 | `EC_INVERSE\|(2,7)\|(2,12)\|O` | elliptic_curve_finite_field_generator.py |
| `EC_POINT_CHECK` | 3 | `EC_POINT_CHECK\|P\|y^2 mod p = 12\|x^3+ax+b mod p = 12` | elliptic_curve_finite_field_generator.py |
| `EC_PUBLIC` | 2 | `EC_PUBLIC\|A=(6,3)\|B=(16,13)` | ecdh_generator.py |
| `EC_SCALAR` | 2 | `EC_SCALAR\|a=2\|aG=(6,3)` | ecdh_generator.py, ecdsa_generator.py |
| `EC_SCALAR_SETUP` | 2 | `EC_SCALAR_SETUP\|k=3\|P=(10,6)` | elliptic_curve_finite_field_generator.py |
| `EC_SETUP` | 3 | `EC_SETUP\|p=23\|a=1\|b=4` | elliptic_curve_finite_field_generator.py |
| `EC_SHARED` | 2 | `EC_SHARED\|aB=(0,11)\|bA=(0,11)` | ecdh_generator.py |
| `EC_SLOPE` | 2 | `EC_SLOPE\|2P\|15` | elliptic_curve_finite_field_generator.py |
| `EC_SLOPE_FORMULA` | 2 | `EC_SLOPE_FORMULA\|2P\|(3x1^2+a)/(2y1)` | elliptic_curve_finite_field_generator.py |
| `EC_X3` | 2 | `EC_X3\|2P\|7` | elliptic_curve_finite_field_generator.py |
| `EC_Y3` | 2 | `EC_Y3\|2P\|3` | elliptic_curve_finite_field_generator.py |
| `EDGE_CHOOSE` | 3 | `EDGE_CHOOSE\|AB\|weight 15\|add A` | mst_generator.py |
| `EDGE_CONSIDER` | 2 | `EDGE_CONSIDER\|AB\|weight 2` | mst_generator.py |
| `EDGE_COUNT` | 2 | `EDGE_COUNT\|m\|5` | euler_circuit_generator.py, graph_counting_generator.py |
| `EDGE_LIST` | 1 | `EDGE_LIST\|AB, AC, AD, AE, BC, BD, BE, CD, CE, DE` | euler_circuit_generator.py |
| `EDGE_WEIGHT` | 2 | `EDGE_WEIGHT\|AB\|4` | dijkstra_generator.py, mst_generator.py |
| `EIGENPAIR` | 2 | `EIGENPAIR\|lambda = 2\|[2, 1]` | ode_system_generator.py |
| `EIGENVALUE` | 1, 2 | `EIGENVALUE\|λ = -4\|p(-4) = 0` | diagonalization_generator.py, eigenvalue_generator.py, matrix_exponential_generator.py, separable_pde_generator.py, svd_generator.py |
| `EIGENVALUES` | 2 | `EIGENVALUES\|A^T A\|16,64` | low_rank_approx_generator.py, matrix_norm_generator.py, pca_generator.py |
| `EIGENVECTOR` | 2 | `EIGENVECTOR\|A + 4I times v = 0\|[1, 0, 0]` | diagonalization_generator.py, eigenvalue_generator.py, matrix_exponential_generator.py, svd_generator.py |
| `EIGEN_CHECK` | 3 | `EIGEN_CHECK\|sigma_y psi\|-1*psi\|lambda=-1` | spin_half_generator.py |
| `EIGEN_MATRIX` | 2 | `EIGEN_MATRIX\|A + 4I\|[[0, 2, 3], [0, 7, -3], [0, 0, 9]]` | eigenvalue_generator.py |
| `EINSTEIN_SETUP` | 2, 3 | `EINSTEIN_SETUP\|symmetrize\|T_ij=[[1, 0], [3, 4]]` | einstein_summation_generator.py |
| `ELEC_FORMULA` | 1 | `ELEC_FORMULA\|V=sum(q_i/r_i)` | electrostatics_generator.py |
| `ELEC_SETUP` | 2, 3 | `ELEC_SETUP\|potential_axis\|q1=9, r1=8\|q2=-1, r2=4` | electrostatics_generator.py |
| `ELEMENT_ORDER` | 2 | `ELEMENT_ORDER\|15\|2` | cayley_table_generator.py |
| `ELEMENT_SCAN` | 3 | `ELEMENT_SCAN\|30\|A\|found` | set_membership_subset_generator.py, set_operations_generator.py |
| `ELIMINATE` | 1 | `ELIMINATE\|(m2-m1)g=(m1+m2)a` | newtons_laws_generator.py |
| `ELIMINATE_LAMBDA` | 2 | `ELIMINATE_LAMBDA\|f_x = f_y\|y = 3*x` | lagrange_multiplier_generator.py |
| `EL_EQUATION` | 1 | `EL_EQUATION\|mL^2*thetaddot+mgL*sin(theta)=0` | lagrangian_generator.py |
| `EL_SOLVE` | 2 | `EL_SOLVE\|thetaddot\|-5*sin(theta)` | lagrangian_generator.py |
| `EMBED_SETUP` | 1 | `EMBED_SETUP\|A=(8,15), B=(12,-5), C=(4,3)` | embedding_similarity_generator.py |
| `ENERGY_FORMULA` | 1 | `ENERGY_FORMULA\|mgh=1/2*m*v^2` | energy_conservation_generator.py |
| `ENERGY_LEVEL` | 2 | `ENERGY_LEVEL\|E_26=hbar*omega*(n+1/2)\|265` | ladder_operator_generator.py |
| `ENERGY_SETUP` | 3 | `ENERGY_SETUP\|gravity_drop\|m=5\|h=320, g=10` | energy_conservation_generator.py |
| `ENERGY_TERM` | 1 | `ENERGY_TERM\|T=1/2*m*L^2*thetadot^2` | lagrangian_generator.py |
| `ENGINE_FORMULA` | 1 | `ENGINE_FORMULA\|W=Qh-Qc` | heat_engine_generator.py |
| `ENGINE_SETUP` | 3 | `ENGINE_SETUP\|engine_efficiency\|Qh=297\|Qc=89` | heat_engine_generator.py |
| `ENQUEUE` | 3 | `ENQUEUE\|B\|from C\|B` | graph_traversal_generator.py |
| `ENTER` | 2 | `ENTER\|x\|most negative reduced cost -8` | simplex_generator.py |
| `ENTROPY_FORMULA` | 1 | `ENTROPY_FORMULA\|DeltaS_mix=-sum n_i ln(x_i)` | entropy_change_generator.py |
| `ENTROPY_SETUP` | 2, 3 | `ENTROPY_SETUP\|eigenvalues=[1/16,1/64,1/16,1/32,1/32,1/4,1/32,1/32,1/32,1/32,1/32,1/16,1/16,1/64,1/4]\|S=-sum lambda log2(lambda)` | entropy_change_generator.py, entropy_generator.py, huffman_coding_generator.py, information_gain_generator.py, mutual_information_generator.py, von_neumann_entropy_generator.py |
| `ENTROPY_SKIP` | 2 | `ENTROPY_SKIP\|H(X,Y)\|p=0` | mutual_information_generator.py |
| `ENTROPY_TERM` | 4 | `ENTROPY_TERM\|row 0\|p=3/4\|I=0.415\|249/800` | entropy_rate_markov_generator.py |
| `ENTROPY_VALUE` | 2 | `ENTROPY_VALUE\|parent\|1` | information_gain_generator.py |
| `ENTROPY_ZERO` | 2 | `ENTROPY_ZERO\|shape_left\|count=0` | information_gain_generator.py |
| `EPSILON_VALUE` | 2 | `EPSILON_VALUE\|eps_122\|0` | index_gymnastics_generator.py |
| `EPS_CLOSURE` | 2 | `EPS_CLOSURE\|{u0}\|{u0,u3}` | nfa_simulation_generator.py |
| `EQUATE_EXP` | 1 | `EQUATE_EXP\|x - 3 = 2` | exponential_equation_generator.py |
| `EQUILIBRIA` | 2 | `EQUILIBRIA\|f(y) = 0\|y=3, y=12` | stability_generator.py |
| `EQ_2PT_SETUP` | 2 | `EQ_2PT_SETUP\|(-4, 2)\|(0, -4)` | equation_from_two_points_generator.py |
| `EQ_OP_BOTH` | 3, 4 | `EQ_OP_BOTH\|add\|10\|x\|8` | absolute_value_equation_generator.py, area_between_curves_generator.py, completing_square_generator.py, curve_analysis_generator.py, error_spotting_generator.py, exponential_equation_generator.py, fill_in_step_generator.py, implicit_diff_generator.py, inverse_function_generator.py, linear_fractional_generator.py, log_diff_higher_order_generator.py, log_equation_generator.py, mean_value_theorem_generator.py, one_step_equation_generator.py, optimization_generator.py, partial_fractions_generator.py, polar_parametric_generator.py, quadratic_factoring_generator.py, quadratic_square_root_generator.py, radical_equation_generator.py, rational_equation_generator.py, related_rates_generator.py, remainder_factor_theorem_generator.py, separable_ode_generator.py, special_solution_equation_generator.py, systems_elimination_generator.py, systems_substitution_generator.py, trig_equation_generator.py, two_step_equation_generator.py |
| `EQ_OP_NOTE` | 3 | `EQ_OP_NOTE\|subtract\|p\|from both sides` | equation_from_two_points_generator.py, literal_equation_generator.py, parallel_perpendicular_line_generator.py, point_slope_generator.py, standard_form_conversion_generator.py |
| `EQ_RESULT` | 2 | `EQ_RESULT\|x\|8` | completing_square_generator.py, error_spotting_generator.py, fill_in_step_generator.py, linear_fractional_generator.py, linear_simple_generator.py, one_step_equation_generator.py, quadratic_factoring_generator.py, quadratic_square_root_generator.py, radical_equation_generator.py, rational_equation_generator.py, special_solution_equation_generator.py, two_step_equation_generator.py |
| `EQ_SETUP` | 1, 2 | `EQ_SETUP\|x = 6/2` | area_between_curves_generator.py, completing_square_generator.py, complex_quadratic_generator.py, cramers_rule_generator.py, discriminant_generator.py, error_spotting_generator.py, exponential_equation_generator.py, fill_in_step_generator.py, linear_fractional_generator.py, literal_equation_generator.py, log_equation_generator.py, one_step_equation_generator.py, polynomial_zeros_generator.py, proportion_word_problem_generator.py, proportional_relationship_generator.py, quadratic_factoring_generator.py, quadratic_generator.py, quadratic_square_root_generator.py, radical_equation_generator.py, rational_equation_generator.py, remainder_factor_theorem_generator.py, special_solution_equation_generator.py, standard_form_conversion_generator.py, trig_equation_generator.py, two_step_equation_generator.py |
| `EQ_SIMPLIFY` | 1 | `EQ_SIMPLIFY\|2x = -18` | error_spotting_generator.py, fill_in_step_generator.py, linear_fractional_generator.py, two_step_equation_generator.py |
| `ESCAPE_CHECK` | 3 | `ESCAPE_CHECK\|n=1\|norm2=9/2\|escaped` | fractal_iteration_generator.py |
| `ESTIMATE` | 2 | `ESTIMATE\|59710 × 38154 ≈ 60000 × 40000\|2400000000` | long_division_generator.py, multi_digit_multiplication_generator.py |
| `ESTIMATE_CHECK` | 3 | `ESTIMATE_CHECK\|4.3 × 10^4\|43200\|rounded estimate` | fermi_estimation_generator.py, long_division_generator.py, multi_digit_multiplication_generator.py |
| `EUCLID_DIV` | 4 | `EUCLID_DIV\|511\|294\|1\|217` | continued_fraction_generator.py, extended_euclid_generator.py, modular_inverse_generator.py, rsa_generator.py |
| `EULER_BACKTRACK` | 3 | `EULER_BACKTRACK\|A\|route suffix A\|stack A-B-C-A-D-B-E` | euler_circuit_generator.py |
| `EULER_CRITERION` | 2 | `EULER_CRITERION\|36^11 mod 23\|1` | quadratic_residue_generator.py |
| `EULER_FORMULA` | 1 | `EULER_FORMULA\|χ = V - E + F` | euler_characteristic_generator.py, euler_formula_generator.py |
| `EULER_NOTE` | 2 | `EULER_NOTE\|2\|sphere-family polyhedron: χ is always 2` | euler_characteristic_generator.py |
| `EULER_ROUTE` | 2 | `EULER_ROUTE\|A-B-C-A-D-B-E-C-D-E-A\|uses 10 edges` | euler_circuit_generator.py |
| `EULER_SETUP` | 2, 3 | `EULER_SETUP\|cube: V = 8, E = 12, F = 6\|V - E + F` | euler_characteristic_generator.py, euler_formula_generator.py |
| `EULER_STACK` | 2 | `EULER_STACK\|initial\|A` | euler_circuit_generator.py |
| `EULER_START` | 2 | `EULER_START\|A\|alphabetically first vertex` | euler_circuit_generator.py |
| `EULER_TRAVERSE` | 3 | `EULER_TRAVERSE\|A->B\|AB\|stack A-B` | euler_circuit_generator.py |
| `EVAL` | 1, 2, 3 | `EVAL\|g(-6)\|28` | arc_length_generator.py, area_between_curves_generator.py, circle_equation_generator.py, complex_division_generator.py, composite_arithmetic_generator.py, conic_standard_form_generator.py, cramers_rule_generator.py, definite_integral_generator.py, derivative_limit_def_generator.py, determinant_generator.py, dot_product_generator.py, ellipse_features_generator.py, euler_method_generator.py, exact_ode_generator.py, five_number_summary_generator.py, function_composition_generator.py, function_operations_generator.py, horner_evaluation_generator.py, hyperbola_features_generator.py, improper_integral_generator.py, lagrange_multiplier_generator.py, legendre_construction_generator.py, limit_evaluation_generator.py, line_integral_generator.py, linear_approx_generator.py, log_conversion_generator.py, log_properties_generator.py, matrix_inverse_generator.py, mean_value_theorem_generator.py, ode_substitution_generator.py, parabola_features_generator.py, parametric_calculus_generator.py, partial_fractions_generator.py, power_series_generator.py, recursive_explicit_generator.py, regular_polygon_area_generator.py, related_rates_generator.py, remainder_factor_theorem_generator.py, riemann_sum_generator.py, row_reduction_generator.py, runge_kutta_generator.py, solid_revolution_generator.py, standard_deviation_generator.py, tangent_line_generator.py, taylor_series_generator.py, triangle_solve_generator.py, trig_equation_generator.py, trig_identity_eval_generator.py, trig_six_functions_generator.py, vector_ops_generator.py |
| `EVAL_AT_ZERO` | 2 | `EVAL_AT_ZERO\|e^0=1\|e^(2*0)=1` | mgf_generator.py |
| `EVAL_PARTIAL` | 3 | `EVAL_PARTIAL\|f_x\|2*2 + 4 - 3\|5` | gradient_generator.py, multivar_chain_rule_generator.py |
| `EV_FORMULA` | 1 | `EV_FORMULA\|E = Σ (payoff)·P` | expected_value_generator.py |
| `EV_SETUP` | 2 | `EV_SETUP\|P($8) = 2/5; P($-1) = 1/5; P($1) = 1/5; P($-4) = 1/5\|expected value of the game` | expected_value_generator.py |
| `EXACT_MATCH` | 2 | `EXACT_MATCH\|F_y = N\|-5*x + g'(y) = -5*x + 6*y + 2` | exact_ode_generator.py |
| `EXPAND` | 1 | `EXPAND\|cancel x^2 and y^2` | complex_locus_generator.py, mobius_transform_generator.py |
| `EXPECTATION` | 3 | `EXPECTATION\|E[X]=26/35\|E[Y]=26/35\|E[XY]=1469/2450` | joint_distribution_generator.py |
| `EXPECTED_PAYOFF` | 1 | `EXPECTED_PAYOFF\|row1 against q` | game_theory_generator.py |
| `EXP_APPLY` | 2 | `EXP_APPLY\|x(t) = e^(At)x(0)\|x(0) = [-5, -6]` | matrix_exponential_generator.py |
| `EXP_CELL` | 2 | `EXP_CELL\|(80·80)/200\|32` | chi_square_generator.py |
| `EXP_DIAG` | 2 | `EXP_DIAG\|e^(Dt)\|[[e^(3t), 0], [0, e^(6t)]]` | matrix_exponential_generator.py |
| `EXP_ENTRY` | 3 | `EXP_ENTRY\|(1,1)\|e^(3t)\|e^(3t)` | matrix_exponential_generator.py |
| `EXP_EXPAND` | 1 | `EXP_EXPAND\|(-11) × (-11) × (-11)` | exponent_generator.py |
| `EXP_FORM` | 1 | `EXP_FORM\|e^(At) = P*e^(Dt)*P^-1` | euler_formula_generator.py, matrix_exponential_generator.py |
| `EXP_PARTIAL` | 3 | `EXP_PARTIAL\|-11\|-11\|121` | exponent_generator.py |
| `EXP_RULE_APPLY` | 3, 4 | `EXP_RULE_APPLY\|multiply\|6\|4\|24` | exponent_generator.py, exponent_mixed_rules_generator.py |
| `EXP_RULE_IDENTIFY` | 2 | `EXP_RULE_IDENTIFY\|power_rule\|(x^a)^b = x^(ab)` | exponent_generator.py, exponent_mixed_rules_generator.py, rational_exponent_generator.py |
| `EXP_RULE_SETUP` | 1 | `EXP_RULE_SETUP\|((8c)^6)^4` | exponent_generator.py, exponent_mixed_rules_generator.py, rational_exponent_generator.py |
| `EXP_RULE_SIMPLIFY` | 1 | `EXP_RULE_SIMPLIFY\|(8c)^24` | exponent_generator.py, exponent_mixed_rules_generator.py |
| `EXP_SETUP` | 2 | `EXP_SETUP\|-11\|3` | exponent_generator.py |
| `EXP_SUB` | 3 | `EXP_SUB\|t/tau\|4\|e^-4` | transient_circuit_generator.py |
| `EXP_VALUE` | 2 | `EXP_VALUE\|exp(-z)\|1` | activation_generator.py |
| `EXT_GCD_SETUP` | 2 | `EXT_GCD_SETUP\|511\|294` | extended_euclid_generator.py, modular_inverse_generator.py, rsa_generator.py |
| `F` | 2, 3 | `F\|4/6\|2/3` | composite_arithmetic_generator.py, derangement_generator.py, fraction_decimal_percent_converter.py, fraction_op_generator.py, mixed_number_operation_generator.py, mobius_transform_generator.py, order_of_operations_generator.py, quaternion_generator.py, radical_rationalize_generator.py, rational_exponent_generator.py, rational_expr_add_sub_generator.py, repeating_decimal_generator.py, simple_probability_generator.py, slope_two_points_generator.py |
| `FACT` | 2 | `FACT\|9\|362880` | derangement_generator.py, named_distribution_generator.py, order_statistics_generator.py, young_tableaux_generator.py |
| `FACTOR` | 1, 2 | `FACTOR\|x^2 + 15x + 56\|(x + 8)(x + 7)` | polynomial_inequality_generator.py, second_order_ode_generator.py, transfer_function_generator.py, undetermined_coeff_generator.py, variation_parameters_generator.py |
| `FACTOR_FORM` | 2 | `FACTOR_FORM\|48\|2^4 * 3` | totient_generator.py |
| `FACTOR_FOUND` | 2 | `FACTOR_FOUND\|2\|4` | totient_generator.py |
| `FACTOR_GROUP` | 3 | `FACTOR_GROUP\|3x^2 - 9x\|3x\|(x - 3)` | conic_standard_form_generator.py, curve_analysis_generator.py, derivative_limit_def_generator.py, factor_grouping_generator.py, factor_trinomial_generator.py |
| `FACTOR_PAIR_GOAL` | 2 | `FACTOR_PAIR_GOAL\|m·n = 5\|m + n = -6` | factor_trinomial_generator.py |
| `FACTOR_SETUP` | 1 | `FACTOR_SETUP\|48` | totient_generator.py |
| `FACT_CHECK` | 3 | `FACT_CHECK\|375\|1\|0` | factors_generator.py |
| `FACT_FORMULA` | 1 | `FACT_FORMULA\|10! = 1·2·3·4·5·6·7·8·9·10` | derangement_generator.py, permutation_combination_generator.py |
| `FACT_PAIR` | 2 | `FACT_PAIR\|1\|375` | factors_generator.py |
| `FACT_SETUP` | 2 | `FACT_SETUP\|10!\|expand the factorial` | permutation_combination_generator.py |
| `FACT_VALUE` | 2 | `FACT_VALUE\|11!\|39916800` | stars_and_bars_generator.py |
| `FEATURE_MAP_SETUP` | 3 | `FEATURE_MAP_SETUP\|K(x,z)=(xz+2)^2\|phi(t)=(t^2,2t,2)\|x=11,z=-9` | feature_map_generator.py |
| `FEATURE_VECTOR` | 2 | `FEATURE_VECTOR\|phi(x)\|(121,22,2)` | feature_map_generator.py |
| `FEEDBACK` | 1 | `FEEDBACK\|T=G/(1+G)` | transfer_function_generator.py |
| `FERMAT_SETUP` | 3 | `FERMAT_SETUP\|prime 31\|base 11\|exponent 74` | totient_generator.py |
| `FERMI_FACTOR` | 2 | `FERMI_FACTOR\|students\|450` | fermi_estimation_generator.py |
| `FERMI_SETUP` | 2 | `FERMI_SETUP\|school pizza slices\|slices/year` | fermi_estimation_generator.py |
| `FIELD_SETUP` | 2 | `FIELD_SETUP\|GF(2)[x]\|addition is XOR` | finite_field_generator.py |
| `FIND_SLOPE` | 2 | `FIND_SLOPE\|Given slope (m1)\|2` | parallel_perpendicular_line_generator.py |
| `FINITE_DIFF_SETUP` | 3 | `FINITE_DIFF_SETUP\|forward_derivative\|x0=-2,h=3\|f0=17,f1=5` | finite_difference_generator.py |
| `FIN_FORMULA` | 1 | `FIN_FORMULA\|I = P*r*t; A = P + I` | finance_generator.py |
| `FIN_SETUP` | 3 | `FIN_SETUP\|simple interest P = 1000\|r = 5%, t = 4\|interest and balance` | finance_generator.py |
| `FIRSTLAW_FORMULA` | 1 | `FIRSTLAW_FORMULA\|W=P*(V2-V1)` | first_law_generator.py |
| `FIRSTLAW_SETUP` | 3 | `FIRSTLAW_SETUP\|isobaric\|P=20, V1=8, V2=12\|Q=110` | first_law_generator.py |
| `FIXED_EQ` | 1 | `FIXED_EQ\|z=(az+b)/(cz+d)` | mobius_transform_generator.py |
| `FIXED_POINT` | 1 | `FIXED_POINT\|2` | mobius_transform_generator.py |
| `FIXED_POINT_SETUP` | 3 | `FIXED_POINT_SETUP\|g(x)=5/13*x+2/5\|x0=-3/4\|iterations=3` | fixed_point_generator.py |
| `FIXED_POINT_UPDATE` | 3 | `FIXED_POINT_UPDATE\|1\|x_0=-3/4\|x_1=29/260` | fixed_point_generator.py |
| `FLAG` | 2 | `FLAG\|4\|-9 ÷ 9 = -1, not -2` | error_spotting_generator.py |
| `FLOOR_DIV` | 3 | `FLOOR_DIV\|5\|2\|2` | algorithm_trace_generator.py |
| `FLOPS_SETUP` | 2 | `FLOPS_SETUP\|rule=2mnk\|m=64,d=256,h=1024,o=64` | flops_memory_generator.py |
| `FLUX_SUM` | 2 | `FLUX_SUM\|(-1 - 3 - 1)*320\|-1600` | vector_theorem_generator.py |
| `FOCUS` | 1 | `FOCUS\|(0, -6)` | ellipse_features_generator.py, hyperbola_features_generator.py, parabola_features_generator.py |
| `FOIL_F` | 2 | `FOIL_F\|First: 7 * 8\|56` | complex_division_generator.py, complex_number_ops_generator.py, multiplying_binomials_generator.py |
| `FOIL_I` | 2 | `FOIL_I\|Inner: (-5i) * 8\|-40i` | complex_division_generator.py, complex_number_ops_generator.py, multiplying_binomials_generator.py |
| `FOIL_L` | 2 | `FOIL_L\|Last: (-5i) * (-i)\|5i^2` | complex_division_generator.py, complex_number_ops_generator.py, multiplying_binomials_generator.py |
| `FOIL_O` | 2 | `FOIL_O\|Outer: 7 * (-i)\|-7i` | complex_division_generator.py, complex_number_ops_generator.py, multiplying_binomials_generator.py |
| `FOIL_SETUP` | 1 | `FOIL_SETUP\|(4 + √6)(4 + √6)` | complex_division_generator.py, complex_number_ops_generator.py, multiplying_binomials_generator.py, radical_multiply_generator.py, trig_identity_verify_generator.py |
| `FORCE_COMPONENT` | 1 | `FORCE_COMPONENT\|parallel=m*g*sin` | newtons_laws_generator.py |
| `FORCE_EQ` | 1 | `FORCE_EQ\|m*a=parallel-friction` | newtons_laws_generator.py |
| `FORM` | 2 | `FORM\|converse\|If n is divisible by 2, then n is divisible by 24.` | conditional_forms_generator.py |
| `FORMULA` | 1, 2 | `FORMULA\|sinh x = (e^x - e^(-x))/2` | collision_generator.py, gaussian_curvature_generator.py, hyperbolic_distance_generator.py, hyperbolic_function_generator.py, or_formula_generator.py, projectile_motion_generator.py, stereographic_generator.py, uncertainty_generator.py |
| `FORM_IDENTIFY` | 2 | `FORM_IDENTIFY\|sum_of_cubes\|a^3 + b^3 = (a + b)(a^2 - ab + b^2)` | completing_square_generator.py, conic_standard_form_generator.py, ellipse_features_generator.py, factor_special_forms_generator.py, hyperbola_features_generator.py, parabola_features_generator.py, radical_multiply_generator.py, radical_rationalize_generator.py, rational_equation_generator.py, rational_exponent_generator.py, rational_expr_add_sub_generator.py, rational_expr_mult_div_generator.py |
| `FOURIER_COEF` | 1 | `FOURIER_COEF\|b_2=-1` | fourier_series_generator.py |
| `FOURIER_SETUP` | 3 | `FOURIER_SETUP\|sawtooth\|A=1\|n=2` | fourier_series_generator.py |
| `FOUR_VECTOR_SETUP` | 3 | `FOUR_VECTOR_SETUP\|signature=+---\|p=[2,-4,-2,4]\|q=[6,4,-5,4]` | four_vector_generator.py |
| `FRACTAL_SETUP` | 4 | `FRACTAL_SETUP\|mandelbrot\|z0=(0,0)\|c=(3/2,3/2)\|N=5` | fractal_iteration_generator.py |
| `FRAC_BUILD` | 2 | `FRAC_BUILD\|90/360\|0.25` | conditional_probability_generator.py, geometric_probability_generator.py |
| `FRAC_REDUCE` | 2 | `FRAC_REDUCE\|10/-15\|-2/3` | angle_measure_generator.py, arc_length_generator.py, arc_sector_generator.py, complex_division_generator.py, frequency_table_generator.py, function_operations_generator.py, hyperbola_features_generator.py, implicit_diff_generator.py, improper_integral_generator.py, probability_addition_rule_generator.py, related_rates_generator.py, right_triangle_trig_generator.py |
| `FRAC_TO_DEC` | 2 | `FRAC_TO_DEC\|43/40\|1.075` | fraction_decimal_percent_converter.py |
| `FREQ_SETUP` | 2 | `FREQ_SETUP\|table — Red: 9, Blue: 1, Green: 4, Yellow: 7, Purple: 12\|total count` | frequency_table_generator.py |
| `FUNC_OP` | 2 | `FUNC_OP\|(g - h)(-6)\|g(-6) - h(-6)` | function_composition_generator.py, function_operations_generator.py |
| `FUNC_SETUP` | 2 | `FUNC_SETUP\|h(x) = 3x + 3\|h(-1)` | domain_range_generator.py, function_composition_generator.py, function_evaluation_generator.py, function_operations_generator.py, function_table_generator.py, inverse_function_generator.py, piecewise_evaluation_generator.py, rational_function_features_generator.py |
| `FUNDAMENTAL_FORM_SETUP` | 3 | `FUNDAMENTAL_FORM_SETUP\|sphere\|R=7\|theta in [0,pi/3], phi in [60,120]` | fundamental_form_generator.py |
| `GAME_SETUP` | 2 | `GAME_SETUP\|payoffs=(1,8;12,4)\|row player maximizes, column player minimizes` | game_theory_generator.py |
| `GAMMA_SETUP` | 3 | `GAMMA_SETUP\|trace\|gamma3,gamma0\|Tr(product)` | gamma_matrix_generator.py |
| `GAS_FORMULA` | 1 | `GAS_FORMULA\|P1*V1/T1=P2*V2/T2` | gas_law_generator.py, gas_stoichiometry_generator.py |
| `GAS_SETUP` | 3 | `GAS_SETUP\|combined_pressure\|P1=12, V1=1, T1=20\|V2=3, T2=9` | gas_law_generator.py |
| `GAS_STOICH_SETUP` | 3 | `GAS_STOICH_SETUP\|mass_to_gas_pressure\|2 H2O2 -> 2 H2O + O2\|given=136 g H2O2, gas=O2` | gas_stoichiometry_generator.py |
| `GATE_MATRIX` | 2 | `GATE_MATRIX\|CNOT\|ket00bra00+ket01bra01+ket11bra10+ket10bra11` | quantum_gate_generator.py |
| `GAUSSIAN_CURVATURE_SETUP` | 2, 3 | `GAUSSIAN_CURVATURE_SETUP\|saddle\|z=(14x^2-18y^2)/2\|point=(0,0)` | gaussian_curvature_generator.py |
| `GAUSS_BONNET_SETUP` | 3 | `GAUSS_BONNET_SETUP\|flat_torus\|width=3, height=32\|chi=0` | gauss_bonnet_generator.py |
| `GAUSS_FORMULA` | 1 | `GAUSS_FORMULA\|E*(4πr^2)=Q` | gauss_law_generator.py |
| `GAUSS_SETUP` | 3 | `GAUSS_SETUP\|sphere\|Q=66\|r=10` | gauss_law_generator.py |
| `GCD` | 2 | `GCD\|gcd(1854,5040)\|18` | derangement_generator.py, pollard_factorization_generator.py |
| `GCD_RESULT` | 1, 2 | `GCD_RESULT\|1` | lcm_generator.py, modular_inverse_generator.py, permutation_group_generator.py, rsa_generator.py, totient_generator.py |
| `GCD_START` | 2 | `GCD_START\|45\|118` | gcf_generator.py, lcm_generator.py |
| `GCD_STEP` | 3 | `GCD_STEP\|45\|118\|45` | gcf_generator.py, lcm_generator.py |
| `GCF_COEFF` | 2 | `GCF_COEFF\|8, 36\|4` | factor_gcf_generator.py, quadratic_factoring_generator.py, rational_expr_simplify_generator.py |
| `GCF_RESULT` | 1 | `GCF_RESULT\|4n^2` | factor_gcf_generator.py, quadratic_factoring_generator.py, rational_expr_simplify_generator.py |
| `GCF_VAR` | 2 | `GCF_VAR\|n^4, n^2\|n^2` | factor_gcf_generator.py, quadratic_factoring_generator.py, rational_expr_simplify_generator.py |
| `GD_SETUP` | 3 | `GD_SETUP\|f(x,y)=1/2*(1x^2+6y^2)\|start=(-4,-6)\|eta=1/8` | gradient_descent_generator.py |
| `GD_UPDATE` | 3 | `GD_UPDATE\|w_old=(-2,2)\|eta=1/8\|w_new=(-7/4,7/4)` | gradient_step_generator.py |
| `GELLMANN_IDENTITY` | 3 | `GELLMANN_IDENTITY\|Tr(lambda_3 lambda_1)\|2 delta_ab\|0` | pauli_algebra_generator.py |
| `GELLMANN_SETUP` | 3 | `GELLMANN_SETUP\|trace\|A=4lambda_3\|B=4lambda_1` | pauli_algebra_generator.py |
| `GENERAL` | 2 | `GENERAL\|a_n\|C1(4)^n + C2(2)^n + 5` | recurrence_generator.py |
| `GEOMETRIC_FORMULA` | 2 | `GEOMETRIC_FORMULA\|c_n = A*(-1)^n/d^(n+1)\|A=-6, d=4` | laurent_series_generator.py |
| `GEOM_FORMULA` | 1 | `GEOM_FORMULA\|P(X > k) = (1-p)^k` | geometric_distribution_generator.py |
| `GEOM_SETUP` | 2 | `GEOM_SETUP\|p = 3/5, q = 2/5\|P(X > 3)` | geometric_distribution_generator.py |
| `GEO_PROB_FORMULA` | 1 | `GEO_PROB_FORMULA\|probability = sector angle / 360` | geometric_probability_generator.py |
| `GEO_PROB_SETUP` | 2 | `GEO_PROB_SETUP\|full circle\|sector angle 90°` | geometric_probability_generator.py |
| `GEO_SETUP` | 2 | `GEO_SETUP\|right triangle, altitude to hypotenuse; segments p = 70 (adjacent to the leg) and q = 77\|the leg adjacent to p` | geometric_mean_generator.py |
| `GF2_XOR` | 3 | `GF2_XOR\|quotient x\|0 xor 1\|1` | finite_field_generator.py |
| `GF_DIV_CHECK` | 3 | `GF_DIV_CHECK\|33 / 5\|not integer\|reject` | generating_function_generator.py |
| `GF_EXPAND` | 2 | `GF_EXPAND\|1/(1 - x^4)\|sum x^(4i), i >= 0` | generating_function_generator.py |
| `GF_SETUP` | 2 | `GF_SETUP\|[x^33]\|1/((1 - x^4)(1 - x^5))` | generating_function_generator.py |
| `GIANT_FACTOR` | 2 | `GIANT_FACTOR\|g^-m mod p\|15` | baby_step_giant_step_generator.py |
| `GIANT_STEP` | 2 | `GIANT_STEP\|i=0\|8` | baby_step_giant_step_generator.py |
| `GOAL` | 1 | `GOAL\|Convert to Slope-Intercept Form (y = mx + b)` | point_slope_generator.py, standard_form_conversion_generator.py |
| `GRAD` | 2 | `GRAD\|1\|5/14` | softmax_gradient_generator.py |
| `GRADIENT_FORMULA` | 1 | `GRADIENT_FORMULA\|grad=(1x,6y)` | gradient_descent_generator.py, matrix_calculus_generator.py |
| `GRAD_ENTRY` | 2 | `GRAD_ENTRY\|g1\|2` | matrix_calculus_generator.py |
| `GRAD_RESULT` | 2 | `GRAD_RESULT\|grad g\|(1, 1)` | lagrange_multiplier_generator.py |
| `GRAD_SETUP` | 3 | `GRAD_SETUP\|f(x,y) = x^2 + 3*y^2 + x*y - 3*x - 5*y\|point (2, 4)\|gradient` | gradient_generator.py |
| `GRAPH_CHANGE` | 3 | `GRAPH_CHANGE\|9am\|10am\|4` | graph_interpret_generator.py |
| `GRAPH_DATA` | 2 | `GRAPH_DATA\|bar_chart\|Art:10,Music:42,Science:30,Math:23` | graph_interpret_generator.py |
| `GRAPH_MAX` | 2 | `GRAPH_MAX\|Music\|42` | graph_interpret_generator.py |
| `GRAPH_MAX_CHANGE` | 3 | `GRAPH_MAX_CHANGE\|10am\|11am\|7` | graph_interpret_generator.py |
| `GRAPH_MIN` | 2 | `GRAPH_MIN\|Soccer\|11` | graph_interpret_generator.py |
| `GRAPH_READ` | 2 | `GRAPH_READ\|Art\|10` | graph_interpret_generator.py |
| `GRAPH_SETUP` | 2 | `GRAPH_SETUP\|vertices A, B, C, D, E\|edges AB, BC, BD, BE, CD` | dijkstra_generator.py, euler_circuit_generator.py, graph_counting_generator.py, graph_traversal_generator.py |
| `GRASSMANN_RESULT` | 3 | `GRASSMANN_RESULT\|constant=-45\|theta=-19\|-45 - 19theta` | grassmann_generator.py |
| `GRASSMANN_SETUP` | 3 | `GRASSMANN_SETUP\|multiply_integrate\|x=5 + theta\|y=-9 - 2theta` | grassmann_generator.py |
| `GREAT_CIRCLE_SETUP` | 3 | `GREAT_CIRCLE_SETUP\|R=8\|A=(0,90)\|B=(60,-90)` | great_circle_generator.py |
| `GROUP` | 2 | `GROUP\|(3x^2 - 9x)\|(4x - 12)` | factor_grouping_generator.py, factor_trinomial_generator.py |
| `GROUP_MULT` | 3 | `GROUP_MULT\|e\|e\|e` | coset_generator.py |
| `GROUP_SETUP` | 2, 3 | `GROUP_SETUP\|U(28)\|multiplication mod n` | cayley_table_generator.py, coset_generator.py, cyclic_group_generator.py |
| `GS_SETUP` | 2 | `GS_SETUP\|vectors [[-2, -1], [1, 3]]\|orthogonal basis, not normalized` | gram_schmidt_generator.py |
| `GS_SUBTRACT` | 2 | `GS_SUBTRACT\|remove projection on u1\|[-1, 2]` | gram_schmidt_generator.py, qr_decomposition_generator.py |
| `GS_VECTOR` | 2 | `GS_VECTOR\|u1 = v1\|[-2, -1]` | gram_schmidt_generator.py |
| `HA` | 1 | `HA\|y = 3/2` | rational_function_features_generator.py |
| `HAMILTON` | 2 | `HAMILTON\|i*i\|-1` | quaternion_generator.py |
| `HAMILTONIAN` | 1 | `HAMILTONIAN\|H=p_theta^2/(2mL^2)+mgL*(1-cos(theta))` | hamiltonian_generator.py |
| `HAMMING_PLACE` | 2 | `HAMMING_PLACE\|positions 1,2,3,4,5,6,7\|p1,p2,d1,p4,d2,d3,d4` | hamming_code_generator.py |
| `HAMMING_RECEIVED` | 1 | `HAMMING_RECEIVED\|r=0001010` | hamming_code_generator.py |
| `HAMMING_SETUP` | 2 | `HAMMING_SETUP\|data=0101\|even parity` | hamming_code_generator.py |
| `HAM_EQ` | 2 | `HAM_EQ\|thetadot=dH/dp_theta\|thetadot=p_theta/360` | hamiltonian_generator.py |
| `HAM_SETUP` | 3 | `HAM_SETUP\|pendulum\|m=10, L=6\|g=10, q=theta` | hamiltonian_generator.py |
| `HARMONIC_SETUP` | 1 | `HARMONIC_SETUP\|u=3x^2 - 3y^2 - 4x - 3y` | cauchy_riemann_generator.py |
| `HAWKING_SETUP` | 3 | `HAWKING_SETUP\|entropy\|S_BH=k_B*c^3*A/(4*hbar*G)\|k_B=4,c=5,A=61,hbar=7,G=10` | hawking_generator.py |
| `HESSIAN_DET` | 3 | `HESSIAN_DET\|D = f_xx*f_yy - f_xy^2\|(-2)*(-10) - 4^2\|4` | hessian_classify_generator.py |
| `HESSIAN_SETUP` | 2 | `HESSIAN_SETUP\|f(x,y) = -x^2 - 5*y^2 + 4*x*y + 8*x - 20*y\|find and classify the critical point` | hessian_classify_generator.py |
| `HESSIAN_TEST` | 3 | `HESSIAN_TEST\|D = 4\|f_xx = -2\|local maximum` | hessian_classify_generator.py |
| `HIDDEN_PRE` | 2 | `HIDDEN_PRE\|h1\|z=2` | backprop_generator.py |
| `HIT_EQ` | 2 | `HIT_EQ\|t0=1+p00*t0+p01*t1\|t1=1+p10*t0+p11*t1` | markov_chain_generator.py |
| `HMM_SETUP` | 2 | `HMM_SETUP\|states H,L\|observations BAA` | viterbi_generator.py |
| `HMM_START` | 1 | `HMM_START\|H=1/2, L=1/2` | viterbi_generator.py |
| `HOLE` | 1 | `HOLE\|x = 3` | rational_function_features_generator.py |
| `HOM_SOL` | 2 | `HOM_SOL\|y_h\|y_h = C1e^(-4x) + C2e^(-2x)` | undetermined_coeff_generator.py, variation_parameters_generator.py |
| `HOOK` | 4 | `HOOK\|(1,1)\|right=2\|below=4\|hook=7` | young_tableaux_generator.py |
| `HORNER_SETUP` | 2 | `HORNER_SETUP\|x^3 + x^2 - 2x + 5\|x = -4` | horner_evaluation_generator.py |
| `HT_SETUP` | 2 | `HT_SETUP\|H0: μ = 85; Ha: μ ≠ 85\|n = 400, x̄ = 92, s = 50, critical value = 1.96` | hypothesis_test_generator.py, two_sample_test_generator.py |
| `HUFFMAN_FORMULA` | 1 | `HUFFMAN_FORMULA\|L=sum p_i*l_i` | huffman_coding_generator.py |
| `HUFFMAN_MERGE` | 2 | `HUFFMAN_MERGE\|A:1/8 + B:1/8\|AB:1/4` | huffman_coding_generator.py |
| `HUFFMAN_SETUP` | 1 | `HUFFMAN_SETUP\|A=1/8, B=1/8, C=1/8, D=1/4, E=1/8, F=1/8, G=1/8` | huffman_coding_generator.py |
| `HYDROGEN_FORMULA` | 1 | `HYDROGEN_FORMULA\|Delta_E=R_E*(1/n_low^2-1/n_high^2)` | hydrogen_atom_generator.py |
| `HYDROGEN_SETUP` | 3 | `HYDROGEN_SETUP\|transition_energy\|n_low=4, n_high=12\|R_E=34 eV` | hydrogen_atom_generator.py |
| `HYPERBOLIC_DISTANCE_SETUP` | 3 | `HYPERBOLIC_DISTANCE_SETUP\|disk\|P=(0,0)\|Q=(4/9,0)` | hyperbolic_distance_generator.py |
| `HYPERBOLIC_SETUP` | 2 | `HYPERBOLIC_SETUP\|e^x=28/15\|e^(-x)=15/28` | hyperbolic_function_generator.py |
| `HYPERCUBE_FORMULA` | 1 | `HYPERCUBE_FORMULA\|diagonal = s·√n` | hypercube_counting_generator.py |
| `HYPERCUBE_SETUP` | 2 | `HYPERCUBE_SETUP\|5-cube with side 8\|main diagonal` | hypercube_counting_generator.py |
| `I` | 2 | `I\|7/2\|2/7` | fraction_op_generator.py, mixed_number_operation_generator.py, rational_expr_mult_div_generator.py |
| `ICE_ROW` | 2 | `ICE_ROW\|initial\|[A]=8, [B]=0` | equilibrium_ice_generator.py |
| `IDENTIFY` | 2 | `IDENTIFY\|order matters\|use P(n, r)` | permutation_combination_generator.py |
| `IDENTITY` | 2 | `IDENTITY\|Vandermonde\|Σ C(15,i)C(15,8-i) = C(30,8)` | counting_classics_generator.py, function_inner_product_generator.py, index_gymnastics_generator.py |
| `IDENTITY_SETUP` | 2 | `IDENTITY_SETUP\|verify: cos x · cot x = csc x - sin x\|transform the right side` | trig_identity_verify_generator.py |
| `IDENT_MATCH` | 1 | `IDENT_MATCH\|cos x · cot x = cos x · cot x` | trig_identity_verify_generator.py |
| `IDENT_SUB` | 1, 2 | `IDENT_SUB\|csc x = 1/sin x` | parametric_calculus_generator.py, trig_identity_verify_generator.py |
| `IE_FORMULA` | 2 | `IE_FORMULA\|n(A union B union C)\|n(A)+n(B)+n(C) - n(AB)-n(AC)-n(BC) + n(ABC)` | inclusion_exclusion_generator.py |
| `IE_SETUP` | 2 | `IE_SETUP\|n(A)=27, n(B)=28, n(C)=35\|n(AB)=12, n(AC)=7, n(BC)=17, n(ABC)=5` | inclusion_exclusion_generator.py |
| `IFACTOR` | 2 | `IFACTOR\|mu = e^(∫ 5 dx)\|e^(5x)` | integrating_factor_generator.py, ode_substitution_generator.py |
| `IG_SETUP` | 3 | `IG_SETUP\|parent pos=8, neg=8\|total=16\|splits=texture,shape` | information_gain_generator.py |
| `IMAGE` | 2 | `IMAGE\|T(-1)\|-6/5` | mobius_transform_generator.py |
| `IMPLICIT_DIFF` | 2 | `IMPLICIT_DIFF\|d/dx of xy\|y + x·y' (product rule)` | implicit_diff_generator.py, log_diff_higher_order_generator.py, related_rates_generator.py |
| `IMPLICIT_SETUP` | 2 | `IMPLICIT_SETUP\|xy = -2\|dy/dx` | implicit_diff_generator.py |
| `IMPROPER_TO_MIX` | 2 | `IMPROPER_TO_MIX\|477/55\|8 37/55` | composite_arithmetic_generator.py, mixed_number_operation_generator.py, order_of_operations_generator.py |
| `INDEGREE` | 2 | `INDEGREE\|A\|0` | graph_traversal_generator.py |
| `INDEGREE_UPDATE` | 2 | `INDEGREE_UPDATE\|B\|0` | graph_traversal_generator.py |
| `INDEP_CHECK` | 3 | `INDEP_CHECK\|P11=1469/2450\|product=676/1225\|no` | joint_distribution_generator.py |
| `INDEP_FORMULA` | 1 | `INDEP_FORMULA\|independent iff P11=P(X=1)P(Y=1)` | joint_distribution_generator.py |
| `INDEX` | 3 | `INDEX\|G size 6\|H size 3\|2` | coset_generator.py |
| `INDEX_METRIC` | 3 | `INDEX_METRIC\|raise\|Minkowski\|g^ii=[-1,1,1,1]` | index_raising_generator.py |
| `INDEX_SETUP` | 3 | `INDEX_SETUP\|c=2\|j=2, k=2\|l=2, m=3` | index_gymnastics_generator.py |
| `INDUCT_ASSUME` | 1 | `INDUCT_ASSUME\|sum to k = (7^(k+1)-1)/(7-1)` | induction_verify_generator.py |
| `INDUCT_BASE` | 2 | `INDUCT_BASE\|n=0\|1 = (r^1-1)/(r-1)` | induction_verify_generator.py |
| `INDUCT_STEP` | 1, 2 | `INDUCT_STEP\|add 7^(k+1)` | induction_verify_generator.py |
| `INEQ_FLIP` | 1 | `INEQ_FLIP\|Dividing by negative number reverses inequality` | domain_range_generator.py, linear_fractional_generator.py, one_step_inequality_generator.py, two_step_inequality_generator.py |
| `INEQ_OP_ALL` | 3 | `INEQ_OP_ALL\|add\|5\|-10 < 2x < 20` | absolute_value_inequality_generator.py, compound_inequality_generator.py |
| `INEQ_OP_BOTH` | 4 | `INEQ_OP_BOTH\|divide\|-9\|x\|10` | domain_range_generator.py, linear_fractional_generator.py, one_step_inequality_generator.py, two_step_inequality_generator.py |
| `INEQ_RESULT` | 3 | `INEQ_RESULT\|x\|>\|10` | domain_range_generator.py, linear_fractional_generator.py, one_step_inequality_generator.py, two_step_inequality_generator.py |
| `INEQ_SETUP` | 1 | `INEQ_SETUP\|-9x < -90` | linear_fractional_generator.py, one_step_inequality_generator.py, polynomial_inequality_generator.py, two_step_inequality_generator.py |
| `INEQ_SIMPLIFY` | 1 | `INEQ_SIMPLIFY\|6x < -36` | domain_range_generator.py, linear_fractional_generator.py, two_step_inequality_generator.py |
| `INFO_GAIN` | 2 | `INFO_GAIN\|texture\|0.045625` | information_gain_generator.py |
| `INFO_SETUP` | 2 | `INFO_SETUP\|p=1/128\|I=-log2(p)` | entropy_generator.py |
| `INFO_TABLE` | 1 | `INFO_TABLE\|3/8=1.415, 1/2=1, 5/8=0.678, 1=0` | information_gain_generator.py |
| `INFO_VALUE` | 2 | `INFO_VALUE\|p=1/2\|I=1` | information_gain_generator.py |
| `INITIAL` | 2 | `INITIAL\|D_0 = 1\|D_1 = 0` | derangement_generator.py |
| `INITIAL_COEFF` | 2 | `INITIAL_COEFF\|a_0\|5280` | series_solution_generator.py |
| `INITIAL_EQ` | 2 | `INITIAL_EQ\|C1 + C2\|-3` | recurrence_generator.py |
| `INITIAL_SYSTEM` | 2 | `INITIAL_SYSTEM\|C1[2, 1] + C2[1, 0]\|[7, 2]` | ode_system_generator.py |
| `INNER_ANTIDERIV` | 2 | `INNER_ANTIDERIV\|dx\|10*x` | double_integral_generator.py, triple_integral_generator.py |
| `INNER_EVAL` | 2, 3 | `INNER_EVAL\|x=y/2..7\|10*(7 - y/2)` | double_integral_generator.py, triple_integral_generator.py |
| `INNER_PRODUCT` | 2 | `INNER_PRODUCT\|inner(phi,psi)\|3+i` | braket_generator.py |
| `INNER_PRODUCT_SETUP` | 3 | `INNER_PRODUCT_SETUP\|interval=[0,2pi]\|f=sin(13x)\|g=cos(23x)` | function_inner_product_generator.py |
| `INSERT_KEY` | 3 | `INSERT_KEY\|pass 1\|13\|index 1` | algorithm_trace_generator.py |
| `INSERT_PLACE` | 2 | `INSERT_PLACE\|index 0\|13, 25, 12, 32, 10, 15, 35` | algorithm_trace_generator.py |
| `INTEGRAL` | 1, 2 | `INTEGRAL\|integral sin(36x) on [0,2pi]\|0` | fourier_series_generator.py, function_inner_product_generator.py, legendre_construction_generator.py |
| `INTEGRAL_SETUP` | 1 | `INTEGRAL_SETUP\|L = integral from r0 to r1 of 1 dr` | metric_arc_length_generator.py |
| `INTEGRATE` | 2 | `INTEGRATE\|v_y = u_x\|v=6xy + 3x - 4y + phi(x)` | cauchy_riemann_generator.py |
| `INTEGRATION_BY_PARTS` | 2 | `INTEGRATION_BY_PARTS\|u=x\|dv=sin(nx)dx` | fourier_series_generator.py |
| `INTEG_RULE` | 2 | `INTEG_RULE\|trig rule\|∫ cos(u) du = sin(u) + C` | antiderivative_generator.py, definite_integral_generator.py, ode_substitution_generator.py, partial_fractions_generator.py, separable_ode_generator.py, solid_revolution_generator.py, u_substitution_generator.py |
| `INTEG_SETUP` | 2 | `INTEG_SETUP\|∫ 2 cos(x) dx\|antiderivative` | antiderivative_generator.py, arc_length_generator.py, definite_integral_generator.py, improper_integral_generator.py, integration_by_parts_generator.py, parametric_calculus_generator.py, partial_fractions_generator.py, u_substitution_generator.py |
| `INTERCEPT_FORMULA` | 1 | `INTERCEPT_FORMULA\|a = ȳ - b·x̄` | regression_generator.py |
| `INTERFERENCE_FORMULA` | 1 | `INTERFERENCE_FORMULA\|d*sin(theta)=m*lambda` | interference_generator.py |
| `INTERFERENCE_SETUP` | 3 | `INTERFERENCE_SETUP\|diffraction_grating\|m=3, lambda=11\|d=64` | interference_generator.py |
| `INTERP_SETUP` | 3 | `INTERP_SETUP\|lagrange\|points=(-3,10), (-2,5), (4,17)\|x=0` | interpolation_generator.py |
| `INTERVAL_CLASS` | 2 | `INTERVAL_CLASS\|s2=-279\|spacelike` | minkowski_interval_generator.py |
| `INT_ABS` | 2 | `INT_ABS\|-7\|7` | integer_operations_generator.py |
| `INT_ALIGN` | 2 | `INT_ALIGN\|82320\|65750` | multi_digit_addition_generator.py, multi_digit_subtraction_generator.py |
| `INT_APPLY_SIGN` | 3 | `INT_APPLY_SIGN\|6\|negative\|-6` | integer_operations_generator.py |
| `INT_OP` | 4 | `INT_OP\|-\|7\|1\|6` | integer_operations_generator.py |
| `INT_REWRITE` | 2 | `INT_REWRITE\|-7 - (-1)\|-7 + 1` | integer_operations_generator.py |
| `INT_SIGN_RULE` | 2 | `INT_SIGN_RULE\|subtract_rule\|Subtracting is adding the opposite` | integer_operations_generator.py |
| `INVERSE_LAPLACE` | 2 | `INVERSE_LAPLACE\|-4/(s + 5)\|-4e^(-5t)` | laplace_ivp_generator.py |
| `INVERSE_MAP` | 2 | `INVERSE_MAP\|x=(u+v)/2\|y=(u-v)/2` | rv_transform_generator.py |
| `INVERSE_METRIC` | 2 | `INVERSE_METRIC\|g^rr=1\|g^thetatheta=1/r^2` | christoffel_generator.py, riemann_tensor_generator.py |
| `INV_FORMULA` | 1 | `INV_FORMULA\|A⁻¹ = (1/det)·[[d, -b], [-c, a]]` | matrix_inverse_generator.py |
| `IRR_SETUP` | 2 | `IRR_SETUP\|c0=-2500,c1=5000\|r0=0,iterations=2` | npv_irr_generator.py |
| `IRR_VALUE` | 2 | `IRR_VALUE\|f1\|2500` | npv_irr_generator.py |
| `ITERATE` | 2 | `ITERATE\|n=1\|z=(3/2,3/2)` | fractal_iteration_generator.py, gradient_descent_generator.py |
| `IVT_SETUP` | 2 | `IVT_SETUP\|f(x) = x^3 - x - 9 on [-2, -1]\|does the IVT guarantee a root?` | mean_value_theorem_generator.py |
| `I_CYCLE` | 2 | `I_CYCLE\|i^2\|-1` | complex_number_ops_generator.py |
| `I_SQUARE` | 2 | `I_SQUARE\|5i^2\|-5` | complex_division_generator.py, complex_log_generator.py, complex_number_ops_generator.py |
| `JACOBIAN` | 2 | `JACOBIAN\|dA\|r dr dtheta` | double_integral_generator.py |
| `JACOBI_END` | 2 | `JACOBI_END\|gcd(145,105)>1\|0` | jacobi_symbol_generator.py |
| `JACOBI_RECIPROCITY` | 3 | `JACOBI_RECIPROCITY\|a mod 4 = 1\|n mod 4 = 1\|keep sign` | jacobi_symbol_generator.py |
| `JACOBI_SETUP` | 3 | `JACOBI_SETUP\|a=145\|n=105\|n odd` | jacobi_symbol_generator.py |
| `JACOBI_SWAP` | 3 | `JACOBI_SWAP\|a=105\|n=5\|sign 1` | jacobi_symbol_generator.py |
| `JACOBI_TWO_RULE` | 3 | `JACOBI_TWO_RULE\|n mod 8 = 1\|keep sign\|sign 1` | jacobi_symbol_generator.py |
| `JAC_DET` | 3 | `JAC_DET\|x_u*y_v - x_v*y_u\|2*(-3) - 1*5\|-11` | jacobian_generator.py |
| `JAC_MATRIX` | 2 | `JAC_MATRIX\|[[x_u, x_v], [y_u, y_v]]\|[[2, 1], [5, -3]]` | jacobian_generator.py, rv_transform_generator.py |
| `JAC_SETUP` | 3 | `JAC_SETUP\|x = 2*u + v\|y = 5*u - 3*v\|d(x,y)/d(u,v)` | jacobian_generator.py |
| `JOINT_SETUP` | 3 | `JOINT_SETUP\|X,Y in {0,1}\|p00=279/2450, p01=351/2450\|p10=351/2450, p11=1469/2450` | joint_distribution_generator.py |
| `KERNEL_BASE` | 3 | `KERNEL_BASE\|A,A\|dot+c=10+0\|10` | feature_map_generator.py, kernel_evaluation_generator.py |
| `KERNEL_EXPONENT` | 2 | `KERNEL_EXPONENT\|A,A\|0` | kernel_evaluation_generator.py |
| `KERNEL_SETUP` | 3 | `KERNEL_SETUP\|type=rbf\|points=A=(3,3), B=(1,1)\|gamma=1/2` | kernel_evaluation_generator.py |
| `KERNEL_VALIDITY` | 1 | `KERNEL_VALIDITY\|psd=true` | kernel_validity_generator.py |
| `KERNEL_VALUE` | 2 | `KERNEL_VALUE\|A,A\|1` | feature_map_generator.py, kernel_evaluation_generator.py, kernel_perceptron_generator.py, kernel_ridge_generator.py |
| `KIN_FORMULA` | 1 | `KIN_FORMULA\|a = (v_f - v_i)/t` | invariant_mass_generator.py, kinematics_generator.py |
| `KIN_SETUP` | 3, 4 | `KIN_SETUP\|v_i = 2 m/s\|v_f = 20 m/s, t = 3 s\|acceleration` | invariant_mass_generator.py, kinematics_generator.py |
| `KL_FORMULA` | 1 | `KL_FORMULA\|D=sum source_i*log2(source_i/target_i)` | kl_divergence_generator.py |
| `KL_SETUP` | 3 | `KL_SETUP\|P=[1024/1365,341/1365]\|Q=[1/1365,1364/1365]\|direction=P to Q` | kl_divergence_generator.py |
| `KMAP_GROUP` | 2 | `KMAP_GROUP\|10, 11\|A` | boolean_algebra_generator.py |
| `KMAP_ROW` | 2 | `KMAP_ROW\|A=0\|0, 1` | boolean_algebra_generator.py |
| `KMAP_SETUP` | 2 | `KMAP_SETUP\|rows A=0,A=1\|columns B=0,B=1` | boolean_algebra_generator.py |
| `KMAP_SIMPLIFY` | 1 | `KMAP_SIMPLIFY\|A OR B` | boolean_algebra_generator.py |
| `KMEANS_SETUP` | 2 | `KMEANS_SETUP\|points=P1=(0,0), P2=(-1,-3), P3=(-1,4), P4=(-5,1)\|centroids=C1=(0,3), C2=(-1,2)` | kmeans_step_generator.py |
| `KNN_DISTANCE` | 3 | `KNN_DISTANCE\|P1\|label=A\|d2=25` | knn_generator.py |
| `KNN_NEIGHBORS` | 1 | `KNN_NEIGHBORS\|P3:1:A,P4:18:A,P1:25:A` | knn_generator.py |
| `KNN_SETUP` | 3 | `KNN_SETUP\|q=(5,-5)\|k=3\|training=P1=(0,-5,A), P2=(-5,4,B), P3=(5,-4,A), P4=(2,-2,A), P5=(0,1,A)` | knn_generator.py |
| `KNN_SORT` | 1 | `KNN_SORT\|P3:1:A,P4:18:A,P1:25:A,P5:61:A,P2:181:B` | knn_generator.py |
| `KP_EXAMPLE` | 3 | `KP_EXAMPLE\|1\|x=-6,y=1\|alpha=(0,0,0)` | kernel_perceptron_generator.py |
| `KP_SETUP` | 3 | `KP_SETUP\|kernel=linear\|data=[(-6,1), (2,1), (4,-1)]\|alpha0=(0,0,0)` | kernel_perceptron_generator.py |
| `KP_TERM` | 2 | `KP_TERM\|j=1\|0` | kernel_perceptron_generator.py |
| `KRAFT_CHECK` | 2, 3 | `KRAFT_CHECK\|sum=1\|complete` | huffman_coding_generator.py, kraft_inequality_generator.py |
| `KRAFT_CLASSIFY` | 2 | `KRAFT_CLASSIFY\|excess=15/16\|no prefix code` | kraft_inequality_generator.py |
| `KRAFT_FORMULA` | 1 | `KRAFT_FORMULA\|sum 2^-l_i` | huffman_coding_generator.py, kraft_inequality_generator.py |
| `KRAFT_SETUP` | 2 | `KRAFT_SETUP\|A=1, B=2, C=1, D=5, E=1, F=3, G=5\|binary prefix code` | kraft_inequality_generator.py |
| `KRAFT_TERM` | 3 | `KRAFT_TERM\|A\|l=1\|1/2` | kraft_inequality_generator.py |
| `KRR_SETUP` | 3 | `KRR_SETUP\|kernel=linear\|data=[(5,5), (-6,1)]\|lambda=3,x*=-6` | kernel_ridge_generator.py |
| `KV_CACHE` | 2 | `KV_CACHE\|values\|16777216` | flops_memory_generator.py |
| `K_EXPR` | 1, 2 | `K_EXPR\|K = [B]^2/[A]\|8/3 = (2x)^2/(8-x)` | equilibrium_ice_generator.py |
| `L` | 3 | `L\|3\|7\|21` | fraction_comparison_generator.py, fraction_op_generator.py, linear_fractional_generator.py, mixed_number_operation_generator.py, rational_expr_add_sub_generator.py |
| `LABEL_COUNT` | 2 | `LABEL_COUNT\|A\|3` | knn_generator.py |
| `LADDER_APPLY` | 2 | `LADDER_APPLY\|a ket26\|sqrt(26) ket25` | ladder_operator_generator.py |
| `LADDER_COMM` | 2 | `LADDER_COMM\|[a,adag] ketn\|ket29` | ladder_operator_generator.py |
| `LADDER_RULE` | 2 | `LADDER_RULE\|J_- = J1_- + J2_-\|lower from highest weights` | clebsch_gordan_generator.py, ladder_operator_generator.py |
| `LADDER_SETUP` | 3 | `LADDER_SETUP\|number_energy\|state=ket26\|hbar=5, omega=2` | ladder_operator_generator.py |
| `LAGRANGE_EQ` | 2 | `LAGRANGE_EQ\|f_x = lambda\|y^3` | lagrange_multiplier_generator.py |
| `LAGRANGE_FACTOR` | 3 | `LAGRANGE_FACTOR\|L_0\|j=1\|-2` | interpolation_generator.py |
| `LAGRANGE_SETUP` | 3 | `LAGRANGE_SETUP\|f(x,y) = x*y^3\|constraint x + y = 16\|maximize` | lagrange_multiplier_generator.py |
| `LAGRANGIAN` | 1, 2 | `LAGRANGIAN\|L=T-V` | lagrangian_generator.py |
| `LAG_SETUP` | 3 | `LAG_SETUP\|pendulum\|m=3, L=2\|g=10, q=theta` | lagrangian_generator.py |
| `LAMBDA_SETUP` | 2 | `LAMBDA_SETUP\|((lambda c. d) (lambda c. (lambda p. p)))\|leftmost-outermost` | lambda_reduction_generator.py |
| `LAPLACE` | 2 | `LAPLACE\|L[y' + 5y]\|(sY + 3) + 5Y` | laplace_ivp_generator.py, transfer_function_generator.py |
| `LAPLACE_TABLE` | 1 | `LAPLACE_TABLE\|L{y'} = sY - y(0); L{e^(kt)} = 1/(s-k); L^-1{1/(s-k)} = e^(kt)` | laplace_ivp_generator.py |
| `LAURENT_SETUP` | 3 | `LAURENT_SETUP\|center a=2\|w=(z-2)\|f=(6 + 4(z-2) - 2(z-2)^2 + (z-2)^3 - 6(z-2)^4 - 3(z-2)^5 - 5(z-2)^6)/(z-2)^2` | laurent_series_generator.py |
| `LAURENT_TERM` | 1 | `LAURENT_TERM\|5(z+4)^-3` | residue_generator.py |
| `LAYERNORM_SETUP` | 3 | `LAYERNORM_SETUP\|x=(-9,1)\|gamma=(4,3)\|beta=(5,4)` | layer_norm_generator.py |
| `LCM_FROM_GCD` | 3 | `LCM_FROM_GCD\|90*53\|1\|4770` | lcm_generator.py |
| `LCM_STEP` | 3 | `LCM_STEP\|1\|2\|2` | permutation_group_generator.py, pollard_factorization_generator.py |
| `LEADING_MINOR` | 2 | `LEADING_MINOR\|Delta1\|-4` | positive_definite_generator.py |
| `LEGENDRE_RESULT` | 3 | `LEGENDRE_RESULT\|1\|1\|quadratic residue` | quadratic_residue_generator.py |
| `LEGENDRE_SETUP` | 2 | `LEGENDRE_SETUP\|a=36\|p=23` | legendre_construction_generator.py, quadratic_residue_generator.py |
| `LIE_EXP_FORM` | 2 | `LIE_EXP_FORM\|e^(theta J)\|cos(theta)I + sin(theta)J` | lie_exponential_generator.py |
| `LIE_EXP_SETUP` | 4 | `LIE_EXP_SETUP\|SO3\|axis=z\|theta=1050 deg\|K=[[0, -1, 0], [1, 0, 0], [0, 0, 0]]` | lie_exponential_generator.py |
| `LIMITING_REAGENT` | 2 | `LIMITING_REAGENT\|H2\|H2O=10 mol` | stoichiometry_generator.py |
| `LIMIT_CHECK` | 2 | `LIMIT_CHECK\|H2O from H2=10 mol\|H2O from O2=20 mol` | stoichiometry_generator.py |
| `LIMIT_SETUP` | 1, 2 | `LIMIT_SETUP\|lim x→-6⁻ of abs(x + 6)/(x + 6)\|one-sided: approach from the left` | derivative_limit_def_generator.py, improper_integral_generator.py, lhopital_generator.py, limit_evaluation_generator.py, power_series_generator.py, series_convergence_generator.py |
| `LINEAR_SYSTEM` | 2 | `LINEAR_SYSTEM\|a=9/11, b=-4/11\|c=-1/3, d=2/3` | markov_chain_generator.py |
| `LINE_EQ` | 1 | `LINE_EQ\|-8x + 16y - 40 = 0` | complex_locus_generator.py |
| `LINE_INTEGRAL` | 3 | `LINE_INTEGRAL\|int_0^1 dot dt\|-1/2 + 12\|23/2` | line_integral_generator.py |
| `LINE_RELATION_SETUP` | 3 | `LINE_RELATION_SETUP\|parallel\|y = 2x - 10\|(-6, -7)` | parallel_perpendicular_line_generator.py |
| `LINE_SETUP` | 2 | `LINE_SETUP\|F(x,y) = <4*x + y - 4, 10*y + x + 3>\|from (1, 4) to (-1, 1)` | line_integral_generator.py |
| `LLL_DONE` | 1 | `LLL_DONE\|[(-1,6),(-9,-1)]` | lll_reduction_generator.py |
| `LLL_SETUP` | 1 | `LLL_SETUP\|[(-10,5),(9,1)]` | lll_reduction_generator.py |
| `LOCUS_SETUP` | 3 | `LOCUS_SETUP\|z=x+iy\|center=(-2,-5)\|radius=5` | complex_locus_generator.py |
| `LOG2` | 2 | `LOG2\|1/16\|-4` | entropy_generator.py, huffman_coding_generator.py, mutual_information_generator.py, von_neumann_entropy_generator.py |
| `LOG2_RATIO` | 3 | `LOG2_RATIO\|i=0\|ratio=1024\|log=10` | kl_divergence_generator.py |
| `LOG_BOTH_SIDES` | 1 | `LOG_BOTH_SIDES\|log_5(5^x) = log_5(55)` | exponential_equation_generator.py, log_diff_higher_order_generator.py, separable_ode_generator.py |
| `LOG_EVAL` | 2 | `LOG_EVAL\|13/5\|ln(13/5)` | hyperbolic_distance_generator.py |
| `LOG_EXACT` | 2 | `LOG_EXACT\|log_10(1000000)\|6` | master_theorem_generator.py |
| `LOG_FORM` | 1 | `LOG_FORM\|log_b(x) = y ⟺ b^y = x` | log_conversion_generator.py, log_equation_generator.py |
| `LOG_FORMULA` | 1 | `LOG_FORMULA\|log z = ln r + i(arg + 2pi*k)` | complex_log_generator.py |
| `LOG_IDENT` | 2 | `LOG_IDENT\|ln(1) = 0\|0` | exponential_equation_generator.py, log_conversion_generator.py |
| `LOG_LIKELIHOOD` | 1 | `LOG_LIKELIHOOD\|ell(lambda)=9*log(lambda)-62*lambda` | mle_generator.py |
| `LOG_ONE_TO_ONE` | 1 | `LOG_ONE_TO_ONE\|3x + 5 = x - 3` | log_equation_generator.py |
| `LOG_POWER` | 2 | `LOG_POWER\|log_2(x^3)\|3log_2(x)` | derivative_transcendental_generator.py, log_diff_higher_order_generator.py, log_properties_generator.py, ph_calculation_generator.py |
| `LOG_PRODUCT` | 1, 2 | `LOG_PRODUCT\|log_2(4x^3y^2)\|log_2(4x^3) + log_2(y^2)` | log_equation_generator.py, log_properties_generator.py, ph_calculation_generator.py |
| `LOG_QUOTIENT` | 2 | `LOG_QUOTIENT\|log_2(x^3y^3) - log_2(z^3)\|log_2(x^3y^3/z^3)` | log_properties_generator.py |
| `LOG_SETUP` | 1, 2 | `LOG_SETUP\|log_2(4x^3y^2)\|expand` | complex_log_generator.py, log_properties_generator.py |
| `LOG_SOFTMAX` | 2 | `LOG_SOFTMAX\|1\|ln(5/14)` | softmax_gradient_generator.py |
| `LOG_SUPPLIED` | 2 | `LOG_SUPPLIED\|log10(1/100)\|-2` | signal_arithmetic_generator.py |
| `LOG_TERM` | 3 | `LOG_TERM\|18\|ln(2)\|18*ln(2)` | entropy_change_generator.py |
| `LOOKUP_SUPPLIED` | 2 | `LOOKUP_SUPPLIED\|e^-1\|3679/10000` | named_distribution_generator.py |
| `LORA_COUNT` | 2 | `LORA_COUNT\|r*(d_in+d_out)\|35392` | param_count_generator.py |
| `LOWRANK_SETUP` | 2 | `LOWRANK_SETUP\|A=[[14,0], [0,20]]\|rank=1` | low_rank_approx_generator.py |
| `LP_CORNER_SETUP` | 3 | `LP_CORNER_SETUP\|max z=x+3y\|0<=x<=22, 0<=y<=8\|x+y<=23` | lp_corner_generator.py |
| `LR_PHASE` | 1 | `LR_PHASE\|decay` | lr_schedule_generator.py |
| `LR_SETUP` | 3 | `LR_SETUP\|base=1/1000\|min=1/10000\|warmup=20,total=220,t=120` | lr_schedule_generator.py |
| `LR_VALUE` | 1 | `LR_VALUE\|11/20000` | lr_schedule_generator.py |
| `LS_LINE` | 2 | `LS_LINE\|a = 8, b = 2\|ŷ = 8 + 2x` | least_squares_generator.py |
| `LS_SETUP` | 2 | `LS_SETUP\|points [(-3, 4), (-1, 4), (1, 8), (3, 16)]\|model y = a + bx` | least_squares_generator.py |
| `LUHN_DIGIT` | 3 | `LUHN_DIGIT\|digit 3\|keep\|3 -> 3` | modular_arithmetic_generator.py |
| `LU_ENTRY` | 3 | `LU_ENTRY\|u11\|a11 = 4\|4` | lu_decomposition_generator.py |
| `LU_RESULT` | 2 | `LU_RESULT\|L\|[[1, 0, 0], [-4, 1, 0], [3, 3, 1]]` | lu_decomposition_generator.py |
| `LU_SETUP` | 2 | `LU_SETUP\|A = [[4, 0, -2], [-16, -1, 3], [12, -3, -20]]\|unit lower L` | lu_decomposition_generator.py |
| `LZ77_EMIT` | 1 | `LZ77_EMIT\|(0,0,d)` | lz_compression_generator.py |
| `LZ77_EXPAND` | 4 | `LZ77_EXPAND\|(0,0,d)\|no copy\|then add d\|out = d` | lz_compression_generator.py |
| `LZ77_MATCH` | 4 | `LZ77_MATCH\|pos 0\|literal\|offset 0, len 0\|next d` | lz_compression_generator.py |
| `LZ77_SEARCH` | 3 | `LZ77_SEARCH\|pos 1\|start 0\|len 1` | lz_compression_generator.py |
| `LZ78_APPEND` | 2 | `LZ78_APPEND\|empty + t\|out = t` | lz_compression_generator.py |
| `LZ78_DICT` | 2 | `LZ78_DICT\|0\|empty` | lz_compression_generator.py |
| `LZ78_EMIT` | 1 | `LZ78_EMIT\|(0,f)` | lz_compression_generator.py |
| `LZ78_LOOKUP` | 2 | `LZ78_LOOKUP\|index 0\|phrase empty` | lz_compression_generator.py |
| `LZ78_MATCH` | 4 | `LZ78_MATCH\|pos 0\|phrase empty\|index 0\|next f` | lz_compression_generator.py |
| `LZ_SETUP` | 2 | `LZ_SETUP\|LZ78 decode\|(0,t), (0,g), (1,g), (1,t), (0,e), (3,t), (2,$)` | lz_compression_generator.py |
| `M` | 3 | `M\|6\|99\|594` | ac_circuit_generator.py, activation_generator.py, adam_step_generator.py, angle_defect_generator.py, angle_measure_generator.py, annuity_generator.py, arc_length_generator.py, arc_sector_generator.py, arithmetic_coding_generator.py, arithmetic_sequence_generator.py, attention_generator.py, backprop_generator.py, bec_channel_generator.py, binomial_probability_generator.py, bisection_generator.py, black_scholes_generator.py, blackbody_generator.py, bond_pricing_generator.py, calorimetry_generator.py, casimir_force_generator.py, casimir_generator.py, cayley_table_generator.py, chain_rule_generator.py, channel_capacity_generator.py, christoffel_generator.py, circle_angle_generator.py, classifier_metrics_generator.py, collision_generator.py, commutator_generator.py, complex_locus_generator.py, complex_log_generator.py, composite_arithmetic_generator.py, confidence_interval_generator.py, conic_standard_form_generator.py, continued_fraction_generator.py, continuous_distribution_generator.py, contour_integral_generator.py, convolution_generator.py, coset_generator.py, counterexample_search_generator.py, counting_classics_generator.py, cramers_rule_generator.py, cross_section_generator.py, crt_generator.py, curve_analysis_generator.py, cyclic_group_generator.py, de_moivre_generator.py, decimal_div_generator.py, definite_integral_generator.py, density_matrix_generator.py, derangement_generator.py, derivative_limit_def_generator.py, derivative_power_rule_generator.py, derivative_transcendental_generator.py, determinant_generator.py, dimensional_analysis_generator.py, doppler_generator.py, dot_product_generator.py, einstein_summation_generator.py, electrostatics_generator.py, elliptic_curve_finite_field_generator.py, embedding_similarity_generator.py, energy_conservation_generator.py, entropy_change_generator.py, entropy_generator.py, entropy_rate_markov_generator.py, equilibrium_ice_generator.py, error_spotting_generator.py, euler_method_generator.py, evaluate_expression_generator.py, expected_value_generator.py, exponential_model_generator.py, extended_euclid_generator.py, factor_special_forms_generator.py, feature_map_generator.py, fermi_estimation_generator.py, fill_in_step_generator.py, finance_generator.py, finite_difference_generator.py, finite_field_generator.py, first_law_generator.py, five_number_summary_generator.py, fixed_point_generator.py, flops_memory_generator.py, four_vector_generator.py, fourier_series_generator.py, fractal_iteration_generator.py, fraction_op_generator.py, function_composition_generator.py, function_evaluation_generator.py, function_operations_generator.py, function_table_generator.py, fundamental_form_generator.py, game_theory_generator.py, gas_law_generator.py, gas_stoichiometry_generator.py, gauss_bonnet_generator.py, gauss_law_generator.py, gaussian_curvature_generator.py, generating_function_generator.py, geometric_distribution_generator.py, geometric_mean_generator.py, geometric_sequence_generator.py, geometry_area_perimeter_generator.py, gradient_descent_generator.py, gradient_step_generator.py, graph_counting_generator.py, graph_interpret_generator.py, grassmann_generator.py, great_circle_generator.py, hamiltonian_generator.py, hawking_generator.py, hermitian_check_generator.py, horner_evaluation_generator.py, huffman_coding_generator.py, hydrogen_atom_generator.py, hypercube_counting_generator.py, hypothesis_test_generator.py, index_gymnastics_generator.py, index_raising_generator.py, information_gain_generator.py, interference_generator.py, interpolation_generator.py, invariant_mass_generator.py, joint_distribution_generator.py, kernel_evaluation_generator.py, kernel_perceptron_generator.py, kernel_ridge_generator.py, kernel_validity_generator.py, kinematics_generator.py, kl_divergence_generator.py, ladder_operator_generator.py, lagrangian_generator.py, laplace_ivp_generator.py, laurent_series_generator.py, layer_norm_generator.py, lcm_generator.py, legendre_construction_generator.py, lhopital_generator.py, limit_evaluation_generator.py, linear_approx_generator.py, log_conversion_generator.py, log_diff_higher_order_generator.py, logistic_growth_generator.py, long_division_generator.py, lp_corner_generator.py, lr_schedule_generator.py, magnetism_generator.py, markov_chain_generator.py, matrix_calculus_generator.py, matrix_group_check_generator.py, matrix_inverse_generator.py, matrix_ops_generator.py, mean_value_theorem_generator.py, method_of_moments_generator.py, metric_arc_length_generator.py, mgf_generator.py, midpoint_generator.py, mixed_number_operation_generator.py, mobius_transform_generator.py, mod_exp_generator.py, modular_inverse_generator.py, multi_step_unit_conversion_generator.py, mutual_information_generator.py, naive_bayes_generator.py, named_distribution_generator.py, natural_units_generator.py, nets_surface_area_generator.py, newton_raphson_generator.py, newtons_laws_generator.py, npv_irr_generator.py, ode_system_generator.py, operation_properties_generator.py, optics_generator.py, optimization_generator.py, or_formula_generator.py, orbital_mechanics_generator.py, order_of_operations_generator.py, order_statistics_generator.py, param_count_generator.py, parametric_calculus_generator.py, particle_in_box_generator.py, partition_function_generator.py, pca_generator.py, percent_problem_generator.py, percent_word_problem_generator.py, perceptron_generator.py, permutation_combination_generator.py, physics_formula_generator.py, piecewise_evaluation_generator.py, planck_units_generator.py, polar_parametric_generator.py, polynomial_zeros_generator.py, portfolio_generator.py, positive_definite_generator.py, primality_test_generator.py, projectile_motion_generator.py, proportion_word_problem_generator.py, proportional_relationship_generator.py, quadratic_residue_generator.py, quantization_generator.py, quantum_formula_generator.py, quark_composition_generator.py, quaternion_generator.py, radical_multiply_generator.py, radical_rationalize_generator.py, rate_conversion_generator.py, ratio_table_generator.py, rational_equation_generator.py, rational_exponent_generator.py, recurrence_generator.py, recursive_explicit_generator.py, reed_solomon_generator.py, regression_generator.py, regular_polygon_area_generator.py, related_rates_generator.py, relativistic_energy_generator.py, remainder_factor_theorem_generator.py, riemann_sum_generator.py, riemann_tensor_generator.py, right_triangle_trig_generator.py, rotational_dynamics_generator.py, round_solids_generator.py, routh_hurwitz_generator.py, row_reduction_generator.py, rsa_generator.py, runge_kutta_generator.py, running_coupling_generator.py, rv_transform_generator.py, scaling_law_generator.py, schwarzschild_generator.py, second_order_ode_generator.py, segment_partition_generator.py, separable_pde_generator.py, series_solution_generator.py, set_builder_roster_generator.py, set_operations_generator.py, shm_generator.py, signal_arithmetic_generator.py, similar_triangles_generator.py, simplex_generator.py, solid_revolution_generator.py, solution_chem_generator.py, special_relativity_generator.py, special_right_triangle_generator.py, spherical_excess_generator.py, spherical_triangle_generator.py, standing_wave_generator.py, stars_and_bars_generator.py, statics_generator.py, stereographic_generator.py, stoichiometry_generator.py, svm_margin_generator.py, synthetic_division_generator.py, tangent_line_generator.py, taxicab_geometry_generator.py, taylor_series_generator.py, temperature_conversion_generator.py, tensor_product_generator.py, tip_bill_split_generator.py, totient_generator.py, transfer_function_generator.py, transformation_generator.py, transient_circuit_generator.py, transportation_generator.py, triangle_area_sas_generator.py, triangle_solve_generator.py, trig_identity_eval_generator.py, two_sample_test_generator.py, uncertainty_generator.py, undetermined_coeff_generator.py, unit_circle_generator.py, unit_conversion_generator.py, vector_ops_generator.py, volume_rect_prism_generator.py, von_neumann_entropy_generator.py, wavefunction_generator.py, young_tableaux_generator.py, z_score_generator.py, z_transform_generator.py |
| `MAG_FORMULA` | 1 | `MAG_FORMULA\|magnitude = √(x^2 + y^2)` | magnetism_generator.py, vector_ops_generator.py |
| `MAG_SETUP` | 3 | `MAG_SETUP\|loop_center\|I=43, R=19\|mu0=1` | magnetism_generator.py |
| `MARGIN` | 2 | `MARGIN\|2/norm(w)\|2/5` | svm_margin_generator.py |
| `MARGINAL` | 1 | `MARGINAL\|P(X=0)=p00+p01` | joint_distribution_generator.py, mutual_information_generator.py |
| `MARKOV_SETUP` | 2, 3 | `MARKOV_SETUP\|absorbing\|row0 to0=2/11, to1=4/11, toA=2/11, toB=3/11\|row1 to0=1/3, to1=1/3, toA=1/6, toB=1/6` | entropy_rate_markov_generator.py, markov_chain_generator.py |
| `MASTER_CASE` | 2 | `MASTER_CASE\|case 2\|Θ(n^6 log n)` | master_theorem_generator.py |
| `MATMUL_FLOPS` | 2 | `MATMUL_FLOPS\|XW1\|33554432` | flops_memory_generator.py |
| `MATRIX_ADD` | 2 | `MATRIX_ADD\|P0+P1\|[[1,0],[0,1]]` | bch_generator.py, casimir_generator.py, projector_generator.py |
| `MATRIX_ENTRY` | 1 | `MATRIX_ENTRY\|P2_01=P00*P01 + P01*P11` | markov_chain_generator.py |
| `MATRIX_ENTRY_SUM` | 3 | `MATRIX_ENTRY_SUM\|(4,1)\|0 + 0\|0` | gamma_matrix_generator.py |
| `MATRIX_EXP` | 3 | `MATRIX_EXP\|e^A\|I + A\|[[1, 3, 0], [0, 1, 0], [0, 0, 1]]` | bch_generator.py |
| `MATRIX_GROUP_SETUP` | 2 | `MATRIX_GROUP_SETUP\|GL2Z\|M=[[-5,4],[-6,5]]` | matrix_group_check_generator.py |
| `MATRIX_MULT` | 2, 3 | `MATRIX_MULT\|row1 dot col1\|1853560809/4293525625*1853560809/4293525625+2126645988/4293525625*2126645988/4293525625\|1853560809/4293525625` | projector_generator.py |
| `MATRIX_POWER` | 2 | `MATRIX_POWER\|K^2\|[[-1, 0, 0], [0, -1, 0], [0, 0, 0]]` | lie_exponential_generator.py |
| `MATRIX_PRODUCT` | 2 | `MATRIX_PRODUCT\|AB\|[[-105i/4, 0], [0, 105i/4]]` | bch_generator.py, casimir_generator.py, gamma_matrix_generator.py, pauli_algebra_generator.py, structure_constant_generator.py |
| `MATRIX_ROW` | 2 | `MATRIX_ROW\|row 1\|0, 0, 0` | graph_counting_generator.py |
| `MATRIX_SCALE` | 2 | `MATRIX_SCALE\|1/2 ladder sum\|[[361/121, 0, 0], [0, 722/121, 0], [0, 0, 361/121]]` | bch_generator.py, casimir_generator.py |
| `MATRIX_SETUP` | 2 | `MATRIX_SETUP\|hermitian\|A=[[17,2],[2,17]]` | hermitian_check_generator.py |
| `MATRIX_SUB` | 2 | `MATRIX_SUB\|AB - BA\|[[0, 0, 0], [0, 0, 0], [0, 3, 0]]` | bch_generator.py |
| `MATRIX_SUM` | 1 | `MATRIX_SUM\|B=A+A^T` | matrix_calculus_generator.py |
| `MATRIX_VALUE` | 2 | `MATRIX_VALUE\|A\|[[0, 7/2], [7/2, 0]]` | pauli_algebra_generator.py, structure_constant_generator.py |
| `MAT_ENTRY` | 2, 3 | `MAT_ENTRY\|(1,1)\|20` | lie_exponential_generator.py, matrix_calculus_generator.py, matrix_ops_generator.py |
| `MAT_SETUP` | 2 | `MAT_SETUP\|A = [[4, 1], [5, -2]], v = [[5], [0]]\|Av` | determinant_generator.py, diagonalization_generator.py, eigenvalue_generator.py, matrix_exponential_generator.py, matrix_inverse_generator.py, matrix_ops_generator.py, row_reduction_generator.py, subspace_basis_generator.py, svd_generator.py |
| `MAX` | 2, 3 | `MAX\|15, 9\|15` | dp_table_generator.py, matrix_norm_generator.py, taxicab_geometry_generator.py |
| `MAXTERM` | 2 | `MAXTERM\|0110\|V OR NOT W OR NOT X OR Y` | boolean_algebra_generator.py |
| `MC_SETUP` | 3 | `MC_SETUP\|expression=a^T x\|a=(2,6)\|x=(-1,4)` | matrix_calculus_generator.py |
| `MEAN` | 1 | `MEAN\|-4` | layer_norm_generator.py |
| `MEAN_DIV` | 3 | `MEAN_DIV\|63\|9\|7` | composite_arithmetic_generator.py, five_number_summary_generator.py, regression_generator.py, simple_stats_generator.py, standard_deviation_generator.py |
| `MEASURE_BASIS` | 3 | `MEASURE_BASIS\|z\|ket+z=ket0\|ket-z=ket1` | spin_half_generator.py |
| `MEASURE_FAVORABLE` | 2 | `MEASURE_FAVORABLE\|sector angle\|90` | geometric_probability_generator.py |
| `MEASURE_PROB` | 3 | `MEASURE_PROB\|computational basis\|P(0)=1/2\|P(1)=1/2` | quantum_gate_generator.py |
| `MEASURE_TOTAL` | 2 | `MEASURE_TOTAL\|full circle angle\|360` | geometric_probability_generator.py |
| `MEDIAN_PAIR` | 2 | `MEDIAN_PAIR\|7\|8` | five_number_summary_generator.py, simple_stats_generator.py |
| `MEDIAN_PICK` | 1, 2 | `MEDIAN_PICK\|9` | five_number_summary_generator.py, simple_stats_generator.py |
| `MEMORY_SETUP` | 3 | `MEMORY_SETUP\|kv_cache\|L=16,h=8,d_k=64\|seq=1024,precision_bytes=1` | flops_memory_generator.py |
| `MEMORY_UNIT` | 2 | `MEMORY_UNIT\|MiB\|16` | flops_memory_generator.py |
| `MERGE_BEGIN` | 3 | `MERGE_BEGIN\|merge 1\|lo=0,mid=1,hi=2\|left 48; right 3` | algorithm_trace_generator.py |
| `MERGE_COMPARE` | 3 | `MERGE_COMPARE\|48\|3\|take right` | algorithm_trace_generator.py |
| `MERGE_DONE` | 3 | `MERGE_DONE\|merge 1\|range 0-1\|array 3, 48, 40, 30, 4` | algorithm_trace_generator.py |
| `MERGE_TAKE` | 2 | `MERGE_TAKE\|3\|merged 3` | algorithm_trace_generator.py |
| `METRIC` | 2 | `METRIC\|taxicab\|d = abs(x2 - x1) + abs(y2 - y1)` | taxicab_geometry_generator.py |
| `METRICS_SETUP` | 1 | `METRICS_SETUP\|TP=18, FP=13, FN=9, TN=29` | classifier_metrics_generator.py |
| `METRIC_ARC_SETUP` | 3 | `METRIC_ARC_SETUP\|polar metric\|ds^2=dr^2+r^2 dtheta^2\|theta=45 deg, r:25->43` | metric_arc_length_generator.py |
| `METRIC_FORMULA` | 1 | `METRIC_FORMULA\|precision=TP/(TP+FP)` | classifier_metrics_generator.py |
| `METRIC_RESTRICT` | 2 | `METRIC_RESTRICT\|dtheta=0\|ds^2=dr^2` | metric_arc_length_generator.py |
| `MGF_SETUP` | 3 | `MGF_SETUP\|P(X=0)=16/45\|P(X=1)=16/45\|P(X=2)=13/45` | mgf_generator.py |
| `MGF_TERM` | 3 | `MGF_TERM\|x=0\|p0*e^(0t)\|16/45` | mgf_generator.py |
| `MIDDLE_EVAL` | 3 | `MIDDLE_EVAL\|phi=0..pi\|int sin(phi) dphi = 2\|2` | triple_integral_generator.py |
| `MIDLINE` | 1 | `MIDLINE\|y = -3` | sinusoid_features_generator.py |
| `MIDPOINT` | 2 | `MIDPOINT\|iter 1\|2` | algorithm_trace_generator.py |
| `MID_FORMULA` | 1 | `MID_FORMULA\|M = ((x1 + x2)/2, (y1 + y2)/2)` | circle_equation_generator.py, midpoint_generator.py |
| `MIN` | 2 | `MIN\|16,64\|16` | matrix_norm_generator.py |
| `MIN3` | 4 | `MIN3\|3\|1\|2\|1` | dp_table_generator.py |
| `MINKOWSKI_FORMULA` | 1 | `MINKOWSKI_FORMULA\|s2=ct^2-x^2` | minkowski_interval_generator.py |
| `MINKOWSKI_SETUP` | 3 | `MINKOWSKI_SETUP\|interval_classification\|ct=11\|x=-20` | minkowski_interval_generator.py |
| `MINTERM` | 2 | `MINTERM\|000\|NOT Q AND NOT R AND NOT S` | boolean_algebra_generator.py |
| `MIN_INITIAL` | 3 | `MIN_INITIAL\|nonaccept A, C\|accept B, D\|{A,C}, {B,D}` | dfa_minimization_generator.py |
| `MIN_REFINE` | 2 | `MIN_REFINE\|round 1\|{A,C}, {B,D}` | dfa_minimization_generator.py |
| `MIN_SIGNATURE` | 3 | `MIN_SIGNATURE\|round 1\|A\|0->B0,1->B1` | dfa_minimization_generator.py |
| `MIN_STABLE` | 1 | `MIN_STABLE\|{A,C}, {B,D}` | dfa_minimization_generator.py |
| `MIN_TRANSITION` | 3 | `MIN_TRANSITION\|{A,C}\|0\|{A,C}` | dfa_minimization_generator.py |
| `MIX_FORMULA` | 2 | `MIX_FORMULA\|q=(d-b)/(a-b-c+d)\|p=(d-c)/(a-b-c+d)` | game_theory_generator.py |
| `MIX_IMPROPER` | 2 | `MIX_IMPROPER\|2 2/7\|16/7` | composite_arithmetic_generator.py, mixed_number_operation_generator.py, order_of_operations_generator.py |
| `MI_FORMULA` | 1 | `MI_FORMULA\|I=H(X)+H(Y)-H(X,Y)` | mutual_information_generator.py |
| `MI_SETUP` | 2 | `MI_SETUP\|rows=[[0,1/2];[1/2,0]]\|task=I(X;Y)` | mutual_information_generator.py |
| `MLE_SETUP` | 2, 3 | `MLE_SETUP\|exponential\|parameter=lambda\|data=[4,3,8,6,2,10,12,10,7]` | mle_generator.py |
| `MOBIUS_SETUP` | 2 | `MOBIUS_SETUP\|T(z)=(3z - 3)/(-4z + 1)\|z0=-1` | mobius_transform_generator.py |
| `MODE` | 2 | `MODE\|2\|10, 13` | frequency_table_generator.py, simple_stats_generator.py |
| `MODEL` | 1 | `MODEL\|A = P(1 - r)^t` | exponential_model_generator.py |
| `MODEL_APPLY` | 1 | `MODEL_APPLY\|A = 36500 · (1 - 0.35)^2` | exponential_model_generator.py |
| `MODEL_OUTPUT` | 1 | `MODEL_OUTPUT\|2` | activation_generator.py |
| `MODEXP_MULTIPLY` | 2 | `MODEXP_MULTIPLY\|bit 1=1\|49` | mod_exp_generator.py, quadratic_residue_generator.py |
| `MODEXP_SETUP` | 3 | `MODEXP_SETUP\|base 49\|exponent 42\|modulus 79` | mod_exp_generator.py |
| `MODEXP_SQUARE` | 2 | `MODEXP_SQUARE\|bit 1=1\|1` | mod_exp_generator.py, quadratic_residue_generator.py |
| `MODEXP_STATE` | 2 | `MODEXP_STATE\|after bit 1\|49` | mod_exp_generator.py, quadratic_residue_generator.py |
| `MODE_COUNT` | 2 | `MODE_COUNT\|1\|1` | simple_stats_generator.py |
| `MOD_INVERSE` | 2 | `MOD_INVERSE\|8 mod 5\|2` | crt_generator.py, ecdsa_generator.py, elliptic_curve_finite_field_generator.py, modular_inverse_generator.py, rsa_generator.py |
| `MOD_NORMALIZE` | 3 | `MOD_NORMALIZE\|2\|mod 5\|2` | modular_inverse_generator.py, rsa_generator.py |
| `MOD_POWER` | 3 | `MOD_POWER\|11^14\|mod 31\|14` | diffie_hellman_generator.py, pollard_factorization_generator.py, primality_test_generator.py, rsa_generator.py, tonelli_shanks_generator.py, totient_generator.py |
| `MOD_REDUCE` | 3 | `MOD_REDUCE\|314\|mod 11\|6` | calendar_arithmetic_generator.py, cayley_table_generator.py, coset_generator.py, crt_generator.py, cyclic_group_generator.py, de_moivre_generator.py, elliptic_curve_finite_field_generator.py, finite_field_generator.py, jacobi_symbol_generator.py, lie_exponential_generator.py, mod_exp_generator.py, modular_arithmetic_generator.py, modular_inverse_generator.py, primality_test_generator.py, quadratic_residue_generator.py, reed_solomon_generator.py, rsa_generator.py, totient_generator.py |
| `MOD_SETUP` | 2, 3, 4 | `MOD_SETUP\|ISBN-10 modulus 11\|prefix 935892730` | modular_arithmetic_generator.py, modular_inverse_generator.py |
| `MOD_SOLVE` | 2 | `MOD_SOLVE\|d ≡ -6 mod 11\|5` | modular_arithmetic_generator.py |
| `MOD_TERM` | 2 | `MOD_TERM\|10 * 9\|90` | modular_arithmetic_generator.py |
| `MOE_FORMULA` | 1 | `MOE_FORMULA\|E = z*·σ/√n` | confidence_interval_generator.py |
| `MOLAR_MASS` | 2 | `MOLAR_MASS\|CaCO3\|100 g/mol` | gas_stoichiometry_generator.py, stoichiometry_generator.py |
| `MOLAR_VOLUME` | 2 | `MOLAR_VOLUME\|1 mol gas\|24 L` | stoichiometry_generator.py |
| `MOMENT` | 2 | `MOMENT\|m1\|3/10` | adam_step_generator.py |
| `MOMENTUM` | 1 | `MOMENTUM\|p1=m1*u1` | collision_generator.py |
| `MOMENT_X` | 3 | `MOMENT_X\|M_x = 1/2 int y^2 dx\|3^2*12^5/10\|1119744/5` | centroid_generator.py |
| `MOMENT_Y` | 3 | `MOMENT_Y\|M_y = int x*y dx\|3*12^4/4\|15552` | centroid_generator.py |
| `MOM_EQUATION` | 2 | `MOM_EQUATION\|E[X]=lambda\|xbar=lambda` | method_of_moments_generator.py |
| `MOM_SETUP` | 3 | `MOM_SETUP\|poisson\|parameter=lambda\|data=[6,2,4,1,1,5,9,3,6,3]` | method_of_moments_generator.py |
| `MONO_ADD_EXP` | 2 | `MONO_ADD_EXP\|x^6 * x^3 = x^(6+3)\|x^9` | monomial_mult_div_generator.py |
| `MONO_DIV_COEFF` | 2 | `MONO_DIV_COEFF\|-35 / -5\|7` | monomial_mult_div_generator.py |
| `MONO_MULT_COEFF` | 2 | `MONO_MULT_COEFF\|-5 * -3\|15` | monomial_mult_div_generator.py |
| `MONO_SETUP` | 1 | `MONO_SETUP\|(-5x^6)(-3x^3)` | monomial_mult_div_generator.py |
| `MONO_SUB_EXP` | 2 | `MONO_SUB_EXP\|x^6 / x^4 = x^(6-4)\|x^2` | monomial_mult_div_generator.py |
| `MOVE_TERM` | 2, 3 | `MOVE_TERM\|+3x\|left\|-5x-9-3x = +7` | area_between_curves_generator.py, completing_square_generator.py, conic_standard_form_generator.py, linear_complex_generator.py, polar_parametric_generator.py, quadratic_factoring_generator.py, quadratic_square_root_generator.py, radical_equation_generator.py, special_solution_equation_generator.py, standard_form_conversion_generator.py |
| `MR_DECOMPOSE` | 2 | `MR_DECOMPOSE\|84\|2^2 * 21` | primality_test_generator.py |
| `MR_SETUP` | 2 | `MR_SETUP\|n=85\|witnesses 11, 18` | primality_test_generator.py |
| `MR_SQUARE` | 2 | `MR_SQUARE\|r=1\|66` | primality_test_generator.py |
| `MR_WITNESS` | 1 | `MR_WITNESS\|11` | primality_test_generator.py |
| `MR_WITNESS_RESULT` | 2 | `MR_WITNESS_RESULT\|11\|composite` | primality_test_generator.py |
| `MSE_FORMULA` | 2 | `MSE_FORMULA\|L=(1/n) sum r_i^2\|grad=(2/n) sum r_i*[1,x_i]` | gradient_step_generator.py |
| `MSE_GRADIENT` | 2 | `MSE_GRADIENT\|g0=-2\|g1=2` | gradient_step_generator.py |
| `MSE_SAMPLE` | 3 | `MSE_SAMPLE\|i=1\|pred=-4\|r=-2` | gradient_step_generator.py |
| `MSE_SETUP` | 3 | `MSE_SETUP\|model y_hat=w0+w1*x\|samples=[(-1,-2), (0,-2)]\|w=(-2,2), eta=1/8` | gradient_step_generator.py |
| `MST_ADD` | 2 | `MST_ADD\|AB\|total 2` | mst_generator.py |
| `MST_SET` | 1 | `MST_SET\|AB` | mst_generator.py |
| `MST_SETUP` | 2 | `MST_SETUP\|weighted undirected graph\|vertices A, B, C, D, E, F` | mst_generator.py |
| `MU` | 2 | `MU\|-17/25\|round=-1` | lll_reduction_generator.py |
| `MULTIPLY_IF` | 2 | `MULTIPLY_IF\|e^(5x)y' + 5e^(5x)y\|20e^(5x)` | integrating_factor_generator.py, ode_substitution_generator.py |
| `MULTIVALUED_LOG` | 2 | `MULTIVALUED_LOG\|ln(7/2) + i*(29pi/90 + 2pi*k)\|k in Z` | complex_log_generator.py |
| `MULTI_FORMULA` | 2 | `MULTI_FORMULA\|n!/(a!b!c!...)\|11! / repeats` | stars_and_bars_generator.py |
| `MULTI_SETUP` | 2 | `MULTI_SETUP\|5 H's, 1 R, 5 M's\|total 11` | stars_and_bars_generator.py |
| `MUL_PARTIAL` | 3 | `MUL_PARTIAL\|6\|68395\|410370` | decimal_mult_generator.py, multi_digit_multiplication_generator.py |
| `MUL_SETUP` | 2 | `MUL_SETUP\|68395\|1956` | decimal_mult_generator.py, multi_digit_multiplication_generator.py |
| `MUL_TERM` | 3 | `MUL_TERM\|12\|(2/3)x\|8x` | linear_fractional_generator.py, polynomial_long_division_generator.py, rational_equation_generator.py |
| `MVT_SETUP` | 2 | `MVT_SETUP\|f(x) = x^2 - 5x - 7 on [-1, 1]\|find the c guaranteed by the MVT` | mean_value_theorem_generator.py |
| `MV_CHAIN_SETUP` | 3 | `MV_CHAIN_SETUP\|z = f(x,y) = x^2 + 4*y^2 - 3*x*y + 6*x\|x = 4*t - 5, y = -2*t - 6\|t = -1` | multivar_chain_rule_generator.py |
| `NATURAL_SETUP` | 3 | `NATURAL_SETUP\|time\|hbar=1,c=1\|t=21/10 eV^-1` | natural_units_generator.py |
| `NB_FEATURE_COUNT` | 3 | `NB_FEATURE_COUNT\|Spam\|long=0\|count=7` | naive_bayes_generator.py |
| `NB_LIKELIHOOD` | 3 | `NB_LIKELIHOOD\|Spam\|long=0\|4/7` | naive_bayes_generator.py |
| `NB_PRIOR` | 2 | `NB_PRIOR\|Spam\|4/9` | naive_bayes_generator.py |
| `NB_SCORE` | 2 | `NB_SCORE\|Spam\|start=4/9` | naive_bayes_generator.py |
| `NB_SETUP` | 3 | `NB_SETUP\|query=long=0, money=0, known=1\|alpha=1\|classes=Spam,Ham` | naive_bayes_generator.py |
| `NCR` | 2 | `NCR\|C(4,3)\|4` | binomial_probability_generator.py, derangement_generator.py, generating_function_generator.py, hypercube_counting_generator.py |
| `NEAREST` | 2 | `NEAREST\|queen\|(2,1)` | embedding_similarity_generator.py |
| `NEED` | 2 | `NEED\|line 2 adds 3, giving -16\|line 4 divides by 8` | fill_in_step_generator.py |
| `NEG_LOG` | 2 | `NEG_LOG\|p=1/32\|ln(32)` | perplexity_generator.py |
| `NET_SETUP` | 2 | `NET_SETUP\|2 rectangles 3 by 9; 2 rectangles 3 by 11; 2 rectangles 9 by 11\|total surface area` | nets_surface_area_generator.py |
| `NEWTON_DD` | 2 | `NEWTON_DD\|f[x0,x1]\|-8` | interpolation_generator.py |
| `NEWTON_SETUP` | 2, 3 | `NEWTON_SETUP\|f(x)=x^2-60\|f'(x)=2x\|x0=7,iterations=3` | newton_raphson_generator.py, newtons_laws_generator.py |
| `NEWTON_STEP` | 2 | `NEWTON_STEP\|1\|1/2` | npv_irr_generator.py |
| `NEWTON_UPDATE` | 3 | `NEWTON_UPDATE\|1\|x_0=7\|x_1=109/14` | newton_raphson_generator.py |
| `NEW_SLOPE` | 2 | `NEW_SLOPE\|New slope (m2) = 2\|Parallel lines have the same slope` | parallel_perpendicular_line_generator.py |
| `NFA_ACCEPT` | 1 | `NFA_ACCEPT\|u5` | nfa_simulation_generator.py |
| `NFA_ACTIVE` | 2 | `NFA_ACTIVE\|start\|{u0,u3}` | nfa_simulation_generator.py |
| `NFA_EPSILON` | 2 | `NFA_EPSILON\|u0\|{u3}` | nfa_simulation_generator.py |
| `NFA_INPUT` | 1 | `NFA_INPUT\|ba` | nfa_simulation_generator.py |
| `NFA_MOVE` | 4 | `NFA_MOVE\|{u0,u3}\|b\|u0->{}; u3->{u5}\|{u5}` | nfa_simulation_generator.py |
| `NFA_READ` | 2 | `NFA_READ\|pos 1\|b` | nfa_simulation_generator.py |
| `NFA_SETUP` | 3 | `NFA_SETUP\|states u0, u3, u5\|alphabet a, b, c\|start u0` | nfa_simulation_generator.py |
| `NFA_TRANSITION` | 3 | `NFA_TRANSITION\|u0\|a\|{u3}` | nfa_simulation_generator.py |
| `NILPOTENT` | 3 | `NILPOTENT\|theta^2=0\|-2theta^2\|0` | grassmann_generator.py |
| `NLL` | 2 | `NLL\|132 tokens\|132*ln(32)` | perplexity_generator.py |
| `NORM2` | 2 | `NORM2\|b1\|125` | lll_reduction_generator.py |
| `NORMALIZE` | 2 | `NORMALIZE\|1/2 + 1/2\|1` | clebsch_gordan_generator.py, layer_norm_generator.py |
| `NORMALIZE_SIGN` | 2 | `NORMALIZE_SIGN\|(-1,6)\|(1,-6)` | lll_reduction_generator.py |
| `NORMAL_EQ` | 2 | `NORMAL_EQ\|X^T X\|[[4, 0], [0, 20]]` | least_squares_generator.py |
| `NORMAL_SLOPE` | 2 | `NORMAL_SLOPE\|-1/(6)\|-1/6` | tangent_line_generator.py |
| `NORMAL_SYMMETRY` | 2 | `NORMAL_SYMMETRY\|N_neg_d1=0.1\|N_neg_d2=0.15` | black_scholes_generator.py |
| `NORM_CHECK` | 2 | `NORM_CHECK\|P(+z)+P(-z)\|1` | spin_half_generator.py |
| `NORM_SETUP` | 2 | `NORM_SETUP\|A: 98 in N(47, 20)\|compare relative standing` | matrix_norm_generator.py, normal_table_generator.py, z_score_generator.py |
| `NORM_SQUARED` | 2 | `NORM_SQUARED\|p\|13` | quaternion_generator.py |
| `NO_REDEX` | 2 | `NO_REDEX\|d\|no beta redex remains` | lambda_reduction_generator.py |
| `NPV_SETUP` | 2 | `NPV_SETUP\|c0=-1000,c1=1450,c2=700,c3=850\|rate=20%` | npv_irr_generator.py |
| `NPV_TERM` | 2 | `NPV_TERM\|t=0\|-1000` | npv_irr_generator.py |
| `NULL_REL` | 2 | `NULL_REL\|x1 - 2*x4 = 0\|x1 = 2*x4` | subspace_basis_generator.py |
| `NULL_VECTOR` | 2 | `NULL_VECTOR\|x4=1\|[2, 1, -3, 1]` | subspace_basis_generator.py |
| `NUMBER_OPERATOR` | 2 | `NUMBER_OPERATOR\|N ket26\|26 ket26` | ladder_operator_generator.py |
| `NW_ALLOC` | 1, 3 | `NW_ALLOC\|cell x11\|min(31,16)\|16` | transportation_generator.py |
| `NYQUIST` | 1 | `NYQUIST\|required rate = 2*f_max` | signal_arithmetic_generator.py |
| `OBJECTIVE` | 1 | `OBJECTIVE\|at (0,0)` | lp_corner_generator.py |
| `OCCURS_CHECK` | 3 | `OCCURS_CHECK\|X\|f(X)\|fail` | unification_generator.py |
| `ODD_VERTICES` | 2 | `ODD_VERTICES\|none\|0` | euler_circuit_generator.py |
| `ODE_SETUP` | 2, 3 | `ODE_SETUP\|dy/dx = y^2, y(0) = 47\|solve` | euler_method_generator.py, exact_ode_generator.py, integrating_factor_generator.py, laplace_ivp_generator.py, logistic_growth_generator.py, ode_substitution_generator.py, ode_system_generator.py, runge_kutta_generator.py, second_order_ode_generator.py, separable_ode_generator.py, series_solution_generator.py, stability_generator.py, undetermined_coeff_generator.py, variation_parameters_generator.py |
| `OPTICS_FORMULA` | 1 | `OPTICS_FORMULA\|1/f=1/d_o+1/d_i` | optics_generator.py |
| `OPTICS_SETUP` | 3 | `OPTICS_SETUP\|mirror_magnification\|f=13, d_o=27\|h_o=18` | optics_generator.py |
| `OPT_SETUP` | 2 | `OPT_SETUP\|square sheet 3816 by 3816; cut corners x and fold\|maximize volume` | optimization_generator.py |
| `ORBIT_FORMULA` | 1 | `ORBIT_FORMULA\|(T2/T1)^2=(a2/a1)^3` | orbital_mechanics_generator.py |
| `ORBIT_SETUP` | 3 | `ORBIT_SETUP\|kepler_third\|T1=48, a1=8\|a2=200` | orbital_mechanics_generator.py |
| `ORDER_PDF` | 1 | `ORDER_PDF\|f_{6:8}(x)=168*x^5*(1-x)^2` | order_statistics_generator.py |
| `ORDER_SETUP` | 3 | `ORDER_SETUP\|n=8\|k=6\|q=1/2` | order_statistics_generator.py |
| `ORDER_START` | 2 | `ORDER_START\|15\|identity 1` | cayley_table_generator.py |
| `ORDER_STEP` | 2 | `ORDER_STEP\|k=1\|15` | cayley_table_generator.py |
| `ORTHOGONALITY` | 2 | `ORTHOGONALITY\|lower multiplet\|orthogonal to higher J` | clebsch_gordan_generator.py |
| `OR_SETUP` | 3 | `OR_SETUP\|EOQ\|D=224\|S=14, H=8` | or_formula_generator.py |
| `OUTER_ANTIDERIV` | 2 | `OUTER_ANTIDERIV\|dx\|8*x^2 + 16*x` | double_integral_generator.py |
| `OUTER_EVAL` | 3 | `OUTER_EVAL\|y=0..14\|10*2*7^2/2\|490` | double_integral_generator.py |
| `OUTER_PRODUCT` | 1 | `OUTER_PRODUCT\|rho=219/224ket00bra00 - sqrt(1095)/224(ket00bra11+ket11bra00) + 5/224ket11bra11` | partial_trace_generator.py |
| `OUTPUT` | 1 | `OUTPUT\|y_hat=-2` | backprop_generator.py |
| `PAIR` | 2 | `PAIR\|apricot\|badger` | one_to_one_correspondence_generator.py |
| `PARALLEL_RELATION` | 1 | `PARALLEL_RELATION\|2x + 8 = 6x - 44` | angle_relationships_generator.py |
| `PARALLEL_SETUP` | 2 | `PARALLEL_SETUP\|alternate_interior\|Alternate interior angles are equal` | angle_relationships_generator.py |
| `PARALLEL_SOLVE` | 2 | `PARALLEL_SOLVE\|-4x = -52\|x = 13` | angle_relationships_generator.py |
| `PARAMS` | 3 | `PARAMS\|W1=[[2,-1], [0,-1]]\|b1=(0,-1)\|v=(-1,1), c=0` | backprop_generator.py |
| `PARAM_PART` | 2 | `PARAM_PART\|attention_per_layer\|16777216` | param_count_generator.py |
| `PARAM_PATH` | 3 | `PARAM_PATH\|r(t)\|(-t + 3, t)\|0 <= t <= 1` | line_integral_generator.py |
| `PARAM_SETUP` | 2, 3 | `PARAM_SETUP\|x = 10t + 2, y = 8t + 14\|eliminate t` | param_count_generator.py, parametric_calculus_generator.py, polar_parametric_generator.py |
| `PARITY` | 1, 2 | `PARITY\|transpositions 5\|odd` | fourier_series_generator.py, permutation_group_generator.py |
| `PARITY_CALC` | 2 | `PARITY_CALC\|p1=d1 xor d2 xor d4\|0 xor 1 xor 1=0` | hamming_code_generator.py |
| `PARTFRAC_SETUP` | 1 | `PARTFRAC_SETUP\|(-2x + 12)/((x - 2)(x - 4)) = A/(x - 2) + B/(x - 4)` | partial_fractions_generator.py, telescoping_generator.py |
| `PARTIAL` | 2 | `PARTIAL\|u_x\|8x - 3` | cauchy_riemann_generator.py, fundamental_form_generator.py, hamiltonian_generator.py, lagrangian_generator.py |
| `PARTIAL_FRAC` | 2 | `PARTIAL_FRAC\|Y(s)\|-4/(s + 5) + 1/(s - 2)` | laplace_ivp_generator.py |
| `PARTIAL_RESULT` | 2 | `PARTIAL_RESULT\|f_x\|6*y^2` | div_curl_generator.py, exact_ode_generator.py, gradient_generator.py, hessian_classify_generator.py, jacobian_generator.py, lagrange_multiplier_generator.py, line_integral_generator.py, multivar_chain_rule_generator.py, partial_derivative_generator.py, vector_theorem_generator.py |
| `PARTIAL_RULE` | 3 | `PARTIAL_RULE\|6*x*y^2\|d/dx\|6*y^2` | partial_derivative_generator.py |
| `PARTIAL_SETUP` | 2 | `PARTIAL_SETUP\|f(x,y) = 6*x*y^2\|f_xy` | partial_derivative_generator.py |
| `PARTIAL_TRACE` | 2 | `PARTIAL_TRACE\|ket00bra00\|ket0bra0` | partial_trace_generator.py |
| `PARTICLE_TABLE` | 1 | `PARTICLE_TABLE\|mu-(Q=-1,B=0,Le=0,Lmu=1); pi0(Q=0,B=0,Le=0,Lmu=0); nu_e(Q=0,B=0,Le=1,Lmu=0); e-(Q=-1,B=0,Le=1,Lmu=0); anti_nu_mu(Q=0,B=0,Le=0,Lmu=-1)` | conservation_law_generator.py |
| `PARTICULAR` | 2 | `PARTICULAR\|y_p\|-2e^x` | undetermined_coeff_generator.py, variation_parameters_generator.py |
| `PARTICULAR_CHECK` | 2 | `PARTICULAR_CHECK\|K = 5\|6K - 8K + 15 = K` | recurrence_generator.py |
| `PARTICULAR_TRY` | 2 | `PARTICULAR_TRY\|a_n = K\|constant forcing` | recurrence_generator.py |
| `PARTITION_FORMULA` | 1 | `PARTITION_FORMULA\|Z=g0+g1*b` | partition_function_generator.py |
| `PARTITION_SETUP` | 3 | `PARTITION_SETUP\|two_level\|g0=1, g1=1\|epsilon=11, b=1/6` | partition_function_generator.py |
| `PARTS_CHOOSE` | 2 | `PARTS_CHOOSE\|u = ln(x), dv = 180 dx\|du = dx/x, v = 180x` | integration_by_parts_generator.py |
| `PARTS_FORMULA` | 1 | `PARTS_FORMULA\|∫ u dv = uv - ∫ v du` | integration_by_parts_generator.py |
| `PASCAL_ROW` | 2 | `PASCAL_ROW\|0\|1` | pascal_triangle_generator.py |
| `PASCAL_SETUP` | 1 | `PASCAL_SETUP\|18C16` | pascal_triangle_generator.py |
| `PATH_DERIV` | 2 | `PATH_DERIV\|r'(t)\|(-1, 1)` | curve_geometry_generator.py, line_integral_generator.py |
| `PAULI_IDENTITY` | 3 | `PAULI_IDENTITY\|sigma_y sigma_x\|i epsilon_ijk sigma_k\|8isigma_z` | pauli_algebra_generator.py |
| `PAULI_MATRIX` | 2 | `PAULI_MATRIX\|sigma_y\|[[0,-i],[i,0]]` | spin_half_generator.py |
| `PAULI_SETUP` | 3 | `PAULI_SETUP\|product\|A=2sigma_y\|B=-4sigma_x` | pauli_algebra_generator.py |
| `PCA_SETUP` | 2 | `PCA_SETUP\|points=[(8,-2), (0,-2), (4,6), (4,-10)]\|population covariance` | pca_generator.py |
| `PC_VECTOR` | 2 | `PC_VECTOR\|e2\|(0,1)` | pca_generator.py |
| `PDA_POP` | 2 | `PDA_POP\|(\|stack=$(` | pda_simulation_generator.py |
| `PDA_PUSH` | 2 | `PDA_PUSH\|(\|stack=$(` | pda_simulation_generator.py |
| `PDA_READ` | 1 | `PDA_READ\|(` | pda_simulation_generator.py |
| `PDA_REJECT` | 1 | `PDA_REJECT\|pop from bottom` | pda_simulation_generator.py |
| `PDA_SETUP` | 2 | `PDA_SETUP\|balanced_parentheses\|stack=$` | pda_simulation_generator.py |
| `PDA_STATE` | 3 | `PDA_STATE\|pos 1\|q\|stack=$` | pda_simulation_generator.py |
| `PDE_SETUP` | 2 | `PDE_SETUP\|u_tt = 36u_xx\|u(x,0)=x^2, u_t(x,0)=0` | separable_pde_generator.py |
| `PDF_FORMULA` | 1 | `PDF_FORMULA\|f_Y(y)=1/(38*sqrt(y))` | rv_transform_generator.py |
| `PD_SETUP` | 2 | `PD_SETUP\|A=[[-4,2], [2,-4]]\|Sylvester criterion` | positive_definite_generator.py |
| `PERCENT_CALC_PART` | 3 | `PERCENT_CALC_PART\|1.555\|1950\|3032.25` | percent_problem_generator.py |
| `PERCENT_TO_DEC` | 2 | `PERCENT_TO_DEC\|87%\|0.87` | annuity_generator.py, bond_pricing_generator.py, composite_arithmetic_generator.py, exponential_model_generator.py, fill_in_step_generator.py, finance_generator.py, fraction_decimal_percent_converter.py, npv_irr_generator.py, percent_problem_generator.py, percent_word_problem_generator.py, piecewise_evaluation_generator.py, portfolio_generator.py, tip_bill_split_generator.py |
| `PERCEPTRON_RULE` | 2 | `PERCEPTRON_RULE\|score=w0+w1*x1+w2*x2\|if y*score <= 0 update` | perceptron_generator.py |
| `PERCEPTRON_SAMPLE` | 3 | `PERCEPTRON_SAMPLE\|i=1\|x=(3,3)\|y=1` | perceptron_generator.py |
| `PERCEPTRON_SCORE` | 2 | `PERCEPTRON_SCORE\|i=1\|score=-13` | perceptron_generator.py |
| `PERCEPTRON_SETUP` | 3 | `PERCEPTRON_SETUP\|eta=1\|w=(-1,-2,-2)\|samples=[(3,3,1), (-2,1,1), (0,-3,-1), (-2,-2,1)]` | perceptron_generator.py |
| `PERCEPTRON_UPDATE` | 2, 3 | `PERCEPTRON_UPDATE\|i=1\|w=(0,1,1)` | perceptron_generator.py |
| `PERIM` | 1 | `PERIM\|42` | geometry_area_perimeter_generator.py, polygon_perimeter_generator.py |
| `PERIOD` | 1 | `PERIOD\|π` | sinusoid_features_generator.py |
| `PERM_COMPOSE` | 3 | `PERM_COMPOSE\|i=1\|tau(i)=5\|sigma(tau(i))=2` | permutation_group_generator.py |
| `PERM_FORMULA` | 1 | `PERM_FORMULA\|P(n, r) = n·(n-1)···(n-r+1), 2 factors` | permutation_combination_generator.py |
| `PERM_RESULT` | 1 | `PERM_RESULT\|[2, 4, 6, 3, 1, 5]` | permutation_group_generator.py |
| `PERM_SETUP` | 2, 3 | `PERM_SETUP\|arrange 2 of 4\|order matters` | permutation_combination_generator.py, permutation_group_generator.py |
| `PERPLEXITY` | 2 | `PERPLEXITY\|exp(CE)\|32` | perplexity_generator.py |
| `PERPLEXITY_SETUP` | 2 | `PERPLEXITY_SETUP\|tokens=132\|p=1/32` | perplexity_generator.py |
| `PE_ENTRY` | 2 | `PE_ENTRY\|0\|1` | positional_encoding_generator.py |
| `PE_SETUP` | 3 | `PE_SETUP\|position=168\|d=2\|theta=pi/2` | positional_encoding_generator.py |
| `PF_PRIME` | 1 | `PF_PRIME\|347` | prime_factorization_generator.py, repeating_decimal_generator.py |
| `PF_STEP` | 3 | `PF_STEP\|1041\|3\|347` | prime_factorization_generator.py, repeating_decimal_generator.py |
| `PHASE_SHIFT` | 1 | `PHASE_SHIFT\|π/2 left` | sinusoid_features_generator.py |
| `PHI_STEP` | 2 | `PHI_STEP\|p=2\|24` | totient_generator.py |
| `PHYS_FORMULA` | 1 | `PHYS_FORMULA\|P = W/t` | physics_formula_generator.py |
| `PHYS_SETUP` | 3 | `PHYS_SETUP\|W = 44700 joules\|t = 5 minutes\|power` | physics_formula_generator.py |
| `PH_FORMULA` | 1 | `PH_FORMULA\|pH=-log10([H+])` | ph_calculation_generator.py |
| `PH_SETUP` | 2, 3 | `PH_SETUP\|hydronium_power\|[H+]=10^-12` | ph_calculation_generator.py |
| `PI2_NUM` | 3 | `PI2_NUM\|-1/1250\|π^2\|-π^2/1250` | casimir_force_generator.py |
| `PICTO_COUNT` | 2 | `PICTO_COUNT\|Giraffes\|1` | graph_interpret_generator.py |
| `PICTO_KEY` | 2 | `PICTO_KEY\|♦\|5` | graph_interpret_generator.py |
| `PIVOT` | 3 | `PIVOT\|row=s1\|column=x\|pivot=1` | simplex_generator.py |
| `PIVOT_COLS` | 2 | `PIVOT_COLS\|columns 1, 2, 3\|rank = 3` | subspace_basis_generator.py |
| `PI_COEFF` | 2 | `PI_COEFF\|17π/12\|17/12` | arc_sector_generator.py |
| `PI_DEN` | 3 | `PI_DEN\|125/1584\|π\|125/(1584π)` | gauss_law_generator.py, hawking_generator.py, magnetism_generator.py |
| `PI_MULT` | 3 | `PI_MULT\|2\|π\|2π` | shm_generator.py |
| `PLACE_DP` | 3 | `PLACE_DP\|2262\|2\|22.62` | decimal_mult_generator.py |
| `PLACE_DP_Q` | 3 | `PLACE_DP_Q\|165\|3\|165` | decimal_div_generator.py, percent_problem_generator.py |
| `PLACE_VALUE` | 2 | `PLACE_VALUE\|B * 16^0\|11` | base_conversion_generator.py |
| `PLANCK_SETUP` | 4 | `PLANCK_SETUP\|length\|hbar=9\|G=16\|c=16` | planck_units_generator.py |
| `PLUS_MINUS` | 2 | `PLUS_MINUS\|y + 41 = ±58\|y + 41 = 58 or y + 41 = -58` | completing_square_generator.py, quadratic_square_root_generator.py, rational_equation_generator.py |
| `POINT_FROM_LAMBDA` | 3 | `POINT_FROM_LAMBDA\|x\|96*5/8\|60` | lagrange_multiplier_generator.py |
| `POINT_SLOPE_SETUP` | 1 | `POINT_SLOPE_SETUP\|y - 2 = -3/2(x + 4)` | equation_from_two_points_generator.py, parallel_perpendicular_line_generator.py, point_slope_generator.py |
| `POLAR_AREA_FORMULA` | 1 | `POLAR_AREA_FORMULA\|A = (1/2) ∫ r^2 dθ` | parametric_calculus_generator.py |
| `POLAR_BOUNDS` | 2 | `POLAR_BOUNDS\|r\|0..6` | double_integral_generator.py |
| `POLAR_CONVERT` | 2 | `POLAR_CONVERT\|x^2 + y^2\|r^2` | double_integral_generator.py |
| `POLAR_EVAL` | 3 | `POLAR_EVAL\|theta range * radial integral\|pi * 324\|324*pi` | double_integral_generator.py |
| `POLAR_FORM` | 1 | `POLAR_FORM\|2sqrt2 cis(135 deg)` | euler_formula_generator.py |
| `POLAR_FORMULA` | 1 | `POLAR_FORMULA\|r = √(x^2 + y^2), tan θ = y/x` | polar_parametric_generator.py |
| `POLAR_SETUP` | 2, 3 | `POLAR_SETUP\|(x, y) = (175, -60)\|polar (r ≥ 0, 0° ≤ θ < 360°)` | parametric_calculus_generator.py, polar_parametric_generator.py |
| `POLES` | 1 | `POLES\|s=-5, -9` | transfer_function_generator.py |
| `POLE_ORDER` | 1 | `POLE_ORDER\|3` | residue_generator.py |
| `POLE_TEST` | 3 | `POLE_TEST\|pole 6\|abs(6) < 5\|outside` | contour_integral_generator.py |
| `POLLARD_FACTOR` | 2 | `POLLARD_FACTOR\|11\|31` | pollard_factorization_generator.py |
| `POLLARD_PM1_SETUP` | 3 | `POLLARD_PM1_SETUP\|n=299\|base=3\|B=6` | pollard_factorization_generator.py |
| `POLLARD_RHO_SETUP` | 3 | `POLLARD_RHO_SETUP\|n=341\|c=1\|x0=7` | pollard_factorization_generator.py |
| `POLYDIV_SETUP` | 2 | `POLYDIV_SETUP\|4x^3 - 14x^2 + 16x - 2\|2x - 4` | finite_field_generator.py, polynomial_long_division_generator.py |
| `POLY_ACCUM` | 2 | `POLY_ACCUM\|x^0\|1` | finite_field_generator.py |
| `POLY_ADD_START` | 1 | `POLY_ADD_START\|max degree 2` | finite_field_generator.py |
| `POLY_COEFF` | 3 | `POLY_COEFF\|sum\|x^0\|0` | finite_field_generator.py |
| `POLY_COMBINE` | 1 | `POLY_COMBINE\|5x + 4` | multiplying_binomials_generator.py, polynomial_add_sub_generator.py |
| `POLY_DIST_NEG` | 1 | `POLY_DIST_NEG\|Distribute negative sign to second polynomial` | polynomial_add_sub_generator.py |
| `POLY_DIV_SETUP` | 1 | `POLY_DIV_SETUP\|(-12x^4 + 30x^2 - 30x) / (6x)` | polynomial_div_monomial_generator.py |
| `POLY_DIV_SPLIT` | 1 | `POLY_DIV_SPLIT\|(-12x^4) / (6x) + (30x^2) / (6x) + (-30x) / (6x)` | polynomial_div_monomial_generator.py |
| `POLY_FORMULA` | 1 | `POLY_FORMULA\|A = (1/2)·a·P` | regular_polygon_area_generator.py |
| `POLY_GROUP_LIKE` | 1 | `POLY_GROUP_LIKE\|(4x +x) + (7 -3)` | multiplying_polynomials_generator.py, polynomial_add_sub_generator.py |
| `POLY_INPUT` | 2 | `POLY_INPUT\|f(x)\|x^2 + 1` | finite_field_generator.py |
| `POLY_MULT_SETUP` | 1 | `POLY_MULT_SETUP\|(-5x - 4)(-2x^2 + x + 3)` | multiplying_polynomials_generator.py |
| `POLY_MUL_START` | 2 | `POLY_MUL_START\|degree 2\|degree 1` | finite_field_generator.py |
| `POLY_REMAINDER` | 1 | `POLY_REMAINDER\|x^2` | finite_field_generator.py |
| `POLY_SCALE` | 3 | `POLY_SCALE\|x^3 - 3x/5\|5/2\|(5x^3 - 3x)/2` | legendre_construction_generator.py |
| `POLY_SETUP` | 1, 2 | `POLY_SETUP\|(4x + 7) + (x - 3)` | factor_gcf_generator.py, factor_grouping_generator.py, factor_special_forms_generator.py, factor_trinomial_generator.py, polynomial_add_sub_generator.py, rational_expr_add_sub_generator.py, rational_expr_mult_div_generator.py, rational_expr_simplify_generator.py, regular_polygon_area_generator.py |
| `POLY_SUB` | 2, 3 | `POLY_SUB\|(4x^3 - 14x^2) - (4x^3 - 8x^2)\|-6x^2` | legendre_construction_generator.py, polynomial_long_division_generator.py |
| `PORT_FORMULA` | 2 | `PORT_FORMULA\|E=wA*rA+wB*rB\|Var=wA^2*varA+wB^2*varB+2*wA*wB*cov` | portfolio_generator.py |
| `PORT_RESULT` | 2 | `PORT_RESULT\|expected_return=0.092\|variance=0.018` | portfolio_generator.py |
| `PORT_SETUP` | 3 | `PORT_SETUP\|wA=0.6,wB=0.4\|rA=6%,rB=14%\|varA=0.01,varB=0.09,cov=0` | portfolio_generator.py |
| `POSTERIOR_PARAM` | 1 | `POSTERIOR_PARAM\|alpha' = alpha + successes` | bayesian_update_generator.py |
| `POST_PRECISION` | 1 | `POST_PRECISION\|prior precision + data precision` | bayesian_update_generator.py |
| `POTENTIAL_BUILD` | 3 | `POTENTIAL_BUILD\|integrate P dx\|2*x^2 + x*y - 4*x + g(y)\|g'(y) remains` | exact_ode_generator.py, line_integral_generator.py |
| `POTENTIAL_RESULT` | 2 | `POTENTIAL_RESULT\|phi(x,y)\|2*x^2 + 5*y^2 + x*y - 4*x + 3*y` | exact_ode_generator.py, line_integral_generator.py |
| `POW` | 2 | `POW\|(3/10)^3\|0.027` | binomial_probability_generator.py, geometric_distribution_generator.py, recurrence_generator.py |
| `POWER_ENTRY` | 3 | `POWER_ENTRY\|(1,1)\|(-81) + 16*2\|-49` | diagonalization_generator.py |
| `POWER_FORM` | 1 | `POWER_FORM\|A^4 = P*D^4*P^-1` | diagonalization_generator.py |
| `POWER_INTEGRAL` | 2 | `POWER_INTEGRAL\|int_0^a x dx\|a^2/2` | continuous_distribution_generator.py, wavefunction_generator.py |
| `POWER_REDUCE` | 2 | `POWER_REDUCE\|11^74\|11^14 mod 31` | totient_generator.py |
| `POWER_RULE` | 2 | `POWER_RULE\|3x^2\|6x` | chain_rule_generator.py, commutator_generator.py, curve_analysis_generator.py, derivative_power_rule_generator.py, derivative_product_quotient_generator.py, derivative_transcendental_generator.py, lhopital_generator.py, linear_approx_generator.py, log_diff_higher_order_generator.py, mean_value_theorem_generator.py, optimization_generator.py, tangent_line_generator.py |
| `POWER_SETUP` | 2 | `POWER_SETUP\|cis(230 deg)^(3i)\|principal logarithm` | complex_log_generator.py |
| `POWER_SET_RESULT` | 1 | `POWER_SET_RESULT\|{{}, {c}, {e}, {c, e}}` | set_operations_generator.py |
| `POWER_SHIFT` | 3 | `POWER_SHIFT\|k=0\|0-2\|-2` | laurent_series_generator.py |
| `PREDICT` | 2 | `PREDICT\|x*\|-57/32` | kernel_ridge_generator.py |
| `PRIME` | 1 | `PRIME\|41` | divisibility_classification_generator.py |
| `PRIM_CANDIDATES` | 2 | `PRIM_CANDIDATES\|visited B\|AB=15, BC=19, BE=22` | mst_generator.py |
| `PRIM_START` | 1 | `PRIM_START\|B` | mst_generator.py |
| `PRINCIPAL_LOG` | 1 | `PRINCIPAL_LOG\|ln(7/2) + i*29pi/90` | complex_log_generator.py |
| `PRINCIPAL_MINOR` | 2 | `PRINCIPAL_MINOR\|K11\|7` | kernel_validity_generator.py |
| `PRIOR_PRECISION` | 1 | `PRIOR_PRECISION\|1/tau^2` | bayesian_update_generator.py |
| `PROBABILITY` | 2 | `PROBABILITY\|P(+z)\|144/169` | spin_half_generator.py |
| `PROB_CONDITIONAL` | 2 | `PROB_CONDITIONAL\|P(yellow given first was black)\|7/18` | compound_probability_generator.py |
| `PROB_DEPENDENT` | 1 | `PROB_DEPENDENT\|Drawing without replacement means dependent events` | compound_probability_generator.py |
| `PROB_DESCRIBE` | 1 | `PROB_DESCRIBE\|Draw with replacement: silver, then red` | compound_probability_generator.py |
| `PROB_IDENTIFY` | 2 | `PROB_IDENTIFY\|P(draw 1 is silver)\|1/5` | compound_probability_generator.py |
| `PROB_INDEPENDENT` | 1 | `PROB_INDEPENDENT\|Replacement restores the same distribution, so the draws are independent` | compound_probability_generator.py |
| `PROB_MULTIPLY` | 3 | `PROB_MULTIPLY\|1/5\|1/5\|1/25` | compound_probability_generator.py |
| `PROB_SETUP` | 2 | `PROB_SETUP\|5\|128` | simple_probability_generator.py |
| `PROB_SIMPLIFY` | 2 | `PROB_SIMPLIFY\|42/342\|7/57` | compound_probability_generator.py |
| `PROB_WEIGHT` | 2 | `PROB_WEIGHT\|0^2\|0` | clebsch_gordan_generator.py |
| `PRODUCT` | 2 | `PRODUCT\|Delta x^2 * Delta p^2\|10201pi^2/12 - 1/2` | uncertainty_generator.py |
| `PROJECT` | 2 | `PROJECT\|P1\|0` | pca_generator.py |
| `PROJECTILE_SETUP` | 3 | `PROJECTILE_SETUP\|vx=29\|vy=40\|g=10` | projectile_motion_generator.py |
| `PROJECTION` | 2 | `PROJECTION\|X*beta\|[2, 6, 10, 14]` | least_squares_generator.py, legendre_construction_generator.py |
| `PROJECTOR_SETUP` | 2 | `PROJECTOR_SETUP\|v=(43053/65525, 49396/65525)\|P=vv^T=[[1853560809/4293525625,2126645988/4293525625],[2126645988/4293525625,2439964816/4293525625]]` | projector_generator.py |
| `PROJ_COEFF` | 3 | `PROJ_COEFF\|v2 on u1\|-5/5\|-1` | gram_schmidt_generator.py |
| `PROJ_VECTOR` | 2 | `PROJ_VECTOR\|-u1\|[2, 1]` | gram_schmidt_generator.py |
| `PROPERTY_MATCH` | 3 | `PROPERTY_MATCH\|multiplicative identity property\|a × 1 = a\|5771 × 1` | operation_properties_generator.py |
| `PROPERTY_RESULT` | 2 | `PROPERTY_RESULT\|reflexive\|no` | relation_check_generator.py |
| `PROP_SETUP` | 1 | `PROP_SETUP\|2/2 = x/3` | proportion_word_problem_generator.py, proportional_relationship_generator.py, similar_triangles_generator.py, triangle_solve_generator.py |
| `PSD_SETUP` | 2 | `PSD_SETUP\|K=[[7,8], [8,11]]\|criterion=all principal minors >= 0` | kernel_validity_generator.py |
| `PURITY` | 1 | `PURITY\|Tr(rho^2)=173/225` | density_matrix_generator.py |
| `PYTHAG_CALCULATE` | 2 | `PYTHAG_CALCULATE\|h² = 2856100 - 1440000 = 1416100\|1416100` | pythag_leg_generator.py |
| `PYTHAG_CONTEXT` | 3 | `PYTHAG_CONTEXT\|ladder\|ladder=1690ft, given=1200ft\|diagram=WDN` | pythag_leg_generator.py |
| `PYTHAG_FORMULA` | 1 | `PYTHAG_FORMULA\|a² + b² = c²` | pythag_hyp_generator.py, pythag_leg_generator.py |
| `PYTHAG_MODEL` | 3 | `PYTHAG_MODEL\|ground=1200\|wall=?\|ladder=1690` | pythag_leg_generator.py |
| `PYTHAG_ROOT` | 2 | `PYTHAG_ROOT\|400\|20` | pythag_leg_generator.py |
| `PYTHAG_SETUP` | 2, 3 | `PYTHAG_SETUP\|legs=12,9\|hypotenuse LQ=?` | pythag_hyp_generator.py, pythag_leg_generator.py |
| `PYTHAG_SOLVE` | 2 | `PYTHAG_SOLVE\|b² = 625 - 225\|400` | pythag_leg_generator.py |
| `PYTHAG_SQUARE` | 2 | `PYTHAG_SQUARE\|15\|225` | pythag_leg_generator.py |
| `PYTHAG_SUBSTITUTE` | 1 | `PYTHAG_SUBSTITUTE\|15² + b² = 25²` | pythag_leg_generator.py |
| `Q1` | 4 | `Q1\|-6\|90\|6\|14` | complex_quadratic_generator.py, polynomial_zeros_generator.py, quadratic_generator.py |
| `Q2` | 4 | `Q2\|-6\|90\|6\|-16` | complex_quadratic_generator.py, polynomial_zeros_generator.py, quadratic_generator.py |
| `QN_ADD` | 4 | `QN_ADD\|Q\|left\|0 + mu-(-1)\|-1` | conservation_law_generator.py |
| `QR_ENTRY` | 2 | `QR_ENTRY\|q1\|[1, 0, 0]` | qr_decomposition_generator.py |
| `QR_SETUP` | 2 | `QR_SETUP\|A = [[2, -3, -3], [0, 2, 0], [0, 0, 5]]\|Gram-Schmidt columns` | qr_decomposition_generator.py |
| `QUADRANT` | 2 | `QUADRANT\|33°\|quadrant I` | angle_measure_generator.py, polar_parametric_generator.py, unit_circle_generator.py |
| `QUADRATIC` | 3 | `QUADRATIC\|3\|-21\|30` | mobius_transform_generator.py |
| `QUANTUM_FORMULA` | 1 | `QUANTUM_FORMULA\|Delta_lambda=h/(m*c)*(1-cos(theta))` | quantum_formula_generator.py |
| `QUANTUM_SETUP` | 2, 3 | `QUANTUM_SETUP\|gates=X then Y then H\|input=e^(i229π/233)·ket0` | quantum_formula_generator.py, quantum_gate_generator.py |
| `QUANT_SETUP` | 3 | `QUANT_SETUP\|x=(13/50,-129/100,-13/25)\|scale=1/25\|zero_point=-5` | quantization_generator.py |
| `QUANT_VALUE` | 2 | `QUANT_VALUE\|1\|2` | quantization_generator.py |
| `QUARK_CHARGE` | 2 | `QUARK_CHARGE\|s\|-1/3` | quark_composition_generator.py |
| `QUARK_SETUP` | 3 | `QUARK_SETUP\|meson,count=229\|s anti_b\|u=2/3,d=-1/3,s=-1/3,c=2/3,b=-1/3; anti=-charge` | quark_composition_generator.py |
| `QUARTILE` | 3 | `QUARTILE\|Q1\|6,8,12,13,23,24,28\|13` | five_number_summary_generator.py |
| `QUAT_COMPONENT` | 3 | `QUAT_COMPONENT\|p*q\|real\|5` | quaternion_generator.py |
| `QUAT_INVERSE` | 2 | `QUAT_INVERSE\|p\|(1/13,-2/13,2/13,-2/13)` | quaternion_generator.py |
| `QUAT_MUL_START` | 3 | `QUAT_MUL_START\|p*q\|p\|q` | quaternion_generator.py |
| `QUAT_RESULT` | 2 | `QUAT_RESULT\|p*q\|(5,-9,8,-5)` | quaternion_generator.py |
| `QUAT_SETUP` | 2 | `QUAT_SETUP\|p=(1,2,-2,2)\|q=(-3,-1,2,-1)` | quaternion_generator.py |
| `QUEUE_STATE` | 2 | `QUEUE_STATE\|initial\|C` | graph_traversal_generator.py |
| `QUOTIENT` | 1 | `QUOTIENT\|x + 1` | finite_field_generator.py |
| `Q_EXPR` | 1 | `Q_EXPR\|Q = [B]/[A]` | equilibrium_ice_generator.py |
| `R` | 1 | `R\|21` | complex_number_ops_generator.py, finite_field_generator.py, long_division_generator.py, polynomial_long_division_generator.py, polynomial_zeros_generator.py, synthetic_division_generator.py |
| `RAPIDITY_SUM` | 2 | `RAPIDITY_SUM\|collinear boosts\|-5/6` | minkowski_interval_generator.py |
| `RATE_MONTHLY` | 2 | `RATE_MONTHLY\|24% / 12\|0.02` | finance_generator.py |
| `RATE_SETUP` | 2 | `RATE_SETUP\|conical tank, radius = height/2; water in at dV/dt = 13 m³/min; depth h = 20 m\|dh/dt` | related_rates_generator.py |
| `RATIO` | 2, 3 | `RATIO\|y = 3*x\|y = 3*x` | lagrange_multiplier_generator.py, simplex_generator.py |
| `RATIONALIZE` | 1 | `RATIONALIZE\|√311/√311` | dot_product_generator.py, limit_evaluation_generator.py, radical_rationalize_generator.py, special_right_triangle_generator.py |
| `RATIO_BASE` | 3 | `RATIO_BASE\|10:16\|2\|5:8` | error_spotting_generator.py, fill_in_step_generator.py, ratio_table_generator.py |
| `RATIO_TABLE` | 2 | `RATIO_TABLE\|Distance (miles): 10, 25, 30, ?\|Time (hours): 16, 40, 48, 88` | error_spotting_generator.py, fill_in_step_generator.py, ratio_table_generator.py |
| `RAW_FORMULA` | 1 | `RAW_FORMULA\|x = μ + z·σ` | z_score_generator.py |
| `REARRANGE_EQ` | 1 | `REARRANGE_EQ\|whole = 6708 / 0.78` | percent_problem_generator.py |
| `RECIPROCAL` | 2 | `RECIPROCAL\|csc θ = 1/sin θ\|-25/24` | trig_six_functions_generator.py |
| `RECOVER_DATA` | 2 | `RECOVER_DATA\|positions 3,5,6,7\|0010` | hamming_code_generator.py |
| `RECT_FORM` | 1 | `RECT_FORM\|-24i` | de_moivre_generator.py, euler_formula_generator.py |
| `RECUR` | 3 | `RECUR\|5P_5 = 9x P_4 - 4P_3\|P_4 = (35x^4 - 30x^2 + 3)/8\|P_3 = (5x^3 - 3x)/2` | legendre_construction_generator.py |
| `RECURRENCE` | 2 | `RECURRENCE\|a_(n+1)\|a_n/(n+1)` | derangement_generator.py, series_solution_generator.py |
| `REC_SETUP` | 1, 2 | `REC_SETUP\|a_n = 6 a_(n-1) - 8 a_(n-2) + 15\|a_0 = 2, a_1 = -3` | master_theorem_generator.py, recurrence_generator.py |
| `REDUCED_DENSITY` | 1 | `REDUCED_DENSITY\|rho_A=[[219/224,0],[0,5/224]]` | partial_trace_generator.py |
| `REFLEXIVE_CHECK` | 2 | `REFLEXIVE_CHECK\|(1, 1)\|missing` | relation_check_generator.py |
| `REGEX_ACCEPT` | 1 | `REGEX_ACCEPT\|q73729_3, q73729_4` | regex_to_automaton_generator.py |
| `REGEX_SETUP` | 3 | `REGEX_SETUP\|(a or b)*(ab or ba)\|alphabet a,b\|canonical progress DFA` | regex_to_automaton_generator.py |
| `REGEX_STATE` | 2 | `REGEX_STATE\|q73729_0\|start` | regex_to_automaton_generator.py |
| `REGEX_TRANSITION` | 3 | `REGEX_TRANSITION\|q73729_0\|a\|q73729_1` | regex_to_automaton_generator.py |
| `REGION` | 2 | `REGION\|both\|{17, 19, 25}` | attribute_sorting_generator.py, venn_region_count_generator.py |
| `REGION_EQ` | 2 | `REGION_EQ\|A ∩ B ∩ C\|1` | venn_region_count_generator.py |
| `REGION_MEASURE` | 3 | `REGION_MEASURE\|area\|4*7\|28` | vector_theorem_generator.py |
| `REGION_REWRITE` | 2 | `REGION_REWRITE\|0 <= y <= 14\|y/2 <= x <= 7` | double_integral_generator.py |
| `REG_ROW` | 3 | `REG_ROW\|x-x̄=-2\|y-ȳ=-4\|product=8` | regression_generator.py |
| `REG_SETUP` | 2 | `REG_SETUP\|points: (1, 63), (2, 71), (3, 69), (4, 67), (5, 65)\|least-squares line` | regression_generator.py |
| `REJECT` | 1, 2 | `REJECT\|x = −45` | conditional_forms_generator.py, counterexample_search_generator.py, factor_trinomial_generator.py, knights_knaves_generator.py, log_conversion_generator.py, log_equation_generator.py, optimization_generator.py, polynomial_inequality_generator.py, radical_equation_generator.py, rational_equation_generator.py, rational_root_generator.py, set_builder_roster_generator.py |
| `RELAX` | 3 | `RELAX\|D->A\|update inf to 6\|via weight 6` | dijkstra_generator.py |
| `RELU` | 3 | `RELU\|z=2\|h=2\|deriv=1` | backprop_generator.py |
| `REL_ENERGY_FORMULA` | 1 | `REL_ENERGY_FORMULA\|E=sqrt(p^2+m^2)` | relativistic_energy_generator.py |
| `REL_ENERGY_SETUP` | 3 | `REL_ENERGY_SETUP\|energy_momentum\|c=1\|p=357, m=980` | relativistic_energy_generator.py |
| `REL_FORMULA` | 1 | `REL_FORMULA\|L=L0/gamma` | special_relativity_generator.py |
| `REL_SETUP` | 2, 3 | `REL_SETUP\|A = {1, 2, 3, 4}\|R = {(2, 4), (3, 1), (3, 2), (3, 3), (3, 4), (4, 1), (4, 2), (4, 3), (4, 4)}` | relation_check_generator.py, special_relativity_generator.py |
| `REPEAT_DETECT` | 2 | `REPEAT_DETECT\|remainder 52 repeats\|repetend 228070175438596491` | repeating_decimal_generator.py |
| `REP_DIM` | 2 | `REP_DIM\|6bar\|6` | young_tableaux_generator.py |
| `RESIDUAL` | 2 | `RESIDUAL\|y - X*beta\|[2, -2, -2, 2]` | least_squares_generator.py |
| `RESIDUE` | 1, 3 | `RESIDUE\|6` | contour_integral_generator.py, residue_generator.py |
| `RESIDUE_SETUP` | 2 | `RESIDUE_SETUP\|a=-4\|f=(5 + 2(z+4) + 6(z+4)^2 + 3(z+4)^3 - 3(z+4)^4)/(z+4)^3` | residue_generator.py |
| `RESIDUE_SUM` | 1 | `RESIDUE_SUM\|-1` | contour_integral_generator.py |
| `RESID_SETUP` | 2 | `RESID_SETUP\|point (1, 63), line ŷ = 63.2 + 0.6x\|residual = observed − predicted` | regression_generator.py |
| `RESOLVE` | 3 | `RESOLVE\|C1\|C2\|not P77634` | resolution_proof_generator.py |
| `RES_EMPTY` | 1 | `RES_EMPTY\|C4` | resolution_proof_generator.py |
| `RES_SETUP` | 1 | `RES_SETUP\|C1=(not P77634), C2=(P77634), C3=(P60707 OR P53376 OR P98597 OR P9208)` | resolution_proof_generator.py |
| `RES_SKIP` | 3 | `RES_SKIP\|C1\|C2\|(P51976)` | resolution_proof_generator.py |
| `REVERSE` | 2 | `REVERSE\|0,0,1,1,1,1,0,1\|10111100` | base_arithmetic_generator.py, base_conversion_generator.py, bitwise_ops_generator.py |
| `REWRITE` | 1, 2 | `REWRITE\|5771 × 1\|5771` | antiderivative_generator.py, arc_length_generator.py, area_between_curves_generator.py, chain_rule_generator.py, circle_equation_generator.py, completing_square_generator.py, complex_division_generator.py, complex_log_generator.py, complex_number_ops_generator.py, complex_quadratic_generator.py, confidence_interval_generator.py, conic_standard_form_generator.py, cramers_rule_generator.py, curve_analysis_generator.py, definite_integral_generator.py, derivative_limit_def_generator.py, derivative_power_rule_generator.py, derivative_product_quotient_generator.py, derivative_transcendental_generator.py, domain_range_generator.py, dot_product_generator.py, euler_formula_generator.py, evaluate_expression_generator.py, exponent_generator.py, exponent_mixed_rules_generator.py, exponential_equation_generator.py, factor_gcf_generator.py, factor_grouping_generator.py, factor_special_forms_generator.py, factor_trinomial_generator.py, frequency_table_generator.py, function_composition_generator.py, function_operations_generator.py, horner_evaluation_generator.py, implicit_diff_generator.py, improper_integral_generator.py, induction_verify_generator.py, integrating_factor_generator.py, integration_by_parts_generator.py, inverse_function_generator.py, lambda_reduction_generator.py, laurent_series_generator.py, lhopital_generator.py, limit_evaluation_generator.py, linear_approx_generator.py, linear_complex_generator.py, linear_fractional_generator.py, literal_equation_generator.py, log_conversion_generator.py, log_diff_higher_order_generator.py, log_equation_generator.py, log_properties_generator.py, logistic_growth_generator.py, master_theorem_generator.py, matrix_inverse_generator.py, method_of_moments_generator.py, mgf_generator.py, midpoint_generator.py, mle_generator.py, normal_table_generator.py, ode_substitution_generator.py, operation_properties_generator.py, optimization_generator.py, order_of_operations_generator.py, parametric_calculus_generator.py, partial_fractions_generator.py, permutation_combination_generator.py, polar_parametric_generator.py, polynomial_zeros_generator.py, power_series_generator.py, quadratic_factoring_generator.py, radical_add_sub_generator.py, radical_equation_generator.py, radical_multiply_generator.py, radical_rationalize_generator.py, radical_variable_simplify_generator.py, rational_equation_generator.py, rational_exponent_generator.py, rational_expr_add_sub_generator.py, rational_expr_mult_div_generator.py, rational_expr_simplify_generator.py, rational_function_features_generator.py, recursive_explicit_generator.py, regression_generator.py, related_rates_generator.py, right_triangle_trig_generator.py, row_reduction_generator.py, separable_ode_generator.py, separable_pde_generator.py, series_convergence_generator.py, series_solution_generator.py, simplify_expression_generator.py, sinusoid_features_generator.py, solid_revolution_generator.py, special_right_triangle_generator.py, special_solution_equation_generator.py, spin_half_generator.py, standard_form_conversion_generator.py, stars_and_bars_generator.py, synthetic_division_generator.py, tangent_line_generator.py, taxicab_geometry_generator.py, taylor_series_generator.py, trig_equation_generator.py, trig_identity_eval_generator.py, trig_identity_verify_generator.py, trig_six_functions_generator.py, u_substitution_generator.py, vector_ops_generator.py, z_transform_generator.py |
| `RG_SETUP` | 3 | `RG_SETUP\|one_loop\|alpha0=1/6\|beta=7,L=3/2` | running_coupling_generator.py |
| `RHO_ITER` | 4 | `RHO_ITER\|1\|x=50, y=114\|abs(r)=64\|gcd=1` | pollard_factorization_generator.py |
| `RICCI_ENTRY` | 2 | `RICCI_ENTRY\|R_phiphi\|1` | riemann_tensor_generator.py |
| `RIDGE_ENTRY` | 2 | `RIDGE_ENTRY\|K\|[[25,-30], [-30,36]]` | kernel_ridge_generator.py |
| `RIEMANN_ENTRY` | 2 | `RIEMANN_ENTRY\|R^phi_theta phi theta\|25/169` | riemann_tensor_generator.py |
| `RIEMANN_SETUP` | 2, 3 | `RIEMANN_SETUP\|f(x) = x^2 on [-1, 3], n = 4\|trapezoid rule` | riemann_sum_generator.py, riemann_tensor_generator.py |
| `RK_COMBINE` | 2 | `RK_COMBINE\|k1+2k2+2k3+k4\|-20769/256` | runge_kutta_generator.py |
| `RK_STAGE` | 3 | `RK_STAGE\|k1\|t=5/2\|Q=19/2` | runge_kutta_generator.py |
| `RODRIGUES_FORM` | 2 | `RODRIGUES_FORM\|e^(theta K)\|I + sin(theta)K + (1-cos(theta))K^2` | lie_exponential_generator.py |
| `ROOT` | 1, 2, 3 | `ROOT\|100\|10` | ac_circuit_generator.py, adam_step_generator.py, cholesky_generator.py, completing_square_generator.py, confidence_interval_generator.py, de_moivre_generator.py, doppler_generator.py, embedding_similarity_generator.py, energy_conservation_generator.py, factor_special_forms_generator.py, four_vector_generator.py, fundamental_form_generator.py, hypothesis_test_generator.py, invariant_mass_generator.py, joint_distribution_generator.py, ladder_operator_generator.py, layer_norm_generator.py, low_rank_approx_generator.py, matrix_norm_generator.py, metric_arc_length_generator.py, or_formula_generator.py, orbital_mechanics_generator.py, planck_units_generator.py, pythag_hyp_generator.py, qr_decomposition_generator.py, quadratic_generator.py, quadratic_square_root_generator.py, radical_add_sub_generator.py, radical_multiply_generator.py, radical_rationalize_generator.py, radical_variable_simplify_generator.py, rational_equation_generator.py, rational_exponent_generator.py, regression_generator.py, relativistic_energy_generator.py, round_solids_generator.py, rv_transform_generator.py, schwarzschild_generator.py, shm_generator.py, svd_generator.py, svm_margin_generator.py, two_sample_test_generator.py |
| `ROOT_ANGLE` | 2 | `ROOT_ANGLE\|k=0\|0 deg` | de_moivre_generator.py |
| `ROOT_EXTRACT` | 2 | `ROOT_EXTRACT\|7\|√7` | exponent_generator.py |
| `ROOT_IDENTIFY` | 3 | `ROOT_IDENTIFY\|343\|49\|7` | exponent_generator.py |
| `ROOT_SETUP` | 1 | `ROOT_SETUP\|√343` | exponent_generator.py, radical_add_sub_generator.py, radical_multiply_generator.py, radical_rationalize_generator.py, radical_variable_simplify_generator.py |
| `ROOT_SIMPLIFY` | 1, 2 | `ROOT_SIMPLIFY\|7√7` | complex_quadratic_generator.py, distance_formula_generator.py, dot_product_generator.py, euler_formula_generator.py, exponent_generator.py, geometric_mean_generator.py, hypercube_counting_generator.py, polar_parametric_generator.py, vector_ops_generator.py |
| `ROSTER` | 2 | `ROSTER\|S\|∅` | set_builder_roster_generator.py |
| `ROTATED_VECTOR` | 1 | `ROTATED_VECTOR\|(-3,1,-3)` | quaternion_generator.py |
| `ROT_FORMULA` | 1 | `ROT_FORMULA\|I=I_cm+m*d^2` | rotational_dynamics_generator.py |
| `ROT_SETUP` | 3 | `ROT_SETUP\|parallel_axis\|I_cm=68, m=28\|d=7` | rotational_dynamics_generator.py |
| `ROUND` | 2 | `ROUND\|3/2\|2` | quantization_generator.py |
| `ROUNDTRIP_ERROR` | 2 | `ROUNDTRIP_ERROR\|sum_abs\|3/100` | quantization_generator.py |
| `ROUND_CHECK` | 3 | `ROUND_CHECK\|4\|8\|>=5` | place_value_rounding_generator.py |
| `ROUND_RESULT` | 2 | `ROUND_RESULT\|19148\|19150` | place_value_rounding_generator.py |
| `ROUTH_ROW` | 2 | `ROUTH_ROW\|s^3\|1, 25` | routh_hurwitz_generator.py |
| `ROUTH_SETUP` | 1 | `ROUTH_SETUP\|p(s)=s^3+8s^2+25s+42` | routh_hurwitz_generator.py |
| `ROW_ENTROPY` | 2 | `ROW_ENTROPY\|H0\|649/800` | entropy_rate_markov_generator.py |
| `ROW_OP` | 1, 2 | `ROW_OP\|R2 → R2 - 3·R1\|[0, 1, 3, 15]` | row_reduction_generator.py, simplex_generator.py, subspace_basis_generator.py |
| `RREF_RESULT` | 2 | `RREF_RESULT\|RREF(A)\|[[1, 0, 0, -2], [0, 1, 0, -1], [0, 0, 1, 3]]` | subspace_basis_generator.py |
| `RSA_DECRYPT` | 2 | `RSA_DECRYPT\|4\|199` | rsa_generator.py |
| `RSA_ENCRYPT` | 2 | `RSA_ENCRYPT\|199\|4` | rsa_generator.py |
| `RSA_PRIVATE_KEY` | 1 | `RSA_PRIVATE_KEY\|d=31` | rsa_generator.py |
| `RSA_PUBLIC_KEY` | 2 | `RSA_PUBLIC_KEY\|n=247\|e=7` | rsa_generator.py |
| `RSA_SETUP` | 3 | `RSA_SETUP\|p=13\|q=19\|message=199` | rsa_generator.py |
| `RSQ_FORMULA` | 1 | `RSQ_FORMULA\|r^2 = Sxy^2/(Sxx·Syy)` | regression_generator.py |
| `RS_CORRECT` | 2 | `RS_CORRECT\|position=2\|[19,33,37,39]` | reed_solomon_generator.py |
| `RS_EVAL` | 2 | `RS_EVAL\|x=10\|84` | reed_solomon_generator.py |
| `RS_LINE` | 3 | `RS_LINE\|m0=42\|m1=32\|agree=2` | reed_solomon_generator.py |
| `RS_PAIR` | 2 | `RS_PAIR\|x=6,12\|y=19,39` | reed_solomon_generator.py |
| `RS_RECEIVED` | 1 | `RS_RECEIVED\|[19,39,37,39]` | reed_solomon_generator.py |
| `RS_SETUP` | 3 | `RS_SETUP\|F_43\|RS(4,2)\|points 6,12,26,33; one error allowed` | reed_solomon_generator.py |
| `S` | 3 | `S\|632\|594\|38` | ac_circuit_generator.py, activation_generator.py, adam_step_generator.py, angle_defect_generator.py, angle_measure_generator.py, annuity_generator.py, arc_length_generator.py, area_between_curves_generator.py, arithmetic_coding_generator.py, arithmetic_sequence_generator.py, backprop_generator.py, bayesian_update_generator.py, bec_channel_generator.py, binomial_probability_generator.py, bisection_generator.py, black_scholes_generator.py, calendar_arithmetic_generator.py, calorimetry_generator.py, casimir_force_generator.py, casimir_generator.py, channel_capacity_generator.py, cholesky_generator.py, circle_angle_generator.py, circle_equation_generator.py, collision_generator.py, commutator_generator.py, complex_locus_generator.py, complex_log_generator.py, complex_number_ops_generator.py, complex_quadratic_generator.py, composite_arithmetic_generator.py, confidence_interval_generator.py, continued_fraction_generator.py, continuous_distribution_generator.py, counting_classics_generator.py, cramers_rule_generator.py, decimal_div_generator.py, definite_integral_generator.py, density_matrix_generator.py, derangement_generator.py, determinant_generator.py, dft_generator.py, distance_formula_generator.py, doppler_generator.py, ellipse_features_generator.py, elliptic_curve_finite_field_generator.py, embedding_similarity_generator.py, entropy_generator.py, equilibrium_ice_generator.py, euler_characteristic_generator.py, euler_circuit_generator.py, euler_method_generator.py, expected_value_generator.py, exponential_model_generator.py, extended_euclid_generator.py, finance_generator.py, finite_difference_generator.py, first_law_generator.py, five_number_summary_generator.py, four_vector_generator.py, fourier_series_generator.py, fractal_iteration_generator.py, fraction_op_generator.py, function_inner_product_generator.py, function_operations_generator.py, fundamental_form_generator.py, game_theory_generator.py, gaussian_curvature_generator.py, generating_function_generator.py, geometric_distribution_generator.py, geometric_sequence_generator.py, gradient_descent_generator.py, gradient_step_generator.py, graph_interpret_generator.py, graph_traversal_generator.py, hamiltonian_generator.py, heat_engine_generator.py, hermitian_check_generator.py, hydrogen_atom_generator.py, hyperbola_features_generator.py, hyperbolic_distance_generator.py, hyperbolic_function_generator.py, hypercube_counting_generator.py, hypothesis_test_generator.py, inclusion_exclusion_generator.py, index_gymnastics_generator.py, information_gain_generator.py, integrating_factor_generator.py, interpolation_generator.py, invariant_mass_generator.py, joint_distribution_generator.py, kernel_evaluation_generator.py, kernel_ridge_generator.py, kernel_validity_generator.py, kinematics_generator.py, kmeans_step_generator.py, knn_generator.py, kraft_inequality_generator.py, ladder_operator_generator.py, lagrangian_generator.py, layer_norm_generator.py, legendre_construction_generator.py, linear_simple_generator.py, logistic_growth_generator.py, long_division_generator.py, low_rank_approx_generator.py, lp_corner_generator.py, lr_schedule_generator.py, manual_square_root_generator.py, markov_chain_generator.py, matrix_group_check_generator.py, matrix_inverse_generator.py, matrix_ops_generator.py, mean_value_theorem_generator.py, metric_arc_length_generator.py, mgf_generator.py, midpoint_generator.py, minkowski_interval_generator.py, mixed_number_operation_generator.py, mle_generator.py, mobius_transform_generator.py, modular_inverse_generator.py, mutual_information_generator.py, naive_bayes_generator.py, named_distribution_generator.py, newton_raphson_generator.py, newtons_laws_generator.py, normal_table_generator.py, npv_irr_generator.py, ode_substitution_generator.py, ode_system_generator.py, optics_generator.py, optimization_generator.py, or_formula_generator.py, order_of_operations_generator.py, order_statistics_generator.py, parabola_features_generator.py, parametric_calculus_generator.py, particle_in_box_generator.py, pca_generator.py, percent_problem_generator.py, percent_word_problem_generator.py, permutation_group_generator.py, ph_calculation_generator.py, piecewise_evaluation_generator.py, polar_parametric_generator.py, pollard_factorization_generator.py, positive_definite_generator.py, probability_addition_rule_generator.py, quadratic_residue_generator.py, quantization_generator.py, quantum_formula_generator.py, quaternion_generator.py, radical_add_sub_generator.py, radical_rationalize_generator.py, rational_expr_add_sub_generator.py, recurrence_generator.py, regression_generator.py, related_rates_generator.py, riemann_sum_generator.py, riemann_tensor_generator.py, rotational_dynamics_generator.py, routh_hurwitz_generator.py, row_reduction_generator.py, rsa_generator.py, runge_kutta_generator.py, rv_transform_generator.py, schwarzschild_generator.py, second_order_ode_generator.py, segment_partition_generator.py, separable_pde_generator.py, series_convergence_generator.py, shm_generator.py, signal_arithmetic_generator.py, slope_two_points_generator.py, softmax_gradient_generator.py, solid_revolution_generator.py, special_relativity_generator.py, spherical_excess_generator.py, spin_half_generator.py, standing_wave_generator.py, stars_and_bars_generator.py, statics_generator.py, stereographic_generator.py, taxicab_geometry_generator.py, taylor_series_generator.py, telescoping_generator.py, temperature_conversion_generator.py, tip_bill_split_generator.py, totient_generator.py, transformation_generator.py, transportation_generator.py, triangle_solve_generator.py, trig_identity_eval_generator.py, trig_six_functions_generator.py, two_sample_test_generator.py, undetermined_coeff_generator.py, unit_circle_generator.py, vector_ops_generator.py, venn_region_count_generator.py, z_score_generator.py |
| `SAMPLE_MOMENT` | 2 | `SAMPLE_MOMENT\|xbar\|4` | method_of_moments_generator.py |
| `SAMPLE_SIZE_FORMULA` | 1 | `SAMPLE_SIZE_FORMULA\|n = (z*/E)^2·p̂(1-p̂)` | confidence_interval_generator.py |
| `SA_BASES` | 2 | `SA_BASES\|2π(20)² = 2π × 400\|800π` | volume_3d_generator.py |
| `SA_FACES` | 3 | `SA_FACES\|top/bottom\|9 × 11\|99` | volume_3d_generator.py |
| `SA_FORMULA` | 1 | `SA_FORMULA\|SA = 2(lw + lh + wh)` | round_solids_generator.py, volume_3d_generator.py |
| `SA_LATERAL` | 2 | `SA_LATERAL\|2π × 20 × 13\|520π` | volume_3d_generator.py |
| `SA_SETUP` | 2 | `SA_SETUP\|rectangular_prism\|l=9, w=11, h=5` | volume_3d_generator.py |
| `SA_TOTAL` | 2 | `SA_TOTAL\|SA = 2(99 + 45 + 55)\|398` | round_solids_generator.py, volume_3d_generator.py |
| `SB_FORMULA` | 1 | `SB_FORMULA\|C(n-1, k-1)` | stars_and_bars_generator.py |
| `SB_SETUP` | 2 | `SB_SETUP\|x1+...+x8 = 12\|xi >= 1` | stars_and_bars_generator.py |
| `SCALE_DIV` | 3 | `SCALE_DIV\|5075\|145\|35` | scaling_generator.py |
| `SCALE_EXACT` | 2 | `SCALE_EXACT\|24*cos\|0` | de_moivre_generator.py, euler_formula_generator.py |
| `SCALE_IDENTIFY` | 2 | `SCALE_IDENTIFY\|5075 meters\|scaled_dimension` | scaling_generator.py |
| `SCALE_MODE` | 3 | `SCALE_MODE\|λ = -3\|(-243)*5\|-1215` | diagonalization_generator.py |
| `SCALE_MULT` | 3 | `SCALE_MULT\|5.75\|27\|155.25` | scaling_generator.py |
| `SCALE_SETUP` | 3 | `SCALE_SETUP\|1 centimeter\|145 meters\|145` | scaling_generator.py |
| `SCALE_SHIFT` | 2 | `SCALE_SHIFT\|1\|1` | layer_norm_generator.py |
| `SCALING_COMPUTE` | 2 | `SCALING_COMPUTE\|6ND\|27648000000000000000` | scaling_law_generator.py |
| `SCALING_SETUP` | 3 | `SCALING_SETUP\|N=96000000\|D=48000000000\|F=67000000000000000` | scaling_law_generator.py |
| `SCHWARZSCHILD_SETUP` | 3, 4 | `SCHWARZSCHILD_SETUP\|time_dilation\|r_s=95\|r=171` | schwarzschild_generator.py |
| `SCI_IDENTIFY` | 2 | `SCI_IDENTIFY\|2.63\|10` | exponent_generator.py |
| `SCI_MOVE_DECIMAL` | 2 | `SCI_MOVE_DECIMAL\|left\|10` | exponent_generator.py |
| `SCI_OPERATION` | 4 | `SCI_OPERATION\|divide_coefficients\|8.36\|1.9\|4.4` | exponent_generator.py |
| `SCI_SETUP` | 1 | `SCI_SETUP\|26300000000` | exponent_generator.py |
| `SCORE_EQ` | 1 | `SCORE_EQ\|9/lambda=62` | mle_generator.py |
| `SEARCH_BOUNDS` | 3 | `SEARCH_BOUNDS\|iter 1\|lo=0\|hi=5` | algorithm_trace_generator.py |
| `SEARCH_STATE` | 2 | `SEARCH_STATE\|lo=3\|hi=5` | algorithm_trace_generator.py |
| `SECOND_DERIV_TEST` | 2 | `SECOND_DERIV_TEST\|f'' < 0 for x < 4, f'' > 0 for x > 4\|concavity changes` | curve_analysis_generator.py, optimization_generator.py |
| `SECOND_PARTIAL` | 2 | `SECOND_PARTIAL\|f_xx\|-2` | hessian_classify_generator.py |
| `SECTION_FORMULA` | 1 | `SECTION_FORMULA\|P = (x1 + m/(m+n)·(x2 - x1), y1 + m/(m+n)·(y2 - y1))` | segment_partition_generator.py |
| `SECTION_SETUP` | 2 | `SECTION_SETUP\|A(3, -8), B(5, -2); ratio 1:1 from A\|point P` | segment_partition_generator.py |
| `SECTOR_FORMULA` | 1 | `SECTOR_FORMULA\|A = (1/2)r^2θ` | arc_sector_generator.py |
| `SELECT_MIN` | 2 | `SELECT_MIN\|D\|0` | dijkstra_generator.py |
| `SELECT_RELEVANT` | 2 | `SELECT_RELEVANT\|base = 47, rate = 15%\|ignore 44 (irrelevant)` | percent_word_problem_generator.py, proportion_word_problem_generator.py |
| `SEPARATE` | 1, 2 | `SEPARATE\|y^(-2) dy = dx` | ode_substitution_generator.py, separable_ode_generator.py, separable_pde_generator.py |
| `SEQ_APPLY` | 1 | `SEQ_APPLY\|a_24 = -4 + (24 - 1)·-9` | arithmetic_sequence_generator.py, geometric_sequence_generator.py, recursive_explicit_generator.py |
| `SEQ_FORMULA` | 1 | `SEQ_FORMULA\|a_n = a_1 + (n - 1)d` | arithmetic_sequence_generator.py, geometric_sequence_generator.py, recursive_explicit_generator.py |
| `SEQ_SETUP` | 2 | `SEQ_SETUP\|-4, -13, -22, -31, ...\|24th term` | arithmetic_sequence_generator.py, geometric_sequence_generator.py, recursive_explicit_generator.py |
| `SERIES` | 1 | `SERIES\|G=G1*G2` | transfer_function_generator.py |
| `SERIES_ASSUME` | 2 | `SERIES_ASSUME\|y\|sum a_n x^n` | series_solution_generator.py |
| `SERIES_GROUP` | 2 | `SERIES_GROUP\|even powers\|cos(theta)I` | lie_exponential_generator.py |
| `SERIES_SETUP` | 2 | `SERIES_SETUP\|Σ -48·(9/4)^n, n ≥ 0\|converge or diverge? find the sum if it converges` | legendre_construction_generator.py, power_series_generator.py, series_convergence_generator.py |
| `SERIES_TERM` | 3 | `SERIES_TERM\|n=0\|1\|1` | grassmann_generator.py |
| `SETUP_PERCENT_EQ` | 1 | `SETUP_PERCENT_EQ\|6708 = 0.78 * whole` | percent_problem_generator.py |
| `SET_SETUP` | 2, 3 | `SET_SETUP\|A = {a}\|B = {1, 2}\|cartesian product` | set_operations_generator.py |
| `SET_SIDE` | 2 | `SET_SIDE\|left\|∅` | counterexample_search_generator.py |
| `SHIFT` | 1, 2 | `SHIFT\|yi = xi - 1\|y1+...+y8 = 4` | algorithm_trace_generator.py, recurrence_generator.py, stars_and_bars_generator.py, z_transform_generator.py |
| `SHM_FORMULA` | 1 | `SHM_FORMULA\|omega^2=g/L` | shm_generator.py |
| `SHM_SETUP` | 3 | `SHM_SETUP\|pendulum_period\|g=10\|L=10` | shm_generator.py |
| `SHORTEST` | 2 | `SHORTEST\|(1,-6)\|norm^2=37` | lll_reduction_generator.py |
| `SIGFIG_ROUND` | 3 | `SIGFIG_ROUND\|43200\|2 significant figures\|4.3 × 10^4` | fermi_estimation_generator.py |
| `SIGMA_EXPAND` | 1 | `SIGMA_EXPAND\|8 + 16 + 32` | sigma_notation_generator.py |
| `SIGMA_SETUP` | 2 | `SIGMA_SETUP\|Σ_(k=0)^(2) 8·2^k\|expand and evaluate` | sigma_notation_generator.py |
| `SIGMA_TERM` | 3 | `SIGMA_TERM\|k=0\|8·2^0\|8` | sigma_notation_generator.py |
| `SIGN` | 3 | `SIGN\|left\|-8\|negative` | bisection_generator.py |
| `SIGNAL_SETUP` | 2, 3 | `SIGNAL_SETUP\|dB power ratio\|P2/P1=1/100` | signal_arithmetic_generator.py |
| `SIGN_CHART` | 2 | `SIGN_CHART\|zeros\|-8, 4` | polynomial_inequality_generator.py |
| `SIGN_RULE` | 2 | `SIGN_RULE\|sin, quadrant III\|negative` | trig_equation_generator.py, trig_identity_eval_generator.py, trig_six_functions_generator.py, unit_circle_generator.py |
| `SIGN_TEST` | 4 | `SIGN_TEST\|(-inf, 3)\|y = 2\|f(y) = -10 (negative)\|down` | stability_generator.py |
| `SIMILAR_APPLY` | 3 | `SIMILAR_APPLY\|4\|5\|20` | scaling_generator.py |
| `SIMILAR_SCALE` | 3 | `SIMILAR_SCALE\|40\|8\|5` | scaling_generator.py |
| `SIMILAR_SETUP` | 3 | `SIMILAR_SETUP\|parallelogram\|8,4\|40 (others unknown)` | scaling_generator.py |
| `SIMPLEX_SETUP` | 3 | `SIMPLEX_SETUP\|max z=8x+4y\|x<=23\|y<=19` | simplex_generator.py |
| `SIM_SETUP` | 2 | `SIM_SETUP\|△ABC ~ △DEF; AB = 8, DE = 20, BC = 10\|find EF` | similar_triangles_generator.py |
| `SIN` | 2 | `SIN\|pi/2\|1` | positional_encoding_generator.py |
| `SINGULAR_VALUE` | 2 | `SINGULAR_VALUE\|sigma1\|14` | low_rank_approx_generator.py |
| `SINUSOID_SETUP` | 2 | `SINUSOID_SETUP\|y = sin(2(x + π/2)) - 3\|amplitude, period, phase shift, midline` | sinusoid_features_generator.py |
| `SIZE_REDUCE` | 2 | `SIZE_REDUCE\|b2=(9, 1)\|b2-(-1)b1=(-1, 6)` | lll_reduction_generator.py |
| `SLOPE_CALC` | 2 | *(not observed in sampling)* | equation_from_two_points_generator.py |
| `SLOPE_FORMULA` | 1 | `SLOPE_FORMULA\|m = (y2 - y1) / (x2 - x1)` | equation_from_two_points_generator.py, regression_generator.py, slope_two_points_generator.py |
| `SLOPE_INT_IDENTIFY` | 2 | `SLOPE_INT_IDENTIFY\|Slope (m)\|-16` | slope_intercept_form_generator.py |
| `SLOPE_INT_MATCH` | 2 | `SLOPE_INT_MATCH\|Compare to Slope-Intercept Form\|y = mx + b` | slope_intercept_form_generator.py |
| `SLOPE_INT_SETUP` | 1 | `SLOPE_INT_SETUP\|y = -33 - 16x` | slope_intercept_form_generator.py |
| `SLOPE_RESULT` | 1 | `SLOPE_RESULT\|-3/2` | equation_from_two_points_generator.py |
| `SLOPE_SETUP` | 2 | `SLOPE_SETUP\|(-3, 8)\|(-6, 9)` | slope_two_points_generator.py |
| `SLOPE_SUBST` | 1 | `SLOPE_SUBST\|m = (9 - 8) / (-6 - (-3))` | equation_from_two_points_generator.py, slope_two_points_generator.py |
| `SLOPE_UNDEFINED` | 1 | `SLOPE_UNDEFINED\|Division by zero` | slope_two_points_generator.py |
| `SOFTMAX_EXP` | 2 | `SOFTMAX_EXP\|1,1\|1` | attention_generator.py, softmax_gradient_generator.py |
| `SOFTMAX_PROB` | 2 | `SOFTMAX_PROB\|1\|5/14` | softmax_gradient_generator.py |
| `SOFTMAX_SETUP` | 3 | `SOFTMAX_SETUP\|z=(3*ln(5),3*ln(8),3*ln(1))\|T=3\|target=3` | softmax_gradient_generator.py |
| `SOFTMAX_WEIGHT` | 2 | `SOFTMAX_WEIGHT\|1,1\|1/2` | attention_generator.py |
| `SOLUTIONS` | 2 | `SOLUTIONS\|cos x = -1/2\|120°, 240°, 480°, 600°, 840°, 960°, 1200°, 1320°` | trig_equation_generator.py |
| `SOLUTION_FORMULA` | 1 | `SOLUTION_FORMULA\|M1*V1=M2*V2` | solution_chem_generator.py |
| `SOLUTION_SETUP` | 3 | `SOLUTION_SETUP\|dilution_stock_volume\|M1=10\|M2=1, V2=351` | solution_chem_generator.py |
| `SOLVE_CONST` | 2 | `SOLVE_CONST\|C1 = 3\|C2 = 3` | ode_system_generator.py, second_order_ode_generator.py, undetermined_coeff_generator.py |
| `SOLVE_U` | 2 | `SOLVE_U\|e^(-x)u = 5e^(-x) + C\|u = 5 + Ce^x` | ode_substitution_generator.py |
| `SOLVE_Y` | 2 | `SOLVE_Y\|e^(5x)y = 4e^(5x) + C\|y = 4 + Ce^(-5x)` | integrating_factor_generator.py, laplace_ivp_generator.py, ode_substitution_generator.py |
| `SOL_ENTRY` | 3 | `SOL_ENTRY\|x1(t)\|(e^(3t))*(-5) + (5*e^(3t) - 5*e^(6t))*(-6)\|-35*e^(3t) + 30*e^(6t)` | matrix_exponential_generator.py |
| `SOL_FORM` | 1, 2 | `SOL_FORM\|y = C1e^(-3x) + C2e^(4x)` | ode_system_generator.py, second_order_ode_generator.py, undetermined_coeff_generator.py, variation_parameters_generator.py |
| `SORT` | 2 | `SORT\|9,15,20,2,1\|1,2,9,15,20` | five_number_summary_generator.py, simple_stats_generator.py |
| `SORT_EDGES` | 1 | `SORT_EDGES\|AB=2, BE=12, AC=15, AF=17, AE=19, BD=21, CD=23` | mst_generator.py |
| `SPECIAL_SOLUTION` | 2 | `SPECIAL_SOLUTION\|13 = 13\|identity: true for every x` | radical_equation_generator.py, special_solution_equation_generator.py |
| `SPEED` | 2, 3 | `SPEED\|norm r'(0)\|11` | curve_geometry_generator.py |
| `SPHERICAL_BOUNDS` | 2 | `SPHERICAL_BOUNDS\|rho\|0..5` | triple_integral_generator.py |
| `SPHERICAL_CONVERT` | 2 | `SPHERICAL_CONVERT\|2 dV\|2*rho^2*sin(phi) drho dphi dtheta` | triple_integral_generator.py |
| `SPHERICAL_COSINES` | 1 | `SPHERICAL_COSINES\|cos(c)=sin(lat1)sin(lat2)+cos(lat1)cos(lat2)cos(dlon)` | great_circle_generator.py |
| `SPHERICAL_COSINE_LAW` | 1 | `SPHERICAL_COSINE_LAW\|cos(a)=cos(b)cos(c)+sin(b)sin(c)cos(A)` | spherical_triangle_generator.py |
| `SPHERICAL_EXCESS_SETUP` | 2 | `SPHERICAL_EXCESS_SETUP\|R=7\|angles=90,150,45` | spherical_excess_generator.py |
| `SPHERICAL_SINE_LAW` | 1 | `SPHERICAL_SINE_LAW\|sin(A)/sin(a)=sin(B)/sin(b)` | spherical_triangle_generator.py |
| `SPHERICAL_TRIANGLE_SETUP` | 2 | `SPHERICAL_TRIANGLE_SETUP\|a=90 deg, b=120 deg, A=90 deg\|find sin(B)` | spherical_triangle_generator.py |
| `SPIN_COMPONENT` | 2 | `SPIN_COMPONENT\|row=1\|-56i/65` | spin_half_generator.py |
| `SPIN_SETUP` | 3 | `SPIN_SETUP\|measurement_probability\|axis=z\|psi=[-12/13,5/13]` | spin_half_generator.py |
| `SPLIT_MIDDLE` | 2 | `SPLIT_MIDDLE\|-5x = -9x + 4x\|3x^2 - 9x + 4x - 12` | factor_trinomial_generator.py |
| `SPLIT_SETUP` | 3 | `SPLIT_SETUP\|texture\|left pos=3, neg=5\|right pos=5, neg=3` | information_gain_generator.py |
| `SQRT_BOTH_SIDES` | 2 | `SQRT_BOTH_SIDES\|(y + 41)^2 = 3364\|y + 41 = ±58` | completing_square_generator.py, quadratic_square_root_generator.py, rational_equation_generator.py |
| `SQRT_DIGIT` | 2 | `SQRT_DIGIT\|4\|root = 4` | manual_square_root_generator.py |
| `SQRT_NEG` | 2 | `SQRT_NEG\|√(-240)\|i√240` | complex_quadratic_generator.py, polynomial_zeros_generator.py |
| `SQRT_SETUP` | 2 | `SQRT_SETUP\|N = 165649\|groups 16, 56, 49` | manual_square_root_generator.py |
| `SQRT_TRIAL` | 3 | `SQRT_TRIAL\|x = 4\|(0 + 4)*4 = 16\|fits` | manual_square_root_generator.py |
| `SQUARE_BOTH_SIDES` | 2 | `SQUARE_BOTH_SIDES\|√(3x - 20) = x - 6\|3x - 20 = (x - 6)^2` | radical_equation_generator.py |
| `SQUARE_FACTOR` | 3 | `SQUARE_FACTOR\|2484\|36 × 69\|36` | radical_add_sub_generator.py, radical_multiply_generator.py, radical_rationalize_generator.py, radical_variable_simplify_generator.py |
| `SQUARE_TEST` | 3 | `SQUARE_TEST\|97\|9^2 = 81, 10^2 = 100\|not a perfect square` | discriminant_generator.py |
| `STABILITY` | 3 | `STABILITY\|y=3\|left down, right up\|unstable` | stability_generator.py |
| `STANDING_BOUNDARY` | 1 | `STANDING_BOUNDARY\|fixed-fixed string allows n=1,2,3,...` | standing_wave_generator.py |
| `STANDING_FORMULA` | 1 | `STANDING_FORMULA\|lambda=2L/n, f=v/lambda` | standing_wave_generator.py |
| `STANDING_SETUP` | 3 | `STANDING_SETUP\|string_harmonic\|n=4\|L=4, v=205` | standing_wave_generator.py |
| `STATEMENT_EVAL` | 3 | `STATEMENT_EVAL\|Bea says Oona is a knight\|T\|consistent` | knights_knaves_generator.py |
| `STATICS_FORMULA` | 1 | `STATICS_FORMULA\|sum_tau_left=0 => RB*L=W*x` | statics_generator.py |
| `STATICS_SETUP` | 3 | `STATICS_SETUP\|supported_beam\|W=198, L=19\|x=15` | statics_generator.py |
| `STATIONARY` | 2 | `STATIONARY\|pi0=2/3\|pi1=1/3` | entropy_rate_markov_generator.py |
| `STAT_ABS_DEV` | 2 | `STAT_ABS_DEV\|-14\|14` | statistics_generator.py |
| `STAT_AVERAGE` | 2 | `STAT_AVERAGE\|(56 + 86) / 2\|71` | statistics_generator.py |
| `STAT_COUNT` | 1 | `STAT_COUNT\|8` | statistics_generator.py |
| `STAT_DEVIATION` | 3 | `STAT_DEVIATION\|29\|43\|-14` | statistics_generator.py |
| `STAT_DIVIDE` | 2 | `STAT_DIVIDE\|288 / 8\|36` | statistics_generator.py |
| `STAT_FREQUENCY` | 2 | `STAT_FREQUENCY\|16\|3` | statistics_generator.py |
| `STAT_MAD` | 3 | `STAT_MAD\|72\|6\|12` | statistics_generator.py |
| `STAT_MAX` | 1 | `STAT_MAX\|95` | statistics_generator.py |
| `STAT_MEAN` | 2 | `STAT_MEAN\|258 / 6\|43` | statistics_generator.py |
| `STAT_MIDDLE` | 2 | `STAT_MIDDLE\|positions 3 and 4\|56, 86` | statistics_generator.py |
| `STAT_MIN` | 1 | `STAT_MIN\|29` | statistics_generator.py |
| `STAT_MODE` | 2 | `STAT_MODE\|54\|4` | statistics_generator.py |
| `STAT_ORDER` | 1 | `STAT_ORDER\|12, 28, 56, 86, 95, 97` | statistics_generator.py |
| `STAT_RANGE` | 2 | `STAT_RANGE\|95 - 29\|66` | statistics_generator.py |
| `STAT_SETUP` | 1 | `STAT_SETUP\|14, 58, 21, 47, 50, 20, 24, 54` | statistics_generator.py |
| `STAT_SUM` | 2 | `STAT_SUM\|14 + 58 + 21 + 47 + 50 + 20 + 24 + 54\|288` | statistics_generator.py |
| `STD` | 1 | `STD\|5` | layer_norm_generator.py |
| `STEADY_EQUATION` | 2 | `STEADY_EQUATION\|pi0*pi01=pi1*pi10\|pi0+pi1=1` | markov_chain_generator.py |
| `STEPPING_STONE` | 2 | `STEPPING_STONE\|enter x21\|+x21 -x22 +x12 -x11` | transportation_generator.py |
| `STEREO_SETUP` | 3, 4 | `STEREO_SETUP\|sphere_to_plane\|X=-4/57\|Y=64/285\|Z=277/285` | stereographic_generator.py |
| `STMT_EVAL` | 3 | `STMT_EVAL\|p\|6 is prime\|F` | logical_connective_eval_generator.py |
| `STOICH_RATIO` | 2 | `STOICH_RATIO\|CaCO3->CO2\|1/1=1` | gas_stoichiometry_generator.py, stoichiometry_generator.py |
| `STOICH_SETUP` | 2, 3 | `STOICH_SETUP\|mass_to_volume\|CaCO3 -> CaO + CO2\|given=1700 g CaCO3, target=CO2` | stoichiometry_generator.py |
| `STRUCTURE_CONSTANT` | 3 | `STRUCTURE_CONSTANT\|epsilon_xyz\|1\|-105iJz` | structure_constant_generator.py |
| `STRUCTURE_SETUP` | 3 | `STRUCTURE_SETUP\|A=7Jx\|B=-15Jy\|epsilon_xyz=1` | structure_constant_generator.py |
| `SU3_SETUP` | 2 | `SU3_SETUP\|left=3bar\|right=3bar` | young_tableaux_generator.py |
| `SUBGROUP` | 2 | `SUBGROUP\|H={e, r, r2}\|size 3` | coset_generator.py |
| `SUBGROUP_ELEM` | 2 | `SUBGROUP_ELEM\|k=1\|5` | coset_generator.py, cyclic_group_generator.py |
| `SUBGROUP_START` | 2 | `SUBGROUP_START\|H=<20>\|identity 0` | coset_generator.py |
| `SUBSET_CHECK` | 3 | `SUBSET_CHECK\|{26}\|subset of A?\|yes` | set_membership_subset_generator.py |
| `SUBSET_SIZE` | 2 | `SUBSET_SIZE\|0\|{}` | set_operations_generator.py |
| `SUBST` | 2, 3 | `SUBST\|x\|5\|-3(5)-2y+6` | arc_length_generator.py, chain_rule_generator.py, curve_analysis_generator.py, derivative_limit_def_generator.py, evaluate_expression_generator.py, function_composition_generator.py, function_evaluation_generator.py, function_operations_generator.py, function_table_generator.py, implicit_diff_generator.py, integrating_factor_generator.py, legendre_construction_generator.py, lhopital_generator.py, limit_evaluation_generator.py, line_integral_generator.py, linear_approx_generator.py, log_diff_higher_order_generator.py, logistic_growth_generator.py, mean_value_theorem_generator.py, ode_substitution_generator.py, optimization_generator.py, parametric_calculus_generator.py, partial_fractions_generator.py, piecewise_evaluation_generator.py, polar_parametric_generator.py, power_series_generator.py, recursive_explicit_generator.py, related_rates_generator.py, remainder_factor_theorem_generator.py, second_order_ode_generator.py, separable_ode_generator.py, tangent_line_generator.py, taylor_series_generator.py, trig_equation_generator.py, u_substitution_generator.py, undetermined_coeff_generator.py |
| `SUBSTITUTE` | 2 | `SUBSTITUTE\|c:=(lambda c. (lambda p. p)) in d\|d` | lambda_reduction_generator.py |
| `SUBSTITUTION` | 2 | `SUBSTITUTION\|u = y^(-1)\|u' = -y^(-2) dy/dx` | ode_substitution_generator.py |
| `SUB_COL` | 3 | `SUB_COL\|col_1\|5-6-borrow0\|->9 (borrow_out 1)` | multi_digit_subtraction_generator.py |
| `SUM` | 2, 3 | `SUM\|63 + 71 + 69 + 67 + 65\|335` | bayesian_update_generator.py, method_of_moments_generator.py, mle_generator.py, regression_generator.py |
| `SUM_ORDER` | 2 | `SUM_ORDER\|Σ i^1\|n^2` | master_theorem_generator.py |
| `SUPPORT` | 2 | `SUPPORT\|0<=x<=19\|0<=y<=361` | rv_transform_generator.py |
| `SUPPORT_TERM` | 2 | `SUPPORT_TERM\|1\|(-3,0)` | svm_margin_generator.py |
| `SVM_SETUP` | 3 | `SVM_SETUP\|x1=(3,0),y1=-1,alpha1=1\|x2=(0,4),y2=1,alpha2=1\|b=-2,x=(0,-5)` | svm_margin_generator.py |
| `SWAP` | 2 | `SWAP\|norm b2=37\|norm b1=125` | lll_reduction_generator.py |
| `SWAP_VARS` | 1 | `SWAP_VARS\|x = (y - 2)/2` | inverse_function_generator.py |
| `SYMMETRIC_CHECK` | 3 | `SYMMETRIC_CHECK\|(2, 4)\|reverse (4, 2)\|present` | relation_check_generator.py |
| `SYMMETRY` | 2 | `SYMMETRY\|odd function\|a0=0, a_n=0` | fourier_series_generator.py |
| `SYNDIV_SETUP` | 2 | `SYNDIV_SETUP\|x^3 + 3x^2 - 6x + 1\|r = 2` | polynomial_zeros_generator.py, synthetic_division_generator.py |
| `SYNDROME_CALC` | 2 | `SYNDROME_CALC\|s1=b1 xor b3 xor b5 xor b7\|0 xor 0 xor 0 xor 0=0` | hamming_code_generator.py |
| `SYNDROME_VALUE` | 2 | `SYNDROME_VALUE\|s1=0, s2=1, s4=0\|position=2` | hamming_code_generator.py |
| `SYN_DROP` | 1 | `SYN_DROP\|1` | horner_evaluation_generator.py, polynomial_zeros_generator.py, synthetic_division_generator.py |
| `SYN_ROW` | 1 | `SYN_ROW\|1, 5, 4, 9` | polynomial_zeros_generator.py, synthetic_division_generator.py |
| `SYS_ADD` | 1 | `SYS_ADD\|Add equations: 9x = 9` | systems_elimination_generator.py |
| `SYS_EQ_NEW` | 1 | `SYS_EQ_NEW\|New equation with x only` | systems_substitution_generator.py |
| `SYS_ISOLATE` | 2 | `SYS_ISOLATE\|Isolate x in Eq 1\|x = -y + 7` | systems_substitution_generator.py |
| `SYS_MULT` | 1 | `SYS_MULT\|Eq1 * -2, Eq2 * -1` | systems_elimination_generator.py |
| `SYS_REWRITE` | 2 | `SYS_REWRITE\|6x + 8y = 30\|3x - 8y = -21` | systems_elimination_generator.py |
| `SYS_SETUP` | 2 | `SYS_SETUP\|y = x + 9\|-2x - 5y = -38` | systems_elimination_generator.py, systems_substitution_generator.py |
| `SYS_SUBST` | 1 | `SYS_SUBST\|Substitute (x + 9) for y in Eq 2` | systems_substitution_generator.py |
| `SYS_SUBST_BACK` | 1 | `SYS_SUBST_BACK\|Substitute x=-1 into Eq 1` | systems_elimination_generator.py, systems_substitution_generator.py |
| `TABLEAU` | 2, 3 | `TABLEAU\|initial\|s1: x + s1 = 23\|s2: y + s2 = 19` | simplex_generator.py |
| `TABLEAU_RULE` | 3 | `TABLEAU_RULE\|3bar x 3bar\|two antiboxes split into symmetric plus antisymmetric\|6bar + 3` | young_tableaux_generator.py |
| `TABLE_ENTRY` | 2 | `TABLE_ENTRY\|f(-2)\|11` | euler_method_generator.py, function_table_generator.py, taylor_series_generator.py |
| `TABLE_LOOKUP` | 2 | `TABLE_LOOKUP\|f(4)\|-11` | de_moivre_generator.py, dot_product_generator.py, euler_formula_generator.py, function_evaluation_generator.py, lie_exponential_generator.py, normal_table_generator.py, pascal_triangle_generator.py, polar_parametric_generator.py, right_triangle_trig_generator.py, triangle_solve_generator.py, trig_equation_generator.py, trig_identity_eval_generator.py, unit_circle_generator.py |
| `TANGENT_PLANE` | 2 | `TANGENT_PLANE\|z = z0 + fx(x-a) + fy(y-b)\|z = 72 + 22*(x - 2) + 33*(y - 4)` | gradient_generator.py |
| `TARGET_STATE` | 2 | `TARGET_STATE\|J=1\|M=0` | clebsch_gordan_generator.py |
| `TAYLOR_FORMULA` | 1 | `TAYLOR_FORMULA\|P_n(x) = Σ f^(k)(a)/k!·(x - a)^k` | taylor_series_generator.py |
| `TAYLOR_SETUP` | 2 | `TAYLOR_SETUP\|f(x) = ln(x), center a = 1\|Taylor polynomial of degree 4` | taylor_series_generator.py |
| `TELESCOPE_CANCEL` | 2 | `TELESCOPE_CANCEL\|survive first and last\|1/25 - 1/124` | telescoping_generator.py |
| `TELE_SETUP` | 1 | `TELE_SETUP\|Σ k=25..123 (1/k - 1/(k+1))` | telescoping_generator.py |
| `TEMP_SCALE` | 2 | `TEMP_SCALE\|z1/T\|ln(5)` | softmax_gradient_generator.py |
| `TENSOR_ENTRY` | 2 | `TENSOR_ENTRY\|S_11\|1` | einstein_summation_generator.py, index_raising_generator.py |
| `TENSOR_RULE` | 1 | `TENSOR_RULE\|diag(a,b) tensor diag(c,d)=diag(ac,ad,bc,bd)` | tensor_product_generator.py |
| `TENSOR_SETUP` | 3 | `TENSOR_SETUP\|A=diag(3,2)\|B=diag(2,0)\|u=[0,3], v=[1,0]` | tensor_product_generator.py |
| `TENSOR_STATE` | 2 | `TENSOR_STATE\|u tensor v\|[0,0,3,0]` | tensor_product_generator.py |
| `TERM` | 2 | `TERM\|i=0: 1·(3/4)^0·(1/4)^5\|0.0009765625` | binomial_probability_generator.py |
| `TERMS` | 1 | `TERMS\|y[0..4]=[1,-6,36,-216,1296]` | z_transform_generator.py |
| `TEST_CHOOSE` | 2 | `TEST_CHOOSE\|geometric series\|common ratio r = 9/4` | power_series_generator.py, series_convergence_generator.py |
| `TEST_STAT_FORMULA` | 1 | `TEST_STAT_FORMULA\|t = (x̄ - μ0)/(s/√n)` | hypothesis_test_generator.py, two_sample_test_generator.py |
| `TF_SETUP` | 3 | `TF_SETUP\|ode\|y''+14y'+45y=4x'+20x\|zero initial conditions` | transfer_function_generator.py |
| `THEOREM` | 1, 2 | `THEOREM\|quadratic formula\|x = (-b ± √(b^2 - 4ac))/(2a)` | angle_defect_generator.py, circle_angle_generator.py, gauss_bonnet_generator.py, geometric_mean_generator.py, logistic_growth_generator.py, mean_value_theorem_generator.py, parametric_calculus_generator.py, polar_parametric_generator.py, quadratic_generator.py, rational_root_generator.py, remainder_factor_theorem_generator.py, series_convergence_generator.py, special_right_triangle_generator.py, spherical_excess_generator.py, taylor_series_generator.py, triangle_solve_generator.py, trig_identity_eval_generator.py, trig_six_functions_generator.py |
| `THEOREM_REWRITE` | 2 | `THEOREM_REWRITE\|circulation\|double integral of Q_x - P_y` | vector_theorem_generator.py |
| `THEOREM_SETUP` | 3 | `THEOREM_SETUP\|Green\|F=<0, 5*x>\|rectangle 4 by 7` | vector_theorem_generator.py |
| `THETA` | 2 | `THETA\|min(9,16)\|9` | transportation_generator.py |
| `THROUGHPUT` | 2 | `THROUGHPUT\|tokens_per_second\|1046875000/9` | scaling_law_generator.py |
| `TIME_COMPONENT` | 2 | `TIME_COMPONENT\|k=1\|1+i` | braket_generator.py |
| `TIME_DERIV` | 2 | `TIME_DERIV\|d/dt(m*L^2*thetadot)\|m*L^2*thetaddot` | lagrangian_generator.py |
| `TIME_EVOLVE` | 2 | `TIME_EVOLVE\|U psi\|[1+i,-1+i]` | braket_generator.py |
| `TM_CONFIG` | 4 | `TM_CONFIG\|step 0\|state=q0\|head=0\|tape=1` | turing_machine_trace_generator.py |
| `TM_HALT` | 2 | `TM_HALT\|step 2\|halted` | turing_machine_trace_generator.py |
| `TM_MOVE` | 3 | `TM_MOVE\|0\|R\|1` | turing_machine_trace_generator.py |
| `TM_READ` | 2 | `TM_READ\|head=0\|1` | turing_machine_trace_generator.py |
| `TM_RULE` | 2 | `TM_RULE\|q0,0\|q0,1,R` | turing_machine_trace_generator.py |
| `TM_SETUP` | 3 | `TM_SETUP\|binary_flip\|input=1\|limit=4` | turing_machine_trace_generator.py |
| `TM_WRITE` | 2 | `TM_WRITE\|head=0\|0` | turing_machine_trace_generator.py |
| `TOPO_AVAILABLE` | 1 | `TOPO_AVAILABLE\|A` | graph_traversal_generator.py |
| `TOPO_READY` | 1 | `TOPO_READY\|B` | graph_traversal_generator.py |
| `TOPO_SELECT` | 2 | `TOPO_SELECT\|A\|A` | graph_traversal_generator.py |
| `TOTIENT_RESULT` | 2 | `TOTIENT_RESULT\|phi(31)\|30` | totient_generator.py |
| `TRACE` | 2 | `TRACE\|3 + 2\|5` | ode_system_generator.py |
| `TRACE_ADD` | 4 | `TRACE_ADD\|gamma3gamma0\|(1,1)\|0 + 0\|0` | gamma_matrix_generator.py |
| `TRACE_ENTRY` | 2 | `TRACE_ENTRY\|(1,1)\|-12` | einstein_summation_generator.py, pauli_algebra_generator.py |
| `TRACE_EXPECT` | 1, 3 | `TRACE_EXPECT\|Tr(rho A)=p0*a+p1*b` | density_matrix_generator.py, gamma_matrix_generator.py |
| `TRACE_SUM` | 2 | `TRACE_SUM\|-12 - 12\|-24` | pauli_algebra_generator.py |
| `TRANSFER` | 1 | `TRANSFER\|H(s)=(4s+20)/(s^2+14s+45)` | transfer_function_generator.py |
| `TRANSFORM_APPLY` | 2 | `TRANSFORM_APPLY\|((-6), -(-1))\|(-6, 1)` | transformation_generator.py |
| `TRANSFORM_RULE` | 1 | `TRANSFORM_RULE\|(x, y) → (y, -x)` | transformation_generator.py |
| `TRANSFORM_SETUP` | 2, 3 | `TRANSFORM_SETUP\|P(-1, -6)\|rotation 270° counterclockwise about the origin` | rv_transform_generator.py, transformation_generator.py |
| `TRANSIENT_FORMULA` | 1 | `TRANSIENT_FORMULA\|tau=L/R` | transient_circuit_generator.py |
| `TRANSIENT_SETUP` | 3 | `TRANSIENT_SETUP\|rl_rise\|R=1, L=3\|V=48, t=12` | transient_circuit_generator.py |
| `TRANSITIVE_CHECK` | 3 | `TRANSITIVE_CHECK\|(2, 4) and (4, 1)\|need (2, 1)\|missing` | relation_check_generator.py |
| `TRANSPORT_SETUP` | 3 | `TRANSPORT_SETUP\|supply=(31,9)\|demand=(16,24)\|costs=(11,4;6,6)` | transportation_generator.py |
| `TRIG_RATIO` | 2 | `TRIG_RATIO\|sin\|opposite/hypotenuse` | right_triangle_trig_generator.py |
| `TRIG_SETUP` | 2 | `TRIG_SETUP\|right triangle, angle 24°, hypotenuse = 55; given sin 24° ≈ 0.4\|the opposite side` | right_triangle_trig_generator.py, trig_identity_eval_generator.py, trig_six_functions_generator.py, unit_circle_generator.py |
| `TRIG_VALUE` | 2, 3 | `TRIG_VALUE\|sin(lat1)=0\|sin(lat2)=sqrt(3)/2\|cos(dlon)=-1` | christoffel_generator.py, great_circle_generator.py, spherical_triangle_generator.py |
| `TRIPLE_EVAL` | 3 | `TRIPLE_EVAL\|rho_part * phi_part * angle\|2*125/3*2*2*pi\|1000/3*pi` | triple_integral_generator.py |
| `TRIPLE_SETUP` | 3 | `TRIPLE_SETUP\|integrand 2\|ball radius 5\|spherical` | triple_integral_generator.py |
| `TRI_ANGLE_SETUP` | 3 | `TRI_ANGLE_SETUP\|2x + 10\|x + 3\|x + 67` | angle_relationships_generator.py |
| `TRI_ANGLE_SOLVE` | 2 | `TRI_ANGLE_SOLVE\|4x + 80 = 180\|x = 25` | angle_relationships_generator.py |
| `TRI_ANGLE_SUM` | 1 | `TRI_ANGLE_SUM\|(2x + 10) + (x + 3) + (x + 67) = 180` | angle_relationships_generator.py |
| `TRI_AREA_FORMULA` | 1 | `TRI_AREA_FORMULA\|Area = (1/2)·a·b·sin C` | triangle_area_sas_generator.py |
| `TRI_SETUP` | 2 | `TRI_SETUP\|45-45-90 triangle, hypotenuse = 198\|leg` | special_right_triangle_generator.py, triangle_area_sas_generator.py, triangle_solve_generator.py |
| `TRUNCATE` | 2 | `TRUNCATE\|rank=1\|discard=14` | low_rank_approx_generator.py |
| `TRUTH_ROW` | 2 | `TRUTH_ROW\|V=0, W=0, X=0, Y=0\|F=1` | boolean_algebra_generator.py |
| `TRY` | 2, 3 | `TRY\|x = −45\|−46 < x ≤ −35 and (x is even and x is perfect square)\|false` | conditional_forms_generator.py, counterexample_search_generator.py, factor_trinomial_generator.py, log_conversion_generator.py, log_equation_generator.py, polynomial_inequality_generator.py, radical_equation_generator.py, rational_equation_generator.py, rational_root_generator.py, set_builder_roster_generator.py |
| `TS_FACTOR` | 3 | `TS_FACTOR\|p-1=72\|q=9\|s=3` | tonelli_shanks_generator.py |
| `TS_INIT` | 4 | `TS_INIT\|m=3\|c=10\|t=72\|r=18` | tonelli_shanks_generator.py |
| `TS_LOOP` | 2 | `TS_LOOP\|i=1\|b=27` | tonelli_shanks_generator.py |
| `TS_NONRESIDUE` | 1 | `TS_NONRESIDUE\|5` | tonelli_shanks_generator.py |
| `TS_SETUP` | 2 | `TS_SETUP\|a=41\|p=73` | tonelli_shanks_generator.py |
| `TWIDDLE` | 1, 3 | `TWIDDLE\|W2=-1` | dft_generator.py |
| `TWOS_SETUP` | 2 | `TWOS_SETUP\|8-bit two's complement\|offset = 2^8 = 256` | base_conversion_generator.py |
| `UC_GUESS` | 2 | `UC_GUESS\|exponential forcing\|y_p = Ae^x` | undetermined_coeff_generator.py |
| `UC_POINT` | 2 | `UC_POINT\|0°\|(1, 0)` | unit_circle_generator.py |
| `UNCERTAINTY_SETUP` | 3 | `UNCERTAINTY_SETUP\|particle in a box\|L=1, hbar=1\|n=101` | uncertainty_generator.py |
| `UNIFY_BIND` | 3 | `UNIFY_BIND\|X\|b\|{X=b}` | unification_generator.py |
| `UNIFY_DECOMPOSE` | 2 | `UNIFY_DECOMPOSE\|f\|2 arguments` | unification_generator.py |
| `UNIFY_FAIL` | 1 | `UNIFY_FAIL\|occurs-check X in f(X)` | unification_generator.py |
| `UNIFY_PAIR` | 2 | `UNIFY_PAIR\|X\|f(X)` | unification_generator.py |
| `UNIFY_SETUP` | 3 | `UNIFY_SETUP\|X\|f(X)\|occurs-check` | unification_generator.py |
| `UNIT_ATTACH` | 3 | `UNIT_ATTACH\|6\|m/s^2\|6 m/s^2` | cross_section_generator.py, kinematics_generator.py, physics_formula_generator.py |
| `UNIT_CONVERT` | 2 | `UNIT_CONVERT\|5 minutes\|300 seconds` | physics_formula_generator.py |
| `UNIT_NORMAL` | 2 | `UNIT_NORMAL\|T'(0)/norm T'(0)\|<-1, 0>` | curve_geometry_generator.py |
| `UNIT_RATE_DIV` | 3 | `UNIT_RATE_DIV\|100¢\|4\|25¢` | unit_rate_generator.py |
| `UNIT_RATE_PICK` | 2 | `UNIT_RATE_PICK\|1\|3` | unit_rate_generator.py |
| `UNIT_RATE_SETUP` | 3 | `UNIT_RATE_SETUP\|4\|pencils\|100¢` | unit_rate_generator.py |
| `UNIT_RATE_TABLE` | 2 | `UNIT_RATE_TABLE\|1,5,8\|3,15,24` | unit_rate_generator.py |
| `UNIT_RULE` | 3 | `UNIT_RULE\|c=1\|L=t\|eV^-1` | natural_units_generator.py |
| `UNIT_TANGENT` | 2 | `UNIT_TANGENT\|r'(0)/speed\|<0, 1>` | curve_geometry_generator.py |
| `UNLIKE_RADICALS` | 2 | `UNLIKE_RADICALS\|√3 ≠ √11\|unlike radicands — cannot combine` | radical_add_sub_generator.py |
| `UNPAIRED` | 2 | `UNPAIRED\|neither\|∅` | one_to_one_correspondence_generator.py |
| `UNROLL` | 2 | `UNROLL\|16, 27, 38, 49\|arithmetic, d = 11` | recursive_explicit_generator.py |
| `UPDATE` | 2 | `UPDATE\|W1_11\|0` | backprop_generator.py, kernel_perceptron_generator.py |
| `U_VECTOR` | 2 | `U_VECTOR\|u1 = A*v1/σ1\|[1/√2, 1/√2]` | svd_generator.py |
| `VA` | 1 | `VA\|x = 1` | rational_function_features_generator.py |
| `VALUE_FORMULA` | 1 | `VALUE_FORMULA\|v=(ad-bc)/(a-b-c+d)` | game_theory_generator.py |
| `VARIANCE` | 1, 2 | `VARIANCE\|Delta x^2\|1/12 - 1/(20402pi^2)` | layer_norm_generator.py, uncertainty_generator.py |
| `VAR_FORMULA` | 1 | `VAR_FORMULA\|Var(X) = Σ P(x)·(x - μ)^2` | expected_value_generator.py |
| `VAR_ROW` | 3 | `VAR_ROW\|3 - 4 = -1\|(-1)^2 = 1\|2/5·1 = 0.4` | expected_value_generator.py |
| `VECTOR_NORM` | 2 | `VECTOR_NORM\|A\|17` | embedding_similarity_generator.py |
| `VECTOR_SETUP` | 2 | `VECTOR_SETUP\|F(x,y) = <5*x - 4*y, x - 4*y>\|divergence and scalar curl` | div_curl_generator.py |
| `VEC_ENTRY` | 3 | `VEC_ENTRY\|(1)\|(-1215)*3 + 704\|-2941` | diagonalization_generator.py |
| `VEC_SETUP` | 2 | `VEC_SETUP\|v = ⟨-2, -2⟩\|magnitude` | dot_product_generator.py, vector_ops_generator.py |
| `VERIFY` | 2 | `VERIFY\|1\|ok` | error_spotting_generator.py |
| `VERTEX` | 1 | `VERTEX\|(0, -5)` | ellipse_features_generator.py, hyperbola_features_generator.py, lp_corner_generator.py, parabola_features_generator.py |
| `VERTEX_SOLVE` | 2 | `VERTEX_SOLVE\|x=0\|y=0` | lp_corner_generator.py |
| `VISIT` | 2 | `VISIT\|C\|C` | graph_traversal_generator.py |
| `VITERBI_BACKTRACE` | 2 | `VITERBI_BACKTRACE\|L->H->H\|27/512` | viterbi_generator.py |
| `VITERBI_CAND` | 3 | `VITERBI_CAND\|t=2,state=H\|from H\|9/128` | convolutional_code_viterbi_generator.py, viterbi_generator.py |
| `VITERBI_INIT` | 3 | `VITERBI_INIT\|H\|obs=B\|1/8` | viterbi_generator.py |
| `VITERBI_PICK` | 2, 3 | `VITERBI_PICK\|t=2,state=H\|from L\|3/32` | convolutional_code_viterbi_generator.py, viterbi_generator.py |
| `VOLUME` | 1 | `VOLUME\|200` | volume_rect_prism_generator.py |
| `VOLUME_SETUP` | 2 | `VOLUME_SETUP\|region between y = 570x (outer) and y = 570x^2 (inner) on [0, 1], about the x-axis\|washer method` | solid_revolution_generator.py |
| `VOL_BASE_AREA` | 2 | `VOL_BASE_AREA\|Base Area = (1/2) × 10 × 10\|50.0` | round_solids_generator.py, volume_3d_generator.py |
| `VOL_CALCULATE` | 2 | `VOL_CALCULATE\|V = 50.0 × 8\|400.0` | round_solids_generator.py, volume_3d_generator.py |
| `VOL_FORMULA` | 1 | `VOL_FORMULA\|V = Base Area × length` | round_solids_generator.py, solid_revolution_generator.py, volume_3d_generator.py |
| `VOL_SETUP` | 2 | `VOL_SETUP\|triangular_prism\|b=10, h_tri=10, length=8` | volume_3d_generator.py |
| `VOP_FORM` | 2 | `VOP_FORM\|u1' = -y2*g/W\|-192/8 * e^(6x)` | variation_parameters_generator.py |
| `WALK_ENTRY` | 2 | `WALK_ENTRY\|A^2[2,1]\|1` | graph_counting_generator.py |
| `WALK_GOAL` | 2 | `WALK_GOAL\|length 2\|2 to 1` | graph_counting_generator.py |
| `WALK_TERM` | 3 | `WALK_TERM\|via 1\|A[2,1]*A[1,1]\|0` | graph_counting_generator.py |
| `WAVE_FORMULA` | 1 | `WAVE_FORMULA\|1=N^2*integral_0^L (x/L)^(2k) dx` | wavefunction_generator.py |
| `WAVE_SETUP` | 3 | `WAVE_SETUP\|power_interval\|psi=N*(x/L)^1\|0<=x<=6` | wavefunction_generator.py |
| `WEEKDAY_SCAN` | 2, 3 | `WEEKDAY_SCAN\|extra day 1\|Thursday\|hit 0` | calendar_arithmetic_generator.py |
| `WEIGHT_VECTOR` | 2 | `WEIGHT_VECTOR\|w\|(-3,4)` | svm_margin_generator.py |
| `WIDTH_SETUP` | 3 | `WIDTH_SETUP\|lifetime\|hbar=17\|Gamma=28` | branching_ratio_generator.py |
| `WORK_DIFF` | 3 | `WORK_DIFF\|phi(end) - phi(start)\|13 - 94\|-81` | line_integral_generator.py |
| `WRONSKIAN` | 2 | `WRONSKIAN\|y1*y2' - y1'*y2\|8` | variation_parameters_generator.py |
| `XOR` | 3 | `XOR\|control=1\|target=1\|0` | quantum_gate_generator.py |
| `YOUNG_SETUP` | 3 | `YOUNG_SETUP\|partition=[3,2,1,1,1]\|n=8\|group=S_8` | young_tableaux_generator.py |
| `Z` | 1 | `Z\|63 R84` | abacus_addition_generator.py, absolute_value_equation_generator.py, absolute_value_inequality_generator.py, ac_circuit_generator.py, activation_generator.py, adam_step_generator.py, algorithm_trace_generator.py, angle_defect_generator.py, angle_measure_generator.py, angle_relationships_generator.py, annuity_generator.py, antiderivative_generator.py, arc_length_generator.py, arc_sector_generator.py, area_between_curves_generator.py, arithmetic_coding_generator.py, arithmetic_sequence_generator.py, attention_generator.py, attribute_sorting_generator.py, baby_step_giant_step_generator.py, backprop_generator.py, base_arithmetic_generator.py, base_conversion_generator.py, bayesian_update_generator.py, bch_generator.py, bec_channel_generator.py, binomial_probability_generator.py, bisection_generator.py, bitwise_ops_generator.py, black_scholes_generator.py, blackbody_generator.py, bond_pricing_generator.py, boolean_algebra_generator.py, braket_generator.py, branching_ratio_generator.py, calendar_arithmetic_generator.py, calorimetry_generator.py, casimir_force_generator.py, casimir_generator.py, cauchy_riemann_generator.py, cayley_table_generator.py, centroid_generator.py, chain_rule_generator.py, channel_capacity_generator.py, chi_square_generator.py, cholesky_generator.py, christoffel_generator.py, circle_angle_generator.py, circle_equation_generator.py, circle_generator.py, classifier_metrics_generator.py, clebsch_gordan_generator.py, collision_generator.py, commutator_generator.py, completing_square_generator.py, complex_division_generator.py, complex_locus_generator.py, complex_log_generator.py, complex_number_ops_generator.py, complex_quadratic_generator.py, composite_arithmetic_generator.py, compound_inequality_generator.py, compound_probability_generator.py, conditional_forms_generator.py, conditional_probability_generator.py, confidence_interval_generator.py, conic_standard_form_generator.py, conservation_law_generator.py, continued_fraction_generator.py, continuous_distribution_generator.py, contour_integral_generator.py, convolution_generator.py, convolutional_code_viterbi_generator.py, coset_generator.py, counterexample_search_generator.py, counting_classics_generator.py, cramers_rule_generator.py, crc_generator.py, cross_section_generator.py, crt_generator.py, curve_analysis_generator.py, curve_geometry_generator.py, cyclic_group_generator.py, cyk_parser_generator.py, de_moivre_generator.py, decimal_add_sub_generator.py, decimal_div_generator.py, decimal_mult_generator.py, definite_integral_generator.py, density_matrix_generator.py, derangement_generator.py, derivative_limit_def_generator.py, derivative_power_rule_generator.py, derivative_product_quotient_generator.py, derivative_transcendental_generator.py, determinant_generator.py, dfa_minimization_generator.py, dfa_simulation_generator.py, dft_generator.py, diagonalization_generator.py, diffie_hellman_generator.py, dijkstra_generator.py, dimensional_analysis_generator.py, discriminant_generator.py, distance_formula_generator.py, div_curl_generator.py, divisibility_classification_generator.py, domain_range_generator.py, doppler_generator.py, dot_product_generator.py, double_integral_generator.py, dp_table_generator.py, dpll_trace_generator.py, ecdh_generator.py, ecdsa_generator.py, eigenvalue_generator.py, einstein_summation_generator.py, electrostatics_generator.py, ellipse_features_generator.py, elliptic_curve_finite_field_generator.py, embedding_similarity_generator.py, energy_conservation_generator.py, entropy_change_generator.py, entropy_generator.py, entropy_rate_markov_generator.py, equation_from_two_points_generator.py, equilibrium_ice_generator.py, error_spotting_generator.py, euler_characteristic_generator.py, euler_circuit_generator.py, euler_formula_generator.py, euler_method_generator.py, evaluate_expression_generator.py, exact_ode_generator.py, expected_value_generator.py, exponent_generator.py, exponent_mixed_rules_generator.py, exponential_equation_generator.py, exponential_model_generator.py, extended_euclid_generator.py, factor_gcf_generator.py, factor_grouping_generator.py, factor_special_forms_generator.py, factor_trinomial_generator.py, factors_generator.py, feature_map_generator.py, fermi_estimation_generator.py, fill_in_step_generator.py, finance_generator.py, finite_difference_generator.py, finite_field_generator.py, first_law_generator.py, five_number_summary_generator.py, fixed_point_generator.py, flops_memory_generator.py, four_vector_generator.py, fourier_series_generator.py, fractal_iteration_generator.py, fraction_comparison_generator.py, fraction_decimal_percent_converter.py, fraction_op_generator.py, frequency_table_generator.py, function_composition_generator.py, function_evaluation_generator.py, function_inner_product_generator.py, function_operations_generator.py, function_table_generator.py, fundamental_form_generator.py, game_theory_generator.py, gamma_matrix_generator.py, gas_law_generator.py, gas_stoichiometry_generator.py, gauss_bonnet_generator.py, gauss_law_generator.py, gaussian_curvature_generator.py, gcf_generator.py, generating_function_generator.py, geometric_distribution_generator.py, geometric_mean_generator.py, geometric_probability_generator.py, geometric_sequence_generator.py, geometry_area_perimeter_generator.py, gradient_descent_generator.py, gradient_generator.py, gradient_step_generator.py, gram_schmidt_generator.py, graph_counting_generator.py, graph_interpret_generator.py, graph_traversal_generator.py, grassmann_generator.py, great_circle_generator.py, hamiltonian_generator.py, hamming_code_generator.py, hawking_generator.py, heat_engine_generator.py, hermitian_check_generator.py, hessian_classify_generator.py, horner_evaluation_generator.py, huffman_coding_generator.py, hydrogen_atom_generator.py, hyperbola_features_generator.py, hyperbolic_distance_generator.py, hyperbolic_function_generator.py, hypercube_counting_generator.py, hypothesis_test_generator.py, implicit_diff_generator.py, improper_integral_generator.py, inclusion_exclusion_generator.py, index_gymnastics_generator.py, index_raising_generator.py, induction_verify_generator.py, information_gain_generator.py, integer_operations_generator.py, integrating_factor_generator.py, integration_by_parts_generator.py, interference_generator.py, interpolation_generator.py, invariant_mass_generator.py, inverse_function_generator.py, jacobi_symbol_generator.py, jacobian_generator.py, joint_distribution_generator.py, kernel_evaluation_generator.py, kernel_perceptron_generator.py, kernel_ridge_generator.py, kernel_validity_generator.py, kinematics_generator.py, kl_divergence_generator.py, kmeans_step_generator.py, knights_knaves_generator.py, knn_generator.py, kraft_inequality_generator.py, ladder_operator_generator.py, lagrange_multiplier_generator.py, lagrangian_generator.py, lambda_reduction_generator.py, laplace_ivp_generator.py, laurent_series_generator.py, layer_norm_generator.py, lcm_generator.py, least_squares_generator.py, legendre_construction_generator.py, lhopital_generator.py, lie_exponential_generator.py, limit_evaluation_generator.py, line_integral_generator.py, linear_approx_generator.py, linear_complex_generator.py, linear_fractional_generator.py, linear_simple_generator.py, literal_equation_generator.py, lll_reduction_generator.py, log_conversion_generator.py, log_diff_higher_order_generator.py, log_equation_generator.py, log_properties_generator.py, logical_connective_eval_generator.py, logistic_growth_generator.py, long_division_generator.py, low_rank_approx_generator.py, lp_corner_generator.py, lr_schedule_generator.py, lu_decomposition_generator.py, lz_compression_generator.py, magnetism_generator.py, manual_square_root_generator.py, markov_chain_generator.py, master_theorem_generator.py, matrix_calculus_generator.py, matrix_exponential_generator.py, matrix_group_check_generator.py, matrix_inverse_generator.py, matrix_norm_generator.py, matrix_ops_generator.py, mean_value_theorem_generator.py, method_of_moments_generator.py, metric_arc_length_generator.py, mgf_generator.py, midpoint_generator.py, minkowski_interval_generator.py, mixed_number_operation_generator.py, mle_generator.py, mobius_transform_generator.py, mod_exp_generator.py, modular_arithmetic_generator.py, modular_inverse_generator.py, monomial_mult_div_generator.py, mst_generator.py, multi_digit_addition_generator.py, multi_digit_multiplication_generator.py, multi_digit_subtraction_generator.py, multi_step_unit_conversion_generator.py, multiplying_binomials_generator.py, multiplying_polynomials_generator.py, multivar_chain_rule_generator.py, mutual_information_generator.py, naive_bayes_generator.py, named_distribution_generator.py, natural_units_generator.py, nets_surface_area_generator.py, newton_raphson_generator.py, newtons_laws_generator.py, nfa_simulation_generator.py, normal_table_generator.py, npv_irr_generator.py, number_comparison_generator.py, ode_substitution_generator.py, ode_system_generator.py, one_step_equation_generator.py, one_step_inequality_generator.py, one_to_one_correspondence_generator.py, operation_properties_generator.py, optics_generator.py, optimization_generator.py, or_formula_generator.py, orbital_mechanics_generator.py, order_of_operations_generator.py, order_statistics_generator.py, parabola_features_generator.py, parallel_perpendicular_line_generator.py, param_count_generator.py, parametric_calculus_generator.py, partial_derivative_generator.py, partial_fractions_generator.py, partial_trace_generator.py, particle_in_box_generator.py, partition_function_generator.py, pascal_triangle_generator.py, pauli_algebra_generator.py, pca_generator.py, pda_simulation_generator.py, percent_problem_generator.py, percent_word_problem_generator.py, perceptron_generator.py, permutation_combination_generator.py, permutation_group_generator.py, perplexity_generator.py, ph_calculation_generator.py, physics_formula_generator.py, piecewise_evaluation_generator.py, place_value_rounding_generator.py, planck_units_generator.py, point_slope_generator.py, polar_parametric_generator.py, pollard_factorization_generator.py, polygon_perimeter_generator.py, polynomial_add_sub_generator.py, polynomial_div_monomial_generator.py, polynomial_inequality_generator.py, polynomial_long_division_generator.py, polynomial_zeros_generator.py, portfolio_generator.py, positional_encoding_generator.py, positive_definite_generator.py, power_series_generator.py, primality_test_generator.py, prime_factorization_generator.py, probability_addition_rule_generator.py, projectile_motion_generator.py, projector_generator.py, proportion_word_problem_generator.py, proportional_relationship_generator.py, pythag_hyp_generator.py, pythag_leg_generator.py, qr_decomposition_generator.py, quadratic_factoring_generator.py, quadratic_generator.py, quadratic_residue_generator.py, quadratic_square_root_generator.py, quantization_generator.py, quantum_formula_generator.py, quantum_gate_generator.py, quark_composition_generator.py, quaternion_generator.py, radical_add_sub_generator.py, radical_equation_generator.py, radical_multiply_generator.py, radical_rationalize_generator.py, radical_variable_simplify_generator.py, rate_conversion_generator.py, ratio_table_generator.py, rational_equation_generator.py, rational_exponent_generator.py, rational_expr_add_sub_generator.py, rational_expr_mult_div_generator.py, rational_expr_simplify_generator.py, rational_function_features_generator.py, rational_root_generator.py, recurrence_generator.py, recursive_explicit_generator.py, reed_solomon_generator.py, regex_to_automaton_generator.py, regression_generator.py, regular_polygon_area_generator.py, related_rates_generator.py, relation_check_generator.py, relativistic_energy_generator.py, remainder_factor_theorem_generator.py, repeating_decimal_generator.py, residue_generator.py, resolution_proof_generator.py, riemann_sum_generator.py, riemann_tensor_generator.py, right_triangle_trig_generator.py, rotational_dynamics_generator.py, round_solids_generator.py, routh_hurwitz_generator.py, row_reduction_generator.py, rsa_generator.py, runge_kutta_generator.py, running_coupling_generator.py, rv_transform_generator.py, scaling_generator.py, scaling_law_generator.py, schwarzschild_generator.py, second_order_ode_generator.py, segment_partition_generator.py, separable_ode_generator.py, separable_pde_generator.py, series_convergence_generator.py, series_solution_generator.py, set_builder_roster_generator.py, set_membership_subset_generator.py, set_operations_generator.py, shm_generator.py, sigma_notation_generator.py, signal_arithmetic_generator.py, similar_triangles_generator.py, simple_probability_generator.py, simple_stats_generator.py, simplex_generator.py, simplify_expression_generator.py, sinusoid_features_generator.py, slope_intercept_form_generator.py, slope_two_points_generator.py, softmax_gradient_generator.py, solid_revolution_generator.py, solution_chem_generator.py, special_relativity_generator.py, special_right_triangle_generator.py, special_solution_equation_generator.py, spherical_excess_generator.py, spherical_triangle_generator.py, spin_half_generator.py, stability_generator.py, standard_deviation_generator.py, standard_form_conversion_generator.py, standing_wave_generator.py, stars_and_bars_generator.py, statics_generator.py, statistics_generator.py, stereographic_generator.py, stoichiometry_generator.py, structure_constant_generator.py, subspace_basis_generator.py, svd_generator.py, svm_margin_generator.py, synthetic_division_generator.py, systems_elimination_generator.py, systems_substitution_generator.py, tangent_line_generator.py, taxicab_geometry_generator.py, taylor_series_generator.py, telescoping_generator.py, temperature_conversion_generator.py, tensor_product_generator.py, tip_bill_split_generator.py, tonelli_shanks_generator.py, totient_generator.py, transfer_function_generator.py, transformation_generator.py, transient_circuit_generator.py, transportation_generator.py, triangle_area_sas_generator.py, triangle_solve_generator.py, trig_equation_generator.py, trig_identity_eval_generator.py, trig_identity_verify_generator.py, trig_six_functions_generator.py, triple_integral_generator.py, turing_machine_trace_generator.py, two_sample_test_generator.py, two_step_equation_generator.py, two_step_inequality_generator.py, u_substitution_generator.py, uncertainty_generator.py, undetermined_coeff_generator.py, unification_generator.py, unit_circle_generator.py, unit_conversion_generator.py, unit_rate_generator.py, variation_parameters_generator.py, vector_ops_generator.py, vector_theorem_generator.py, venn_region_count_generator.py, viterbi_generator.py, volume_3d_generator.py, volume_rect_prism_generator.py, von_neumann_entropy_generator.py, wavefunction_generator.py, young_tableaux_generator.py, z_score_generator.py, z_transform_generator.py |
| `ZERO` | 1 | `ZERO\|s=-5` | transfer_function_generator.py |
| `ZERO_PRODUCT` | 2 | `ZERO_PRODUCT\|(x + 8)(x - 4)\|x = -8 or x = 4` | area_between_curves_generator.py, curve_analysis_generator.py, domain_range_generator.py, log_equation_generator.py, optimization_generator.py, polynomial_inequality_generator.py, polynomial_zeros_generator.py, quadratic_factoring_generator.py, radical_equation_generator.py, trig_equation_generator.py |
| `ZSCORE` | 2 | `ZSCORE\|(98 - 47)/20\|2.55` | normal_table_generator.py, z_score_generator.py |
| `ZSCORE_FORMULA` | 1 | `ZSCORE_FORMULA\|z = (x - μ)/σ` | z_score_generator.py |
| `ZT_PAIR` | 1 | `ZT_PAIR\|Z{r^n u[n]}=1/(1-r z^-1)` | z_transform_generator.py |
| `ZT_SETUP` | 2, 3 | `ZT_SETUP\|difference\|y[n]-(-6)y[n-1]=delta[n]\|y[-1]=0` | z_transform_generator.py |
