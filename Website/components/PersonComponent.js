import React from 'react';

/**
 * The PersonComponent displays information about a person, including their name, role, description, and image. It is used in the 'About'-page.
 *
 * @param {string} name - The name of the person.
 * @param {string} role - The role of the person.
 * @param {string} description - The description of the person.
 * @param {string} imageUrl - The URL of the person's image.
 * @returns {JSX.Element} The PersonComponent.
 */
const PersonComponent = ({ name, role, description, imageUrl }) => {
  return (
    <div className="flex items-center mt-10 mr-4">
      <div className="bg-white rounded-lg shadow-lg p-4 flex-1 relative">
        <div className="flex gap-4 relative z-0">
          {/* Image */}
          <img className="w-1/2 h-auto max-h-[300px] rounded-lg object-contain filter grayscale" src={imageUrl} alt={name} />
          <div>
            <div className="mb-4">
              {/* Name */}
              <h3 className="text-xl font-semibold">{name}</h3>
              {/* Role */}
              <p className="text-blue-400 text-base font-semibold">{role}</p>
            </div>
            {/* Description */}
            <p className="text-gray-700">{description}</p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default PersonComponent;









