<?php
if(isset($_GET['fname'])){
echo htmlentities($_GET['fname']);
}
?>

<form>
<label for="fname">First name:</label><br>
<input type="text" id="fname" name="fname" value="John"><br>
<input type="submit" value="Submit">
</form>