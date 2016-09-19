import java.util.*;


/**
 * Computes A' per student and performs meta-analysis to get Z significance tests to
 * compare two models. This approach accounts for the fact that each observation may
 * not be independent (i.e. same students in dataset).
 * 
 * Generally, this class requires a tab-delimited input file with headers on the first line.
 * Minimally, the headers must include "student" and "right", where student is a unique student
 * identifier, and right is the ground-truth observation. You can add as many other columns
 * as you like.
 * 
 * This file should be sorted by student.
 * 
 * In addition, the class takes the name of two other columns to represent model predictions.
 * This class will compare the two models on how well they predict the "right" column using A'
 * and meta-analysis. 
 * 
 * 
 * If the order is not proper it will show NaN
 * 
 * RSB 16 Jan 2010 THIS CLASS WILL GIVE UNPREDICTABLE RESULTS IF YOU GIVE IT DATA
 * WITH THE LETTER E (FOR EXPONENTIAL) IN IT!
 * MAKE SURE INPUT IS FORMATTED AS NUMBER NOT SCIENTIFIC
 * 
 * @author Original author: Ryan S.J.d. Baker
 * @author Extensions made by Sujith Gowda and Michael Sao Pedro
 * 
 */
public class AprimeperstudentD 
{
	public static final String StudentHeaderName = "student";
	public static final String labelHeaderName = "right";

	private static final int NUMACTIONS = 200000; 
	private static final int MODELS = 2; 
	private static final int STUDENTS = 10000;
	

	double action_corrects[] = new double[NUMACTIONS];
	double model_lnminusone_values[][] = new double[MODELS][NUMACTIONS];

	int student_begins[] = new int[STUDENTS];
	int student_ends[] = new int[STUDENTS];
	String student_names[] = new String[STUDENTS];

	double aprimes[][] = new double[STUDENTS][MODELS];
	double SEs[][] = new double[STUDENTS][MODELS];
	double SIZEs[][] = new double[STUDENTS][MODELS];

	String model_names[] = new String[MODELS];

	int numrecords = -1;
	int numstudents = -1;

	
	/**
	 * if true, disqualify se for students with under 3 observations, or no tp or no fp
	 */
	boolean cautious_se = false;

	/**
	 * true is weighted Z (Whitlock, 2005); false is Stouffer's test
	 */
	boolean weighted_z = false;

//////////////////////////////////////////////////////////////////////////////
//////////////////////////////////////////////////////////////////////////////
//////////////////////////////////////////////////////////////////////////////
	
	public AprimeperstudentD() 
	{
	}
	
	public AprimeperstudentD(boolean cautious, boolean weighted)
	{
		cautious_se = cautious;
		weighted_z = weighted;
	}

//////////////////////////////////////////////////////////////////////////////
//////////////////////////////////////////////////////////////////////////////
//////////////////////////////////////////////////////////////////////////////

	public void a_prime_general(String file, String extinput1, String extinput2) throws Exception
	{
		model_names[0] = extinput1;
		model_names[1] = extinput2;
		input_student_records(file, extinput1, extinput2);
		a_prime_driver_labeled(extinput1, extinput2);
	}

	/**
	 * Compute the A' values, SE's etc. and report out the Z-test comparison between the
	 * two models, named set1 & set2. Assumes that all arrays from input data have been
	 * read in.
	 */
	public void a_prime_driver_labeled(String set1, String set2) 
	{
		for (int i = 0; i < MODELS; i++) 
		{
			a_prime(action_corrects, model_lnminusone_values[i], model_names[i], i);
		}
		
		Z_TEST(set1, set2);
	}

	public String lookup_p(double Z) {
		double abs_z = java.lang.Math.abs(Z);
		if (abs_z > 3.3)
			return "<0.001";
		if (abs_z > 2.58)
			return "<0.01";
		if (abs_z > 2.44)
			return "0.01";
		if (abs_z > 2.25)
			return "0.02";
		if (abs_z > 2.11)
			return "0.03";
		if (abs_z > 2.01)
			return "0.04";
		if (abs_z > 1.92)
			return "0.05";
		if (abs_z > 1.85)
			return "0.06";
		if (abs_z > 1.78)
			return "0.07";
		if (abs_z > 1.72)
			return "0.08";
		if (abs_z > 1.67)
			return "0.09";
		if (abs_z > 1.62)
			return "0.10";
		if (abs_z > 1.57)
			return "0.11";
		if (abs_z > 1.53)
			return "0.12";
		return ">0.12";
	}

