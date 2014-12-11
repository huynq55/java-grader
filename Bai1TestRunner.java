import org.junit.Test;
import static org.junit.Assert.assertEquals;
import org.junit.runner.JUnitCore;
import org.junit.runner.Result;
import org.junit.runner.notification.Failure;

public class Bai1TestRunner {

	@Test
	public void test() {
		Program p = new Program();
		assertEquals(0, p.Puzzle(0));
		assertEquals(2, p.Puzzle(1));
		assertEquals(4, p.Puzzle(2));
	}

	public static void main(String[] args) {
		Result result = JUnitCore.runClasses(Bai1TestRunner.class);
		for (Failure failure : result.getFailures()) {
			String myFailure = new String(failure.toString());
			myFailure = myFailure.replace("<", " ");
			myFailure = myFailure.replace(">", " ");
			System.out.println(myFailure);			
		}
		System.out.println(result.wasSuccessful());
	}

}
