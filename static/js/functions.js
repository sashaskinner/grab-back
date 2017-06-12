// external file for home.html
// functions for grab back d3 map and chartjs


///////////////////////////////////////////////////////////////////////////////
// POPULATE REVERSE CHARTS
// -- should be called when reverse chart buttons are pressed

// update reverse chart employee
function updateReverseChartEmployee() {
    
    $("#district-rank").remove();
    $("#graph-container").append("<canvas id='district-rank' width=450, height=400></canvas>");
    
    var ctx = $("#district-rank");
    var yearValue = $("#year").val();

    $.get("/chart-data-employee-reverse?year="+yearValue, function (results) {
      var data = {
        labels: results[0],
        datasets: [
        {
          data: results[1],
          backgroundColor: ["#2f78c4", "#2f78c4", "#2f78c4", "#2f78c4", "#2f78c4", "#084081"]
        }]
      };

      var districtRankChart = new Chart(ctx, {
        type: 'horizontalBar',
        data: data,
        options: {
            responsive: false,
            title: {
                display: true,
                text: 'Districts With Lowest % Female Employees in Management'
              },
             legend: {
                display: false
            }}
            });
    });

    } // end updateReverseChartEmployee

//update reverse chart manager 
function updateReverseChartManager() {

    // draw chartjs chart
    $("#district-rank").remove();
    $("#graph-container").append("<canvas id='district-rank' width=450, height=400</canvas>");
    
    var ctx = $("#district-rank");

    $.get("/chart-data-manager-reverse?year="+yearValue, function (results) {
        var data = {
          labels: results[0],
          datasets: [
          {
            data: results[1],
            backgroundColor: ["#2f78c4", "#2f78c4", "#2f78c4", "#2f78c4", "#2f78c4", "#084081"]
          }]
        };

        var districtRankChart = new Chart(ctx, {
          type: 'horizontalBar',
          data: data,
          options: {
              responsive: false,
              title: {
                  display: true,
                  text: 'Districts With Lowest % Female Employees in Management'
                },
               legend: {
                  display: false
              }}
              });
  });

  } // end updateReverseChartManager



// CREATE BAR CHARTS 
///////////////////////////////////////////////////////////////////////////////
function createRankChartEmployee() {

$("#district-rank").remove();
$("#graph-container").append("<canvas id='district-rank' width=450, height=400</canvas>");

var ctx = $("#district-rank");

var yearValue = $("#year").val();

$.get("/chart-data-employee?year="+yearValue, function (results) {
  var data = {
    labels: results[0],
    datasets: [
    {
      data: results[1],
      backgroundColor: ["#2f78c4", "#2f78c4", "#2f78c4", "#2f78c4", "#2f78c4", "#084081"]
    }]
  };

  var districtRankChart = new Chart(ctx, {
    type: 'horizontalBar',
    data: data,
    options: {
        responsive: false,
        title: {
            display: true,
            text: 'Districts With Highest % Female Employees'},
        legend: {
            display: false
        }
          }}
        );
});
}


function createRankChartManager() {

$("#district-rank").remove();
$("#graph-container").append("<canvas id='district-rank' width=450, height=400</canvas>");

var ctx = $("#district-rank");

var yearValue = $("#year").val();

$.get("/chart-data-manager?year="+yearValue, function (results) {
  var data = {
    labels: results[0],
    datasets: [
    {
      data: results[1],
      backgroundColor: ["#2f78c4", "#2f78c4", "#2f78c4", "#2f78c4", "#2f78c4", "#084081"]
    }]
  };

  var districtRankChart = new Chart(ctx, {
    type: 'horizontalBar',
    data: data,
    options: {
        responsive: false,
        title: {
            display: true,
            text: 'Districts With Highest % Female Employees in Management'
          },
        legend: {
            display: false
        }}
        });
});
}

function createReverseChartEmployee() {

$("#district-rank").remove();
$("#graph-container").append("<canvas id='district-rank' width=450, height=400</canvas>");

var ctx = $("#district-rank");

var yearValue = $("#year").val();

$.get("/chart-data-employee-reverse?year="+yearValue, function (results) {
  var data = {
    labels: results[0],
    datasets: [
    {
      data: results[1],
      backgroundColor: ["#2f78c4", "#2f78c4", "#2f78c4", "#2f78c4", "#2f78c4", "#084081"]
    }]
  };

  var districtRankChart = new Chart(ctx, {
    type: 'horizontalBar',
    data: data,
    options: {
        responsive: false,
        title: {
            display: true,
            text: 'Districts With Lowest % Female Employees'},
        legend: {
            display: false
        }
        }
        });
});
}