	/**
	 * @param Aprime
	 * @param SEAprime
	 * @return Z score
	 */
	private double getZComparisonFromChance(double Aprime, double SEAprime)
	{
		return (Aprime - 0.5) / SEAprime;
	}
	
	/**
	 * Write out results of Z-test and show the results for each A' student test.
	 * Won't write out data for a student if A' is invalid for EITHER model.
	 * 
	 * Also computes if each model differs from chance (A' = .5), ignoring cases where SE(A') is zero
	 * 
	 * @param set1
	 * @param set2
	 */
	public void Z_TEST(String set1, String set2) 
	{
		System.out.println("StuLocalID\tStuName\t" + set1 + "\t" + set2 + "\tm1_chance_Z\tm1_chance_p\tm2_chance_Z\t2_chance_p\tdiff_Z\tdiff_p");

		double aggregate_btwnmodels_Z = 0;
		double aggregate_model1chance_Z = 0;
		double aggregate_model2chance_Z = 0;		
		double difference_count = 0;
		double model1_chance_count = 0;
		double model2_chance_count = 0;
		double aprimes_1 = 0;
		double aprimes_2 = 0;
		double total_df = 0;
		for (int stu = 0; stu < numstudents; stu++) {
			if ((aprimes[stu][0] > -1) && (aprimes[stu][1] > -1) && SEs[stu][0] > -1 && SEs[stu][1] > -1) {
				System.out.print(stu);
				System.out.print("\t");
				System.out.print(student_names[stu]);
				System.out.print("\t");
				System.out.format("%.4f", aprimes[stu][0]);
				aprimes_1 = aprimes_1 + aprimes[stu][0];
				System.out.print(" (");
				System.out.format("%.4f", SEs[stu][0]);
				System.out.print(")\t");
				System.out.format("%.4f", aprimes[stu][1]);
				aprimes_2 = aprimes_2 + aprimes[stu][1];
				System.out.print(" (");
				System.out.format("%.4f", SEs[stu][1]);
				System.out.print(")\t");
				
				// --- Model 1 difference from chance
				if(Math.abs(SEs[stu][0]) > .00001)
				{
					model1_chance_count++;
					double Z = getZComparisonFromChance(aprimes[stu][0], SEs[stu][0]);
					aggregate_model1chance_Z += Z;
					System.out.format("%.4f\t%s\t", Z, lookup_p(Z));
				}
				else
				{
					System.out.print("---\t---\t");
				}
								
				// --- Model 2 difference from chance
				if(Math.abs(SEs[stu][1]) > .00001)
				{
					model2_chance_count++;
					double Z = getZComparisonFromChance(aprimes[stu][1], SEs[stu][1]);
					aggregate_model2chance_Z += Z;
					System.out.format("%.4f\t%s\t", Z, lookup_p(Z));
				}
				else
				{
					System.out.print("---\t---\t");					
				}
				
				// --- Comparison of both models
				double Z = (aprimes[stu][1] - aprimes[stu][0]);
				double denom = java.lang.Math.sqrt(SEs[stu][0] * SEs[stu][0]+ SEs[stu][1] * SEs[stu][1]);
				if(Math.abs(denom) < .00001 && Math.abs(Z) < .00001) // set Z to be zero if the numerator and denom are both zero (prevents NaN) 
				{
					Z = 0.0;
				}
				else
				{
					Z /= denom; // do the z calculation as normal
				}
						 
				System.out.format("%.4f\t%s\n", Z, lookup_p(Z));
				
				if (weighted_z) {
					aggregate_btwnmodels_Z = aggregate_btwnmodels_Z + Z * (SIZEs[stu][0] - 2);
					total_df = total_df
							+ ((SIZEs[stu][0] - 2) * (SIZEs[stu][0] - 2));
				} 
				else
				{
					aggregate_btwnmodels_Z = aggregate_btwnmodels_Z + Z;
				}
				difference_count++;
			}
		}

		double avg_1 = aprimes_1 / difference_count;
		double avg_2 = aprimes_2 / difference_count;
		double StoufferZdiff_model1_chance = aggregate_model1chance_Z / Math.sqrt(model1_chance_count);
		double StoufferZdiff_model2_chance = aggregate_model2chance_Z / Math.sqrt(model2_chance_count);

		System.out.println();
		System.out.println();

		System.out.println("Average A prime (" + set1 + ") = " + avg_1 + "  Differs from chance: Z=" + StoufferZdiff_model1_chance + " p: " + lookup_p(StoufferZdiff_model1_chance) + " n=" + model1_chance_count);
		System.out.println("Average A prime (" + set2 + ") = " + avg_2 + "  Differs from chance: Z=" + StoufferZdiff_model2_chance + " p: " + lookup_p(StoufferZdiff_model2_chance) + " n=" + model2_chance_count);

		System.out.print("\nMeta Z Difference between models");
		if (weighted_z)
			System.out.print(" (Weighted Z)= ");
		else
			System.out.print(" (Stouffer's method Z)= ");

		double metaz = 0.0;

		if (weighted_z)
			metaz = aggregate_btwnmodels_Z / java.lang.Math.sqrt(total_df);
		else
			metaz = aggregate_btwnmodels_Z / java.lang.Math.sqrt(difference_count); // Stouffer's Z
		System.out.println(metaz + " p: " + lookup_p(metaz) + " n=" + difference_count);
	}
	
