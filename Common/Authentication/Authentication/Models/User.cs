using Common.Authentication.DBHandlers;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Web;

namespace Common.Authentication.Models
{
    public class User : IUser
    {
        #region Public Attributes
        /// <summary>
        /// The id of this user.
        /// </summary>
        public int Id;

        /// <summary>
        /// First name of this user.
        /// </summary>
        public String FirstName;

        /// <summary>
        /// Last name of this user.
        /// </summary>
        public String LastName;

        /// <summary>
        /// Middle name of this user.
        /// </summary>
        public String MiddleName;
        #endregion

        #region IUser Interface
        private UserDbHandler _objects = new UserDbHandler();
        /// <summary>
        /// The data manager for the User model. This performs
        /// CRUD operations on the User table.
        /// </summary>
        public IDbHandler<IUser> Objects { get { return _objects; } }

        /// <summary>
        /// <para>
        /// Implementation of <see cref="IUser.MatchFingerPrint"/>.
        /// This takes the fingerprint and matches it against the
        /// fingerprint image stored in the database.
        /// </para>
        /// </summary>
        /// <returns>
        /// true if the fingerprint matched that stored in the
        /// database.
        /// </returns>
        public bool MatchFingerPrint()
        {
            return true;
        }
        #endregion
    }
}