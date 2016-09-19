import java.util.ArrayList;
import java.util.HashMap;
import java.util.Map;

/**
 * Generic code for computing Hanley & McNeill (1982) A'.
 * 
 * @author Sujith Gowda, revised by Michael Sao Pedro
 */
public class SimpleAPrime 
{
	public static final String APRIME = "APRIME";
	public static final String TRUE_POSITIVES = "TP";
	public static final String FALSE_POSITIVES = "FP";
	
	/**
	 * Compute A' from a file given as input
	 * 
	 */
	public Map<String,Double> computeAPrimeFromFile(String file, String delim, String labelcol, String predictcol) throws Exception
	{
		BufferedTextFileReader reader = new BufferedTextFileReader(file, delim);
		HashMap<String,String> line = null;
		ArrayList<HashMap<String,String>> data = new ArrayList<HashMap<String,String>>();

		while( (line = reader.readLine()) != null)
		{
			data.add(line);
		}
		
		if(!reader.getHeaders().contains(labelcol))
		{
			System.err.println("Data file does not contain label column named: " + labelcol);
			System.err.println("These columns were read in: " + reader.getHeaders().toString());
			System.exit(1);
		}
		if(!reader.getHeaders().contains(predictcol))
		{
			System.err.println("Data file does not contain label column named: " + predictcol);
			System.err.println("These columns were read in: " + reader.getHeaders().toString());
			System.exit(1);
		}
		
		return computeAPrime(data, labelcol, predictcol);
	}
	
	
	public Map<String,Double> computeAPrime(ArrayList<HashMap<String,String>> data, String labelcol, String predictcol)
	{
		ArrayList<Double> zeroPredictions = new ArrayList<Double>();
		ArrayList<Double> onePredictions = new ArrayList<Double>();
		
		for(HashMap<String,String> line : data)
		{
		  int label;
		  String labelstr = line.get(labelcol);		  
		  
		  if(labelstr.equals("\"Y\""))
		  {
			  label = 1;
		  }
		  else if(labelstr.equals("\"N\""))
		  {
			  label = 0;
		  }
		  else
		  {
		    label = Integer.parseInt(labelstr);
		  }
		  
		  double prediction = Double.parseDouble(line.get(predictcol));
		
		  if(label == 1)
		  {
			  onePredictions.add(prediction);
		  }
		  else
		  {
			  zeroPredictions.add(prediction);
		  }
		}
		
		return computeAPrime(zeroPredictions, onePredictions);
	}
	
	
	/**
	 * Compute A'
	 * 
	 */
	public Map<String,Double> computeAPrime(ArrayList<Double> zeroPredictions, ArrayList<Double> onePredictions)
	{
		double correct = 0;
		long count = 0;
		for(double zeroP : zeroPredictions)
		{
			for(double oneP : onePredictions)
			{
				if(zeroP < oneP)
					correct += 1;
				else if( Math.abs(zeroP - oneP) < .0001 )
					correct += 0.5;
				count++;
			}
		}
		
		HashMap<String, Double> results = new HashMap<String, Double>();
		results.put(APRIME, correct / count);
		results.put(TRUE_POSITIVES, correct);
		results.put(FALSE_POSITIVES, count - correct);
		
		return results;
	}
	
//////////////////////////////////////////////////////////////////////////////
//////////////////////////////////////////////////////////////////////////////
//////////////////////////////////////////////////////////////////////////////
	
	public static void main(String[] args) 
	{		
		SimpleAPrime computer = new SimpleAPrime();
		
		if(args.length < 4)
		{
			System.err.println("Usage: java SimpleAPrime filename delimiter labelcolumnname predictcolumnname");
			System.err.println("- filename has first row as column labels, all other rows data. It is delimited by the 'delimiter' given as input to the program.");
			System.err.println("- delimiter should be wrapped in quotes. For csv, do \",\". For tab, do \"\t\". For tab, don't use the \\t, hit the actual tab key.");
			System.err.println("- labelcolumnname contains the binary true values trying to be predicted. Use 0 or \"N\" for false, and 1 or \"Y\" for true. Note the \" must be present for \"Y\"/\"N\"!");
			System.err.println("- predictcolumnname contains numerical values which reflect predictions of the binary labelcolumnname");
			System.err.println("\nExample with rapidminer output:");
			System.err.println("java SimpleAPrime mycsvfile.csv \",\" \"NuCode\" \"confidence(Y)\"");
			System.err.println("  - For rapidminer, columnames contain quotes, so the quotes must be used here as well.");
			System.err.println("\nExample with BKT output in tab-delim:");
			System.err.println("java SimpleAPrime mytabdelimBKTfile.txt \"\t\" right pobsmodel");
			System.exit(1);
		}
		
		try
		{
		  Map<String,Double> results = computer.computeAPrimeFromFile(args[0], args[1], args[2], args[3]);
		  System.out.println("A' = " + results.get(APRIME));
		  System.out.println("True Positives = " + results.get(TRUE_POSITIVES));
		  System.out.println("False Positives = " + results.get(FALSE_POSITIVES));		  
		}
		catch(Exception e)
		{
			System.err.println("Exception:");
			System.err.println(e.getMessage());
			e.printStackTrace();
		}
	}

}