function createReverseChartManager() {

    $("#district-rank").remove();
    $("#graph-container").append("<canvas id='district-rank' width=450, height=400</canvas>");

    var ctx = $("#district-rank");

    var yearValue = $("#year").val();

    $.get("/chart-data-manager-reverse?year="+yearValue, function (results) {
      var data = {
        labels: results[0],
        datasets: [
        {
          data: results[1],
          backgroundColor: ["#2f78c4", "#2f78c4", "#2f78c4", "#2f78c4", "#2f78c4", "#084081"]
        }]
      };

      var districtRankChart = new Chart(ctx, {
        type: 'horizontalBar',
        data: data,
        options: {
            responsive: false,
            title: {
                display: true,
                text: 'Districts With Lowest % Female Employees in Management'
              },
             legend: {
                display: false
            }}
            });
        });
      }


// update just chart



// UPDATE CHARTS
///////////////////////////////////////////////////////////////////////////////
// update rank chart employee
function updateRankChartEmployee() {

  $("#district-rank").remove();
  $("#graph-container").append("<canvas id='district-rank' width=450, height=400></canvas>");
  
  var ctx = $("#district-rank");
    
    $.get("/chart-data-employee?year="+yearValue,
      function (results) {
          var data = {
            labels: results[0],
            datasets: [
            {
              data: results[1],
              backgroundColor: ["#2f78c4", "#2f78c4", "#2f78c4", "#2f78c4", "#2f78c4", "#084081"]
            }]
      };

      var districtRankChart = new Chart(ctx, {
        type: 'horizontalBar',
        data: data,
        options: {
            responsive: false,
            title: {
                display: true,
                text: 'Districts With Highest % Female Employees'},
            legend: {
                display: false
            }
              }}
            );
    });

}

function updateRankChartManager() {

  $("#district-rank").remove();
  $("#graph-container").append("<canvas id='district-rank' width=450, height=400></canvas>");

  createRankChartManager();

  }


// change data based on button click
////////////////////////////////////
// all employees button selected ///

$("#allEmp").on("click", function () {
  alert("allEmp clicked");
});

$("#allEmp").on("change", function () {

        console.log("allEmp button selection has been changed!");
        
        var yearValue = $("#year").val();
        var zipcode = $("#zipcode-entry").val();

        var zipOnly = $("#view-zip-compare").is(":checked");

        queue()
        .defer(d3.json, "/us.json")
        .defer(d3.json, "/us-congress-113.json")
        .defer(d3.json, "/district-employee-info.json?year="+yearValue)
        .await(ready);

  if ( zipOnly === false ) {

        $("#district-rank").remove();
        $("#graph-container").append("<canvas id='district-rank' width=450, height=400></canvas>");
        
        var ctx = $("#district-rank");
          
          $.get("/chart-data-employee?year="+yearValue,
            function (results) {
                var data = {
                  labels: results[0],
                  datasets: [
                  {
                    data: results[1],
                    backgroundColor: ["#2f78c4", "#2f78c4", "#2f78c4", "#2f78c4", "#2f78c4", "#084081"]
                  }]
            };

            var districtRankChart = new Chart(ctx, {
              type: 'horizontalBar',
              data: data,
              options: {
                  responsive: false,
                  title: {
                      display: true,
                      text: 'Districts With Highest % Female Employees'},
                  legend: {
                      display: false
                  }
                    }}
                  );
          });
        } // end if statement

 else if ( zipOnly === true ) {
    
    $.get("/zipcode-lookup.json?year="+yearValue, { "zipcode-entry":zipcode }, ZipcodeLookup);

 } //end else if 

  });



$("#manager").on("change", function () {

  console.log("manager button selection has been changed!");


  var yearValue = $("#year").val();
  var zipcode = $("#zipcode-entry").val();
  
  var zipOnly = $("#view-zip-compare").is(":checked");

  queue()
        .defer(d3.json, "/us.json")
        .defer(d3.json, "/us-congress-113.json")
        .defer(d3.json, "/district-manager-info.json?year="+yearValue)
        .await(ready);
  
  if ( zipOnly === false ) {

    updateRankChartManager();

 } // end if statement

 else if ( zipOnly === true ) {
    
    $.get("/zipcode-lookup.json?year="+yearValue, { "zipcode-entry":zipcode }, ZipcodeLookup);

 } //end else if 

} // end anonymous function for on manager click.
);



// bottom five employee districts selected 
$("#bottomFiveEmp").on("change", function () {

    console.log("bottom five emp button has been changed!");
    
    $("#district-rank").remove();
    $("#graph-container").append("<canvas id='district-rank' width=450, height=400></canvas>");
    
    var ctx = $("#district-rank");
    var yearValue = $("#year").val();

    $.get("/chart-data-employee-reverse?year="+yearValue, function (results) {
      var data = {
        labels: results[0],
        datasets: [
        {
          data: results[1],
          backgroundColor: ["#2f78c4", "#2f78c4", "#2f78c4", "#2f78c4", "#2f78c4", "#084081"]
        }]
      };

      var districtRankChart = new Chart(ctx, {
        type: 'horizontalBar',
        data: data,
        options: {
            responsive: false,
            title: {
                display: true,
                text: 'Districts With Lowest % Female Employees'},
            legend: {
                display: false
            }
            }
            });
    });
  }) 


  

