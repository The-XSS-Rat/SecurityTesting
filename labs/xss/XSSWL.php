<?php
if(isset($_GET['fname'])){
$name = $_GET['fname'];
if (!$name = filter_var($name, FILTER_VALIDATE_EMAIL)){
echo "Please enter an email address";
}else{
echo "Good!! $name";
}
}
?>

<form>
<label for="fname">First name:</label><br>
<input type="text" id="fname" name="fname" value="John"><br>
<input type="submit" value="Submit">
</form>
<br> <br>