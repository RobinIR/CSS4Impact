import PersonComponent from "../components/PersonComponent";

/**
 * The AboutPage that displays information about the team.
 *
 * @returns {JSX.Element} - The rendered AboutPage component.
 */

export default function AboutPage() {
  return (
    <div className="flex flex-col items-center">
      <div className="flex mt-10">
        <div className="w-2/4 pl-10 mx-15">
          <span className="text-black text-6xl font-semibold ml-20">
            Meet Our{" "}
          </span>
          <span className="text-blue-500 text-6xl font-semibold">Team</span>
          <span>
            <p className="text-gray-600 text-base font-normal mb-4 mt-10 mx-20">
              Give it up for the incredible tech wizards who spent a whopping 9
              months diving headfirst into the world of web scraping, NLP, HCI,
              and research! These fearless explorers fearlessly navigated the
              depths of code, unearthing valuable data with their web scraping
              sorcery. With their mastery of Natural Language Processing (NLP),
              they transformed raw text into meaningful insights, leaving no
              stone unturned. Their expertise in Human-Computer Interaction
              (HCI) ensured a seamless user experience, making the project not
              just functional, but a joy to interact with. And let's not forget
              their relentless dedication to research, always seeking the newest
              and most innovative solutions.
            </p>
          </span>
        </div>

        <div className="w-2/4 rounded-lg shadow-lg overflow-hidden">
          <img
            src="/img/group_full.png"
            alt="Team Group"
            width="870"
            height="500"
            className="object-cover grayscale float-right"
          />
        </div>
      </div>

      {/* PersonComponent instances for team members */}

      <div className="flex w-full flex-row  justify-start">
        <div className="w-1/2 m-10">
          <PersonComponent
            name="Apurva"
            role="NLP & UI"
            description="Ah, behold the Prankster of our project, the one and only designer extraordinaire! With a mischievous twinkle in their eye, they bring a much-needed dose of humor to our workplace. Not only are they a wizard when it comes to designing, but they also make every collaboration with them a joyous adventure. Working with this chill and fun-loving individual is like a breath of fresh air, making even the most challenging tasks feel like a breeze. Keep spreading your creativity and laughter, because we're lucky to have you on our team!"
            imageUrl="/img/groupMembers/apurva.png"
          />
        </div>
      </div>
      <div className="flex w-full flex-row  justify-end">
        <div className="w-1/2 m-10">
          <PersonComponent
            name="Lisa"
            role="Research & Project Management"
            description="Ah, the unsung hero of the research team! This remarkable person, let's call her the Stressbuster Dynamo, may bear the weight of the world on her shoulders, but her helpful and friendly nature never wavers. She's like a dedicated workhorse, tirelessly tackling tasks with unwavering determination. And beneath her tough exterior lies the heart of a kind-hearted soul, always ready to lend a helping hand. Oh, and rumour has it that she possesses a sneaky talent for food thievery, a skill that both impresses and amuses her colleagues. Keep shining, Stressbuster Dynamo, you're a rockstar in the world of research!"
            imageUrl="/img/groupMembers/lisa.jpeg"
          />
        </div>
      </div>
      <div className="flex w-full flex-row  justify-start">
        <div className="w-1/2 m-10">
          <PersonComponent
            name="Jule"
            role="Front-end & Kanban Master"
            description="Ah, behold the majestic unicorn of the frontend team! This one person, let's call them the Retro Mastermind, possesses a rare talent for conjuring up fantastic activities that breathe life into team retrospectives. She is not just a problem solver, but a superhero armed with a keyboard, swooping in to save the day with their coding prowess. With communication skills that could rival a silver-tongued diplomat, they effortlessly bridge the gap between team members. And let's not forget their uncanny ability to produce developer memes that could make even the grumpiest programmer crack a smile. Bravo, Retro Mastermind, you're a true legend in the realm of frontend!"
            imageUrl="/img/groupMembers/jule.png"
          />
        </div>
      </div>
      <div className="flex w-full flex-row justify-end">
        <div className="w-1/2 m-10">
          <PersonComponent
            name="Ravi"
            role="Research, UI & Project Management"
            description="Ah, behold the legendary Project Daddy of the research team! This extraordinary individual is like a guiding light, always lending a helping hand wherever it's needed. With the grace and finesse of a project management guru, they flawlessly orchestrate the intricate dance of tasks and deadlines. Their dedication and unwavering support are like a warm blanket on a chilly day, providing comfort and encouragement to their teammates. And let's not forget their superhuman ability to survive on little to no sleep, as they tirelessly work to ensure project success. Bravo, Project Daddy, you're a true force to be reckoned with in the world of research!"
            imageUrl="/img/groupMembers/ravi.jpg"
          />
        </div>
      </div>
      <div className="flex w-full flex-row  justify-start">
        <div className="w-1/2 m-10">
          <PersonComponent
            name="Deepika"
            role="Research & Documentation"
            description="Introducing the fabulous Girl Boss of the documentation team! With her infectious energy and a heart full of fun, she brings a lively atmosphere to the workplace. She's always there to lend a hand, especially when it comes to documenting every detail. Though she may have a reputation for being fashionably late, her reliability is unmatched, ensuring that her teammates can count on her when it matters most. Keep being your awesome self, Girl Boss, and let the documentation kingdom thrive under your reign!"
            imageUrl="/img/groupMembers/deepika.jpeg"
          />
        </div>
      </div>
      <div className="flex w-full flex-row justify-end">
        <div className="w-1/2 m-10">
          <PersonComponent
            name="Merle"
            role="Research & Project Management "
            description="Behold, the towering titan of our research team! This fun-loving force of nature is none other than our very own Organized Oasis. With a smile that could outshine a disco ball, she brings joy to our project while keeping everything in order. This research team member is also the ultimate team player. She knows how to collaborate and bring out the best in everyone around them. "
            imageUrl="/img/groupMembers/merle.jpg"
          />
        </div>
      </div>
      <div className="flex w-full flex-row  justify-start">
        <div className="w-1/2 m-10">
          <PersonComponent
            name="Imdadul"
            role="NLP"
            description="Meet our very own NLP whisperer! Despite being as shy as a retiring turtle, this remarkable individual takes the lead in our NLP team with a quiet confidence that commands respect. His reliability and hardworking nature are unmatched, always going above and beyond to deliver exceptional results. But what truly sets him apart is his unwavering support for his team members, lifting them up with encouragement and guidance. He may be shy, but his impact on our team is anything but subtle!"
            imageUrl="/img/groupMembers/imdadul.jpg"
          />
        </div>
      </div>
      <div className="flex w-full flex-row justify-end">
        <div className="w-1/2 m-10">
          <PersonComponent
            name="Saad"
            role="CS"
            description="Introducing our very own CS superhero - the master of solutions! This extraordinary individual seems to have an answer for everything, turning even the most complex problems into a piece of cake. But what's truly impressive is his ability to stay as chill as ice in high-pressure situations, radiating a calmness that spreads like a cool breeze in the office. With a friendly and engaging demeanour, he effortlessly builds rapport with colleagues and clients alike, making interactions an absolute delight."
            imageUrl="/img/groupMembers/saad.jpg"
          />
        </div>
      </div>
      <div className="flex w-full flex-row  justify-start">
        <div className="w-1/2 m-10">
          <PersonComponent
            name="Robin"
            role="CS"
            description="Meet our coding wizard extraordinaire! This individual is not just a mere mortal when it comes to coding; they possess a supernatural genius that leaves us all in awe. But it's not all serious business - their good sense of humour adds a delightful sprinkle of joy to the team, turning even the most intense coding sessions into a laugh riot. Their hardworking nature is truly commendable, as they put in countless hours and effort, working effortlessly to ensure the success of every project they touch. We're lucky to have this coding maestro on our team! "
            imageUrl="/img/groupMembers/robin.png"
          />
        </div>
      </div>
      <div className="flex w-full flex-row justify-end">
        <div className="w-1/2 m-10">
          <PersonComponent
            name="Tofayel"
            role="CS"
            description="Allow me to introduce our very own undercover backend magician! While they may not flaunt their skills in the limelight, behind the scenes, he is the driving force that keeps our project running smoothly. With his open-minded approach, he effortlessly communicates his ideas and thoughts, creating an environment where collaboration thrives. His dedication and hard work are truly commendable, as he pours his heart and soul into every task, leaving no stone unturned. Trust me, this unsung hero's efforts are the secret ingredient that makes our CS team shine!"
            imageUrl="/img/groupMembers/tofayel.jpg"
          />
        </div>
      </div>
      <div className="flex w-full flex-row  justify-start">
        <div className="w-1/2 m-10">
          <PersonComponent
            name="Asif"
            role="NLP"
            description=" Let me introduce you to the NLP team's very own Uno master! Not only does he excel at creating his own set of rules to spice up the game, but he also brings that same creative flair to their work. His contribution to integrating NLP with our database has been nothing short of groundbreaking, pushing the boundaries of what is possible. On top of his impressive skills, he is always ready to lend a helping hand, making them an invaluable asset to the team. Get ready to experience the magic of this Uno-playing, NLP innovator!"
            imageUrl="/img/groupMembers/asif.jpeg"
          />
        </div>
      </div>
      <div className="flex w-full flex-row justify-end">
        <div className="w-1/2 m-10">
          <PersonComponent
            name="Nazia"
            role="Research"
            description=" Prepare to be charmed by the Cute and Candid, the Super Honest Superstar of the project. This extraordinary individual has a knack for delivering honest feedback in the most refreshing and constructive way possible. While she may occasionally feel the weight of stress, she is an unwavering team player, always stepping up to support their colleagues. Her insatiable curiosity and enthusiasm for learning make her a true asset to the team, constantly seeking out new knowledge and skills."
            imageUrl="/img/groupMembers/Nazia.jpeg"
          />
        </div>
      </div>
      <div className="flex w-full flex-row  justify-start">
        <div className="w-1/2 m-10">
          <PersonComponent
            name="Hatim"
            role="CS"
            description="Meet the brainiac of the CS team, a true master of ideas and discussions! This individual has a knack for coming up with brilliant solutions and is a pro at engaging in insightful conversations. Whether it's brainstorming sessions or troubleshooting, he excels at finding innovative ways to tackle problems. Get ready to be amazed by his sharp wit and fantastic problem-solving skills."
            imageUrl="/img/groupMembers/hatim.png"
          />
        </div>
      </div>
    </div>
  );
}
