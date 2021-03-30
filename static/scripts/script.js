//your-link/home view functions

function viewHome(){
	var barcont = document.getElementsByClassName("your-url")[0];
	var toremove = document.getElementsByClassName("remove")[0];
	var toremove2 = document.getElementsByClassName("remove")[1];
	var image = document.getElementsByClassName("image")[0];
	image.style.marginTop = "23%";
	barcont.style.display = "none";
	toremove.style.display = "block";
	toremove2.style.display = "block";
}

function viewYourLink(){
	var barcont = document.getElementsByClassName("your-url")[0];
	var toremove = document.getElementsByClassName("remove")[0];
	var toremove2 = document.getElementsByClassName("remove")[1];
	barcont.style.display = "block";
	toremove.style.display = "none";
	toremove2.style.display = "none";
}

// Copy link function
function copyLink() {
	var copyText = document.getElementById("new_url");
	var popup = document.getElementById("myPopup");
	copyText.select();
	document.execCommand("copy");
  	popup.classList.toggle("show");
  	setTimeout(changePopUp, 1800);
}

function changePopUp(){
	var popup = document.getElementById("myPopup");
	popup.classList.toggle("show");
}

//adaptive mobile header
function mobileNavbar() {
	var el = document.getElementById("header-right");
	if (el.style.display === "flex") {
    el.style.display = "none";
    } else {
    el.style.display = "flex";
    el.style.animation = "animatenavbar 0.8s";
    }
}
//all links window
// Get the modal
var modal = document.getElementById("myModal");

// Get the button that opens the modal
var btn = document.getElementById("myBtn");

// Get the <span> element that closes the modal
var span = document.getElementById("close");

// When the user clicks the button, open the modal 
function openClose() {
  modal.style.display = "block";
}

// When the user clicks on <span> (x), close the modal
span.onclick = function() {
  modal.style.display = "none";
}

// When the user clicks anywhere outside of the modal, close it
window.onclick = function(event) {
  if (event.target == modal) {
    modal.style.display = "none";
  }
}

function setRandom() {
	var randomnum = document.getElementById("randomnum").value;
	var checkbox = document.getElementById("randomcheck");
	var randominput = document.getElementById("input2");
	if (checkbox.checked == true) {
		randominput.value = randomnum;
	} else if (checkbox.checked == false) {
		randominput.value = "";
	}
}

function navbarAnimation(x) {
		x.classList.toggle("change");
}