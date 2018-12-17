/*
 * 		Author: Charan Kumar Yellanki
 * 		Description: This program takes space separated clingo program as input and 
 * 			returns minimized clingo program as output by applying syntactic minimization rules.
 * 		Input: A text file containing clingo program
 * 		Output: A minimized clingo program 
 *
 */
import java.io.File;
import java.io.IOException;
import java.util.ArrayList;
import java.util.HashSet;
import java.util.Hashtable;
import java.util.Iterator;
import java.util.List;
import java.util.Map;
import java.util.Scanner;
import java.util.Set;
import java.util.Arrays;
import java.util.Collections;
import java.io.BufferedWriter;
import java.io.FileWriter; 

// The object of this class stores head and body of each clause
class Rule_hashset{
	HashSet<Integer> head=new HashSet<Integer>();
	HashSet<Integer> positive_head=new HashSet<Integer>();
	HashSet<Integer> negative_head=new HashSet<Integer>();
	HashSet<Integer> body=new HashSet<Integer>();
	HashSet<Integer> pos_body=new HashSet<Integer>();
	HashSet<Integer> neg_body=new HashSet<Integer>();
}
public class SimplifyProgramInput_2 {

	// Method to minimize the given clingo program
	public static void main(String args[]) throws IOException{

		String inputFile = args[0];
		String outputFile = args[1];

		// File fileDescriptor = new File("meow_ch.lp");
		File fileDescriptor = new File(inputFile);
		@SuppressWarnings("resource")
		Scanner scanNumLines = new Scanner(fileDescriptor);
		int rows = 0, columns = 0;
		
		//code for calculating number of rows in a table
		while(scanNumLines.hasNextLine()){
			rows++;
			scanNumLines.nextLine();
		
		}
		
		// Code for calculating number of columns in a table
		@SuppressWarnings("resource")
		Scanner scanLine = new Scanner(fileDescriptor);
		int count=0;
		while(scanLine.hasNextLine()) {
			String one_row = scanLine.nextLine();
			for(@SuppressWarnings("unused") String index: one_row.split(" ")){
				count++;
			}
			if(columns<count) {
				columns=count;
			}
			count=0;

		}
		
		System.out.println("rows: "+ rows + " columns: "+ columns);
		
		// Reading input from file (Input is in tabular format)
		@SuppressWarnings("resource")
		Scanner eachLine = new Scanner(fileDescriptor);
		String body_table[][] = new String[rows][columns-1];
		String head_table[][] = new String[rows][columns-1];
		int r=0, c=0;
		boolean head_flag=true;
		while(eachLine.hasNextLine()){
			String line = eachLine.nextLine();
			for(String value : line.split(" ")){
				if(!value.equals(":-")){
					if(head_flag) {
						head_table[r][c++] = value;
					}
					else {
						body_table[r][c++] = value;
					}
				}
				else {
					c=0;
					head_flag=false;
				}
			}
			head_flag=true;
			r++;
			c=0;
			
		}
		// Printing the given input to console
		System.out.println("\nGiven Input:");
		for(int i=0; i<rows; i++){
			head_table[i]=Arrays.stream(head_table[i]).filter(s -> (s != null && s.length() > 0)).toArray(String[]::new);
			for(int j=0; j<head_table[i].length; j++) {
				System.out.print(head_table[i][j]+" ");
			}
			body_table[i]=Arrays.stream(body_table[i]).filter(s -> (s != null && s.length() > 0)).toArray(String[]::new);
			System.out.print(":- ");
			for(int j=0; j<body_table[i].length; j++){
				System.out.print(body_table[i][j]+" ");
			}
			System.out.println();
		}
		
		// For each row(clause) head and body is initialized
		Rule_hashset rule[] = new Rule_hashset[rows];
		for(int i=0; i< rows; i++){
			rule[i] = new Rule_hashset();
		}
		
		int key;
		int max = 1;
		String str;
		Hashtable<Integer, String> ht = new Hashtable<Integer, String>();
		
		// Initializing body and head sets using hashtable
		for(int i=0; i< rows; i++){
			for(int j=0; j<body_table[i].length; j++){
				//System.out.println(body_table[i][j]);
				if(body_table[i][j] != null && (body_table[i][j].contains("+") || body_table[i][j].contains("-"))){
					str=body_table[i][j].substring(1);
				}
				else{
					str =body_table[i][j];
				}
				if(ht.containsValue(str)){				// checking whether a literal is in hashtable or not
			        for(Map.Entry entry: ht.entrySet()){
			            if(str.equals(entry.getValue())){
			                key = (int) entry.getKey();
			                if(body_table[i][j].contains("-")){
			                	key=-key;
			                	rule[i].body.add(key);
			                	rule[i].neg_body.add(-key);		//adding negative literals to negative body
			                }
			                else{
			                	rule[i].body.add(key);
			                	rule[i].pos_body.add(key);		// adding positive literals to positive body
			                }
			                
			                break; //breaking because its one to one map
			            }
			        }
				}
				// if literal is not present in hashtable, then adding it to hashtable
			    else{
			    	if(body_table[i][j].contains("+") || body_table[i][j].contains("-")){
			    		ht.put(max, body_table[i][j].substring(1));
			    		if(body_table[i][j].contains("-")){
			    			rule[i].body.add(-max);
			    			rule[i].neg_body.add(max);
			    		}
			    		else{
			    			rule[i].body.add(max);
			    			rule[i].pos_body.add(max);
			    		}
			    	}
			    	else{
			    		ht.put(max, body_table[i][j]);
			    		rule[i].body.add(max);
			    		rule[i].pos_body.add(max);
			    		
			    	}
			    	
			        max++;
			    }
			
			}
		}
		// Initializing head hashsets using hashtable
		for(int i=0; i<rows; i++){
			for(int j=0; j<head_table[i].length; j++) {
				if(head_table[i][j].contains("+") || head_table[i][j].contains("-")){
					str=head_table[i][j].substring(1);
				}
				else{
					str =head_table[i][j];
				}
				
				if(ht.containsValue(str)){
			        for(Map.Entry entry: ht.entrySet()){
			            if(str.equals(entry.getValue())){
			                key = (int) entry.getKey();
			                if(head_table[i][j].contains("-")){
			                	key=-key;
			                	rule[i].head.add(key);
			                	rule[i].negative_head.add(key);
			                }
			                else{
			                	rule[i].head.add(key);
			                	rule[i].positive_head.add(key);
			                }
			                
			                break; //breaking because its one to one map
			            }
			        }
				}
				// if literal is not present in hashtable, then adding it to hashtable
			    else{
			    	if(head_table[i][j].contains("+") || head_table[i][j].contains("-")){
			    		ht.put(max, head_table[i][j].substring(1));
			    		if(head_table[i][j].contains("-")){
			    			rule[i].head.add(-max);
			    			rule[i].negative_head.add(max);
			    		}
			    		else{
			    			rule[i].head.add(max);
			    			rule[i].positive_head.add(max);
			    		}
			    	}
			    	else{
			    		ht.put(max, head_table[i][j]);
			    		rule[i].head.add(max);
			    		rule[i].positive_head.add(max);
			    		
			    	}
			        
			        max++;
			    }
			}
		
		}
			
		/*	
		for(int i=0; i < rows-1; i++){
			
			for(int j=0; j<columns-1; j++){
				System.out .print(rule[i].body[j] + " ");
			}
			System.out.println();
		}*/
		System.out.println("\nProgram in Literals: ");
		for(int i=0; i<rows; i++){
			System.out.println("row "+ i);
			for(Integer value:rule[i].head){
				System.out.print(value+ " ");
			}
			System.out.print(" :- ");
			for(Integer value:rule[i].pos_body){
				System.out.print(value+ " ");
			}
			for(Integer value:rule[i].neg_body){
				System.out.print("-"+value+ " ");
			}
			System.out.println();
		}
		
		HashSet<Integer> ruleNumbers=new HashSet<Integer>();
		for(int i=0; i<rows; i++){
			ruleNumbers.add(i);
		}
		
		//call to tautology
		tautology(ruleNumbers,rule,rows);
		
		System.out.println("\nAfter Implementing tautology:");
		printProgramInNumerals(ruleNumbers, rule);
		
		//call to RED+
		// reducePositive(ruleNumbers, rule);
		
		// System.out.println("\nAfter applying red+:");
		// printProgramInNumerals(ruleNumbers, rule);
		
		//call to RED-
		reduceNegative(ruleNumbers, rule);
		
		System.out.println("\nAfter applying RED-:");
		printProgramInNumerals(ruleNumbers, rule);
		
		//call to NON_MIN
		nonMin(ruleNumbers, rule);
		
		System.out.println("\nAfter applying NONMIN:");
		printProgramInNumerals(ruleNumbers, rule);

		
		//call GPPE
		// gppe(ruleNumbers, rule, rows);
		
		// System.out.println("\nAfter applying all GPPE:");
		// printProgramInNumerals(ruleNumbers, rule);
		
		//call to CONTRA
		contra(ruleNumbers, rule);
		
		System.out.println("\nAfter applying CONTRA:");
		printProgramInNumerals(ruleNumbers, rule);
		
		//call to S-IMP
		sImp(ruleNumbers, rule);
		
		System.out.println("\nAfter applying S-IMP:");
		printProgramInNumerals(ruleNumbers, rule);
		
		//call to LSH
		LSH(ruleNumbers, rule);
		
		System.out.println("\nAfter applying LSH:");
		printProgramInNumerals(ruleNumbers, rule);
		
		System.out.println("\n\n*********  Final program is: ********\n\n");
		String result = printProgramInTerms(ruleNumbers, rule, ht);

		w.write("Writing final file");

		BufferedWriter writer = new BufferedWriter(new FileWriter(outputFile));
	    writer.write(result);
	    writer.close();

	}//End of main 
	
