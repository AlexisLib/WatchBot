'use strict';
console.log('Loading function');

/* Stock Ticker format parser */
const parser = /^\{\"iduser\"\: \"[0-9]+\"\, \"gender\"\: \"[a-z]+\"\, \"age\"\: \"[0-9]+\"\, \"height\"\: \"[0-9]+\"\, \"weight\"\: \"[0-9]+\"\, \"steps\"\: \"[0-9]+\"\, \"heartbeat\"\: \"[0-9]+\"\, \"blood_pressure\"\: \"[.0-9\/]+\"\, \"temperature\"\: \"[.0-9]+\"\, \"date\"\: \"[0-9-]+\"\, \"hour\"\: \"[0-9:]+\"\}/;

exports.handler = (event, context, callback) => {
    let success = 0; // Number of valid entries found
    let failure = 0; // Number of invalid entries found
    let dropped = 0; // Number of dropped entries 

    /* Process the list of records and transform them */
    const output = event.records.map((record) => {

        const entry = (Buffer.from(record.data, 'base64')).toString('utf8');
        
        console.log(entry);
        
        let match = parser.exec(entry);
        if (match) {
            let parsed_match = JSON.parse(match); 
            var milliseconds = new Date().getTime();
            /* Add timestamp and convert to CSV */
            const result = `${parsed_match.iduser},${parsed_match.gender},${parsed_match.age},${parsed_match.height},${parsed_match.weight},${parsed_match.steps},${parsed_match.heartbeat},${parsed_match.blood_pressure},${parsed_match.temperature},${parsed_match.date},${parsed_match.hour}`+"\n";
            const payload = (Buffer.from(result, 'utf8')).toString('base64');
            /* Transformed event */
            success++;  
            return {
                recordId: record.recordId,
                result: 'Ok',
                data: payload,
            };
        }
        else {
            /* Failed event, notify the error and leave the record intact */
            console.log("Failed event : "+ record.data);
            failure++;
            return {
                recordId: record.recordId,
                result: 'ProcessingFailed',
                data: record.data,
            };
        }

    });
    console.log(`Processing completed.  Successful records ${output.length}.`);
    callback(null, { records: output });
};