// bottom five manager districts selected
  $("#bottomFiveManager").on("change", function () {

  console.log("bottom five manager button has been changed!");

  // draw chartjs chart
  $("#district-rank").remove();
  $("#graph-container").append("<canvas id='district-rank' width=450, height=400</canvas>");
  
  var ctx = $("#district-rank");

  var yearValue = $("#year").val();

  $.get("/chart-data-manager-reverse?year="+yearValue, function (results) {
      var data = {
        labels: results[0],
        datasets: [
        {
          data: results[1],
          backgroundColor: ["#2f78c4", "#2f78c4", "#2f78c4", "#2f78c4", "#2f78c4", "#084081"]
        }]
      };

      var districtRankChart = new Chart(ctx, {
        type: 'horizontalBar',
        data: data,
        options: {
            responsive: false,
            title: {
                display: true,
                text: 'Districts With Lowest % Female Employees in Management'
              },
             legend: {
                display: false
            }}
            });
});

});


//////////////////////
// was the slider used?

$("#year").on("input", function () {

  console.log("year input has changed!");

  var yearValue = $("#year").val();
  var zipcode = $("#zipcode-entry").val();
  var zipOnly = $("#view-zip-compare").is(":checked");

  $("#currentYear").text("Percent women employed in " + yearValue);
  $("#sliderYear").text(yearValue);


  if (zipOnly === true && $('input[name=empType]:checked', '#category').val() === "allEmps") {
  
    $.get("/zipcode-lookup.json?year="+yearValue, {"zipcode-entry":zipcode}, ZipcodeLookup);

  } // end if statement

  else if (zipOnly === true && $('input[name=empType]:checked', '#category').val() === "Managers") {

    $.get("/zipcode-lookup.json?year="+yearValue, {"zipcode-entry":zipcode}, ZipcodeLookup);


} // end else if statement


  else if ($('input[name=empType]:checked', '#category').val() === "Managers") {

  queue()
        .defer(d3.json, "/us.json")
        .defer(d3.json, "/us-congress-113.json")
        .defer(d3.json, "/district-manager-info.json?year="+yearValue)
        .await(ready);

  updateRankChartManager();

} // end if statement (if radio button "manager is checked")

else if ($('input[name=empType]:checked', '#category').val() === "allEmps") {
  
  queue()
        .defer(d3.json, "/us.json")
        .defer(d3.json, "/us-congress-113.json")
        .defer(d3.json, "/district-employee-info.json?year="+yearValue)
        .await(ready);


  updateRankChartEmployee();
}

else if ($("input[type=radio][id=bottomFiveEmp]:checked").val() == "on") {

    updateReverseChartEmployee();

  } // end else if radio button checked is bottomFiveEmp

else if ($("input[type=radio][id=bottomFiveManager]:checked").val() == "on") {

  updateReverseChartManager();

} // end else if radio butoon checked is bottomFiveManager

});


///////////////////////////////////////////////////////////////////////////////
//Populate Chart From ZIPCODE Search
function ZipcodeLookup(results) {

  // clear current chart
  $("#district-rank").remove();
  // assign id for new chart.
  $("#graph-container").append("<canvas id='district-rank' width=450, height=400</canvas>");

  var ctx = $("#district-rank");
  var empOn = $('input[name=empType]:checked', '#category').val();
          
  if ( empOn === "allEmps" ) {
      
      var data = {
        labels: ["District No. " + results.lookup_dist + " (All)",
                  results.lookup_state,
                  'U.S.'],
        datasets: [
        {
          data: [results.lookup_percent, results.state_emp_avg, results.us_emp_avg],
          backgroundColor: ['#c6dbef','#6baed6','#08306b']

        }]
      };
  }

  else {
      
      var data = {
        labels: ["District No. " + results.lookup_dist + " (Managers)",
                  results.lookup_state,
                  'U.S.'],
        datasets: [
        {
          data: [results.manager_lookup_percent, results.state_manager_avg, results.us_manager_avg],
          backgroundColor: ['#c6dbef','#6baed6','#08306b']

        }]
      };
  }

  var stateUSCompare = new Chart(ctx, {
    type: 'horizontalBar',
    data: data,
    options: {
        responsive: false,
        legend: {
          display: false
        },
        title: {
            display: true,
            text: 'District vs State & US Average'
          }}});

} // end function


// called if zipcode-submit button is clicked
function getDistrictId(evt) {
    evt.preventDefault();
    var yearValue = $("#year").val();
    var zipcode = $("#zipcode-entry").val();
    $.get("/zipcode-lookup.json?year="+yearValue, { "zipcode-entry":zipcode }, ZipcodeLookup);
}


// Listen for "click" on zipcode-submit button
$("#zipcode-submit").on("click", getDistrictId);