	public static Set<Set<Integer>> powerSet(Set<Integer> originalSet) {
        Set<Set<Integer>> sets = new HashSet<Set<Integer>>();
        if (originalSet.isEmpty()) {
            sets.add(new HashSet<Integer>());
            return sets;
        }
        List<Integer> list = new ArrayList<Integer>(originalSet);
        Integer head = list.get(0);
        Set<Integer> rest = new HashSet<Integer>(list.subList(1, list.size()));
        for (Set<Integer> set : powerSet(rest)) {
            Set<Integer> newSet = new HashSet<Integer>();
            newSet.add(head);
            newSet.addAll(set);
            sets.add(newSet);
            sets.add(set);
        }
        return sets;
    }//End of powerSet
	// Description: This method prints the program in numbers format
	public static void printProgramInNumerals(HashSet<Integer> ruleNumbers, Rule_hashset rule[]) {
		for(Integer i: ruleNumbers){
			System.out.println("row "+ (i+1));
			for(Integer value:rule[i].head){
				System.out.print(value+ " ");
			}
			System.out.print(" :- ");
			for(Integer value:rule[i].pos_body){
				System.out.print(value+ " ");
			}
			for(Integer value:rule[i].neg_body){
				System.out.print("-"+value+ " ");
			}
			System.out.println();
		}
	}// End if printProgramInNumerals
	
