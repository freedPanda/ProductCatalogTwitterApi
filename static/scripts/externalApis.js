

twttr.ready(
    function (twttr) {
        twttr.events.bind(
            'tweet',
            async function (event) {
                let date = new Date();
                date = date.toDateString();
                date = date.slice(4,16);
                sendTweetData(date);
            }
          );
    }
  );

  async function sendTweetData(date){
      try{
        response = await axios.post('/datevst', data={'solut':date});
      }catch(error){

      }
      
  }