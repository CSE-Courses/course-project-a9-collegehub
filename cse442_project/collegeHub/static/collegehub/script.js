var temp_L = document.querySelectorAll(".template:nth-child(2n)");
var att = document.createAttribute("data-aos");       // Create a "class" attribute
att.value = "fade-right";                           // Set the value of the class attribute
for (let i = 0; i < temp_L.length; i++) {
    temp_L[i].setAttributeNode(att);
}