	// Description: This method prints the actual program
	public static String printProgramInTerms(HashSet<Integer> ruleNumbers, Rule_hashset rule[], Hashtable<Integer, String> ht) {
		String result = "";
		for(Integer i: ruleNumbers){
			//System.out.println("row "+ i);
			for(Integer value:rule[i].head){
				System.out.print(ht.get(value)+ " ");
				result += ht.get(value)+ " ";
			}
			System.out.print(" :- ");
			result += " :- ";
			for(Integer value:rule[i].pos_body){
				System.out.print(ht.get(value)+ " ");
				result += ht.get(value)+ " ";
			}
			for(Integer value:rule[i].neg_body){
				System.out.print("-"+ht.get(value)+ " ");
				result += "-"+ht.get(value)+ " ";
			}
			result += "\n";
			System.out.println();
		}
		return result;
	}// End if printProgramInTerms
	// Description: This method removes a rule if it has common elements in head and positive body
	public static void tautology(HashSet<Integer> ruleNumbers, Rule_hashset rule[], int rows) {
		for(int i=0; i<rows; i++){
			HashSet<Integer> temp=new HashSet<Integer>(rule[i].head);
			temp.retainAll(rule[i].pos_body);
			if(!temp.isEmpty()){
				rule[i]=null;
				ruleNumbers.remove(i);
			}
		}
	}//End of tautology
	
