import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.StringTokenizer;

/**
 * Utility to read in text-based files for processing by other computational tools, line-by-line.
 * 
 * @author Mike Sao Pedro (mikesp@wpi.edu)
 *
 */
public class BufferedTextFileReader 
{
	private ArrayList<String> headers;
	private BufferedReader reader;
	private String delimiter;
	
	public BufferedTextFileReader(String filename, String delim)
	{
		headers = new ArrayList<String>();
		this.delimiter = delim;
		
		try
		{
		   reader = new BufferedReader(new FileReader(filename));
		   StringTokenizer st = new StringTokenizer(reader.readLine(), delimiter); //header
		   while(st.hasMoreElements()) { headers.add(st.nextToken()); } 
		}
		catch(Exception e)
		{
			e.printStackTrace();
		}
		
	}
	
	public ArrayList<String> getHeaders()
	{
		return this.headers;
	}
	
	public HashMap<String,String> readLine() throws IOException
	{
	    String line = reader.readLine();
	    if(line == null) return null;
	    
		HashMap<String, String> mapping = new HashMap<String, String>();
		StringTokenizer st = new StringTokenizer(line, delimiter);
		int ctr = 0;
		while(st.hasMoreElements())
		{
			mapping.put(headers.get(ctr), st.nextToken());
			ctr++;
		}
		
		return mapping;
	}
	
	public void close() throws IOException
	{
		reader.close();
	}

}
