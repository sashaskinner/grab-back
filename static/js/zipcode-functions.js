      function ZipcodeLookup(results) {
        
        // clear current chart
        $("#district-rank").remove();
        
        // assign id for new chart.
        $("#graph-container").append(
          "<canvas id='district-rank' width=450, height=400</canvas>");
        
        var ctx = $("#district-rank");
        var empOn = $('input[name=empType]:checked', '#category').val();
        
        // if button requesting entire labor force data is checked
        // look-up results for that data        
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
        // if the allEmp button is not selected, 
        // look up data for management positions
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

        // create Chart.js chart with data comparing requested zipcode to
        // state average and U.S. average
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

      function getDistrictId(evt) {
          evt.preventDefault();
          var yearValue = $("#year").val();
          var zipcode = $("#zipcode-entry").val();
          $.get("/zipcode-lookup.json?year="+yearValue, { "zipcode-entry":zipcode }, ZipcodeLookup);
      }

      $("#zipcode-submit").on("click", getDistrictId);