	/**
	 * Compute Hanley & McNeill (1982) A'
	 * 
	 * Note: if there is not at least one "zeroPrediction" and at least one "onePrediction", then A' is undefined.
	 */	
	public double getSimpleAprime(ArrayList<Double> zeroPredictions, ArrayList<Double> onePredictions) 
	{
		double correct = 0;
		long count = 0;
		for (double zeroP : zeroPredictions) {
			for (double oneP : onePredictions) {
				if (zeroP < oneP)
					correct += 1;
				else if (Math.abs(zeroP - oneP) < .0001)
					correct += 0.5;
				count++;
			}
		}
		
		double aprime = correct / count;
		return aprime;
	}

	/**
	 * Compute A', SE(A'), size = true pos + false pos
	 * per student for a given model, indexed by modelidx.
	 * 
	 * Fills in A' and SE of -1 if certain conditions aren't met. This indicates to
	 * the Z_TEST function to not use those values when doing the meta analytical A' and
	 * Z test.
	 */
	public double a_prime(double actual[], double predicts[],
			String population, int modelidx) {

		for (int stu = 0; stu < student_ends.length; stu++) {

			int total_tp = 0;
			int total_fp = 0;
			
			ArrayList<Double> zeroPredictions = new ArrayList<Double>();
			ArrayList<Double> onePredictions = new ArrayList<Double>();


			for (int i = student_begins[stu]; i <= student_ends[stu]; i++) 
			{
				if(i >= numrecords)
				{
					System.err.println("INVALID NUMBER OF RECORDS FOR MODEL " + population);
					System.err.println("Trying to access record " + i + " when there are only " + numrecords + " read in.");
				}

				if (actual[i] > 0)
					total_tp += 1;
				else if (actual[i] != -1)
					total_fp += 1;
			
				if (Math.abs(actual[i]) < .00001){
					zeroPredictions.add(predicts[i]);
				}else{
					onePredictions.add(predicts[i]);
				}
			}
			
			double segarea = getSimpleAprime(zeroPredictions, onePredictions);

			if (standard_error(segarea, total_tp, total_fp) > -1) 
			{
				aprimes[stu][modelidx] = segarea;
				SEs[stu][modelidx] = standard_error(segarea, total_tp, total_fp);
				SIZEs[stu][modelidx] = total_tp + total_fp;
			} 
			else
			{
				aprimes[stu][modelidx] = -1;
				SEs[stu][modelidx] = -1;
			}

			if (stu == 1)
				System.out.println();

			
			  //System.out.print(population); System.out.print("\t");
			  //System.out.print(student_names[stu]); System.out.print("\t");
			  //System.out.print(segarea); System.out.print("\t");
			  //System.out.println(total_tp + "\t" + total_fp + "\t" + standard_error(segarea,total_tp,total_fp));
			 

			if ((segarea > 1) || (segarea < 0)) {
				System.err.println("INVALID A-PRIME VALUE OBTAINED!");
				System.err.println(segarea);
				System.err.println(stu);
				System.err.println(total_tp);
				System.err.println(total_fp);
			}

		}
		return -1;
	}

