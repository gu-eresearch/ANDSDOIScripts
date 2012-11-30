<html>
<head>
	<style>
		fieldset{
			width: 600px;
			border: 1px dotted #333
		}
	</style>
</head>
<body>
	<h1>ANDS Cite My Data DOI Tools</h1>
	<p><i>Super Minimalistic Interface for Cite my Data service</i></p>
	<fieldset>
		<legend>DOI Lookup</legend>
		<form method="POST" action="doi_lookup_new.php">
			<span>DOI ID</span>
			<input type="text" name="DOI_id" value="" size="100" /><br/>
			<input type="submit" value="Submit" />
		</form>	
	</fieldset>

	<br />

	<fieldset>
		<legend>DOI Update</legend>
		<form method="POST" action="doi_update_new.php">
			<span>DOI ID</span>
			<input type="text" name="DOI_id" value="" size="100" /> <br/>
			<span>Url</span>
			<input type="text" name="url" value="" size="100" /> <br/>

			<input type="submit" value="Submit" />
		</form>	
	</fieldset>


		<br />

	<fieldset>
		<legend>DOI Minting</legend>
		<form method="POST" action="doi_mint_new.php">
			<span>XML</span>
			<textarea name="xml" size="100"></textarea> <br/>
			<span>Url</span>
			<input type="text" name="url" value="" size="100" /> <br/>

			<input type="submit" value="Submit" />
		</form>	
	</fieldset>

</body>
</html>