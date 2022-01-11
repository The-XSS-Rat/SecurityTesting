<!-- Global site tag (gtag.js) - Google Analytics -->
<script async src="https://www.googletagmanager.com/gtag/js?id=G-8L64ZBYXXW"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());

  gtag('config', 'G-8L64ZBYXXW');
</script>

<?php 
	//This makes XXE possible
    libxml_disable_entity_loader (false);
    //Grab the input sent to the PHP file (POST body)
    $xmlfile = file_get_contents('php://input');
    //Create a new DOM document to send the XML to
    $dom = new DOMDocument();
    $dom->loadXML($xmlfile, LIBXML_NOENT | LIBXML_DTDLOAD);
    //Grab the data from the file
    $cheese = simplexml_import_dom($dom);
    $cheeseType = $cheese->cheeseType;
    if($cheeseType==""){
    	echo "Please make a POST request with the following data\<br><br>&lt;cheese><br>&nbsp;&nbsp;&nbsp;
    &lt;cheeseType>Test&lt;/cheeseType><br>
&lt;/cheese>";
    }else{
	    echo "I also LOVEEEE $cheeseType";
    }
    
?> 