	public double standard_error(double aprime, int total_tp, int total_fp) {
		if (total_tp + total_fp < 2)
			return -1.0;
		if ((total_tp == 0) || (total_fp == 0) || (total_fp + total_tp < 3)
				|| (aprime == 0))
			if (cautious_se)
				return -1.0; // not enough data here to validly calculate
			else
				return 0.0;

		double aoneminusa = aprime * (1 - aprime);
		double naminus1 = total_tp - 1;
		double q1 = aprime / (2 - aprime);
		double a2 = aprime * aprime;
		double q1minusa2 = q1 - a2;
		double natimes = naminus1 * q1minusa2;
		double nnminus1 = total_fp - 1;
		double q2 = (2 * a2) / (1 + aprime);
		double q2minusa2 = q2 - a2;
		double nntimes = nnminus1 * q2minusa2;
		double top = aoneminusa + natimes + nntimes;
		//System.out.println("AoneminusA: " + aoneminusa + "  Natimes: " + natimes + "  NNtimes: " + nntimes + "  Top: " + top);
		double nann = total_tp*total_fp; // MikeSP 11/27/12 Fixed from naminus1*nnminus1 since that's not the formula in Hanley & McNeill
		if (nann == 0.0)
			if (cautious_se)
				return -1.0; // not enough data here to validly calculate
			else
				return 0.0;
		double inside = top / nann;
		double se = java.lang.Math.sqrt(inside);

		return se;
	}

	/**
	 * Current assumption: You can only compare two models. The code was like this before
	 * MikeSP's mods, actually.
	 * 
	 */
	public void input_student_records(String file, String model1, String model2) throws Exception
	{
		BufferedTextFileReader reader = new BufferedTextFileReader(file, "\t");
		HashMap<String,String> line = null;
		
		int linenum = 0;
		int studentidx = 0;
		String student = null;
		String curstudent = "";
		
		while( (line = reader.readLine()) != null)
		{
			student = line.get(StudentHeaderName);
			
			// --- If name of student switches, cut off the index for previous student, and mark where
			//     new student actions begin.
			if (!curstudent.equals(student)) 
			{
				curstudent = student;
				student_begins[studentidx] = linenum;
				student_names[studentidx] = curstudent;
				if (studentidx > 0)
				{
					student_ends[studentidx - 1] = linenum - 1;
				}
				
				studentidx++;
			}
			
			action_corrects[linenum] = Integer.parseInt(line.get(labelHeaderName));
			model_lnminusone_values[0][linenum] = Double.parseDouble(line.get(model1));
			model_lnminusone_values[1][linenum] = Double.parseDouble(line.get(model2));
			
			linenum++;
		}

		student_ends[studentidx - 1] = linenum - 1; // last element in lnminusone_values arrays

		numstudents = studentidx;
		numrecords = linenum;
		System.err.println("Num records: " + numrecords);
		System.err.println("Num students: " + numstudents);
	}

//////////////////////////////////////////////////////////////////////////////
//////////////////////////////////////////////////////////////////////////////
//////////////////////////////////////////////////////////////////////////////
	
	public static void main(String args[]) throws Exception 
	{
		AprimeperstudentD h = new AprimeperstudentD();

    	if (args.length<3)
    	{
			System.err.println("Usage: inputfile model1 model2");
			System.err.println("inputfile: data generated from Proto.java");
			System.err.println("model1/model2: column headers in inputfile (e.g. bounded) representing a prediction made by a named BKT model.");
			return;

    	}

    	h.a_prime_general(args[0], args[1], args[2]);
	}

}