	// Description: some term belongs to negative body of rule-1 and there does not exist a rule-2
	// where that term belongs to head of rule-2, then replace r1 with {r'}+
	public static void reducePositive(HashSet<Integer> ruleNumbers, Rule_hashset rule[]) {
		boolean red_pos_flag=false;
		for(Integer i:ruleNumbers){
			Iterator<Integer> iter = rule[i].pos_body.iterator();
			while(iter.hasNext()){
				int value=iter.next();
				for(Integer j:ruleNumbers){
					if(i!=j && rule[j].head.contains(value)){
						red_pos_flag=true;
						break;
					}
				}
				if(red_pos_flag==false){
					iter.remove();
				}
				red_pos_flag=false;
			}
		}
	}//End of RED+
	
	// Description: If there are any facts that belongs to negative body of some rule r1, then remove r1.
	public static void reduceNegative(HashSet<Integer> ruleNumbers, Rule_hashset rule[]) {
		HashSet<Integer> remove=new HashSet<Integer>();
		for(Integer i:ruleNumbers){
			if(!rule[i].head.isEmpty() && rule[i].pos_body.isEmpty() && rule[i].neg_body.isEmpty()){
				for(Integer j:ruleNumbers){
					
					if(i!=j && rule[j].neg_body.containsAll(rule[i].head)){
						remove.add(j);
					} 
				}
			}
		}
		ruleNumbers.removeAll(remove);
		remove.clear();
	}// End of RED-
	
	// Description: If any rule-1 subsumes any other rule-2, then remove rule-2
	public static void nonMin(HashSet<Integer> ruleNumbers, Rule_hashset rule[]) {
		HashSet<Integer> remove=new HashSet<Integer>();
		for(Integer i:ruleNumbers){
			for(Integer j:ruleNumbers){
				if(i!=j && !remove.contains(j)){
					if(rule[i].head.containsAll(rule[j].head) && rule[i].pos_body.containsAll(rule[j].pos_body) && rule[i].neg_body.containsAll(rule[j].neg_body)){
						//ruleNumbers.remove(i);
						remove.add(i);
						break;
					}
				}
			}
		}
		ruleNumbers.removeAll(remove);
		remove.clear();
	}//End of NON-MIN
	
	// Description: There exists literal belongs to positive body of rule-1, there exists a rule-2 in program P
	// where the given literal belongs to head of r-2, then replace rule-1 with G'a
	public static void gppe(HashSet<Integer> ruleNumbers, Rule_hashset rule[], int rows) {
		HashSet<Integer> remove=new HashSet<Integer>();
		Rule_hashset rule_copy[] = new Rule_hashset[rows];
		for(int i=0; i< rows; i++){
			//rule[i].body = new int[columns-1];
			//rule[i].head = new String("");
			rule_copy[i] = new Rule_hashset();
		}
		
		boolean gppe_flag=false;
		for(Integer i:ruleNumbers){
			Iterator<Integer> iter = rule[i].pos_body.iterator();
			while(iter.hasNext()){
				
				Integer pos_value=iter.next();
				for(Integer j:ruleNumbers){
					if(i!=j && rule[j].head.contains(pos_value) && !remove.contains(i)){
						//System.out.println("i: "+i);
						rule[j].head.remove(pos_value);
						rule[i].head.addAll(rule[j].head);
						iter.remove();
						//rule[i].pos_body.remove(pos_value);
						rule[i].pos_body.addAll(rule[j].pos_body);
						rule[i].neg_body.addAll(rule[j].neg_body);
						//ruleNumbers.remove(j);
						remove.add(j);
						gppe_flag=true;
						break;
					}
				}
				if(gppe_flag) {
					gppe_flag=false;
					break;
				}
			}
		}
		ruleNumbers.removeAll(remove);
		remove.clear();
	}//End of GPPE
	
