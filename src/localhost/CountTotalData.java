package localhost;

import java.io.File;
import java.io.FileNotFoundException;
import java.util.*;

// Total data: 4937970
// Total keys:1094059

public class CountTotalData {
      public static void main(String[] args) {
            String dir = System.getProperty("user.dir")+"/data/GDS_logs.txt";
            File fp = new File(dir);
            Set<String> set = new HashSet<>();
            try {
                  Scanner scanner = new Scanner(fp);
                  int cnt = 0;
                  while(scanner.hasNextLine()) {
                        String s = scanner.nextLine();
                        String key = s.split("\\|")[0];
                        set.add(key);
                        if(cnt%10000==0) {
                              System.out.println("example data "+(cnt/10000)+": "+s);
                        }
                        cnt++;
                  }
                  System.out.println("Total data: "+cnt);
                  scanner.close();
                  System.out.println("Total keys:"+set.size());
            } catch(FileNotFoundException e) {
                  e.printStackTrace();
            }
      }
}