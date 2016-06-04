<?php

/*

MIT License

Copyright (c) [2016] [Okan Ulas Gezeroglu]

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

You can select an uploaded svg file and draw it using pathfinder.
*/

$imageFolder = 'images/';
$imageTypes = '{*.svg}';
$sortByImageName = false;
$newestImagesFirst = true;
$images = glob($imageFolder . $imageTypes, GLOB_BRACE);

?>

<html>
	<head>
		<meta charset="utf-8" />
		<meta name="viewport" content="width=device-width" />
		<title>SVG DRAW</title>
		
		<link rel="stylesheet" href="css/content.css" />
		<link rel="stylesheet" href="css/rangeslider.css">
		<script src="js/jquery/1.12.3/jquery-1.12.3.min.js"></script>
	</head>
	<body>

	<!-- DRAW SVG BUTTON-->
			
	<div>	
		<button id="draw_svg" style="margin-top:10px;">
		<img src="images/btn_draw_svg.png"/>
		</button>
	</div>
		
	<!-- UPLOADED SVG IMAGES -->

	<div id="images">
		<form action="">
			<?php
				foreach ($images as $image) 
				{
					$name = 'Image name: ' . substr($image, strlen($imageFolder), strpos($image, '.') - strlen($imageFolder));
			    	echo '<div id="image_entry">';
			    	echo '<input type="radio" name="image" value="'.$image.'" style="height:300px" > <img style="height:300px" src="' . $image . '" alt="' . $name . '" title="' . $name . '"><br>';
			    	echo '</div>';
				}
			?>
		</form>
	</div>

	</body>
</html>

<script>

$(document).ready(function() {
	// DRAW SVG
	$('#draw_svg').click(function(){
		var selectedVal = "";
		var selected = $("input[type='radio'][name='image']:checked");
		if (selected.length > 0) {
			selectedVal = selected.val();
		}
		console.log("SelectedVal:"+selectedVal);
		$.post( "python_socket_server.php", { action: "send",data:"draw_svg|"+selectedVal });
	})
});
</script>


