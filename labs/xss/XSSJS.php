<?php
if(isset($_GET['fname'])){
echo "<script>document.write('" . $_GET['fname'] . "');</script>";
}
?>

<form>
<label for="fname">First name:</label><br>
<input type="text" id="fname" name="fname" value="John"><br>
<input type="submit" value="Submit">
</form>

In here we can see some JS 

document.write('" . $_GET['fname'] . "');