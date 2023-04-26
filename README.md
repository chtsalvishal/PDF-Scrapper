
# PDF Scrapper

Python based PDF file content extractor using Regular Expression


> ## Config.json

This file contains the metadata that the model uses to run. config contains dictionary type information that is directly loaded onto the model. It includes the following columns and has different meaning as follows:

* `pdfs_location (required):` Denotes the location from which the pdfs are meant to be extracted. It needs to be an absolute path like C:\\Users\\HelloWorld\\Documents\\. It is important to delimit the \ as shown in the example.
* `pagestart (optional):` Denotes the start of the page from where the model has to read information in the pdf. This can be set to any number less the total page. since it is python page 1 is given by 0. By default leave it at 0, or change as per need.
* `pageend (optional):` Denotes the end of the page from where the model has to stop the read. This can be set to any number less than or equal to total page. Make sure to have this greater than pagestart. If you want to read all the pages leave it as 0 and the model will automatically read the whole document.
* `footer_regex (required):` Provides the regular expression that the engine has to use to remove footer information in the PDF document. Refer to the Example for sample regex. Since it is JSON \ could be escaped using \\ or left as is. Engine will work either way.
* `remove_headings (optional):` If there are specific list of sentences that needs to be removed from the document provide them here to have it removed. By default you can leave it '' to not remove anything.
* `paragraph_regex (required):` Use this to provide the regular expression that will fetch the paragraph that needs to be extracted from the PDF. Refer to the example for more assistance with regex. Since it is JSON \ could be escaped using \\ or left as is. Engine will work either way.
* `para_correction_regex (optional):` Use this if there are any specific requirement to remove empty space within the paragraph heading or other formatting and corrections needs to be done.
* `search_start (optional):` Use this if there are specific sentence/regex pattern to which the model has to start from. This is can be left '' if there are not sentences to goto.
* `search_end (optional):` Use this if there are specific sentence/regex pattern  to which the model has to stop at. This is can be left '' if there are not sentences to goto.



> ## Output

By default model is configured to read all the documents one by one from the input location which ever is configured in the config file and store the outputs with the same name as source pdf with '_scrapped' attached to it. 


> ## Example Provided

In the example provided we try to extract certain questions that follow a specific format and can be uniquely identified. Using that structure a regular expression was constructed to identify the questions first. Following this the document is split based on the questions, with logic we now anything between two questions is the answer, so we can gather them once it is split and stored onto a list. This is exactly what has been done. 

The sample configuration file contains the json code as below 

```
{
	"pdfs_location": "C:\\Users\\VishalPattabiraman\\Documents\\PDF_Scrapper\\input\\", 
	"pagestart": 0, 
	"pageend": 0, 
	"footer_regex": "(Application ID:+[\\w\\s\\n]+\\nCreated date:[\\w\\s:/\\n]+Page+[\\s]?[0-9]+)", 
	"remove_headings": ["Activities Planned for/with Data", "Data Characteristics", "Section 3 – Data and Privacy", "Risk Questions", "Consent Questions", "Recruitment Questions", "People in dependent or unequal relationships", "Children and young people", "Participant Specific Questions", "Survey/Interview/Focus Group Research", "Method Specific Questions", "Setting of research", "Evaluations", "Restrictions", "Disclosure of interests","Benefit  Questions"], 
	"paragraph_regex": "\n([QMP][\\s]?\\d[.\\d\\s]+[’\\w\\s/(),-]+[?.:])",
	"para_correction_regex":"([QMP][\\s]?\\d[.\\d\\s]+)([’\\w\\s/(),-]+[?.:])",
	"search_start":"Human Research Ethics Application[\\s\\n]+Application Management Information",
	"search_end":"Section 4 – Attachments and Declarations"
}
```

- `pdfs_location`, `pagestart`, `pageend` are self explanatory as shown in the dictionary definition section above.

- `footer_regex` **([\\w\\s:/\n]+Page [0-9]+)** here uses any word using **\w**, checks for blank space **\s**, new line **\n**, and if it contains colon **:**. All these are included into a square bracket **[]** to denote that **any** of them can be identified. The plus **+** sign after the square bracket denotes the above characters can happen 1 or more times repeatedly (non-greedy). In order to end the identification of text the `Page` word is used ending with a digit `[0-9]`.
- `paragraph_regex` **([QMP][\\s]?\\d[.\\dP]+[’\\w\\s/(),-]+[?.:])** here identifies lines starting with characters **[QMP]** which can be followed by blank space **\s** zero or ones using **?**. Following to which we search for digits from `0-9` using **\d** with a dot **.** followed by another digit or multiple digits **\d**. Following this any words **\w** or blank space **\s** or `/(),-` checked for occurence one or more times using plus **+**. In order to end the selection string we search for **[?.:]** and produce the final paragraph.
- `para_correction_regex` **([QMP][\\s]?\\d[.\\d\\s]+)([’\\w\\s/(),-]+[?.:])** there are two groups here, group 1 **([QMP][\\s]?\\d[.\\d\\s]+)** contains the begining of the paragraph which will be corrected and group 2 **([’\\w\\s/(),-]+[?.:])** will be used to append to the corrected string.
- `remove_headings` contains the list of characters from the documents that are titles and other unwanted text that is provided as a list which will be removed by the model.
- `search_start` is used in order pinpoint a specific text from large  document and end the search using `search_end`.



> ## FAQs

- Important to note that this code works by converting the pdf into a stream of text. So Tables and their corresponding structure do not sit well. It will still extract the content but not the structure of the table. 

- This can extract bulletpoints, checkbox, ticks and other pdf special characters as along as it is utf-8 encoded.
- Words in the Paragraphs might be split into two which is an observered behaviour.
