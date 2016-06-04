
<!-- 
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
 -->
<html>
	<head>
		<meta charset="utf-8" />
		<meta name="viewport" content="width=device-width" />
		<title>Pathfinder</title>
		
		<link rel="stylesheet" href="css/content.css" />
		<link rel="stylesheet" href="css/rangeslider.css">
		<script src="js/jquery/1.12.3/jquery-1.12.3.min.js"></script>
		
		<script src="js/rangeslider.js"></script>
	</head>
	<body>
		<!-- TITLE -->
		<div id="title">
			<div class="logo">
				<img class="padding10" src="images/logo.png"/>
			</div>
		</div>
		<!-- LEFT MENU -->
		<div class="left_menu_container">
			<!-- START SERVER BUTTON -->
			<div class="menu_row">
				<button id="start_server">
				<img src="images/btn_start_server.png"/>
				</button>
			</div>
			<!-- CLEAR CONSOLE -->
			<div class="menu_row">
				<button class="grey_wide_button" id="clear_console">CLEAR CONSOLE</button>
			</div>
			<!-- FEED PAPER ROW -->
			<div class="menu_row">
				<div class="grey_box" align=center>FEED</div>
				<button class="red_box_btn" id="feed_paper_in">
				<img src="images/btn_up.png"/>
				</button>
				<button class="red_box_btn" id="feed_paper_out">
				<img src="images/btn_down.png"/>
				</button>
				<button class="red_box_btn" id="stop_feed_paper">
				<img src="images/btn_stop.png"/>
				</button>
			</div>
			<!-- SET PEN ROW -->
			<div class="menu_row">
				<div class="grey_box" align=center>PEN</div>
				<button class="red_box_btn" id="move_pen_up">
				<img src="images/btn_up.png"/>
				</button>
				<button class="red_box_btn" id="move_pen_down">
				<img src="images/btn_down.png"/>
				</button>
				<button class="red_box_btn" id="set_pen_position">
				<img src="images/btn_confirm.png"/>
				</button>
			</div>
			<!-- DISPLAY INFO ROW -->
			<div class="menu_row">
				<button class="grey_wide_button" id="get_info">DISPLAY STATUS</button>
			</div>
			<!-- CALIBRATE -->
			<div class="menu_row">
				<button class="grey_wide_button" id="calibrate">CALIBRATE</button>
			</div>
			<!-- FORCE STOP -->
			<div class="menu_row">
				<button class="grey_wide_button" id="force_stop">FORCE STOP</button>
			</div>
			<!-- DRAW MAZE -->
			<div class="menu_row" style="height:230px">
				<div>
					<div class="slider_label">WIDTH:<span id="width_label">5<span></div>
					<input id="width_slider" type="range" min="3" max="20" data-rangeslider>
				</div>
				<div>
					<div class="slider_label">HEIGHT:<span id="height_label">5</span></div>
					<input id="height_slider" type="range" min="3" max="20" data-rangeslider>
				</div>
				<div>
					<div class="slider_label">SIZE:<span id="size_label" >100</span></div>
					<input id="size_slider" type="range" min="50" max="150" step="10" data-rangeslider>
				</div>
				<button  id="draw_maze" style="margin-top:10px;">
				<img src="images/btn_draw_maze.png"/>
				</button>
			</div>
			<!-- DRAW SVG -->
			<div class="menu_row" style="height:160px;">
				
				<input id="uploadFile" placeholder="Choose File" disabled="disabled" style="margin-bottom:10px;width: 280px;" />
					<div class="fileUpload btn btn-primary">
					    <div class="grey_wide_button" align="center" style="width:150px;height:40px;padding-top:20px">Select File</div>
					    <input id="uploadBtn" type="file" class="upload" style="height: 50px;width: 150px;" />
					</div>
					<button class="grey_wide_button" id="upload_svg" style="width:120px;margin-left:10px;">UPLOAD</button>
				
				<button id="draw_svg" style="margin-top:10px;">
				<img src="images/btn_draw_svg.png"/>
				</button>
			</div>
		</div>
		<div class="console_container" id="console_container">
		</div>
	</body>
