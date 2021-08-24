	
	function changeSource()
		{
			var x = $( "#id_source").val();
			if ( x == "tour" || x == "fit") {
				$( "#tourBox" ).show();
				}
			else {
				$( "#tourBox" ).hide();
			}
			return true;
		};
	


	
	$( "#id_source" ).change(changeSource);

	changeSource();

	



	
	function dateConfig()
		{
			$( "#dateBlock").show();
			$( "#sortedBlock").hide();		
			$( "#searchBlock").hide();
			$( "#agentBlock" ).hide();
		}

	function searchConfig()
		{
			$( "#searchBlock").show();
			$( "#sortedBlock").show();		
			$( "#agentBlock" ).hide();
			$( "#dateBlock").hide();
		}
	
	function agentConfig()
		{
			$( "#searchBlock").show();
			$( "#sortedBlock").show();		
			$( "#agentBlock" ).show();
			$( "#dateBlock").hide();
		}
	
	
	$( "#dateBlock").hide();
	$( "#sortedBlock").show();
	
	searchConfig();

	if ( $( "#listSelect").val() == "agent" ) {
		agentConfig();
	}

	else if ( $( "#listSelect").val() == "calendar" ) {
		dateConfig();	
	}

	$( "#listSelect").change ( function() {
		var ls = $( '#listSelect' ).val();
		
		if ( ls == "agent" ) {
			agentConfig();
		}
		else if ( ls == "calendar" ) {
			dateConfig();
		}
		else {
			searchConfig();
		}	
	});
	
	
	

