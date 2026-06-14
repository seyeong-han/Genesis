- why don't we need the OpenAlex api key? Are we not using the api to collect the papers and researchers in the frontend? we need to have options that users can select their desired researchers from OpenAlex. show the researcher candidates in real-time by grepping the best citation researchers for each discipline. users can select how many papers should OpenAlex grep and which papers to add.

- let's redesign the frontend for our project. review the whole page and update them with ours. for example:
 we don't upload the files. we are searching the researchers and papers using OpenAlex api. if the user ask question, then llm suggests multi-discipline and their researchers and papers automatically. we need to include at least 43 disciplinaries from @illuminate_young/project/0612_claude_hackathon/Genesis/researcher.md as a default so that the science question doesn't bring only science researchers but bring from nature, philosophy. We need diversity to be able to discover the cross-discipline findings. i'd like to show hundreds of agents are initialized to discuss the incoming questions for the hackathon demo. what is the ideal number of researchers and papers to set up the base knowledge graph?


 why do we have 42 agents? my intention was each agent represents each researcher. do you think creating agents separately with the graph edges (paper, researchers, methods, etc) is better approach for our goal?


 let's redesign the frontend for our project. review the whole page and update them with ours. for example, remove chinese main page and only leaves english. support inputs with the file upload or OpenAlex paper or researcher search.  estimate how long will it take to process my desired initial point. only two hours left for hackathon right now. estimate this "list up 43 disciplinaries from @illuminate_young/project/0612_claude_hackathon/Genesis/researcher and bring one paper per each researcher." 


 이게 지금 현재 localhost:3000 상황인데 여기서 기다리고 있으면 돼? 그러면 report가 나오는거야? rounds 는 0/72로 계속 안바뀌고 있는데 이거 맞는지 검증해. 그리고 타임존은 PDT로 해야 돼.