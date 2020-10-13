function add_card() {
    var Uniname = document.getElementById("add_uniname").value;
    var major = document.getElementById("add_major").value;
    var year = document.getElementById("add_year").value;
    $("#education-container").append("<div class=\"card mb-3 marg-20 edu-card\" id=\""+Uniname+"\" style=\"max-width: 440px;\">\n" +
        "                    <div class=\"row no-gutters\">\n" +
        "                        <div class=\"col-md-4\">\n" +
        "                            <img src=\"images/preview.jpg\" class=\"card-img\" alt=\"edu-logo\">\n" +
        "                        </div>\n" +
        "                        <div class=\"col-md-8\">\n" +
        "                            <div class=\"dropdown \">\n" +
        "                                <button type=\"button\" class=\"option-button\" id=\""+Uniname+"-Button\" data-toggle=\"dropdown\" aria-haspopup=\"true\" aria-expanded=\"false\">\n" +
        "                                    <i class=\"fas fa-ellipsis-v\"></i>\n" +
        "                                </button>\n" +
        "                                <div class=\"dropdown-menu\" aria-labelledby=\""+Uniname+"-Button\">\n" +
        "                                    <button class=\"dropdown-item\"  data-toggle=\"modal\" data-target=\"#edit_card\">Edit</button>\n" +
        "                                    <button class=\"dropdown-item\"  onclick=\"removeme('"+Uniname+"')\">Remove</button>\n" +
        "                                </div>\n" +
        "                            </div>\n" +
        "                            <div class=\"card-body\" >\n" +
        "                                <h5 class=\"card-title\">"+Uniname+"</h5>\n" +
        "                                <p class=\"card-text\">Major: "+major+"</p>\n" +
        "                                <p class=\"card-text\"><small class=\"text-muted\">"+year+"</small></p>\n" +
        "                            </div>\n" +
        "                        </div>\n" +
        "                    </div>\n" +
        "                    <div class=\"modal fade\" id=\"edit_card\" tabindex=\"-1\" aria-labelledby=\"edit_cardLabel\" aria-hidden=\"true\">\n" +
        "                        <div class=\"modal-dialog\">\n" +
        "                            <div class=\"modal-content\">\n" +
        "                                <div class=\"modal-header\">\n" +
        "                                    <h5 class=\"modal-title\" id=\"edit_cardLabel\">Add Education card</h5>\n" +
        "                                    <button type=\"button\" class=\"close\" data-dismiss=\"modal\" aria-label=\"Close\">\n" +
        "                                        <span aria-hidden=\"true\">&times;</span>\n" +
        "                                    </button>\n" +
        "                                </div>\n" +
        "                                <div class=\"modal-body\">\n" +
        "                                    <h1>prefilled card text</h1>\n" +
        "                                </div>\n" +
        "\n" +
        "                            </div>\n" +
        "                        </div>\n" +
        "                    </div>\n" +
        "                </div>")
}

function removeme(me) {
    $("#"+me).remove()
}
function rename_section(holder,rename) {
    document.getElementById(holder).innerText = document.getElementById(rename).value
}

function section_add() {
    var name = document.getElementById("new_section_name").value;
    $("#sections-container").append("  <section id=\""+ name +"\">\n" +
        "            <div class=\"section-heading\">\n" +
        "                <h1 id=\""+ name +"-heading-text\">"+ name +"</h1>\n" +
        "                <button type=\"button\" class=\"option-button\"  data-toggle=\"modal\" data-target=\"#"+ name +"_rename_section\"><i class=\"fas fa-pencil-alt\"></i></button>\n" +
        "            </div>\n" +
        "            <div class=\"ellipse-container\">\n" +
        "                <button type=\"button\" data-toggle=\"modal\" data-target=\"#"+ name +"_add_card\" class=\"option-button\"> <i class=\"fas fa-plus\"></i></button>\n" +
        "            </div>\n" +
        "            <div class=\"modal fade\" id=\""+ name +"_rename_section\" tabindex=\"-1\" aria-labelledby=\""+ name +"_rename_sectionLabel\" aria-hidden=\"true\">\n" +
        "                <div class=\"modal-dialog\">\n" +
        "                    <div class=\"modal-content\">\n" +
        "                        <div class=\"modal-header\">\n" +
        "                            <h5 class=\"modal-title\" id=\""+ name +"_rename_sectionLabel\">Rename Section</h5>\n" +
        "                            <button type=\"button\" class=\"close\" data-dismiss=\"modal\" aria-label=\"Close\">\n" +
        "                                <span aria-hidden=\"true\">&times;</span>\n" +
        "                            </button>\n" +
        "                        </div>\n" +
        "                        <div class=\"modal-body\">\n" +
        "                            <form onsubmit=\"return false\">\n" +
        "                                <div class=\"form-group\">\n" +
        "                                    <label for=\""+ name +"_new_name\">New Name</label>\n" +
        "                                    <input type=\"text\" class=\"form-control\" id=\""+ name +"_new_name\" aria-describedby=\"emailHelp\">\n" +
        "                                </div>\n" +
        "                                <button data-dismiss=\"modal\"  type=\"submit\" class=\"btn btn-primary\" onclick=\"rename_section('"+ name +"-heading-text','"+ name +"_new_name')\">Rename</button>\n" +
        "                            </form>\n" +
        "                        </div>\n" +
        "\n" +
        "                    </div>\n" +
        "                </div>\n" +
        "            </div>\n" +
        "            <div class=\"modal fade\" id=\""+ name +"_add_card\" tabindex=\"-1\" aria-labelledby=\""+ name +"_add_cardLabel\" aria-hidden=\"true\">\n" +
        "                <div class=\"modal-dialog\">\n" +
        "                    <div class=\"modal-content\">\n" +
        "                        <div class=\"modal-header\">\n" +
        "                            <h5 class=\"modal-title\" id=\""+ name +"_add_cardLabel\">Add Education card</h5>\n" +
        "                            <button type=\"button\" class=\"close\" data-dismiss=\"modal\" aria-label=\"Close\">\n" +
        "                                <span aria-hidden=\"true\">&times;</span>\n" +
        "                            </button>\n" +
        "                        </div>\n" +
        "                        <div class=\"modal-body\">\n" +
        "                           <h3>every section will have its own form</h3>\n" +
        "                        </div>\n" +
        "\n" +
        "                    </div>\n" +
        "                </div>\n" +
        "            </div>\n" +
        "            <div id=\""+ name +"-container\">\n" +
        "\n" +
        "            </div>\n" +
        "        </section>")
}

function remove_section() {
    var name = document.getElementById("remove_section_name").value;
    $("#sections-container").children("#"+name).remove()
}

// $("#edit_uniname").val(document.getElementById("uniname").innerText);
// $("#edit_major").val(document.getElementById("major").innerText);
// $("#edit_year").val(document.getElementById("year").innerText);
//

// function edit() {
//     var Uniname = document.getElementById("edit_uniname").value;
//     var major = document.getElementById("edit_major").value;
//     var year = document.getElementById("edit_year").value;
//     document.getElementById("uniname").innerText = Uniname;
//     document.getElementById("major").innerText = major;
//     document.getElementById("uniname").innerText = year;
// }
