<?

/**
 * This file saves a raw image sent in the post as a parameter called imageData
 * It is quite insecure - you should actually check that the file is an image
 * before saving it but this is a simple example. 
 * based on http://www.re-cycledair.com/html-5-canvas-saving-to-a-file-with-php
 */

$data = substr($_POST['imageData'], strpos($_POST['imageData'], ",") + 1);
$decodedData = base64_decode($data);
if (!file_exists("./upload") || !is_writeable("./upload/")){
  echo("ERROR! You need to create the upload folder and give PHP permission to write to it!");
  exit(0);
}
$filename = "./upload/canvas.png";
$fp = fopen($filename, 'wb');
fwrite($fp, $decodedData);
fclose($fp);
//echo ($_SERVER["HTTP_REFERER"]);
//$this_dir = str_replace(basename($_SERVER["HTTP_REFERER"]), "", $_SERVER["HTTP_REFERER"]); 
echo ($_SERVER["HTTP_REFERER"].$filename);

?>

