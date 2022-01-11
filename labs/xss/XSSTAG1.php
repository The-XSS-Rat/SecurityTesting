<?php
if(isset($_GET['fname'])){
echo "<input value='" . $_GET['fname'] . "'>";
}
?>

<form>
<label for="fname">First name:</label><br>
<input type="text" id="fname" name="fname" value="Prof. Snape"><br>
<input type="submit" value="Submit">
</form>