	// Description: If positive body and negative body has common terms, then remove that rule.
	public static void contra(HashSet<Integer> ruleNumbers, Rule_hashset rule[]) {
		HashSet<Integer> remove=new HashSet<Integer>();
		for(Integer i:ruleNumbers){
			HashSet<Integer> temp=new HashSet<Integer>(rule[i].pos_body);
			temp.retainAll(rule[i].neg_body);
			if(!temp.isEmpty()){
				rule[i]=null;
				remove.add(i);
				//ruleNumbers.remove(i);
			}
		}
		ruleNumbers.removeAll(remove);
		remove.clear();
	}//End of CONTRA
	
	// Description: if r is s-imp of r', then remove r' from the program.
	public static void sImp(HashSet<Integer> ruleNumbers, Rule_hashset rule[]) {
		HashSet<Integer> remove=new HashSet<Integer>();
		for(Integer i: ruleNumbers) {
			Set<Set<Integer>> sets=new HashSet<Set<Integer>>();
			sets=powerSet(rule[i].neg_body);
			for(Set<Integer> subset:sets) {
				for(Integer j: ruleNumbers) {
					if(i!=j) {
						Set<Integer> head_temp=new HashSet<Integer>();
						Set<Integer> posbody_temp=new HashSet<Integer>();
						Set<Integer> negbody_temp=new HashSet<Integer>();
						head_temp.addAll(rule[i].head);
						posbody_temp.addAll(rule[i].pos_body);
						negbody_temp.addAll(rule[i].neg_body);
						head_temp.addAll(subset);
						negbody_temp.removeAll(subset);
						if(head_temp.containsAll(rule[j].head) && 
								posbody_temp.containsAll(rule[j].pos_body) &&
								negbody_temp.containsAll(rule[j].neg_body)) {
							remove.add(i);
							//System.out.println(i);
						}
					}
				}
			}
		}
		ruleNumbers.removeAll(remove);
		remove.clear();
	}//End of S-IMP
	
	// Description: if r is head cycle free in P, then replace r with r->
	public static void LSH(HashSet<Integer> ruleNumbers, Rule_hashset rule[]) {
		HashSet<Integer> remove=new HashSet<Integer>();
		ArrayList<Integer> nodes=new ArrayList<Integer>();
		for(Integer i:ruleNumbers) {
			for(Integer element:rule[i].head) {
				if(!nodes.contains(element)) {
					nodes.add(element);
				}
			}
			
			for(Integer element:rule[i].pos_body) {
					if(!nodes.contains(element)) {
						nodes.add(element);
				}
			}
		}
		int max=Collections.max(nodes)+1;
		int graph[][]=new int[max][max];
		
		for(int i=0;i<max;i++) {
			for(int j=0;j<max;j++) {
				graph[i][j]=0;
			}
		}
		
		for(Integer element1:nodes) {
			for(Integer element2:nodes) {
				for(Integer num:ruleNumbers) {
					if(rule[num].head.contains(element1) && rule[num].pos_body.contains(element2)) {
						graph[element1][element2]=1;
					}
				}
			}
		}
		
		for(Integer i:ruleNumbers) {
			for(Integer element1:rule[i].head) {
				for(Integer element2:rule[i].head) {
					if(graph[element1][element2]!=graph[element2][element1]) {
						if(!rule[i].head.isEmpty()) {
							rule[i].head.remove(element1);
							rule[i].neg_body.addAll(rule[i].head);
							rule[i].head.removeAll(rule[i].head);
							rule[i].head.add(element1);
							//remove.add(i);
						}
							
					}
				}
			}
		}
		ruleNumbers.removeAll(remove);
		remove.clear();
	}//End of LSH
}//End of class InputProcessing_HashTable

