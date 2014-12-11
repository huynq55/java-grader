import org.junit.Test;
import static org.junit.Assert.assertEquals;
import org.junit.runner.JUnitCore;
import org.junit.runner.Result;
import org.junit.runner.notification.Failure;

public class Bai3TestRunner {

	@Test
	public void test() {
		Program p = new Program();
		assertEquals(1, p.Puzzle(1, 1));
		assertEquals(1, p.Puzzle(1, 5));
		assertEquals(1, p.Puzzle(1, 0));
		assertEquals(2, p.Puzzle(2, 1));
	}

	public static void main(String[] args) {
		Result result = JUnitCore.runClasses(Bai3TestRunner.class);
		for (Failure failure : result.getFailures()) {
			String myFailure = new String(failure.toString());
			myFailure = myFailure.replace("<", " ");
			myFailure = myFailure.replace(">", " ");
			System.out.println(myFailure);			
		}
		System.out.println(result.wasSuccessful());
	}

}