</html>
<script>
$(document).ready(function() {
var $document = $(document);
var selector = '[data-rangeslider]';
var $element = $(selector);

document.getElementById("uploadBtn").onchange = function () {
    document.getElementById("uploadFile").value = this.value;
};

var slideElements = [];
slideElements["width_slider"] = $('#width_label');
slideElements["height_slider"] = $('#height_label');
slideElements["size_slider"] = $('#size_label');
// Basic rangeslider initialization
$element.rangeslider({
// Deactivate the feature detection
polyfill: false,
// Callback function
onInit: function() {

},
// Callback function
onSlide: function(position, value) {
var id = this.$element[0].id;
slideElements[id].text(value);
},
// Callback function
onSlideEnd: function(position, value) {
var id = this.$element[0].id;
slideElements[id].text(value);
}
});


$( "body" ).keydown(function(e) {
	console.log("keydown "+e.keyCode);
	  if(e.keyCode == 38 || e.which == 38){ // UP
	  	$.post( "python_socket_server.php", { action: "send", data:"feed_paper_out_inc" })
	  }else if(e.keyCode == 40 || e.which == 40){ // DOWN
	  	$.post( "python_socket_server.php", { action: "send", data:"feed_paper_in_inc" })
	  }else if(e.keyCode == 39){ // RIGHT
	  	$.post( "python_socket_server.php", { action: "send", data:"move_right" })
	  }else if(e.keyCode == 37){ // LEFT
		$.post( "python_socket_server.php", { action: "send", data:"move_left" })
	  }else if(e.keyCode == 32){ // SPACE
	  	$.post( "python_socket_server.php", { action: "send", data:"switch_pen_pos" })
	  }else if(e.keyCode == 90){ // z
	  	$.post( "python_socket_server.php", { action: "send", data:"switch_pen_state" })
	  }
});

$( "body" ).keyup(function(e) {
	  if(e.keyCode == 38 || e.which == 38){ // UP
	  	$.post( "python_socket_server.php", { action: "send", data:"feed_paper_stop_inc" })
	  }else if(e.keyCode == 40|| e.which == 40){ // DOWN
	  	$.post( "python_socket_server.php", { action: "send", data:"feed_paper_stop_inc" })
	  }else if(e.keyCode == 39){ // RIGHT
	  	$.post( "python_socket_server.php", { action: "send", data:"move_stop" })
	  }else if(e.keyCode == 37){ // LEFT
	  	$.post( "python_socket_server.php", { action: "send", data:"move_stop" })
	  }else if(e.keyCode == 32){ // SPACE

	  }
});


// START SERVER BUTTON
		$('#start_server').click(function(){
		$.post( "python_socket_server.php", { action: "start_server" })
		.done(function( data ) {
		logMessage(data);
		});
		})
// PAPER FEED
		$('#feed_paper_in').click(function(){
		$.post( "python_socket_server.php", { action: "send",data:"feed_paper_in" })
		})
		$('#clear_console').click(function(){
			var el = document.getElementById("console_container");
			el.innerHTML= "";
		})
		$('#feed_paper_out').click(function(){
		$.post( "python_socket_server.php", { action: "send",data:"feed_paper_out" })
		})
		$('#stop_feed_paper').click(function(){
		$.post( "python_socket_server.php", { action: "send",data:"stop_feed" })
		})
		// PEN POSITION
		$('#move_pen_up').click(function(){
		$.post( "python_socket_server.php", { action: "send",data:"move_pen_up" })
		})

		$('#move_pen_down').click(function(){
		$.post( "python_socket_server.php", { action: "send",data:"move_pen_down" })
		})

		$('#set_pen_position').click(function(){
		$.post( "python_socket_server.php", { action: "send",data:"set_pen_position" })
		})
		// CALIBRATE
		$('#calibrate').click(function(){
		$.post( "python_socket_server.php", { action: "send",data:"calibrate" })
		})
		// DISPLAY INFO
		$('#get_info').click(function(){
		$.post( "python_socket_server.php", { action: "send",data:"get_info" })
		})
		// FORCE STOP
		$('#force_stop').click(function(){
		$.post( "python_socket_server.php", { action: "send",data:"force_stop" })
		})

		// DRAW MAZE
		$('#draw_maze').click(function(){
			var d = "draw_maze |"+$('#width_label').text()+"|"+$('#height_label').text()+"|"+$('#size_label').text();
		$.post( "python_socket_server.php", { action: "send",data:d})
		})

		// UPLOAD SVG
		$('#upload_svg').click(function(){
			
			var fileInput = document.querySelector("#uploadBtn");

		    var xhr = new XMLHttpRequest();
		    xhr.open('POST', 'upload.php');

		    xhr.upload.onprogress = function(e) 
		    {
		        /* 
		        * values that indicate the progression
		        * e.loaded
		        * e.total
		        */
		        console.log(e.loaded+":"+e.total);
		    };

		    xhr.onload = function()
		    {
		        alert('upload complete');
		    };

		    // upload success
		    if (xhr.readyState == 4 && (xhr.status == 200 || xhr.status == 0))
		    {
		        // if your server sends a message on upload sucess, 
		        // get it with xhr.responseText
		        alert(xhr.responseText);
		    }

		    var form = new FormData();
		    form.append('upload_file', fileInput.files[0]);

		    xhr.send(form);

		})

		// DRAW SVG
		$('#draw_svg').click(function(){
			window.open("svg_draw.php","_blank");
		})

		if (!!window.EventSource) {
	      var source = new EventSource("python_console.php");

	      source.addEventListener("message", function(e) {
	        logMessage(e.lastEventId+"--> "+e.data);
	      }, false);
	      
	      source.addEventListener("open", function(e) {
	        logMessage("OPENED:");
	      }, false);

	      source.addEventListener("error", function(e) {
	        logMessage("ERROR:");
	        if (e.readyState == EventSource.CLOSED) {
	          logMessage("CLOSED");
	        }
	      }, false);
	    } else {
      		document.getElementById("notSupported").style.display = "block";
	    }

	    logMessage("Welcome to Lego Pathfinder");
	    logMessage("Waiting for socket server");

		
		function logMessage(obj) {
			var el = document.getElementById("console_container");
			var entry = '<div class="console_entry"> > '+obj+' </div>';
			el.innerHTML= entry+el.innerHTML;
		}
});
</script>




