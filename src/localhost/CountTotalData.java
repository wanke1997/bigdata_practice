package localhost;

import java.io.File;
import java.io.FileNotFoundException;
import java.util.Scanner;

// Total data: 4937970

public class CountTotalData {
      public static void main(String[] args) {
            String dir = System.getProperty("user.dir")+"/data/GDS_logs.txt";
            File fp = new File(dir);
            try {
                  Scanner scanner = new Scanner(fp);
                  int cnt = 0;
                  while(scanner.hasNextLine()) {
                        String s = scanner.nextLine();
                        if(cnt%10000==0) {
                              System.out.println("example data "+(cnt/10000)+": "+s);
                        }
                        cnt++;
                  }
                  System.out.println("Total data: "+cnt);
                  scanner.close();
            } catch(FileNotFoundException e) {
                  e.printStackTrace();
            }
      }
}